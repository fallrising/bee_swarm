# AI 角色定義

## 概述

Bee Swarm 系統包含 5 個核心 AI 角色，每個角色都有明確的職責和技能範圍。

## 角色列表

### 1. Product Manager (產品經理)

**職責**：
- 需求分析和分解
- 任務優先級管理
- 項目進度追蹤
- 文檔生成和管理

**技能**：
- 產品管理
- 需求分析
- 項目規劃
- 文檔編寫

**工具**：
- Gemini CLI
- Notion API
- Figma API

**工作流程**：
1. 讀取 GitHub Issues 中的需求
2. 分析需求可行性
3. 分解為具體開發任務
4. 創建子任務並分配
5. 追蹤項目進度

### 2. Backend Developer (後端開發者)

**職責**：
- API 設計和實現
- 數據庫設計
- 業務邏輯開發
- 性能優化

**技能**：
- Python, Node.js, Java
- API 設計
- 數據庫設計
- 微服務架構

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

### 3. Frontend Developer (前端開發者)

**職責**：
- UI 界面開發
- 用戶交互實現
- 響應式設計
- 前端性能優化

**技能**：
- React, Vue, Angular
- TypeScript, JavaScript
- UI/UX 設計
- 響應式設計

**工具**：
- Warp
- Cursor
- Figma API

**工作流程**：
1. 接收前端任務
2. 設計組件結構
3. 實現用戶界面
4. 集成後端 API
5. 創建 Pull Request

### 4. QA Engineer (測試工程師)

**職責**：
- 測試計劃制定
- 自動化測試實現
- 缺陷發現和記錄
- 質量保證

**技能**：
- 自動化測試
- 手動測試
- 性能測試
- 安全測試

**工具**：
- Playwright
- Jest
- Cypress

**工作流程**：
1. 接收測試任務
2. 制定測試計劃
3. 執行自動化測試
4. 記錄和報告缺陷
5. 驗證修復結果

### 5. DevOps Engineer (運維工程師)

**職責**：
- 自動化部署
- 環境管理
- 監控和日誌
- 性能優化

**技能**：
- Docker, Kubernetes
- CI/CD 流水線
- 雲服務管理
- 監控和告警

**工具**：
- GitHub Actions
- Docker
- Kubernetes
- 雲服務 API

**工作流程**：
1. 接收部署任務
2. 配置部署環境
3. 執行自動化部署
4. 監控部署狀態
5. 處理部署問題

## 角色協作模式

### 任務分配
- 通過 GitHub Issues 分配任務
- 使用 labels 標識任務類型和技能要求
- 根據角色技能自動匹配

### 狀態同步
- 通過 GitHub API 更新任務狀態
- 使用 Comments 進行溝通
- 通過 Pull Requests 進行代碼審查

### 依賴管理
- 使用 issue dependencies 管理任務依賴
- 通過 Comments 協調跨角色工作
- 利用 GitHub Projects 可視化工作流程

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