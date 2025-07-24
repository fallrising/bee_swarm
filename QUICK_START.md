# 🚀 Bee Swarm 快速開始指南

## 📋 文檔信息
- **目標讀者**：所有新用戶
- **完成時間**：5-10 分鐘
- **先決條件**：基本的命令行操作
- **最後更新**：2025年1月

## 🎯 三種快速體驗路徑

根據你的興趣和背景，選擇最適合的路徑：

### 🔍 路徑一：概念理解（5 分鐘）
**適合**：想要快速了解項目理念的用戶

1. **閱讀核心概念**：[CONTEXT.md](CONTEXT.md) （2 分鐘）
2. **理解項目價值**：[核心理念](docs/01-項目背景/核心理念.md) （2 分鐘）
3. **查看架構設計**：[混合架構設計](docs/混合架構設計.md) （1 分鐘瀏覽）

✅ **完成標誌**：理解什麼是 AI 團隊異步協作

### 🛠️ 路徑二：技術實施（10 分鐘）
**適合**：想要動手實踐的開發者

1. **安裝 Gemini CLI**：
   ```bash
   npm install -g @google/gemini-cli
   gemini --version
   ```

2. **設置 API Key**：
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. **測試基本功能**：
   ```bash
   gemini --prompt "Hello, Bee Swarm!" --model gemini-1.5-flash
   ```

4. **克隆項目**：
   ```bash
   git clone https://github.com/your-username/bee_swarm.git
   cd bee_swarm
   ```

5. **測試 PM Agent 配置**：
   ```bash
   cd roles/product_manager
   gemini --prompt "分析這個項目的角色配置" --all_files
   ```

✅ **完成標誌**：成功運行 Gemini CLI 並與項目互動

### 🔬 路徑三：模擬驗證（8 分鐘）
**適合**：研究者和想要理解協作效果的用戶

1. **安裝模擬環境**：
   ```bash
   pip install simpy colorama
   ```

2. **運行基本模擬**：
   ```bash
   cd docs/05-模擬工具/scripts
   python basic_simulation.py
   ```

3. **查看模擬結果**：觀察 AI 角色協作過程

4. **運行場景對比**：
   ```bash
   python scenario_comparison.py
   ```

✅ **完成標誌**：看到混合架構 vs 純容器架構的性能對比

## 🎛️ 完整設置（30 分鐘）

如果你想要完整的開發環境，按照以下步驟：

### 階段一：基礎環境（10 分鐘）

1. **系統要求檢查**：
   ```bash
   node --version  # >= 18
   npm --version   # >= 9
   git --version   # >= 2.30
   ```

2. **安裝核心工具**：
   ```bash
   # Gemini CLI
   npm install -g @google/gemini-cli
   
   # GitHub CLI
   brew install gh  # macOS
   # 或 sudo apt install gh  # Linux
   
   # Python 環境（可選，用於模擬）
   pip install simpy colorama pandas matplotlib
   ```

3. **配置 API Keys**：
   ```bash
   # Gemini API Key
   export GEMINI_API_KEY="your-gemini-key"
   
   # GitHub Token（如果需要 Actions）
   export GITHUB_TOKEN="your-github-token"
   ```

### 階段二：項目設置（10 分鐘）

1. **Fork 並克隆項目**：
   ```bash
   gh repo fork fallrising/bee_swarm
   git clone https://github.com/your-username/bee_swarm.git
   cd bee_swarm
   ```

2. **驗證項目結構**：
   ```bash
   tree -L 2  # 查看項目結構
   ls -la roles/  # 檢查角色配置
   ```

3. **測試 AI 角色配置**：
   ```bash
   cd roles/product_manager
   gemini --all_files --prompt "檢查這個角色的配置是否正確"
   ```

### 階段三：功能驗證（10 分鐘）

1. **運行模擬測試**：
   ```bash
   cd docs/05-模擬工具/scripts
   python basic_simulation.py
   ```

