# Bee Swarm Gemini CLI 最佳實踐指南

## 📚 官方文檔參考

- **官方 GitHub 倉庫**：https://github.com/google-gemini/gemini-cli（⭐ 63.5k stars）
- **配置文檔**：https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md
- **工具說明**：https://github.com/google-gemini/gemini-cli/blob/main/docs/

## 🎯 參數使用策略

基於 Bee Swarm 專案的混合架構設計和 Google 官方 Gemini CLI，以下是參數的最佳使用方式。

### 📋 任務分類與參數選擇

#### 🚀 輕量任務（GitHub Actions）
**特徵**：快速執行、成本敏感、簡單邏輯
```bash
gemini \
  --model gemini-1.5-flash \
  --prompt "執行簡單任務" \
  --yolo \
  --sandbox
```

**典型場景**：
- Issue 標籤分類
- 狀態報告生成
- 簡單的文檔更新
- 基本的項目統計

#### 🧠 複雜任務（GitHub Actions 或容器）
**特徵**：需要深度分析、複雜推理、多步驟操作
```bash
gemini \
  --model gemini-1.5-pro-latest \
  --prompt "執行複雜分析任務" \
  --yolo \
  --sandbox \
  --all_files \
  --checkpointing \
  --debug_mode
```

**典型場景**：
- Epic 分解和 PRD 撰寫
- 架構設計決策
- 複雜的需求分析
- 跨模塊的重構計劃

#### 🔧 維護任務（定期執行）
**特徵**：定期執行、穩定可靠、無需交互
```bash
gemini \
  --model gemini-1.5-flash \
  --prompt "執行維護檢查" \
  --yolo \
  --sandbox \
  --all_files
```

**典型場景**：
- 項目健康檢查
- 依賴版本檢查
- 文檔同步更新
- 性能指標收集

## 💰 成本優化策略

### 模型選擇決策樹
```
任務複雜度？
├── 簡單邏輯
│   └── gemini-1.5-flash (💰 低成本)
├── 中等複雜度  
│   └── gemini-1.5-flash + --all_files (📊 上下文增強)
└── 高複雜度
    └── gemini-1.5-pro-latest (🧠 高精度)
```

### 成本控制實踐
```bash
# ✅ 成本友好的組合
--model gemini-1.5-flash --prompt "簡單任務"

# ⚖️ 平衡性能和成本
--model gemini-1.5-flash --all_files --prompt "中等任務"

# 💎 高精度，用於關鍵任務
--model gemini-1.5-pro-latest --all_files --checkpointing
```

### 實際成本估算
```
每月預估使用量：
├── 輕量任務：200次 × Flash API = $2-5
├── 中等任務：50次 × Flash + 上下文 = $3-8  
└── 複雜任務：10次 × Pro = $5-15

總計：$10-28/月 (vs 容器 $50/月)
節省：45-80%
```

## 🛡️ 安全與可靠性

### 生產環境參數組合
```bash
# 🔒 最安全的執行方式
gemini \
  --sandbox \                 # 沙盒隔離
  --yolo \                    # 自動執行（無人值守）
  --debug_mode \              # 詳細日誌
  --checkpointing \           # 任務檢查點
  --telemetry                 # 遙測監控
```

### 沙盒配置最佳實踐
```dockerfile
# roles/product_manager/.gemini/sandbox.Dockerfile
FROM gemini-cli-sandbox

# 安裝項目特定依賴
RUN apt-get update && apt-get install -y \
    git \
    gh \
    jq

# 配置 GitHub CLI
COPY ./scripts/setup-gh.sh /setup-gh.sh
RUN chmod +x /setup-gh.sh
```

### 錯誤處理策略
```bash
# 🔄 帶降級的執行方式
gemini \
  --model gemini-1.5-pro-latest \
  --prompt "複雜任務" \
  --yolo \
  --sandbox \
  --debug_mode \
  || gemini \
     --model gemini-1.5-flash \
     --prompt "簡化版任務" \
     --yolo \
     --sandbox
```

## 📊 監控與除錯

### 日誌與遙測配置
```bash
# 📈 完整的監控設置
gemini \
  --debug_mode \                          # 詳細日誌
  --telemetry \                           # 啟用遙測
  --telemetry-log-prompts \               # 記錄 prompt
  --show_memory_usage \                   # 記憶使用情況
  --prompt "任務描述"
```

