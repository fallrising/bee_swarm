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
├── Product Manager (產品經理)
├── Backend Developer (後端開發者)
├── Frontend Developer (前端開發者)
└── DevOps Engineer (運維工程師)
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

3. 驗證配置：
```bash
python3 scripts/validate_config.py
```

4. 啟動系統：
```bash
# 生產環境
./scripts/switch_env.sh production

# 或測試環境
./scripts/switch_env.sh test
```

## 📋 核心功能

### 🤖 AI 團隊協作
- 基於 GitHub Issues 的任務分配
- 智能工作流管理
- 異步協作通信
- 明確的角色職責邊界

### 🔄 自動化工作流
- GitHub Actions 集成
- 定時任務觸發
- 事件驅動響應
- 配置驗證機制

### 📊 透明化管理
- 所有協調過程在 GitHub 上可見
- 完整的版本控制歷史
- 清晰的審計軌跡
- 簡化的架構設計

## 🏗️ 項目結構

```
bee_swarm/
├── roles/               # AI 角色定義
├── scripts/             # 工作流腳本
├── docs/                # 項目文檔
├── docker-compose.yml   # 生產環境配置
├── docker-compose.test.yml # 測試環境配置
└── .github/workflows/   # GitHub Actions
```

## 🔧 配置說明

### 環境變量

創建 `.env` 文件並配置以下變量：

```bash
# GitHub 配置
GITHUB_REPOSITORY=your-org/your-repo
GITHUB_OWNER=your-org

# AI 角色 GitHub Token
GITHUB_TOKEN_PM_01=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_BACKEND_01=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_FRONTEND_01=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_DEVOPS_01=ghp_xxxxxxxxxxxxxxxxxxxx

# AI 工具 API 密鑰
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### GitHub Secrets

在 GitHub 倉庫設置中添加以下 secrets：

- `GITHUB_TOKEN_PM_01`: 產品經理的 GitHub Token
- `GITHUB_TOKEN_BACKEND_01`: 後端開發者的 GitHub Token
- `GITHUB_TOKEN_FRONTEND_01`: 前端開發者的 GitHub Token
- `GITHUB_TOKEN_DEVOPS_01`: DevOps 工程師的 GitHub Token
- `OPENAI_API_KEY`: OpenAI API 密鑰
- `ANTHROPIC_API_KEY`: Anthropic API 密鑰
- `GEMINI_API_KEY`: Gemini API 密鑰

## �� 環境管理

### 生產環境
```bash
# 啟動生產環境
./scripts/switch_env.sh production

# 檢查狀態
./scripts/switch_env.sh status

# 驗證配置
./scripts/switch_env.sh validate
```

### 測試環境
```bash
# 啟動測試環境
./scripts/switch_env.sh test

# 清理環境
./scripts/switch_env.sh cleanup
```

## 📖 文檔

詳細文檔請查看 [docs/](docs/) 目錄：

- [架構設計](docs/architecture.md) - 系統架構和設計原則
- [角色定義](docs/roles.md) - AI 角色定義和職責
- [工作流程](docs/workflows.md) - 工作流程和協作模式
- [部署指南](docs/deployment.md) - 部署和配置說明
- [執行計劃](docs/execution-plan.md) - 項目執行計劃

## 🔒 安全特性

- **配置驗證**: 自動驗證環境變量配置
- **GitHub Secrets**: 使用 GitHub Secrets 管理敏感信息
- **環境分離**: 測試和生產環境完全分離
- **資源限制**: 合理的容器資源配置

## 📈 性能優化

- **簡化架構**: 移除不必要的基礎設施組件
- **資源優化**: 根據角色需求調整資源配置
- **快速啟動**: 優化容器啟動時間
- **配置簡化**: 大幅減少配置複雜度

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