2. **測試 GitHub 整合**（可選）：
   ```bash
   # 創建測試 Issue
   gh issue create --title "測試 Epic" --body "這是一個測試 Epic" --label "epic"
   ```

3. **檢查文檔連結**：
   ```bash
   # 驗證主要文檔可以正常訪問
   ls PROJECT_INDEX.md CONTEXT.md README.md
   ```

## 🔗 下一步選擇

根據你的完成路徑，選擇後續行動：

### 📚 深入學習
- **理解架構**：[混合架構設計](docs/混合架構設計.md)
- **技術詳解**：[Gemini CLI 最佳實踐](Gemini-CLI-最佳實踐.md)
- **完整文檔**：[PROJECT_INDEX.md](PROJECT_INDEX.md)

### 🛠️ 開始開發
- **配置角色**：為其他角色創建 Gemini 配置
- **自定義工作流程**：修改 `.github/workflows/`
- **本地測試**：在本地環境測試 AI Agent

### 🔬 深入研究
- **模擬分析**：[協作效果分析](docs/05-模擬工具/協作效果分析.md)
- **案例研究**：[教育遊戲項目](docs/08-應用案例/教育遊戲項目.md)
- **理論基礎**：[設計約束](docs/01-項目背景/設計約束.md)

### 🚀 生產部署
- **設置 GitHub Secrets**：配置生產環境
- **啟用 GitHub Actions**：取消註解工作流程
- **監控設置**：建立性能監控

## 🆘 常見問題和故障排除

### ❓ 常見問題

**Q: Gemini CLI 安裝失敗？**
```bash
# 清理 npm 緩存
npm cache clean --force
npm install -g @google/gemini-cli

# 檢查 Node.js 版本
node --version  # 需要 >= 18
```

**Q: API Key 無效？**
```bash
# 測試 API Key
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
     https://generativelanguage.googleapis.com/v1/models
```

**Q: 模擬腳本運行失敗？**
```bash
# 檢查 Python 環境
python --version  # 需要 >= 3.8
pip list | grep simpy
```

### 🔧 故障排除步驟

1. **檢查環境變數**：
   ```bash
   echo $GEMINI_API_KEY
   echo $GITHUB_TOKEN
   ```

2. **驗證網絡連接**：
   ```bash
   ping google.com
   curl -I https://api.github.com
   ```

3. **重置配置**：
   ```bash
   rm -rf ~/.gemini  # 重置 Gemini CLI 配置
   ```

## 📞 獲取幫助

- **項目文檔**：[PROJECT_INDEX.md](PROJECT_INDEX.md)
- **詳細指南**：[官方快速開始指南.md](官方快速開始指南.md)
- **技術問題**：查看 [GitHub Issues](https://github.com/fallrising/bee_swarm/issues)
- **社區討論**：查看項目 Discussions

## 🎉 恭喜！

完成任意一個路徑後，你已經：

✅ 理解了 Bee Swarm 的核心概念  
✅ 體驗了 AI 團隊協作的基本流程  
✅ 準備好進行更深入的探索

**🚀 現在選擇你的下一步冒險吧！**

---

## 📍 導航幫助

### 🧭 您現在的位置
[項目首頁](README.md) > **快速開始** > 您在這裡

### 🎯 推薦下一步
- **新手**：[CONTEXT.md](CONTEXT.md) → [核心理念](docs/01-項目背景/核心理念.md)
- **開發者**：[混合架構設計](docs/混合架構設計.md) → [Gemini CLI 最佳實踐](Gemini-CLI-最佳實踐.md)
- **研究者**：[模擬工具](docs/05-模擬工具/) → [應用案例](docs/08-應用案例/)
- **管理者**：[文件檢查計劃.md](文件檢查計劃.md) → [PROJECT_INDEX.md](PROJECT_INDEX.md)

*最後更新：2025年1月 | 預計閱讀時間：5-30分鐘* 