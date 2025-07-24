# Bee Swarm

一個基於 GitHub 的 AI 團隊協作自動化工作流系統，通過 **容器化多角色多帳號架構** 實現真實的團隊協作體驗。

## 🎯 項目概述

Bee Swarm 採用創新的 **GitHub-Centric + 多角色多帳號** 架構，每個 AI 角色擁有獨立的帳號體系，通過容器化部署實現：

- 🔐 **真實的權限隔離**：每個角色有獨立的 GitHub 帳號和服務權限
- 🤝 **真實的協作體驗**：角色間通過 GitHub Issues、PR、Comments 進行真實協作
- 📊 **清晰的活動追蹤**：每個角色的 commit、issue 創建、PR 都有明確的身份標識
- 🔄 **獨立的服務集成**：角色可接入不同的專業工具（Figma、Supabase、AWS等）
- 🐳 **容器化管理**：簡化多帳號的部署和維護複雜度

## 🏗️ 系統架構

### 核心架構設計
```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Platform (協調中心)                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Issues │ Projects │ Actions │ Comments │ PRs │ Wiki     │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
    ┌───────────▼─┐   ┌─────────▼──┐   ┌──────▼──────┐
    │ PM Container │   │ Dev Containers│   │ DevOps Cont │
    │              │   │              │   │             │
    │ pm-bot       │   │ frontend-bot │   │ devops-bot  │
    │ @company.com │   │ backend-bot  │   │ @company.com│
    │              │   │ @company.com │   │             │
    └──────────────┘   └──────────────┘   └─────────────┘
```

### 多帳號協作流程
```
┌─────────────────────────────────────────────────────────────┐
│                   真實協作工作流                              │
├─────────────────────────────────────────────────────────────┤
│ 1. PM Bot 創建 Epic Issue                                   │
│    ├── GitHub: pm-bot@company.com                          │ 
│    ├── Email: 通知 frontend-bot & backend-bot               │
│    └── Slack: 創建專案頻道                                   │
│                                                             │
│ 2. Frontend Bot 響應並分解任務                               │
│    ├── GitHub: frontend-bot@company.com                    │
│    ├── Figma: 同步設計資源                                   │ 
│    └── Comments: @backend-bot 討論 API 需求                 │
│                                                             │
│ 3. Backend Bot 設計 API 並實作                               │
│    ├── GitHub: backend-bot@company.com                     │
│    ├── Supabase: 資料庫結構設計                             │
│    └── PR: 提交 API 實作供 review                          │
│                                                             │
│ 4. DevOps Bot 處理部署                                      │
│    ├── GitHub: devops-bot@company.com                      │
│    ├── AWS: 基礎設施管理                                    │
│    └── Actions: 自動化 CI/CD                               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速開始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- GitHub 帳戶（建議為每個角色創建獨立帳號）

### 多帳號設置

#### 1. 創建 AI 角色帳號
為每個角色創建獨立的 GitHub 帳號：
```
pm-bot@yourcompany.com          # 產品經理
frontend-bot@yourcompany.com    # 前端開發者  
backend-bot@yourcompany.com     # 後端開發者
devops-bot@yourcompany.com      # DevOps 工程師
```

#### 2. 配置角色權限
```yaml
# GitHub 權限建議配置
pm-bot:
  permissions:
    - issues:write          # 創建和管理 Issues
    - projects:admin        # 管理專案看板
    - wiki:write           # 維護文檔
    - discussions:write     # 參與討論

frontend-bot:
  permissions:
    - issues:read          # 讀取需求
    - pull_requests:write  # 提交前端代碼
    - pages:write          # 部署前端頁面

backend-bot:
  permissions:
    - issues:read          # 讀取需求
    - pull_requests:write  # 提交後端代碼
    - packages:write       # 發布套件
    - secrets:read         # 讀取部署配置

devops-bot:
  permissions:
    - actions:write        # 管理 CI/CD
    - deployments:write    # 執行部署
    - environments:write   # 管理環境
```

### 安裝步驟

1. 克隆項目：
```bash
git clone https://github.com/your-username/bee_swarm.git
cd bee_swarm
```

2. 配置環境變量：
```bash
cp env.example .env
# 編輯 .env 文件，配置每個角色的 GitHub Token 和專業服務 API Key
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

