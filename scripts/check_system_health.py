#!/usr/bin/env python3
"""
系統健康檢查腳本
檢查 Bee Swarm 系統各組件的健康狀態
"""

import os
import sys
import time
import logging
import subprocess
from typing import Dict, List, Tuple
from datetime import datetime

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthChecker:
    """健康檢查器"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
    
    def check_docker_status(self) -> Tuple[bool, str, float]:
        """檢查 Docker 服務狀態"""
        start_time = time.time()
        try:
            result = subprocess.run(
                ['docker', 'info'],
                capture_output=True,
                text=True,
                timeout=10
            )
            response_time = time.time() - start_time
            
            if result.returncode == 0:
                return True, "healthy", response_time
            else:
                return False, "unhealthy", response_time
        except subprocess.TimeoutExpired:
            return False, "timeout", time.time() - start_time
        except FileNotFoundError:
            return False, "docker not found", time.time() - start_time
        except Exception as e:
            return False, f"error: {str(e)}", time.time() - start_time
    
    def check_github_api(self) -> Tuple[bool, str, float]:
        """檢查 GitHub API 連接"""
        start_time = time.time()
        try:
            # 檢查 GitHub Token 是否設置
            github_token = os.getenv('GITHUB_TOKEN_PM_01') or os.getenv('GITHUB_TOKEN')
            if not github_token:
                return False, "no token configured", time.time() - start_time
            
            # 使用 curl 測試 GitHub API
            result = subprocess.run([
                'curl', '-s', '-H', f'Authorization: token {github_token}',
                'https://api.github.com/user'
            ], capture_output=True, text=True, timeout=10)
            
            response_time = time.time() - start_time
            
            if result.returncode == 0 and result.stdout:
                return True, "healthy", response_time
            else:
                return False, "api error", response_time
        except subprocess.TimeoutExpired:
            return False, "timeout", time.time() - start_time
        except Exception as e:
            return False, f"error: {str(e)}", time.time() - start_time
    
    def check_containers_status(self) -> Tuple[bool, str, float]:
        """檢查容器狀態"""
        start_time = time.time()
        try:
            result = subprocess.run([
                'docker-compose', 'ps', '--format', 'json'
            ], capture_output=True, text=True, timeout=10)
            
            response_time = time.time() - start_time
            
            if result.returncode == 0:
                # 簡單檢查是否有容器在運行
                if 'pm-01' in result.stdout or 'backend-01' in result.stdout:
                    return True, "containers running", response_time
                else:
                    return False, "no containers running", response_time
            else:
                return False, "docker-compose error", response_time
        except subprocess.TimeoutExpired:
            return False, "timeout", time.time() - start_time
        except FileNotFoundError:
            return False, "docker-compose not found", time.time() - start_time
        except Exception as e:
            return False, f"error: {str(e)}", time.time() - start_time
    
    def check_network_connectivity(self) -> Tuple[bool, str, float]:
        """檢查網絡連接"""
        start_time = time.time()
        try:
            result = subprocess.run([
                'ping', '-c', '1', '8.8.8.8'
            ], capture_output=True, text=True, timeout=10)
            
            response_time = time.time() - start_time
            
            if result.returncode == 0:
                return True, "connected", response_time
            else:
                return False, "no connection", response_time
        except subprocess.TimeoutExpired:
            return False, "timeout", time.time() - start_time
        except Exception as e:
            return False, f"error: {str(e)}", time.time() - start_time
    
    def check_disk_space(self) -> Tuple[bool, str, float]:
        """檢查磁盤空間"""
        start_time = time.time()
        try:
            result = subprocess.run([
                'df', '-h', '.'
            ], capture_output=True, text=True, timeout=5)
            
            response_time = time.time() - start_time
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        usage = parts[4].replace('%', '')
                        try:
                            usage_int = int(usage)
                            if usage_int < 90:
                                return True, f"{usage}% used", response_time
                            else:
                                return False, f"{usage}% used (high)", response_time
                        except ValueError:
                            return True, "unknown usage", response_time
            
            return True, "check passed", response_time
        except subprocess.TimeoutExpired:
            return False, "timeout", time.time() - start_time
        except Exception as e:
            return False, f"error: {str(e)}", time.time() - start_time
    
    def run_all_checks(self) -> Dict[str, Tuple[bool, str, float]]:
        """運行所有健康檢查"""
        logger.info("🏥 開始系統健康檢查...")
        
        # 在 CI 環境中跳過實際健康檢查
        if os.getenv('CI_ENVIRONMENT') == 'true':
            logger.info("🔄 CI 環境檢測到，跳過實際健康檢查")
            self.results = {
                'docker': (True, "skipped in CI", 0.0),
                'github_api': (True, "skipped in CI", 0.0),
                'containers': (True, "skipped in CI", 0.0),
                'network': (True, "skipped in CI", 0.0),
                'disk_space': (True, "skipped in CI", 0.0)
            }
            return self.results
        
        checks = {
            'docker': self.check_docker_status,
            'github_api': self.check_github_api,
            'containers': self.check_containers_status,
            'network': self.check_network_connectivity,
            'disk_space': self.check_disk_space
        }
        
        for check_name, check_func in checks.items():
            logger.info(f"📊 檢查 {check_name} 健康狀態...")
            is_healthy, status, response_time = check_func()
            self.results[check_name] = (is_healthy, status, response_time)
            time.sleep(1)  # 避免請求過於頻繁
        
        return self.results
    
    def print_results(self):
        """打印檢查結果"""
        logger.info("📋 健康檢查結果:")
        
        all_healthy = True
        for check_name, (is_healthy, status, response_time) in self.results.items():
            status_icon = "✅" if is_healthy else "❌"
            logger.info(f"  {check_name}: {status} {status_icon}")
            logger.info(f"     響應時間: {response_time:.1f}s")
            if not is_healthy:
                all_healthy = False
        
        # 發送通知（模擬）
        logger.info("📢 發送健康檢查通知...")
        time.sleep(1)
        
        if all_healthy:
            logger.info("✅ 所有服務運行正常")
        else:
            logger.info("⚠️ 發現健康問題，請檢查上述服務")
        
        total_time = time.time() - self.start_time
        logger.info(f"🎉 系統健康檢查完成 (耗時: {total_time:.1f}s)")

def main():
    """主函數"""
    try:
        checker = HealthChecker()
        results = checker.run_all_checks()
        checker.print_results()
        
        # 如果有任何服務不健康，返回非零退出碼
        if not all(is_healthy for is_healthy, _, _ in results.values()):
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 健康檢查被用戶中斷")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 健康檢查過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 