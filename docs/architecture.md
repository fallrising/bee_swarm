# Bee Swarm 架構設計

## 概述

Bee Swarm 是一個基於 GitHub 的 AI 團隊協作系統，採用 **GitHub-Centric** 架構，通過 GitHub 的現有功能實現 AI 角色之間的協調和通信。

## 核心架構

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

## 設計原則

### 1. 簡化優先
- 移除複雜的中央協調器
- 利用 GitHub 現有功能
- 最小化外部依賴

### 2. 透明性
- 所有協調過程在 GitHub 上可見
- 完整的版本控制歷史
- 清晰的審計軌跡

### 3. 異步協作
- AI 角色輪流處理任務
- 通過 GitHub 狀態同步
- 避免即時通信的複雜性

## 工作流程

### 任務分配流程
1. **需求輸入**：用戶在 GitHub Issues 中描述需求
2. **自動觸發**：GitHub Actions 定時掃描新任務
3. **角色分配**：根據 issue labels 分配給合適的 AI 角色
4. **任務處理**：AI 容器啟動並處理任務
5. **狀態更新**：通過 GitHub API 更新任務狀態

### 協作流程
1. **任務分解**：Product Manager 將大任務分解為小任務
2. **開發協作**：Backend/Frontend 開發者並行開發
3. **代碼審查**：通過 Pull Requests 進行代碼審查
4. **測試驗證**：DevOps Engineer 執行測試和部署
5. **部署上線**：DevOps Engineer 處理部署和監控

## 技術實現

### GitHub Actions 觸發
```yaml
# .github/workflows/ai-trigger.yml
name: AI Task Trigger
on:
  schedule:
    - cron: '*/30 * * * *'  # 每30分鐘觸發
  issues:
    types: [opened, assigned, labeled]

jobs:
  trigger-ai:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger AI containers
        run: |
          # 根據issue類型觸發對應的AI容器
```

### AI 容器設計
```python
# 每個AI容器的啟動邏輯
async def main():
    # 1. 讀取角色說明書
    role_config = load_role_config()
    
    # 2. 通過GitHub API獲取待處理issues
    pending_issues = get_pending_issues(role_config.skills)
    
    # 3. 處理任務
    for issue in pending_issues:
        await process_issue(issue, role_config)
        
    # 4. 更新狀態
    update_issue_status(issue)
```

## 優勢

### 相比複雜協調器的優勢
1. **簡化架構**：減少一個複雜的組件
2. **利用現有工具**：GitHub 已經很成熟
3. **透明性**：所有協調過程都在 GitHub 上可見
4. **版本控制**：所有變更都有歷史記錄
5. **權限管理**：利用 GitHub 的權限系統

### 實際效果
- 降低維護複雜度
- 提高系統可靠性
- 簡化部署流程
- 增強可觀察性 