### 🤖 真實 AI 團隊協作
- **多帳號身份管理**：每個角色有獨立的 GitHub 身份和 commit 歷史
- **真實的任務分配**：PM 可以真實地 assign issues 給其他角色
- **跨角色溝通**：通過 GitHub comments、mentions、email 通知
- **權限邊界清晰**：每個角色只能訪問其職責範圍內的資源

### 🔄 異步協作工作流
- **事件驅動響應**：角色根據 GitHub events 自動響應
- **智能工作流管理**：基於 GitHub Actions 的自動化觸發
- **並行任務處理**：不同角色可同時處理不同部分
- **衝突解決機制**：自動處理 merge conflicts 和優先級

### 📊 專業服務整合
```python
# 每個角色整合專業工具
frontend_services = {
    'figma': 'design_sync',      # 設計稿同步
    'vercel': 'auto_deploy',     # 自動部署
    'lighthouse': 'performance'   # 性能監控
}

backend_services = {
    'supabase': 'database_mgmt',  # 資料庫管理
    'docker_hub': 'image_build',  # 容器映像
    'postman': 'api_testing'      # API 測試
}

devops_services = {
    'aws': 'infrastructure',      # 基礎設施
    'terraform': 'iac',          # 基礎設施即代碼
    'prometheus': 'monitoring'    # 監控告警
}
```

### 🔍 透明化協作追蹤
- **完整的協作歷史**：所有角色互動都在 GitHub 上可見
- **清晰的責任歸屬**：每個 commit、issue、PR 都有明確作者
- **協作網絡分析**：可視化角色間的協作模式
- **績效指標統計**：各角色的貢獻量化分析

## 🏗️ 項目結構

```
bee_swarm/
├── roles/                    # AI 角色定義和容器配置
│   ├── product_manager/      # PM 角色容器
│   │   ├── Dockerfile       # PM 專用容器配置
│   │   ├── prompt.md        # PM 角色 prompt
│   │   └── config/          # PM 專用工具配置
│   ├── frontend_developer/  # 前端開發者容器
│   ├── backend_developer/   # 後端開發者容器
│   └── devops_engineer/     # DevOps 工程師容器
├── scripts/                 # 工作流腳本
├── docs/                    # 專案文檔
├── docker-compose.yml       # 生產環境多容器編排
├── docker-compose.test.yml  # 測試環境配置
└── .github/workflows/       # GitHub Actions
```

## 🔧 配置說明

### 環境變量

創建 `.env` 文件並配置以下變量：

```bash
# GitHub 配置
GITHUB_REPOSITORY=your-org/your-repo
GITHUB_OWNER=your-org

# AI 角色 GitHub Token (每個角色獨立帳號)
GITHUB_TOKEN_PM_01=ghp_xxxxxxxxxxxxxxxxxxxx           # pm-bot 帳號
GITHUB_TOKEN_BACKEND_01=ghp_xxxxxxxxxxxxxxxxxxxx      # backend-bot 帳號  
GITHUB_TOKEN_FRONTEND_01=ghp_xxxxxxxxxxxxxxxxxxxx     # frontend-bot 帳號
GITHUB_TOKEN_DEVOPS_01=ghp_xxxxxxxxxxxxxxxxxxxx       # devops-bot 帳號

# 角色專用服務 API 密鑰
# PM 專用
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx

# Frontend 專用
FIGMA_TOKEN=figd_xxxxxxxxxxxxxxxxxxxx
VERCEL_TOKEN=xxxxxxxxxxxxxxxxxxxx

# Backend 專用  
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY_BACKEND=xxxxxxxxxxxxxxxxxxxx
DOCKER_HUB_TOKEN=xxxxxxxxxxxxxxxxxxxx

# DevOps 專用
AWS_ACCESS_KEY_ID=AKIA xxxxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
TERRAFORM_TOKEN=xxxxxxxxxxxxxxxxxxxx

# 通用 AI 服務
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### 容器化多角色配置

```yaml
# docker-compose.yml 範例
version: '3.8'
services:
  pm-agent:
    build: 
      context: .
      dockerfile: roles/product_manager/Dockerfile
    environment:
      - ROLE=ProductManager
      - GITHUB_TOKEN=${GITHUB_TOKEN_PM_01}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./secrets/pm:/secrets
    networks:
      - ai-team-network
      
  frontend-agent:
    build:
      context: .  
      dockerfile: roles/frontend_developer/Dockerfile
    environment:
      - ROLE=FrontendDeveloper
      - GITHUB_TOKEN=${GITHUB_TOKEN_FRONTEND_01}
      - FIGMA_TOKEN=${FIGMA_TOKEN}
      - VERCEL_TOKEN=${VERCEL_TOKEN}
    networks:
      - ai-team-network
      
  backend-agent:
    build:
      context: .
      dockerfile: roles/backend_developer/Dockerfile  
    environment:
      - ROLE=BackendDeveloper
      - GITHUB_TOKEN=${GITHUB_TOKEN_BACKEND_01}
      - SUPABASE_KEY=${SUPABASE_KEY_BACKEND}
    networks:
      - ai-team-network
      
  devops-agent:
    build:
      context: .
      dockerfile: roles/devops_engineer/Dockerfile
    environment:
      - ROLE=DevOpsEngineer  
      - GITHUB_TOKEN=${GITHUB_TOKEN_DEVOPS_01}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    networks:
      - ai-team-network

