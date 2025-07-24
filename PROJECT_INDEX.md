# Bee Swarm 項目文件索引

## 🎯 項目概覽

**Bee Swarm** 是一個基於 GitHub 的 AI 團隊協作概念設計與模擬框架，專注於探索 AI 角色如何透過異步分工實現高效協作。

## 📚 核心文檔導航

### 🚀 快速開始（新用戶必讀）

| 文檔 | 描述 | 重要性 |
|------|------|--------|
| [README.md](README.md) | 項目總體介紹和快速開始 | ⭐⭐⭐ |
| [官方快速開始指南.md](官方快速開始指南.md) | 基於 Google Gemini CLI 的詳細實施指南 | ⭐⭐⭐ |
| [CONTEXT.md](CONTEXT.md) | **核心思想指導文檔** - 所有設計決策的基準 | ⭐⭐⭐ |

### 🏗️ 架構設計文檔

| 文檔 | 描述 | 狀態 |
|------|------|------|
| [docs/混合架構設計.md](docs/混合架構設計.md) | **混合架構方案** - 容器 + GitHub Actions | ✅ 最新 |
| [docs/02-系統架構/整體架構.md](docs/02-系統架構/整體架構.md) | 原始容器架構設計 | 📋 需更新 |
| [docs/02-系統架構/AI角色設計.md](docs/02-系統架構/AI角色設計.md) | AI 角色定義和職責 | 📋 需更新 |
| [docs/02-系統架構/通信協調.md](docs/02-系統架構/通信協調.md) | 異步協作機制 | 📋 需更新 |

### 🔧 實施指南

| 文檔 | 描述 | 適用對象 |
|------|------|----------|
| [Gemini-CLI-最佳實踐.md](Gemini-CLI-最佳實踐.md) | Gemini CLI 參數使用最佳實踐 | 開發者 |
| [docs/06-使用指南/快速開始.md](docs/06-使用指南/快速開始.md) | 原始快速開始指南 | 📋 需更新 |
| [docs/06-使用指南/配置指南.md](docs/06-使用指南/配置指南.md) | 系統配置說明 | 📋 需更新 |
| [docs/07-部署運維/](docs/07-部署運維/) | 部署和運維文檔 | DevOps |

### 📊 項目管理

| 文檔 | 描述 | 用途 |
|------|------|------|
| [文件檢查計劃.md](文件檢查計劃.md) | 基於 CONTEXT.md 的文件檢查標準 | 質量控制 |
| [CHANGELOG.md](CHANGELOG.md) | 項目變更歷史 | 版本管理 |
| [docs/09-附錄/變更日誌.md](docs/09-附錄/變更日誌.md) | 詳細變更記錄 | 參考 |

## 🎭 AI 角色配置

### 混合架構角色（最新）

| 角色 | 配置目錄 | Gemini 配置 | 容器配置 | 狀態 |
|------|----------|-------------|----------|------|
| Product Manager | [roles/product_manager/](roles/product_manager/) | ✅ 已配置 | ✅ 已配置 | 🚀 就緒 |
| Backend Developer | [roles/backend_developer/](roles/backend_developer/) | 📋 待配置 | ✅ 已配置 | 🔄 進行中 |
| Frontend Developer | [roles/frontend_developer/](roles/frontend_developer/) | 📋 待配置 | ✅ 已配置 | 🔄 進行中 |
| DevOps Engineer | [roles/devops_engineer/](roles/devops_engineer/) | 📋 待配置 | ✅ 已配置 | 🔄 進行中 |

### 角色配置結構
```
roles/{role_name}/
├── .gemini/                    # 🆕 Gemini CLI 配置
│   ├── settings.json          # 角色專屬設定
│   └── GEMINI.md              # 角色上下文
├── Dockerfile                 # 容器版本配置
└── prompt.md                  # 原始 prompt（保持相容）
```

## 🛠️ 工作流程和自動化

### GitHub Actions（暫時禁用）

| Workflow | 文件 | 狀態 | 說明 |
|----------|------|------|------|
| Product Manager | [.github/workflows/product-manager.yml](.github/workflows/product-manager.yml) | 🚫 禁用 | 保留代碼，待測試 |

### 腳本工具

| 腳本 | 描述 | 用途 |
|------|------|------|
| [scripts/role-management.sh](scripts/role-management.sh) | 角色管理腳本 | 容器操作 |
| [docs/07-部署運維/scripts/](docs/07-部署運維/scripts/) | 部署腳本集 | 自動化部署 |

## 📖 學習和研究資源

### 核心理念文檔

| 文檔 | 描述 | 目標讀者 |
|------|------|----------|
| [docs/01-項目背景/核心理念.md](docs/01-項目背景/核心理念.md) | 項目定位和價值主張 | 所有人 |
| [docs/01-項目背景/設計約束.md](docs/01-項目背景/設計約束.md) | 技術約束和設計原則 | 技術人員 |
| [docs/01-項目背景/發展歷程.md](docs/01-項目背景/發展歷程.md) | 項目演進歷史 | 研究者 |

