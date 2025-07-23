#!/usr/bin/env python3
"""
通知角色分配的腳本 (Mock 版本)
用於 GitHub Actions 工作流程中通知角色分配
"""

import os
import sys
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函數 - Mock 版本"""
    try:
        logger.info("🎯 開始處理角色分配通知 (Mock 模式)...")
        
        # 獲取環境變量（如果存在）
        issue_number = os.getenv('ISSUE_NUMBER', '123')
        assignee = os.getenv('ASSIGNEE', 'ai-developer')
        repo = os.getenv('GITHUB_REPOSITORY', 'test/repo')
        
        logger.info(f"📋 Issue #{issue_number} 分配給 {assignee}")
        
        # Mock Issue 數據
        mock_issue_data = {
            "number": issue_number,
            "title": "實現新功能模塊",
            "assignee": assignee,
            "labels": ["enhancement", "frontend"],
            "repository": repo,
            "html_url": f"https://github.com/{repo}/issues/{issue_number}"
        }
        
        logger.info(f"📝 Issue 標題: {mock_issue_data['title']}")
        logger.info(f"🏷️ 標籤: {', '.join(mock_issue_data['labels'])}")
        
        # 模擬通知過程
        logger.info("📢 發送角色分配通知...")
        
        # 模擬通知結果
        notify_success = True
        comment_success = True
        
        if notify_success:
            logger.info(f"✅ 成功通知角色分配給 {assignee}")
        else:
            logger.warning("⚠️ 通知角色分配失敗")
        
        if comment_success:
            logger.info("✅ 成功在 Issue 中添加評論")
        else:
            logger.warning("⚠️ 添加評論失敗")
        
        # 設置環境變量
        with open(os.environ.get('GITHUB_ENV', '/dev/null'), 'a') as f:
            f.write("ROLE_ASSIGNMENT_NOTIFIED=true\n")
            f.write(f"NOTIFICATION_TIME={datetime.now().isoformat()}\n")
            f.write(f"ISSUE_NUMBER={issue_number}\n")
            f.write(f"ASSIGNEE={assignee}\n")
        
        logger.info("🎉 角色分配通知處理完成 (Mock 模式)")
        
    except Exception as e:
        logger.error(f"❌ 處理角色分配通知時發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 