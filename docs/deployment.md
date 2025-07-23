# 部署指南

## 概述

Bee Swarm 採用簡化的部署架構，每個 AI 角色運行在獨立的容器中，通過 GitHub 進行協調。

## 系統架構

```
GitHub Repository
    ↓
GitHub Actions (觸發器)
    ↓
AI Containers (角色容器)
├── Product Manager Container
├── Backend Developer Container
├── Frontend Developer Container
├── QA Engineer Container
└── DevOps Engineer Container
```

## 部署步驟

### 1. 環境準備

#### 系統要求
- **操作系統**：Ubuntu 20.04+ 或 CentOS 8+
- **Docker**：20.10+
- **Docker Compose**：2.0+
- **Git**：2.30+
- **Python**：3.8+

#### 安裝 Docker
```bash
# Ubuntu
sudo apt update
sudo apt install docker.io docker-compose

# CentOS
sudo yum install docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 項目配置

#### 克隆項目
```bash
git clone https://github.com/your-username/bee_swarm.git
cd bee_swarm
```

#### 環境變量配置
```bash
# 複製環境變量模板
cp env.example .env

# 編輯環境變量
nano .env
```

**必需配置**：
```env
# GitHub 配置
GITHUB_TOKEN_PM=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_BACKEND=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_FRONTEND=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_QA=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_DEVOPS=ghp_xxxxxxxxxxxxxxxxxxxx

# GitHub 倉庫配置
GITHUB_REPOSITORY=your-username/bee_swarm
GITHUB_OWNER=your-username

# AI 工具配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### 3. 容器部署

#### 構建基礎鏡像
```bash
# 構建 VNC 基礎鏡像
cd roles/product_manager
docker build -t bee-swarm-vnc-base .

# 構建 AI 工具鏡像
cd ../novnc_llm_cli
docker build -t bee-swarm-ai-tools .
```

#### 構建角色鏡像
```bash
# 構建各角色鏡像
for role in product_manager backend_developer frontend_developer qa_engineer devops_engineer; do
    cd roles/$role
    docker build -t bee-swarm-$role .
    cd ../..
done
```

#### 啟動容器
```bash
# 使用 Docker Compose 啟動
docker-compose up -d

# 或手動啟動各容器
docker run -d --name pm-container bee-swarm-product_manager
docker run -d --name backend-container bee-swarm-backend_developer
docker run -d --name frontend-container bee-swarm-frontend_developer
docker run -d --name qa-container bee-swarm-qa_engineer
docker run -d --name devops-container bee-swarm-devops_engineer
```

### 4. GitHub Actions 配置

#### 創建工作流文件
```bash
mkdir -p .github/workflows
```

#### AI 觸發工作流
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
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Trigger AI containers
        run: |
          # 根據 issue 類型觸發對應的 AI 容器
          python scripts/trigger_ai_containers.py
```

### 5. 驗證部署

#### 檢查容器狀態
```bash
# 檢查所有容器狀態
docker ps

# 檢查容器日誌
docker logs pm-container
docker logs backend-container
docker logs frontend-container
docker logs qa-container
docker logs devops-container
```

#### 測試 GitHub 集成
```bash
# 測試 GitHub API 連接
python scripts/test_github_integration.py

# 創建測試 Issue
python scripts/create_test_issue.py
```

## 配置說明

### 角色配置

每個角色都有獨立的配置文件：

```yaml
# roles/product_manager/config.yml
role:
  id: "pm-01"
  name: "Product Manager"
  username: "pm_ai_001"
  skills: ["product_management", "requirements_analysis"]
  tools: ["gemini-cli", "notion-api"]
  max_workload: 80
```

### 網絡配置

```yaml
# docker-compose.yml
version: '3.8'
services:
  product-manager:
    image: bee-swarm-product_manager
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN_PM}
    ports:
      - "5901:5900"  # VNC 端口
      - "6081:6080"  # noVNC 端口
```

### 安全配置

```bash
# 設置防火牆規則
sudo ufw allow 5901:5905/tcp  # VNC 端口
sudo ufw allow 6081:6085/tcp  # noVNC 端口
sudo ufw enable
```

## 監控和維護

### 健康檢查
```bash
# 檢查容器健康狀態
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 檢查系統資源使用
docker stats
```

### 日誌管理
```bash
# 查看容器日誌
docker logs -f pm-container

# 清理舊日誌
docker system prune -f
```

### 備份和恢復
```bash
# 備份容器數據
docker commit pm-container bee-swarm-pm-backup

# 恢復容器
docker run -d --name pm-restored bee-swarm-pm-backup
```

## 故障排除

### 常見問題

1. **容器無法啟動**
   ```bash
   # 檢查 Docker 服務狀態
   sudo systemctl status docker
   
   # 檢查容器日誌
   docker logs <container-name>
   ```

2. **GitHub API 連接失敗**
   ```bash
   # 檢查 Token 配置
   echo $GITHUB_TOKEN_PM
   
   # 測試 API 連接
   curl -H "Authorization: token $GITHUB_TOKEN_PM" https://api.github.com/user
   ```

3. **VNC 連接失敗**
   ```bash
   # 檢查端口是否開放
   netstat -tlnp | grep 5901
   
   # 檢查防火牆設置
   sudo ufw status
   ```

### 性能優化

1. **資源限制**
   ```yaml
   # docker-compose.yml
   services:
     product-manager:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

2. **日誌輪轉**
   ```yaml
   # docker-compose.yml
   services:
     product-manager:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ``` 