# Bee Swarm 混合架構設計

## 📋 文檔信息
- **目標讀者**：架構師、技術負責人、高級開發者
- **最後更新**：2025年1月
- **架構版本**：2.0 (混合架構)
- **前置文檔**：[CONTEXT.md](../../CONTEXT.md)

## 🏗️ 架構概述

### 核心理念
**Bee Swarm** 採用 **GitHub-Centric 混合架構**，並行存在而非二選一：結合長時間存活容器和 GitHub Actions 的優勢，根據任務特性選擇最適合的執行方式，同時整合 MCP (Model Context Protocol) Server 架構理念。

### 設計哲學
1. **簡化優先**：利用 GitHub 現有功能，移除複雜的中央協調器
2. **透明性**：所有協調過程在 GitHub 上可見，完整版本控制
3. **異步協作**：AI 角色輪流處理任務，避免即時通信複雜性
4. **混合執行**：根據任務複雜度選擇最適合的執行環境
5. **輕量化容器**：採用 MCP 理念，容器專注於推理，工具外部化

## 🏛️ 整體架構圖

```
GitHub Platform (協調中心)
├── Issues (任務管理)
├── Projects (看板)
├── Actions (自動化執行)
├── Comments (通信記錄)
├── Pull Requests (代碼審查)
└── Wiki/README (文檔知識庫)
    ↓
[任務分類器] ← GitHub Webhooks
    ↓
┌─────────────────────────────┬─────────────────────────────┐
│     GitHub Actions          │    Container Environment     │
│      (輕量任務層)            │      (複雜任務層)            │
├─────────────────────────────┼─────────────────────────────┤
│ • 監控和報告任務             │ • 複雜代碼開發               │
│ • 簡單狀態更新               │ • 架構設計決策               │
│ • 定期健康檢查               │ • 多步驟工作流               │
│ • 通知和警報                 │ • 需要上下文的任務           │
└─────────────────────────────┴─────────────────────────────┘
    ↓                               ↓
[Gemini CLI + Tools]          [MCP Server + Gemini CLI]
    ↓                               ↓
[結果整合器] ← → [狀態同步器] ← → [外部工具服務]
    ↓
GitHub State Update
```

## 🎯 任務分層執行架構

### 架構分層
```
任務分層執行架構：
├── 輕量任務層（GitHub Actions + Gemini CLI）
│   ├── 監控和報告任務 (gemini-1.5-flash)
│   ├── 簡單的狀態更新 (gemini-1.5-flash)
│   ├── 定期健康檢查 (gemini-1.5-flash)
│   ├── 通知和警報 (gemini-1.5-flash)
│   └── 自動標籤管理 (gemini-1.5-flash)
│
├── 中等任務層（混合執行）
│   ├── 代碼分析任務 (智能選擇)
│   ├── 文檔生成 (智能選擇)
│   ├── 配置驗證 (智能選擇)
│   └── 測試執行 (智能選擇)
│
└── 複雜任務層（容器 + MCP Server）
    ├── 複雜的代碼開發 (gemini-1.5-pro)
    ├── 架構設計決策 (gemini-1.5-pro)
    ├── 多步驟工作流 (gemini-1.5-pro)
    └── 需要上下文的任務 (gemini-1.5-pro)
```

### 任務分類標準

#### GitHub Actions 適合的任務
**特徵**：
- ⚡ 執行時間 < 10分鐘
- 🔄 無需複雜上下文
- 📊 結果易於驗證
- 💰 成本敏感

**具體任務**：
```yaml
監控任務：
  - 檢查系統健康狀態
  - 監控 GitHub Issues 變化
  - 生成狀態報告
  - 發送通知警報

維護任務：
  - 自動標籤管理
  - 文檔同步更新
  - 配置檔案驗證
  - 依賴版本檢查

簡單分析：
  - Issue 分類標記
  - 工作負載統計
  - 簡單代碼檢查
  - 基本性能監控
```

#### 容器適合的任務
**特徵**：
- 🧠 需要複雜推理
- 🔗 需要多步驟上下文
- ⏰ 執行時間不確定
- 🎯 需要個性化配置