networks:
  ai-team-network:
    driver: bridge
```

## 🌟 架構優勢

### ✅ 多帳號架構的優勢

1. **真實協作體驗**
   - 真實的 GitHub 用戶互動（@mentions、assignments、reviews）
   - 完整的 email 通知工作流
   - 清晰的 commit 作者歷史

2. **權限隔離與安全**
   - 每個角色只能訪問其職責範圍內的資源
   - 細粒度的 GitHub 權限控制
   - 獨立的服務帳號，降低安全風險

3. **專業工具整合**
   - PM 整合產品管理工具（Notion、Figma、Analytics）
   - 開發者整合開發工具（GitHub、Supabase、Docker）
   - DevOps 整合基礎設施工具（AWS、Terraform、Monitoring）

4. **清晰的協作追蹤**
   - 每個 issue、PR、commit 都有明確的責任歸屬
   - 可視化的協作網絡和工作流
   - 完整的審計軌跡

### 🐳 容器化優勢

1. **管理複雜度簡化**
   - 統一的部署和擴展機制
   - 隔離的運行環境
   - 簡化的依賴管理

2. **靈活的擴展性**
   - 輕鬆添加新角色
   - 獨立的角色版本管理
   - 彈性的資源分配

3. **可靠的運行環境**
   - 一致的開發和生產環境
   - 快速的容災恢復
   - 資源使用監控

## 📈 性能優化

- **容器資源優化**：根據角色職責調整 CPU/內存配置
- **並行協作處理**：多角色可同時處理不同任務
- **智能任務調度**：基於依賴關係的任務優先級
- **緩存機制**：減少重複的 API 調用和計算

## 🔒 安全特性

- **多層權限控制**：GitHub 權限 + 容器隔離 + 服務帳號分離
- **配置驗證機制**：自動驗證所有角色的認證配置
- **敏感信息管理**：使用 GitHub Secrets 和 Docker secrets
- **審計日誌完整**：所有角色活動都有完整記錄

## 📖 文檔

詳細文檔請查看 [docs/](docs/) 目錄：

- [架構設計](docs/architecture.md) - 多帳號容器化架構詳解
- [角色定義](docs/roles.md) - AI 角色定義和職責邊界
- [工作流程](docs/workflows.md) - 跨角色協作流程和模式
- [GitHub 敏捷開發指南](docs/github-agile-methodology.md) - GitHub 敏捷開發工作流方法論
- [GitHub 進階自動化](docs/github-agile-advanced.md) - GitHub 全功能敏捷開發工作流擴展
- [部署指南](docs/deployment.md) - 多容器部署和配置說明
- [執行計劃](docs/execution-plan.md) - 項目執行計劃

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
2. 創建新的 Issue（會有對應的 AI 角色回應）
3. 聯繫維護團隊

---

*本項目由多角色 AI 團隊自動維護 - 體驗真實的 AI 協作工作流*

