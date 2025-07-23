#!/usr/bin/env python3
"""
檢查待處理任務的腳本 (Mock 版本)
用於 GitHub Actions 工作流程中檢查是否有待處理的任務
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
        logger.info("🔍 開始檢查待處理任務 (Mock 模式)...")
        
        # Mock 數據
        mock_pending_tasks = [
            {"number": 1, "title": "實現用戶認證功能"},
            {"number": 2, "title": "修復登錄頁面 bug"},
            {"number": 3, "title": "添加數據庫連接池"}
        ]
        
        logger.info(f"📋 找到 {len(mock_pending_tasks)} 個待處理任務")
        
        for task in mock_pending_tasks:
            logger.info(f"  - #{task['number']}: {task['title']}")
        
        # 設置環境變量供後續步驟使用
        with open(os.environ.get('GITHUB_ENV', '/dev/null'), 'a') as f:
            f.write(f"PENDING_TASKS_COUNT={len(mock_pending_tasks)}\n")
            f.write("HAS_PENDING_TASKS=true\n")
            f.write(f"CHECK_TIME={datetime.now().isoformat()}\n")
        
        logger.info("✅ 檢查待處理任務完成 (Mock 模式)")
        
    except Exception as e:
        logger.error(f"❌ 檢查待處理任務時發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 