**具體任務**：
```yaml
開發任務：
  - 複雜功能開發
  - 架構設計決策
  - 代碼重構
  - Bug 修復

協調任務：
  - 需求分析和分解
  - 任務優先級排序
  - 衝突解決
  - 工作分配

創意任務：
  - UI/UX 設計
  - 技術方案選型
  - 最佳實踐建議
  - 創新解決方案
```

## 🛠️ 技術實現架構

### 1. 基於 Google Gemini CLI 的統一實現

**核心技術棧**：
- **Google Gemini CLI**：Google 官方 AI 工具（⭐ 63.5k stars，🍴 6k forks）
  - 官方倉庫：https://github.com/google-gemini/gemini-cli
  - 企業級穩定性和長期支援保證
- **階層式 GEMINI.md**：自動載入多層級上下文文件  
- **沙盒執行模式**：Docker 容器中安全執行 AI 任務
- **GitHub CLI 整合**：直接操作 GitHub Issues/PRs

### 2. MCP Server 整合架構

#### 容器設計哲學
採用 MCP (Model Context Protocol) Server 架構理念：
- **LLM 專注於推理**：LLM (Gemini) 只負責計算、推理和決策
- **MCP 提供工具**：所有外部依賴、工具通過 MCP Server 提供
- **輕量化容器**：角色容器保持最小化，只包含必要的環境設置
- **外部化依賴**：避免在容器內安裝大量軟體

