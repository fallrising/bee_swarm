# GitHub 敏捷開發工作流指南

## 🏗️ 核心結構設計

### **階層架構**
```
Epic (大型功能)
├── Issue (用戶故事/功能需求)
│   ├── Sub-issue (具體開發任務)
│   ├── Sub-issue (測試任務)
│   └── Sub-issue (文檔任務)
└── Task (獨立小任務)
```

## 📋 工作項目類型定義

### **1. Epic**
- **用途**: 大型功能或產品目標
- **實現**: GitHub Issue + `epic` 標籤
- **包含**: 完整的產品需求文檔 (PRD)
- **示例**: "用戶認證系統"、"支付模組重構"

### **2. Issue**
- **用途**: 用戶故事或功能需求
- **實現**: 標準 GitHub Issue
- **包含**: 驗收標準、設計需求
- **示例**: "用戶可以通過郵箱註冊"

### **3. Sub-issues**
- **用途**: 具體的開發、測試、設計任務
- **實現**: GitHub Sub-issues 功能
- **包含**: 技術實現細節、工作估時
- **示例**: "實現註冊 API 端點"、"編寫註冊表單組件"

### **4. Task**
- **用途**: 獨立的維護或支援任務
- **實現**: GitHub Issue + `task` 標籤
- **示例**: "更新依賴套件"、"優化數據庫查詢"

## 🔄 敏捷開發流程

### **Sprint 規劃階段**
1. **Epic 分解**
   ```markdown
   # Epic: 用戶認證系統
   
   ## 產品目標
   實現完整的用戶認證流程，包括註冊、登入、密碼重設
   
   ## 驗收標準
   - [ ] 用戶可以通過郵箱註冊
   - [ ] 用戶可以登入系統
   - [ ] 用戶可以重設密碼
   
   ## 相關 Issues
   - #123 用戶註冊功能
   - #124 用戶登入功能  
   - #125 密碼重設功能
   ```

2. **Issue 創建**
   ```markdown
   # Issue: 用戶註冊功能
   
   ## 用戶故事
   作為新用戶，我希望能夠通過郵箱和密碼註冊帳號
   
   ## 驗收標準
   - [ ] 註冊表單驗證
   - [ ] 郵箱唯一性檢查
   - [ ] 密碼強度驗證
   - [ ] 確認郵件發送
   
   ## Sub-issues
   - [ ] #126 設計註冊表單 UI
   - [ ] #127 實現註冊 API
   - [ ] #128 編寫註冊測試
   ```

3. **Sub-issues 分配**
   ```markdown
   # Sub-issue: 實現註冊 API
   
   ## 技術需求
   - 建立 `/api/register` 端點
   - 實現輸入驗證
   - 密碼雜湊處理
   - 整合郵件服務
   
   ## 估時: 8 小時
   ## 負責人: @backend-dev
   ```

### **開發執行階段**

#### **1. 分支策略**
```bash
# Epic 分支
git checkout -b epic/user-authentication

# Feature 分支 (從 Epic 分支建立)
git checkout -b feature/user-registration

# Task 分支 (從 Feature 分支建立)  
git checkout -b task/registration-api
```

#### **2. Pull Request 流程**
```markdown
# PR Template
## 相關 Issue
Closes #127

## 變更說明
- 實現用戶註冊 API 端點
- 新增輸入驗證中介軟體
- 整合郵件通知服務

## 測試清單
- [ ] 單元測試通過
- [ ] 整合測試通過
- [ ] API 文檔已更新

## 審查要求
- @senior-dev (代碼架構)
- @security-lead (安全審查)
```

## 📊 GitHub Projects 看板配置

### **Epic 追蹤看板**
| 欄位名稱 | 類型 | 用途 |
|---------|------|------|
| Epic | 單選 | Epic 分類 |
| Status | 狀態 | 進行狀態 |
| Priority | 單選 | 優先級 |
| Assignee | 人員 | 負責人 |
| Progress | 計算 | 完成度 |

### **Sprint 執行看板**
```
待辦事項 | 進行中 | 審查中 | 已完成
--------|--------|--------|--------
Issue   | Issue  | PR     | Issue
Sub-issue| Sub-issue| PR   | Sub-issue
Task    | Task   | PR     | Task
```

## 🔧 自動化工作流

### **GitHub Actions 範例**
```yaml
name: Issue Management
on:
  issues:
    types: [opened, closed]
  pull_request:
    types: [opened, closed]

jobs:
  update-progress:
    runs-on: ubuntu-latest
    steps:
      - name: Update Epic Progress
        uses: actions/github-script@v6
        with:
          script: |
            // 自動更新 Epic 進度
            // 當 Sub-issue 完成時更新父 Issue
            // 當 Issue 完成時更新 Epic
```

## 📈 追蹤和報告

### **進度追蹤**
- **Epic 層級**: 查看所有相關 Issues 的完成狀態
- **Issue 層級**: 查看 Sub-issues 完成進度
- **Sprint 層級**: 使用 Milestone 追蹤衝刺目標

### **指標監控**
- Burndown Chart (通過 Projects Insights)
- Velocity 追蹤 (每 Sprint 完成的點數)
- Cycle Time (從開始到完成的時間)
- Lead Time (從創建到部署的時間)

## 🎯 最佳實踐

### **Issue 命名規範**
```
Epic: [EPIC] 功能名稱
Issue: [STORY] 作為...我希望...以便...
Sub-issue: [TASK] 具體技術任務描述
Task: [TASK] 維護/支援任務描述
```

### **標籤策略**
```
類型標籤: epic, story, task, bug
優先級: priority/high, priority/medium, priority/low
領域: frontend, backend, devops, design
狀態: blocked, in-review, ready-for-test
```

### **Milestone 管理**
- **Sprint Milestones**: Sprint 1, Sprint 2...
- **Release Milestones**: v1.0, v1.1...
- **Epic Milestones**: 按功能領域分組

---

## 📝 與 Bee Swarm 專案的整合

這個工作流讓您的團隊可以在 GitHub 原生環境中實現完整的敏捷開發流程，從高層級的 Epic 規劃到具體的開發任務執行都能有效追蹤和管理。

## 🚀 進階功能

如需更深度的 GitHub 整合和自動化功能，請參考：

👉 **[GitHub 全功能敏捷開發工作流擴展](./github-agile-advanced.md)**

進階版本包含：
- 🤖 AI 輔助代碼審查和自動化
- 📚 GitHub Wiki 自動同步
- 🔍 Advanced Security 集成
- 📊 自動化報告和效能分析
- 📱 智能通知系統
- ⚙️ 完整的 CI/CD 自動化

### **在 Bee Swarm 專案中的應用**
- **Epic**: 如 "MCP 角色系統重構"、"教育遊戲模擬引擎"
- **Issues**: 具體的角色功能需求或遊戲功能
- **Sub-issues**: 各角色的具體開發任務
- **Task**: 系統維護、文檔更新等獨立任務

### **與現有工作流的協調**
請參考 [`docs/workflows.md`](./workflows.md) 了解專案特定的技術工作流程，本文檔提供的是更高層級的專案管理方法論。 