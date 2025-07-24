#!/usr/bin/env python3
"""
配置驗證腳本
用於驗證 Bee Swarm 系統的環境變量配置
"""

import os
import sys
import re
from typing import Dict, List, Tuple
from datetime import datetime

# 設置日誌
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigValidator:
    """配置驗證器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed_checks = 0
        self.total_checks = 0
    
    def validate_required_env_vars(self) -> bool:
        """驗證必需的環境變量"""
        logger.info("🔍 驗證必需的環境變量...")
        
        # 在 CI 環境中跳過嚴格驗證
        if os.getenv('CI_ENVIRONMENT') == 'true':
            logger.info("🔄 CI 環境檢測到，跳過嚴格環境變量驗證")
            self.total_checks += 1
            self.passed_checks += 1
            return True
        
        required_vars = {
            'GITHUB_REPOSITORY': 'GitHub 倉庫地址',
            'GITHUB_OWNER': 'GitHub 組織/用戶名',
            'GITHUB_TOKEN_PM_01': '產品經理 GitHub Token',
            'GITHUB_TOKEN_BACKEND_01': '後端開發 GitHub Token',
            'GITHUB_TOKEN_FRONTEND_01': '前端開發 GitHub Token',
            'GITHUB_TOKEN_DEVOPS_01': 'DevOps GitHub Token',
            'OPENAI_API_KEY': 'OpenAI API 密鑰',
            'ANTHROPIC_API_KEY': 'Anthropic API 密鑰',
            'GEMINI_API_KEY': 'Gemini API 密鑰'
        }
        
        missing_vars = []
        for var, description in required_vars.items():
            self.total_checks += 1
            if not os.getenv(var):
                missing_vars.append(f"{var} ({description})")
                self.errors.append(f"缺少必需的環境變量: {var}")
            else:
                self.passed_checks += 1
        
        if missing_vars:
            logger.error(f"❌ 缺少 {len(missing_vars)} 個必需的環境變量:")
            for var in missing_vars:
                logger.error(f"  - {var}")
            return False
        
        logger.info(f"✅ 所有 {len(required_vars)} 個必需的環境變量都已配置")
        return True
    
    def validate_github_tokens(self) -> bool:
        """驗證 GitHub Token 格式"""
        logger.info("🔍 驗證 GitHub Token 格式...")
        
        token_vars = [
            'GITHUB_TOKEN_PM_01',
            'GITHUB_TOKEN_BACKEND_01',
            'GITHUB_TOKEN_FRONTEND_01',
            'GITHUB_TOKEN_DEVOPS_01'
        ]
        
        invalid_tokens = []
        for var in token_vars:
            self.total_checks += 1
            token = os.getenv(var)
            if token:
                if not token.startswith('ghp_'):
                    invalid_tokens.append(var)
                    self.errors.append(f"{var} 格式不正確，應以 'ghp_' 開頭")
                else:
                    self.passed_checks += 1
            else:
                # 已在 required_env_vars 中檢查過，這裡跳過
                continue
        
        if invalid_tokens:
            logger.error(f"❌ 發現 {len(invalid_tokens)} 個格式不正確的 GitHub Token:")
            for var in invalid_tokens:
                logger.error(f"  - {var}")
            return False
        
        logger.info("✅ GitHub Token 格式正確")
        return True
    
    def validate_api_keys(self) -> bool:
        """驗證 API 密鑰格式"""
        logger.info("🔍 驗證 API 密鑰格式...")
        
        api_keys = {
            'OPENAI_API_KEY': ('sk-', 'OpenAI API 密鑰'),
            'ANTHROPIC_API_KEY': ('sk-ant-', 'Anthropic API 密鑰'),
            'GEMINI_API_KEY': (None, 'Gemini API 密鑰')  # Gemini 沒有固定前綴
        }
        
        invalid_keys = []
        for var, (prefix, description) in api_keys.items():
            self.total_checks += 1
            key = os.getenv(var)
            if key:
                if prefix and not key.startswith(prefix):
                    invalid_keys.append(f"{var} ({description})")
                    self.errors.append(f"{var} 格式不正確，應以 '{prefix}' 開頭")
                else:
                    self.passed_checks += 1
            else:
                # 已在 required_env_vars 中檢查過，這裡跳過
                continue
        
        if invalid_keys:
            logger.error(f"❌ 發現 {len(invalid_keys)} 個格式不正確的 API 密鑰:")
            for key in invalid_keys:
                logger.error(f"  - {key}")
            return False
        
        logger.info("✅ API 密鑰格式正確")
        return True
    
    def validate_github_repository(self) -> bool:
        """驗證 GitHub 倉庫格式"""
        logger.info("🔍 驗證 GitHub 倉庫格式...")
        
        self.total_checks += 1
        repo = os.getenv('GITHUB_REPOSITORY')
        owner = os.getenv('GITHUB_OWNER')
        
        if repo and owner:
            # 檢查倉庫格式是否為 owner/repo
            if '/' in repo and repo.split('/')[0] == owner:
                self.passed_checks += 1
                logger.info("✅ GitHub 倉庫格式正確")
                return True
            else:
                self.errors.append("GITHUB_REPOSITORY 格式不正確，應為 'owner/repo' 格式")
                logger.error("❌ GitHub 倉庫格式不正確")
                return False
        else:
            # 已在 required_env_vars 中檢查過
            return True
    
    def validate_vnc_passwords(self) -> bool:
        """驗證 VNC 密碼配置"""
        logger.info("🔍 驗證 VNC 密碼配置...")
        
        vnc_vars = [
            'VNC_PASSWORD_PM_01',
            'VNC_PASSWORD_BACKEND_01',
            'VNC_PASSWORD_FRONTEND_01',
            'VNC_PASSWORD_DEVOPS_01'
        ]
        
        weak_passwords = []
        for var in vnc_vars:
            self.total_checks += 1
            password = os.getenv(var)
            if password:
                if len(password) < 6:
                    weak_passwords.append(var)
                    self.warnings.append(f"{var} 密碼過短，建議至少 6 位字符")
                else:
                    self.passed_checks += 1
            else:
                self.warnings.append(f"{var} 未設置，將使用默認密碼")
        
        if weak_passwords:
            logger.warning(f"⚠️ 發現 {len(weak_passwords)} 個弱密碼:")
            for var in weak_passwords:
                logger.warning(f"  - {var}")
        
        logger.info("✅ VNC 密碼配置檢查完成")
        return True
    
    def validate_ttyd_passwords(self) -> bool:
        """驗證 TTYD 密碼配置"""
        logger.info("🔍 驗證 TTYD 密碼配置...")
        
        ttyd_vars = [
            'TTYD_PASSWORD_PM_01',
            'TTYD_PASSWORD_BACKEND_01',
            'TTYD_PASSWORD_FRONTEND_01',
            'TTYD_PASSWORD_DEVOPS_01'
        ]
        
        weak_passwords = []
        for var in ttyd_vars:
            self.total_checks += 1
            password = os.getenv(var)
            if password:
                if len(password) < 8:
                    weak_passwords.append(var)
                    self.warnings.append(f"{var} 密碼過短，建議至少 8 位字符")
                else:
                    self.passed_checks += 1
            else:
                self.warnings.append(f"{var} 未設置，將使用默認密碼")
        
        if weak_passwords:
            logger.warning(f"⚠️ 發現 {len(weak_passwords)} 個弱密碼:")
            for var in weak_passwords:
                logger.warning(f"  - {var}")
        
        logger.info("✅ TTYD 密碼配置檢查完成")
        return True
    
    def generate_report(self) -> None:
        """生成驗證報告"""
        logger.info("\n" + "="*50)
        logger.info("📊 配置驗證報告")
        logger.info("="*50)
        
        logger.info(f"✅ 通過檢查: {self.passed_checks}/{self.total_checks}")
        logger.info(f"❌ 錯誤數量: {len(self.errors)}")
        logger.info(f"⚠️ 警告數量: {len(self.warnings)}")
        
        if self.errors:
            logger.info("\n❌ 錯誤詳情:")
            for error in self.errors:
                logger.info(f"  - {error}")
        
        if self.warnings:
            logger.info("\n⚠️ 警告詳情:")
            for warning in self.warnings:
                logger.info(f"  - {warning}")
        
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        logger.info(f"\n📈 成功率: {success_rate:.1f}%")
        
        if len(self.errors) == 0:
            logger.info("🎉 配置驗證通過！")
        else:
            logger.info("💥 配置驗證失敗，請修復上述錯誤後重試。")

def main():
    """主函數"""
    logger.info("🚀 開始 Bee Swarm 配置驗證...")
    
    validator = ConfigValidator()
    
    # 執行所有驗證
    checks = [
        validator.validate_required_env_vars,
        validator.validate_github_tokens,
        validator.validate_api_keys,
        validator.validate_github_repository,
        validator.validate_vnc_passwords,
        validator.validate_ttyd_passwords
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    # 生成報告
    validator.generate_report()
    
    # 設置環境變量供後續步驟使用
    with open(os.environ.get('GITHUB_ENV', '/dev/null'), 'a') as f:
        f.write(f"CONFIG_VALIDATION_PASSED={'true' if all_passed else 'false'}\n")
        f.write(f"CONFIG_ERRORS_COUNT={len(validator.errors)}\n")
        f.write(f"CONFIG_WARNINGS_COUNT={len(validator.warnings)}\n")
        f.write(f"CONFIG_CHECK_TIME={datetime.now().isoformat()}\n")
    
    if all_passed:
        logger.info("✅ 配置驗證完成，可以啟動系統")
        sys.exit(0)
    else:
        logger.error("❌ 配置驗證失敗，請修復錯誤後重試")
        sys.exit(1)

if __name__ == "__main__":
    main() 