### 工作流程文檔

| 文檔 | 描述 | 更新狀態 |
|------|------|----------|
| [docs/03-工作流程/異步協作流程.md](docs/03-工作流程/異步協作流程.md) | 異步協作機制 | 📋 需要混合架構更新 |
| [docs/03-工作流程/任務管理.md](docs/03-工作流程/任務管理.md) | 任務分配和管理 | 📋 需要混合架構更新 |
| [docs/03-工作流程/狀態同步.md](docs/03-工作流程/狀態同步.md) | 狀態同步機制 | 📋 需要混合架構更新 |

### 模擬和驗證

| 文檔 | 描述 | 狀態 |
|------|------|------|
| [docs/05-模擬工具/](docs/05-模擬工具/) | SimPy 模擬器相關文檔 | ✅ 完整 |
| [docs/05-模擬工具/SimPy模擬器.md](docs/05-模擬工具/SimPy模擬器.md) | 模擬器使用指南 | ✅ 完整 |
| [docs/05-模擬工具/協作效果分析.md](docs/05-模擬工具/協作效果分析.md) | 效果分析方法 | ✅ 完整 |

### 應用案例

| 文檔 | 描述 | 完成度 |
|------|------|---------|
| [docs/08-應用案例/教育遊戲項目.md](docs/08-應用案例/教育遊戲項目.md) | 完整應用案例 | ✅ 完整 |
| [docs/education-game-project/](docs/education-game-project/) | 詳細案例文檔 | ✅ 完整 |

## 📋 文檔狀態總覽

### ✅ 最新且完整的文檔
- [CONTEXT.md](CONTEXT.md) - 核心思想指導
- [官方快速開始指南.md](官方快速開始指南.md) - 實施指南
- [docs/混合架構設計.md](docs/混合架構設計.md) - 混合架構設計
- [Gemini-CLI-最佳實踐.md](Gemini-CLI-最佳實踐.md) - 技術實踐
- [roles/product_manager/.gemini/](roles/product_manager/.gemini/) - PM 角色配置

### 📋 需要更新的文檔
- [docs/02-系統架構/](docs/02-系統架構/) - 需要融入混合架構
- [docs/03-工作流程/](docs/03-工作流程/) - 需要更新工作流程
- [docs/06-使用指南/](docs/06-使用指南/) - 需要更新使用方式
- [docs/07-部署運維/](docs/07-部署運維/) - 需要混合部署指南

### 🔄 待完成的任務
- 為其他角色創建 Gemini CLI 配置
- 更新現有文檔以反映混合架構
- 建立統一的文檔格式和風格
- 完善文檔間的交叉引用

## 🎯 閱讀建議

### 👥 不同角色的閱讀路徑

#### 🆕 新用戶（第一次接觸）
1. [README.md](README.md) - 了解項目
2. [CONTEXT.md](CONTEXT.md) - 理解核心思想
3. [docs/01-項目背景/核心理念.md](docs/01-項目背景/核心理念.md) - 深入理念

#### 🛠️ 技術實施者
1. [CONTEXT.md](CONTEXT.md) - 核心思想
2. [官方快速開始指南.md](官方快速開始指南.md) - 實施指南
3. [docs/混合架構設計.md](docs/混合架構設計.md) - 架構設計
4. [Gemini-CLI-最佳實踐.md](Gemini-CLI-最佳實踐.md) - 技術細節

#### 📊 項目管理者
1. [CONTEXT.md](CONTEXT.md) - 核心思想
2. [文件檢查計劃.md](文件檢查計劃.md) - 質量管理
3. [docs/01-項目背景/](docs/01-項目背景/) - 背景和約束
4. [docs/05-模擬工具/](docs/05-模擬工具/) - 驗證工具

#### 🔬 研究者
1. [docs/01-項目背景/](docs/01-項目背景/) - 理論基礎
2. [docs/05-模擬工具/](docs/05-模擬工具/) - 模擬驗證
3. [docs/08-應用案例/](docs/08-應用案例/) - 實際案例
4. [docs/education-game-project/](docs/education-game-project/) - 詳細案例

## 🔗 重要外部資源

- **Google Gemini CLI 官方倉庫**：https://github.com/google-gemini/gemini-cli（⭐ 63.5k stars）
- **官方配置文檔**：https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md
- **SimPy 模擬框架**：https://simpy.readthedocs.io/

---

## 📝 使用此索引

1. **快速導航**：使用目錄跳轉到感興趣的部分
2. **狀態追蹤**：關注文檔的更新狀態標記
3. **角色導向**：根據你的角色選擇合適的閱讀路徑
4. **定期更新**：此索引會隨著項目發展持續更新

*最後更新：2025年1月* | *下次計劃更新：文檔重組完成後* 