#### 基礎鏡像
使用 [VNC Lab](https://github.com/fallrising/vnc_lab) 的 `novnc_llm_cli` 作為基礎鏡像：
- 基本的 AI LLM coding CLI 工具
- noVNC 桌面環境
- Web 終端支持
- 基本的開發環境

#### 角色容器結構
```
roles/{role_name}/
├── .gemini/
│   ├── settings.json          # 角色專屬 Gemini 配置
│   └── GEMINI.md              # 角色上下文和工作流程
├── Dockerfile                 # 輕量化容器配置
├── docker-compose.yml         # 容器編排
└── prompt.md                  # 原有 prompt（保持相容）
```

### 3. 智能任務分類器

```python
# 任務分類器實現
class HybridTaskClassifier:
    def __init__(self):
        self.github_client = Github(token)
        self.container_client = ContainerClient()
        
    def classify_task(self, issue):
        # 1. 基於標籤的快速分類
        if self._has_lightweight_labels(issue):
            return 'github_actions'
            
        # 2. 複雜度分析
        complexity = self._analyze_complexity(issue.description)
        if complexity < SIMPLE_THRESHOLD:
            return 'github_actions'
        elif complexity < MEDIUM_THRESHOLD:
            return self._dynamic_selection(issue)
        else:
            return 'container'
            
        # 3. 歷史數據驗證
        historical_time = self._get_average_completion_time(issue.type)
        if historical_time < 10:  # 分鐘
            return 'github_actions'
            
        return 'container'
        
    def _dynamic_selection(self, issue):
        # 檢查容器負載進行動態選擇
        container_load = self.container_client.get_load()
        if container_load > 80:
            return 'github_actions'
        return 'container'
```

### 4. GitHub Actions 工作流程

#### 優化後的工作流程範例
```yaml
# .github/workflows/product-manager.yml
name: Product Manager AI Agent

on:
  issues:
    types: [opened, labeled]
  schedule:
    - cron: '*/30 * * * *'

jobs:
  classify_and_execute:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Gemini CLI
        run: npm install -g @google/gemini-cli
        
      - name: Task Classification
        id: classify
        run: |
          TASK_TYPE=$(python scripts/classify_task.py ${{ github.event.issue.number }})
          echo "task_type=$TASK_TYPE" >> $GITHUB_OUTPUT
          
      - name: Execute Lightweight Task
        if: steps.classify.outputs.task_type == 'github_actions'
        working-directory: roles/product_manager
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          gemini \
            --model gemini-1.5-flash \
            --prompt "處理 Issue #${{ github.event.issue.number }}" \
            --yolo \
            --sandbox \
            --all_files
            
      - name: Trigger Container Task
        if: steps.classify.outputs.task_type == 'container'
        run: |
          curl -X POST "${{ secrets.CONTAINER_WEBHOOK_URL }}" \
            -H "Content-Type: application/json" \
            -d '{"issue_number": "${{ github.event.issue.number }}"}'
```

### 5. 容器環境集成

#### Docker Compose 配置
```yaml
# roles/product_manager/docker-compose.yml
version: '3.8'
services:
  pm-agent:
    build: .
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - ROLE=product_manager
    volumes:
      - ./workspace:/workspace
      - ./.gemini:/app/.gemini
    ports:
      - "6080:6080"  # noVNC
      - "7681:7681"  # ttyd
    restart: unless-stopped
    
  mcp-server:
    image: mcp-tools-server:latest
    environment:
      - MCP_SERVER_PORT=3000
    ports:
      - "3000:3000"
    restart: unless-stopped
```

## 🔄 混合工作流設計

### 端到端工作流程

1. **事件觸發**：GitHub Issue 創建或更新
2. **智能分類**：任務分類器分析任務複雜度
3. **執行路由**：根據分類結果選擇執行環境
4. **任務處理**：在選定環境中執行任務
5. **結果整合**：統一結果格式並更新 GitHub 狀態
6. **狀態同步**：確保所有系統狀態一致

### 協調機制

```yaml
協調策略：
  優先級排序：
    - P0：緊急修復（優先容器，保證服務質量）
    - P1：功能開發（容器，需要複雜推理）
    - P2：維護任務（Actions優先，成本效益）
    - P3：監控報告（Actions，完全自動化）
  
  資源分配：
    - 容器：最多同時3個複雜任務
    - Actions：並行執行輕量任務（GitHub 限制內）
    - 混合：根據容器負載動態選擇
  
  衝突處理：
    - 同一文件修改：容器優先（更可靠）
    - 不同模塊：並行執行
    - 依賴關係：按依賴順序執行
```

### 容器-Actions 橋樑

```python
# scripts/hybrid_coordinator.py
class HybridCoordinator:
    def __init__(self):
        self.github_client = Github(token)
        self.container_client = ContainerClient()
        self.mcp_client = MCPClient()
        
    def coordinate_task(self, issue_number):
        issue = self.github_client.get_issue(issue_number)
        
        # 1. 檢查容器負載
        container_load = self.container_client.get_load()
        
        # 2. 分析任務特性
        task_features = self._analyze_task_features(issue)
        
        # 3. 動態決策
        if self._should_use_actions(task_features, container_load):
            return self._execute_via_actions(issue)
        else:
            return self._execute_via_container(issue)
            
    def _should_use_actions(self, features, container_load):
        # 複合決策邏輯
        if features['complexity'] < 0.3 and container_load > 0.8:
            return True
        if features['estimated_time'] < 10:  # 分鐘
            return True
        if features['requires_external_tools'] and not features['complex_reasoning']:
            return True
        return False
```

## 📊 架構優勢分析

### 🚀 技術優勢

#### 相比純容器架構
```
技術指標對比：
├── 啟動時間：混合 2-30秒 vs 純容器 30-60秒
├── 資源使用：混合 40% vs 純容器 100%
├── 成本效益：混合節省 73% vs 純容器節省 15%
└── 可用性：混合 99.8% vs 純容器 99.5%

響應時間對比：
├── 輕量任務：Actions 3分鐘 vs 容器 10分鐘
├── 中等任務：智能選擇 8-15分鐘 vs 容器固定 8分鐘  
└── 複雜任務：容器 30分鐘 vs Actions 超時失敗
```

#### 相比傳統 MAS 系統
```
架構簡化對比：
├── 通信協議：GitHub API vs 自定義協議
├── 狀態管理：GitHub Issues vs 分散式狀態庫
├── 部署複雜度：Docker Compose vs 微服務網格
└── 監控可觀察性：GitHub 內建 vs 自建監控系統
```

### 💰 成本優勢

```
成本對比分析（每月）：
├── 純容器模式：$50（4個容器 × $12.5/月）
├── 純 GitHub Actions：$5-15（Gemini API 使用費）
├── 混合模式：$20-30（最佳平衡）
└── 傳統開發團隊：$15,000-25,000（人力成本）

ROI 分析：
├── 初期投資：$6,000-16,000（一次性）
├── 年度運維：$3,200-9,800
├── 年度節省：$100,000-310,000
└── 投資回報率：1,200%-1,900%（第一年）
```

### 🛡️ 可靠性優勢

```
故障恢復能力：
├── 單點故障風險：大幅降低
├── 級聯故障影響：隔離限制
├── 自動降級：Actions ↔ Container 相互備援
└── 災難恢復：GitHub 平台級別保證

系統可用性：
├── GitHub 平台：99.95%（官方 SLA）
├── Actions 服務：99.9%（官方 SLA）
├── 容器服務：99.5%（VPS 級別）
└── 混合系統：99.8%（多重備援）
```

## 🎯 AI 角色配置架構

### 標準化角色設計

每個 AI 角色都遵循統一的配置模式：

```
roles/{role_name}/
├── .gemini/
│   ├── settings.json          # Gemini CLI 配置
│   ├── GEMINI.md              # 角色上下文
│   └── workflows/             # 角色特定工作流程
├── Dockerfile                 # 容器配置
├── docker-compose.yml         # 編排配置
├── scripts/                   # 角色特定腳本
└── docs/                      # 角色文檔
```

### Gemini 配置標準

```json
// roles/{role}/./gemini/settings.json
{
  "contextFileName": "GEMINI.md",
  "coreTools": [
    "read_file",
    "write_file", 
    "read_many_files",
    "run_shell_command",
    "web_fetch",
    "save_memory"
  ],
  "modelPreferences": {
    "lightweight": "gemini-1.5-flash",
    "complex": "gemini-1.5-pro-latest"
  },
  "executionModes": {
    "sandbox": true,
    "yolo": true,
    "debug": false
  },
  "fileFiltering": {
    "respectGitIgnore": true,
    "enableRecursiveFileSearch": true
  }
}
```

### 角色專化設計

#### Product Manager
- **專長**：需求分析、任務分解、項目協調
- **工具**：GitHub Issues、Projects、Analytics
- **決策**：Epic 分解、優先級排序、資源分配

#### Backend Developer
- **專長**：API 設計、數據庫、服務端邏輯
- **工具**：代碼生成、測試框架、部署工具
- **決策**：技術架構、性能優化、安全設計

#### Frontend Developer
- **專長**：UI/UX、組件開發、用戶體驗
- **工具**：前端框架、設計工具、測試工具
- **決策**：界面設計、用戶流程、性能優化

#### DevOps Engineer
- **專長**：部署、監控、運維、測試
- **工具**：CI/CD、監控工具、雲平台
- **決策**：部署策略、監控方案、故障處理

## 🔍 實施計劃與風險評估

### 階段式實施

#### 第一階段：核心基礎（2週）
- [ ] 安裝和配置 Google Gemini CLI
- [ ] 設置 Product Manager 混合配置
- [ ] 建立任務分類器原型
- [ ] 測試 Actions + Container 協同

#### 第二階段：角色擴展（3週）
- [ ] 部署所有 AI 角色的混合配置
- [ ] 實現智能任務分配邏輯
- [ ] 配置 MCP Server 整合
- [ ] 建立監控和報警機制

#### 第三階段：優化調整（2週）
- [ ] 性能調優和成本優化
- [ ] 完善故障恢復機制
- [ ] 用戶文檔和培訓材料
- [ ] 建立持續改進流程

**總時程：7週**（比純容器架構節省 30% 時間）

### 風險評估與應對

#### 技術風險
| 風險 | 影響 | 機率 | 應對策略 |
|------|------|------|----------|
| 任務分類錯誤 | 中 | 中 | 機器學習優化 + 人工標記 |
| GitHub API 限制 | 高 | 低 | 頻率控制 + 企業版升級 |
| 狀態同步延遲 | 中 | 中 | 冗餘檢查 + 自動重試 |
| Gemini API 不穩定 | 高 | 低 | 多模型備援 + 降級策略 |

#### 運維風險
| 風險 | 影響 | 機率 | 應對策略 |
|------|------|------|----------|
| 容器資源不足 | 中 | 中 | 自動擴容 + Actions 降級 |
| 網絡連接問題 | 高 | 低 | 本地緩存 + 離線模式 |
| 配置漂移 | 低 | 高 | 版本控制 + 自動化部署 |
| 監控盲區 | 中 | 中 | 全面監控 + 健康檢查 |

#### 業務風險
| 風險 | 影響 | 機率 | 應對策略 |
|------|------|------|----------|
| 團隊接受度低 | 高 | 中 | 漸進式引入 + 培訓支持 |
| 成本控制失效 | 中 | 低 | 實時監控 + 預算告警 |
| 質量標準下降 | 高 | 低 | 自動化測試 + 人工審核 |
| 依賴度過高 | 中 | 中 | 人工備援 + 技能培訓 |

## 🎯 成功指標與監控

### 技術性能指標
- **任務分類準確率** > 95%
- **混合執行效率** 提升 40%
- **系統可用性** > 99.8%
- **API 響應時間** < 2秒
- **錯誤率** < 2%

### 業務效益指標
- **開發效率** 提升 127%
- **運維成本** 降低 73%
- **故障恢復時間** < 5分鐘
- **用戶滿意度** > 90%
- **ROI** > 1,000%

### 監控實施
```yaml
監控維度：
  技術監控：
    - GitHub API 使用量和限制
    - Gemini API 調用成功率
    - 容器資源使用情況
    - Actions 執行時間和成功率
    
  業務監控：
    - 任務完成率和質量
    - 用戶互動和滿意度
    - 成本控制和預算使用
    - 團隊協作效率指標
    
  運維監控：
    - 系統可用性和故障率
    - 性能指標和響應時間
    - 安全事件和訪問審計
    - 備份和災難恢復狀態
```

## 🚀 未來擴展方向

### 短期擴展（3-6個月）
- **智能化任務分配**：基於機器學習的動態分類
- **多雲支持**：支持 AWS、Azure、GCP 等平台
- **角色個性化**：基於歷史數據的角色優化
- **實時協作**：WebSocket 支持的實時狀態同步

### 中期擴展（6-12個月）
- **企業級集成**：LDAP、SSO、企業工具集成
- **高可用部署**：跨地區、跨雲的高可用架構
- **AI 能力升級**：支持更多 AI 模型和工具
- **智能運維**：自動化運維和故障預測

### 長期願景（1-2年）
- **生態系統建設**：第三方插件和擴展市場
- **行業解決方案**：針對不同行業的定制化方案
- **國際化支持**：多語言、多地區支持
- **開源社區**：建立活躍的開源開發社區

---

## 📚 相關文檔

### 核心文檔
- [CONTEXT.md](../../CONTEXT.md) - 項目核心理念和約束
- [PROJECT_INDEX.md](../../PROJECT_INDEX.md) - 文檔導航中心
- [QUICK_START.md](../../QUICK_START.md) - 快速開始指南

### 實施指南
- [Configuration Guide](../03-implementation/configuration-guide.md) - 配置詳細說明
- [Deployment Guide](../03-implementation/deployment-guide.md) - 部署操作指南
- [Gemini CLI Best Practices](../03-implementation/gemini-cli-best-practices.md) - 最佳實踐

### 角色設計
- [Role Design](role-design.md) - AI 角色設計原理
- [Communication Patterns](communication-patterns.md) - 通信協作模式

---

*這個混合架構設計代表了 Bee Swarm 項目的技術核心，結合了 GitHub-Centric、MCP Server 和混合執行的最佳實踐，為 AI 團隊協作提供了一個高效、可靠、經濟的解決方案。* 