### GitHub Actions 整合監控
```yaml
# .github/workflows 中的監控配置
- name: Execute with Monitoring
  run: |
    # 執行任務並收集指標
    gemini \
      --prompt "$TASK_PROMPT" \
      --yolo \
      --sandbox \
      --debug_mode \
      --telemetry \
      2>&1 | tee gemini-execution.log
      
    # 分析執行結果
    if [ $? -eq 0 ]; then
      echo "✅ 任務成功執行"
      gh issue comment $ISSUE_NUMBER --body "AI Agent 成功完成任務"
    else
      echo "❌ 任務執行失敗"
      gh issue comment $ISSUE_NUMBER --body "AI Agent 執行失敗，請檢查日誌"
    fi

- name: Upload Execution Logs
  uses: actions/upload-artifact@v4
  with:
    name: gemini-logs
    path: gemini-execution.log
```

## 🔄 記憶管理策略

### 上下文檔案層級
```
專案上下文層級：
1. ~/.gemini/GEMINI.md              # 全域設定
2. project/.gemini/GEMINI.md        # 專案設定  
3. roles/pm/.gemini/GEMINI.md       # 角色設定
4. --all_files                      # 自動載入所有檔案
```

### 記憶最佳實踐
```bash
# 🧠 智能上下文管理
gemini \
  --all_files \                     # 自動載入專案檔案
  --prompt "基於專案上下文執行任務" \
  --yolo \
  --sandbox

# 📝 手動記憶管理
gemini
/memory show                        # 檢視當前記憶
/memory refresh                     # 重新載入上下文
```

## 📋 角色專屬配置範例

### Product Manager
```json
// roles/product_manager/.gemini/settings.json
{
  "contextFileName": "GEMINI.md",
  "coreTools": ["read_file", "write_file", "run_shell_command", "web_fetch"],
  "fileFiltering": {
    "respectGitIgnore": true,
    "enableRecursiveFileSearch": true
  }
}
```

```bash
# PM 典型任務執行
gemini \
  --model gemini-1.5-pro-latest \
  --prompt "分析 Epic 並創建 PRD" \
  --yolo \
  --sandbox \
  --all_files \
  --checkpointing
```

### Backend Developer
```bash
# 後端開發任務
gemini \
  --model gemini-1.5-flash \
  --prompt "實現 API 端點" \
  --yolo \
  --sandbox \
  --debug_mode
```

### DevOps Engineer
```bash
# 運維任務
gemini \
  --model gemini-1.5-flash \
  --prompt "檢查部署狀態" \
  --yolo \
  --sandbox \
  --telemetry
```

## 🚀 CI/CD 集成模式

### 事件驅動執行
```yaml
# GitHub Actions 觸發器
on:
  issues:
    types: [opened, labeled]        # Epic 分析
  schedule:
    - cron: "0 */2 * * *"          # 定期協調
  workflow_dispatch:               # 手動觸發
    inputs:
      task_type:
        type: choice
        options:
        - epic_analysis
        - project_coordination  
        - requirement_analysis
```

### 並行執行策略
```yaml
jobs:
  lightweight_tasks:
    runs-on: ubuntu-latest
    if: contains(github.event.issue.labels.*.name, 'quick')
    steps:
      - run: gemini --model gemini-1.5-flash --prompt "輕量任務" --yolo
      
  complex_tasks:
    runs-on: ubuntu-latest  
    if: contains(github.event.issue.labels.*.name, 'epic')
    steps:
      - run: gemini --model gemini-1.5-pro-latest --prompt "複雜分析" --yolo --checkpointing
```

## 📈 效能優化建議

### 快取策略
```bash
# ⚡ 利用 GitHub Actions 快取
- uses: actions/cache@v4
  with:
    path: ~/.gemini
    key: gemini-cache-${{ hashFiles('**/.gemini/GEMINI.md') }}
```

### 批次處理
```bash
# 📦 批次處理多個 Issues  
gemini \
  --prompt "分析以下 Issues 並批次處理：$ISSUE_LIST" \
  --all_files \
  --yolo \
  --sandbox
```

## 🎯 成功指標追蹤

### KPI 監控
```
技術指標：
├── 任務完成率 > 95%
├── 平均執行時間 < 5分鐘  
├── 錯誤率 < 3%
└── 成本控制在預算內

業務指標：
├── Epic 分解準確率 > 90%
├── PRD 質量評分 > 4/5
├── 開發效率提升 > 40%
└── 協作滿意度 > 85%
```

### 持續改進
```bash
# 📊 定期分析執行數據
gemini \
  --prompt "分析過去一週的 AI Agent 執行數據，提供優化建議" \
  --model gemini-1.5-pro-latest \
  --all_files \
  --yolo
```

---

*這些最佳實踐確保 Bee Swarm 的混合架構能夠高效、安全、經濟地運行，充分發揮 Gemini CLI 的強大功能。* 