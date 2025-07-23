# Bee Swarm

一個基於 GitHub 的 AI 團隊協作自動化工作流系統。

## 🎯 項目概述

Bee Swarm 採用 **GitHub-Centric** 架構，通過 GitHub 的現有功能實現 AI 角色之間的協調和通信，簡化系統架構，提高可維護性。

## 🏗️ 系統架構

```
GitHub Platform (協調中心)
├── Issues (任務管理)
├── Projects (看板)
├── Actions (觸發器)
├── Comments (通信)
├── Pull Requests (代碼審查)
└── Wiki/README (文檔)

    ↓

AI Containers (角色容器)
├── Product Manager
├── Backend Developer
├── Frontend Developer
├── QA Engineer
└── DevOps Engineer
```

## 🚀 快速開始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- GitHub 帳戶

### 安裝步驟

1. 克隆項目：
```bash
git clone https://github.com/your-username/bee_swarm.git
cd bee_swarm
```

2. 配置環境變量：
```bash
cp env.example .env
# 編輯 .env 文件，配置 GitHub Token 和 AI 工具 API Key
```

3. 構建和啟動容器：
```bash
docker-compose up -d
```

## 📋 核心功能

### 🤖 AI 團隊協作
- 基於 GitHub Issues 的任務分配
- 智能工作流管理
- 異步協作通信

### 🔄 自動化工作流
- GitHub Actions 集成
- 定時任務觸發
- 事件驅動響應

### 📊 透明化管理
- 所有協調過程在 GitHub 上可見
- 完整的版本控制歷史
- 清晰的審計軌跡

## 🏗️ 項目結構

```
bee_swarm/
├── roles/               # AI 角色定義
├── scripts/             # 工作流腳本
├── docs/                # 項目文檔
└── .github/workflows/   # GitHub Actions
```

## 🔧 配置說明

### 環境變量

創建 `.env` 文件並配置以下變量：

```bash
# GitHub 配置
GITHUB_TOKEN_PM=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_BACKEND=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_FRONTEND=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_QA=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_DEVOPS=ghp_xxxxxxxxxxxxxxxxxxxx

# GitHub 倉庫配置
GITHUB_REPOSITORY=your-username/bee_swarm
GITHUB_OWNER=your-username

# AI 工具配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### GitHub Secrets

在 GitHub 倉庫設置中添加以下 secrets：

- `GITHUB_TOKEN_PM`: Product Manager 的 GitHub Token
- `GITHUB_TOKEN_BACKEND`: Backend Developer 的 GitHub Token
- `GITHUB_TOKEN_FRONTEND`: Frontend Developer 的 GitHub Token
- `GITHUB_TOKEN_QA`: QA Engineer 的 GitHub Token
- `GITHUB_TOKEN_DEVOPS`: DevOps Engineer 的 GitHub Token

## 🧪 測試模式

目前所有腳本運行在 **測試模式** 下：

- ✅ 無需配置複雜的外部服務
- ✅ 工作流可立即運行
- ✅ 所有數據都是預設的測試數據
- ✅ 便於開發和測試

### 測試腳本列表

- `check_pending_tasks.py` - 檢查待處理任務
- `trigger_ai_containers.py` - 觸發 AI 容器
- `notify_role_assignment.py` - 通知角色分配
- `handle_pr_events.py` - 處理 PR 事件
- `check_system_health.py` - 檢查系統健康狀態
- `create_backup.py` - 創建系統備份
- `update_documentation.py` - 更新項目文檔

### 運行測試

```bash
# 測試所有腳本
python3 scripts/test_scripts.py

# 測試單個腳本
python3 scripts/check_pending_tasks.py
```

## 📖 文檔

詳細文檔請查看 [docs/](docs/) 目錄：

- [架構設計](docs/architecture.md) - 系統架構和設計原則
- [角色定義](docs/roles.md) - AI 角色定義和職責
- [工作流程](docs/workflows.md) - 工作流程和協作模式
- [部署指南](docs/deployment.md) - 部署和配置說明
- [執行計劃](docs/execution-plan.md) - 項目執行計劃
- [工作流修復記錄](docs/workflow-fixes.md) - 工作流修復歷史

## 🤝 貢獻

1. Fork 本項目
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 創建 Pull Request

## 📄 許可證

本項目採用 MIT 許可證 - 詳見 [LICENSE](LICENSE) 文件

## 🆘 支持

如果遇到問題或有建議，請：

1. 查看 [Issues](../../issues) 頁面
2. 創建新的 Issue
3. 聯繫維護團隊

---

*本項目由 AI 團隊自動維護*

