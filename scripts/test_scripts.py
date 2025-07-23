#!/usr/bin/env python3
"""
測試腳本
用於驗證所有 GitHub Actions 腳本的基本功能
"""

import os
import sys
import subprocess
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_script(script_name: str, env_vars: dict = None) -> bool:
    """測試單個腳本"""
    try:
        logger.info(f"測試腳本: {script_name}")
        
        # 設置環境變量
        test_env = os.environ.copy()
        if env_vars:
            test_env.update(env_vars)
        
        # 設置測試環境變量
        test_env.update({
            'GITHUB_TOKEN': 'test_token',
            'GITHUB_REPOSITORY': 'test/repo',
            'CLOUDFLARE_TUNNEL_URL': 'https://test.example.com',
            'ISSUE_NUMBER': '1',
            'ASSIGNEE': 'test_user',
            'PR_NUMBER': '1',
            'PR_ACTION': 'opened',
            'PROMETHEUS_URL': 'http://localhost:9090',
            'GRAFANA_URL': 'http://localhost:3000',
            'SLACK_WEBHOOK_URL': 'https://hooks.slack.com/test',
            'BACKUP_S3_BUCKET': 'test-bucket',
            'AWS_ACCESS_KEY_ID': 'test_key',
            'AWS_SECRET_ACCESS_KEY': 'test_secret'
        })
        
        # 運行腳本（只測試語法，不實際執行）
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', f'scripts/{script_name}'],
            capture_output=True,
            text=True,
            env=test_env,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info(f"✅ {script_name} 語法檢查通過")
            return True
        else:
            logger.error(f"❌ {script_name} 語法檢查失敗: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"❌ {script_name} 執行超時")
        return False
    except Exception as e:
        logger.error(f"❌ {script_name} 測試失敗: {e}")
        return False

def main():
    """主函數"""
    logger.info("開始測試所有腳本...")
    
    # 要測試的腳本列表
    scripts = [
        'check_pending_tasks.py',
        'trigger_ai_containers.py',
        'notify_role_assignment.py',
        'handle_pr_events.py',
        'check_system_health.py',
        'create_backup.py',
        'update_documentation.py'
    ]
    
    # 測試每個腳本
    results = {}
    for script in scripts:
        results[script] = test_script(script)
    
    # 輸出測試結果
    logger.info("\n測試結果摘要:")
    all_passed = True
    for script, passed in results.items():
        status = "✅ 通過" if passed else "❌ 失敗"
        logger.info(f"  {script}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 所有腳本測試通過！")
        return 0
    else:
        logger.error("\n💥 部分腳本測試失敗！")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 