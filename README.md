# Bee Swarm

一個基於 AI 團隊協作的自動化工作流程系統。

## 📊 項目狀態

**最後更新時間**: 2025-07-23 22:59:08

### 倉庫信息
- **星標數**: 42 ⭐
- **分支數**: 15 🍴
- **開放 Issues**: 3 📝
- **開放 Pull Requests**: 2 🔄
- **最後更新**: 2025-07-23T10:30:00Z

### 最近活動
#### 最近提交
- `abc123` feat: 添加新功能模塊 (2025-07-23)
- `def456` fix: 修復登錄問題 (2025-07-22)
- `ghi789` docs: 更新文檔 (2025-07-21)

#### 開放 Issues
- #1 實現用戶認證功能
- #2 修復登錄頁面 bug
- #3 添加數據庫連接池

#### 開放 Pull Requests
- #1 添加新功能特性
- #2 修復 UI 問題

## 🚀 快速開始

### 前置要求

- Python 3.11+
- Docker 和 Docker Compose
- GitHub 帳戶

### 安裝

1. 克隆倉庫：
```bash
git clone https://github.com/your-username/bee_swarm.git
cd bee_swarm
```

2. 複製環境變量文件：
```bash
cp env.example .env
```

3. 啟動服務：
```bash
docker-compose up -d
```

## 📋 功能特性

### 🤖 AI 團隊協作
- 自動任務分配和通知
- 智能工作流程管理
- 實時狀態監控

### 🔄 自動化工作流程
- GitHub Actions 集成
- 定時任務執行
- 事件驅動觸發

### 📊 系統監控
- 健康狀態檢查
- 性能指標監控
- 自動備份

### 📚 文檔管理
- 自動文檔更新
- 版本控制集成
- 項目狀態追蹤

## 🏗️ 系統架構

```
bee_swarm/
├── coordinator/          # 協調器服務
├── roles/               # AI 角色定義
├── scripts/             # 工作流程腳本
├── docs/                # 項目文檔
└── .github/workflows/   # GitHub Actions
```

## 🔧 配置

### 環境變量

創建 `.env` 文件並配置以下變量：

```bash
# GitHub 配置
GITHUB_TOKEN=your_github_token
GITHUB_REPOSITORY=your_username/bee_swarm

# 可選配置（Mock 版本不需要）
CLOUDFLARE_TUNNEL_URL=your_tunnel_url
PROMETHEUS_URL=your_prometheus_url
GRAFANA_URL=your_grafana_url
SLACK_WEBHOOK_URL=your_slack_webhook
```

### GitHub Secrets

在 GitHub 倉庫設置中添加以下 Secrets：

- `GITHUB_TOKEN`: GitHub API 訪問令牌
- `CLOUDFLARE_TUNNEL_URL`: Cloudflare Tunnel URL（可選）
- `PROMETHEUS_URL`: Prometheus 服務 URL（可選）
- `GRAFANA_URL`: Grafana 服務 URL（可選）
- `SLACK_WEBHOOK_URL`: Slack Webhook URL（可選）

## 🧪 Mock 模式

目前所有腳本都運行在 **Mock 模式** 下，這意味著：

- ✅ 不需要配置複雜的外部服務
- ✅ 工作流程可以立即運行
- ✅ 所有數據都是預設的 mock 數據
- ✅ 便於開發和測試

### Mock 腳本列表

- `check_pending_tasks.py` - 檢查待處理任務
- `trigger_ai_containers.py` - 觸發 AI 容器
- `notify_role_assignment.py` - 通知角色分配
- `handle_pr_events.py` - 處理 PR 事件
- `check_system_health.py` - 檢查系統健康狀態
- `create_backup.py` - 創建系統備份
- `update_documentation.py` - 更新項目文檔

### 測試 Mock 腳本

```bash
# 測試所有腳本
python3 scripts/test_scripts.py

# 測試單個腳本
python3 scripts/check_pending_tasks.py
```

## 📖 文檔

詳細文檔請查看 [docs/](docs/) 目錄：

- [系統概述](docs/level1/system-overview.md)
- [角色系統](docs/level2/role-system.md)
- [工作流程系統](docs/level3/workflow-system.md)
- [通信協議](docs/level4/communication-protocol.md)
- [實現詳情](docs/level5/implementation-details.md)
- [工作流程修復記錄](docs/workflow-fixes.md)

## 🤝 貢獻

1. Fork 本項目
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 📄 許可證

本項目採用 MIT 許可證 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 🆘 支持

如果您遇到問題或有建議，請：

1. 查看 [Issues](../../issues) 頁面
2. 創建新的 Issue
3. 聯繫維護團隊

---

*此項目由 AI 團隊自動維護*

