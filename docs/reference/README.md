# 📚 參考資料

## 📍 您現在的位置
[項目首頁](../../README.md) > [文檔索引](../../PROJECT_INDEX.md) > **參考資料** > 您在這裡

## 🎯 參考導航

本目錄提供 Bee Swarm 項目的完整參考資料，包括 API 文檔、術語解釋、外部資源和變更記錄。

## 📖 核心參考文檔

### 📋 API 和接口
- **[API 參考](api-reference.md)** - 完整的 API 文檔
- **[Gemini CLI 參數](gemini-cli-reference.md)** - 所有參數說明
- **[GitHub Actions 接口](github-actions-api.md)** - Actions 相關 API

### 📚 術語和概念
- **[名詞解釋](glossary.md)** - 項目相關術語定義
- **[概念索引](concept-index.md)** - 核心概念快速查找
- **[縮寫對照](abbreviations.md)** - 常用縮寫說明

### 🔗 外部資源
- **[官方資源](external-resources.md)** - Google Gemini CLI 等官方文檔
- **[學術參考](academic-references.md)** - 相關研究論文
- **[工具生態](tool-ecosystem.md)** - 相關工具和平台

## 📊 現有參考文檔

### ✅ 完整參考
| 文檔 | 描述 | 狀態 |
|------|------|------|
| [API參考](../09-附錄/API參考.md) | API 接口說明 | ✅ 完整 |
| [名詞解釋](../09-附錄/名詞解釋.md) | 術語定義 | ✅ 完整 |
| [參考資料](../09-附錄/參考資料.md) | 外部資源鏈接 | ✅ 完整 |
| [變更日誌](../09-附錄/變更日誌.md) | 詳細變更記錄 | ✅ 完整 |

### 🆕 新增參考
- **[Gemini CLI 完整參考](gemini-cli-complete-reference.md)** - 所有參數和用法
- **[GitHub API 集成](github-api-integration.md)** - GitHub API 使用指南
- **[性能基準](performance-benchmarks.md)** - 系統性能參考數據

## 🔧 API 快速參考

### Gemini CLI 核心參數

| 參數 | 描述 | 示例 |
|------|------|------|
| `--model` | 指定 AI 模型 | `--model gemini-1.5-flash` |
| `--prompt` | 直接傳遞提示 | `--prompt "分析代碼"` |
| `--yolo` | 自動批准工具調用 | `--yolo` |
| `--sandbox` | 啟用沙盒模式 | `--sandbox` |
| `--all_files` | 載入所有檔案 | `--all_files` |

### GitHub API 常用端點

| 端點 | 用途 | 方法 |
|------|------|------|
| `/repos/{owner}/{repo}/issues` | Issue 管理 | GET, POST |
| `/repos/{owner}/{repo}/pulls` | PR 管理 | GET, POST |
| `/repos/{owner}/{repo}/actions/runs` | Actions 狀態 | GET |

## 📚 術語快速查找

### 🤖 AI 相關
- **Agent**：AI 智能體，具有特定角色和功能的 AI 實體
- **LLM**：Large Language Model，大型語言模型
- **Prompt**：提示詞，給 AI 的指令或問題
- **Tool Calling**：工具調用，AI 執行特定功能的機制

### 🏗️ 架構相關
- **Hybrid Architecture**：混合架構，結合容器和 GitHub Actions
- **Asynchronous Collaboration**：異步協作，不需要即時互動的協作方式
- **GitHub-Centric**：以 GitHub 為中心的開發模式

### 📊 性能相關
- **ROI**：Return on Investment，投資回報率
- **Latency**：延遲時間，響應時間
- **Throughput**：吞吐量，單位時間處理能力

## 🔗 外部資源快速鏈接

### 🏢 官方資源

#### Google Gemini CLI
- **[官方倉庫](https://github.com/google-gemini/gemini-cli)** - ⭐ 63.5k stars
- **[配置文檔](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md)**
- **[API 密鑰申請](https://makersuite.google.com/app/apikey)**

#### GitHub 平台
- **[GitHub Actions 文檔](https://docs.github.com/en/actions)**
- **[GitHub API 參考](https://docs.github.com/en/rest)**
- **[GitHub CLI 文檔](https://cli.github.com/manual/)**

### 📚 學術資源

#### 多智能體系統
- **[Wooldridge, M. (2009)](https://www.cs.ox.ac.uk/people/michael.wooldridge/)** - "An Introduction to MultiAgent Systems"
- **[Stone, P., & Veloso, M. (2000)](https://www.cs.utexas.edu/~pstone/)** - "Multiagent Systems: A Survey"

#### 軟體工程協作
- **[Herbsleb, J. D. (2007)](https://herbsleb.org/)** - "Global Software Engineering"
- **[Bird, C. (2009)](https://www.microsoft.com/en-us/research/people/cbird/)** - "Mining Git"

## 📈 版本和變更

### 🔄 版本歷史
- **v1.0.0**：基礎容器架構
- **v2.0.0**：混合架構引入
- **v2.1.0**：Google Gemini CLI 集成
- **v2.2.0**：文檔重組和優化

### 📝 最新變更
詳細變更記錄請參考：
- **[CHANGELOG.md](../../CHANGELOG.md)** - 主要變更摘要
- **[詳細變更日誌](../09-附錄/變更日誌.md)** - 完整變更記錄

## 🆘 獲取幫助

### 📞 技術支持
- **[GitHub Issues](https://github.com/fallrising/bee_swarm/issues)** - 報告問題和需求
- **[GitHub Discussions](https://github.com/fallrising/bee_swarm/discussions)** - 社群討論
- **[故障排除](../06-使用指南/故障排除.md)** - 常見問題解決

### 🔍 搜索技巧
1. **使用 Ctrl+F** 在文檔中快速搜索
2. **查看 PROJECT_INDEX.md** 獲取完整導航
3. **參考術語表** 了解專業名詞

---

*快速查找所需的參考資料和技術文檔* 