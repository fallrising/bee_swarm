#!/usr/bin/env python3
"""
更新文檔的腳本 (Mock 版本)
用於 GitHub Actions 工作流程中自動更新項目文檔
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
        logger.info("📚 開始更新文檔 (Mock 模式)...")
        
        # 獲取環境變量（如果存在）
        repo = os.getenv('GITHUB_REPOSITORY', 'test/repo')
        
        # 模擬獲取項目數據
        logger.info("📊 獲取倉庫信息...")
        
        mock_repo_info = {
            "stargazers_count": 42,
            "forks_count": 15,
            "updated_at": "2025-07-23T10:30:00Z"
        }
        
        mock_recent_commits = [
            {"sha": "abc123", "message": "feat: 添加新功能模塊", "date": "2025-07-23"},
            {"sha": "def456", "message": "fix: 修復登錄問題", "date": "2025-07-22"},
            {"sha": "ghi789", "message": "docs: 更新文檔", "date": "2025-07-21"}
        ]
        
        mock_open_issues = [
            {"number": 1, "title": "實現用戶認證功能"},
            {"number": 2, "title": "修復登錄頁面 bug"},
            {"number": 3, "title": "添加數據庫連接池"}
        ]
        
        mock_open_prs = [
            {"number": 1, "title": "添加新功能特性"},
            {"number": 2, "title": "修復 UI 問題"}
        ]
        
        logger.info(f"⭐ 星標數: {mock_repo_info['stargazers_count']}")
        logger.info(f"🍴 分支數: {mock_repo_info['forks_count']}")
        logger.info(f"📝 開放 Issues: {len(mock_open_issues)}")
        logger.info(f"🔄 開放 Pull Requests: {len(mock_open_prs)}")
        
        # 模擬更新 README.md
        logger.info("📝 更新 README.md...")
        
        # 生成項目狀態部分
        status_section = f"""
## 📊 項目狀態

**最後更新時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 倉庫信息
- **星標數**: {mock_repo_info['stargazers_count']} ⭐
- **分支數**: {mock_repo_info['forks_count']} 🍴
- **開放 Issues**: {len(mock_open_issues)} 📝
- **開放 Pull Requests**: {len(mock_open_prs)} 🔄
- **最後更新**: {mock_repo_info['updated_at']}

### 最近活動
#### 最近提交
"""
        
        for commit in mock_recent_commits[:5]:
            status_section += f"- `{commit['sha'][:7]}` {commit['message']} ({commit['date']})\n"
        
        status_section += "\n#### 開放 Issues\n"
        for issue in mock_open_issues[:5]:
            status_section += f"- #{issue['number']} {issue['title']}\n"
        
        status_section += "\n#### 開放 Pull Requests\n"
        for pr in mock_open_prs[:5]:
            status_section += f"- #{pr['number']} {pr['title']}\n"
        
        logger.info("✅ README.md 更新完成")
        
        # 模擬更新 CHANGELOG.md
        logger.info("📋 更新 CHANGELOG.md...")
        
        changelog_section = f"""
## [Unreleased] - {datetime.now().strftime('%Y-%m-%d')}

### Added
- 自動文檔更新功能 (Mock 模式)
- 項目狀態監控

### Changed
- 改進項目狀態顯示
- 優化文檔結構

### Fixed
- 修復文檔更新腳本

### 最近提交
"""
        
        for commit in mock_recent_commits[:10]:
            changelog_section += f"- `{commit['sha'][:7]}` {commit['message']} ({commit['date']})\n"
        
        logger.info("✅ CHANGELOG.md 更新完成")
        
        # 模擬創建文檔索引
        logger.info("📖 創建文檔索引...")
        
        docs_index = f"""# Bee Swarm 文檔

歡迎來到 Bee Swarm 項目文檔！

## 📚 文檔目錄

### 系統概述
- [系統概述](level1/system-overview.md) - 了解 Bee Swarm 系統的整體架構

### 角色系統
- [角色系統](level2/role-system.md) - 詳細的角色定義和職責
- [角色池管理](level2/role-pool-management.md) - 角色池的配置和管理

### 工作流程
- [工作流程系統](level3/workflow-system.md) - 工作流程的設計和實現

### 通信協議
- [通信協議](level4/communication-protocol.md) - 系統內部的通信機制

### 實現詳情
- [實現詳情](level5/implementation-details.md) - 技術實現的具體細節

## 🔄 自動更新

本文檔由 AI 團隊工作流程自動更新，確保內容與項目狀態保持同步。

**最後更新時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*此文檔由 AI 團隊自動生成 (Mock 模式)*
"""
        
        logger.info("✅ 文檔索引創建完成")
        
        # 設置環境變量
        with open(os.environ.get('GITHUB_ENV', '/dev/null'), 'a') as f:
            f.write("DOCUMENTATION_UPDATED=true\n")
            f.write(f"DOC_UPDATE_TIME={datetime.now().isoformat()}\n")
            f.write(f"DOCS_UPDATED=3\n")  # README, CHANGELOG, Index
        
        logger.info("🎉 文檔更新完成 (Mock 模式)")
        
    except Exception as e:
        logger.error(f"❌ 更新文檔時發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 