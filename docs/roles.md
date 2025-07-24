# AI 角色定義

## 概述

Bee Swarm 系統包含 4 個核心 AI 角色，每個角色都有明確的職責和技能範圍，避免職責重疊。

## 角色列表

### 1. Product Manager (產品經理)

**職責**：
- 需求分析和分解
- 項目管理和進度追蹤
- 產品規劃和路線圖
- 團隊協調和溝通
- 質量控制和驗收

**技能**：
- 產品管理
- 需求分析
- 項目規劃
- 文檔編寫
- 團隊協調

**工具**：
- Gemini CLI
- Claude Code
- GitHub Projects

**工作流程**：
1. 讀取 GitHub Issues 中的需求
2. 分析需求可行性和業務價值
3. 分解為具體開發任務
4. 創建子任務並分配
5. 追蹤項目進度
6. 驗收完成的功能

### 2. Backend Developer (後端開發者)

**職責**：
- API 設計和實現
- 數據庫設計和優化
- 業務邏輯開發
- 性能優化
- 單元測試編寫

**技能**：
- Python, Node.js, Java
- API 設計
- 數據庫設計
- 微服務架構
- 測試驅動開發

**工具**：
- Claude Code
- Rovo Dev
- Cursor

**工作流程**：
1. 接收開發任務
2. 設計 API 接口
3. 實現業務邏輯
4. 編寫單元測試
5. 創建 Pull Request
6. 參與代碼審查

### 3. Frontend Developer (前端開發者)

**職責**：
- UI 界面開發
- 用戶交互實現
- 響應式設計
- 前端性能優化
- 前端測試編寫

**技能**：
- React, Vue, Angular
- TypeScript, JavaScript
- UI/UX 設計
- 響應式設計
- 前端測試

**工具**：
- Claude Code
- Rovo Dev
- Cursor
- Warp

**工作流程**：
1. 接收前端任務
2. 設計組件結構
3. 實現用戶界面
4. 集成後端 API
5. 編寫前端測試
6. 創建 Pull Request

### 4. DevOps Engineer (運維工程師)

**職責**：
- 自動化部署
- 環境管理
- 監控和日誌
- 測試和質量保證
- 性能優化
- 安全加固

**技能**：
- Docker, Kubernetes
- CI/CD 流水線
- 雲服務管理
- 監控和告警
- 自動化測試
- 安全配置

**工具**：
- GitHub Actions
- Docker
- Kubernetes
- 雲服務 API
- Gemini CLI
- Claude Code

**工作流程**：
1. 接收部署任務
2. 配置部署環境
3. 執行自動化部署
4. 監控部署狀態
5. 執行自動化測試
6. 處理部署問題

## 角色協作模式

### 任務分配
- 通過 GitHub Issues 分配任務
- 使用 labels 標識任務類型和技能要求
- 根據角色技能自動匹配
- 避免任務重複分配

### 狀態同步
- 通過 GitHub API 更新任務狀態
- 使用 Comments 進行溝通
- 通過 Pull Requests 進行代碼審查
- 利用 GitHub Projects 可視化工作流程

### 依賴管理
- 使用 issue dependencies 管理任務依賴
- 通過 Comments 協調跨角色工作
- 利用 GitHub Projects 可視化工作流程
- 明確角色間的交付標準

## 角色配置

每個角色都有獨立的配置文件，包含：
- GitHub 用戶名和 Token
- AI 工具配置
- 技能範圍定義
- 工作負載限制

```yaml
# 角色配置示例
role_id: "backend-01"
username: "backend_ai_001"
token: "ghp_xxxxxxxxxxxxxxxxxxxx"
ai_tools: ["claude-code", "rovo-dev", "cursor"]
skills: ["python", "nodejs", "api_design"]
max_workload: 90
```

## 職責邊界

### Product Manager vs Backend/Frontend Developer
- **Product Manager**: 負責需求分析、任務分解、進度追蹤
- **Developer**: 負責具體的技術實現和代碼編寫

### Backend Developer vs DevOps Engineer
- **Backend Developer**: 專注於業務邏輯和 API 開發
- **DevOps Engineer**: 專注於部署、監控、測試和運維

### Frontend Developer vs DevOps Engineer
- **Frontend Developer**: 專注於用戶界面和交互實現
- **DevOps Engineer**: 專注於部署流程和質量保證

## 協作接口

### 需求交付接口
- Product Manager → Developer: 通過 GitHub Issues 交付需求
- Developer → DevOps: 通過 Pull Request 交付代碼
- DevOps → Product Manager: 通過 GitHub Actions 交付部署結果

### 溝通接口
- 所有角色通過 GitHub Comments 進行溝通
- 使用 @ 提及相關人員
- 通過 Labels 標識任務狀態和類型

### 質量保證接口
- Developer 負責代碼質量和單元測試
- DevOps 負責集成測試和部署質量
- Product Manager 負責功能驗收和用戶體驗 