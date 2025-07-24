# 部署指南

## 概述

Bee Swarm 採用簡化的 GitHub-Centric 架構，部署過程更加簡單和可靠。

## 系統要求

### 硬件要求

#### 最小配置
- **CPU**: 2 核心
- **內存**: 4GB RAM
- **存儲**: 20GB 可用空間
- **網絡**: 穩定的互聯網連接

#### 推薦配置
- **CPU**: 4 核心
- **內存**: 8GB RAM
- **存儲**: 50GB 可用空間
- **網絡**: 高速互聯網連接

### 軟件要求

- **操作系統**: Linux (Ubuntu 20.04+ / CentOS 8+)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.25+

## 部署步驟

### 1. 環境準備

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安裝 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 將用戶添加到 docker 組
sudo usermod -aG docker $USER
```

### 2. 項目部署

```bash
# 克隆項目
git clone https://github.com/your-org/bee_swarm.git
cd bee_swarm

# 配置環境變量
cp env.example .env
```

### 3. 環境變量配置

編輯 `.env` 文件，配置以下必需變量：

```bash
# GitHub 配置
GITHUB_REPOSITORY=your-org/your-repo
GITHUB_OWNER=your-org

# AI 角色 GitHub Token
GITHUB_TOKEN_PM_01=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_BACKEND_01=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_FRONTEND_01=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN_DEVOPS_01=ghp_xxxxxxxxxxxxxxxxxxxx

# AI 工具 API 密鑰
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
```

### 4. 配置驗證

```bash
# 驗證配置
python3 scripts/validate_config.py
```

### 5. 啟動系統

```bash
# 啟動生產環境
./scripts/switch_env.sh production

# 或啟動測試環境
./scripts/switch_env.sh test
```

## 環境管理

### 生產環境

```bash
# 啟動生產環境
./scripts/switch_env.sh production

# 檢查狀態
./scripts/switch_env.sh status

# 查看日誌
docker-compose logs -f

# 停止環境
docker-compose down
```

### 測試環境

```bash
# 啟動測試環境
./scripts/switch_env.sh test

# 檢查狀態
./scripts/switch_env.sh status

# 查看日誌
docker-compose -f docker-compose.test.yml logs -f

# 停止環境
docker-compose -f docker-compose.test.yml down
```

### 環境清理

```bash
# 清理所有環境
./scripts/switch_env.sh cleanup
```

## 監控和維護

### 系統狀態檢查

```bash
# 檢查容器狀態
docker-compose ps

# 檢查資源使用
docker system df

# 檢查網絡狀態
docker network ls | grep bee-swarm
```

### 日誌管理

```bash
# 查看所有容器日誌
docker-compose logs

# 查看特定容器日誌
docker-compose logs pm-01

# 實時查看日誌
docker-compose logs -f
```

### 備份和恢復

```bash
# 備份數據卷
docker run --rm -v bee_swarm_pm_01_data:/data -v $(pwd):/backup alpine tar czf /backup/pm_data_backup.tar.gz -C /data .

# 恢復數據卷
docker run --rm -v bee_swarm_pm_01_data:/data -v $(pwd):/backup alpine tar xzf /backup/pm_data_backup.tar.gz -C /data
```

## 故障排除

### 常見問題

#### 1. 配置驗證失敗

**問題**: 配置驗證腳本報告錯誤
**解決方案**:
```bash
# 檢查環境變量
python3 scripts/validate_config.py

# 修復缺失的配置項
# 重新運行驗證
```

#### 2. 容器啟動失敗

**問題**: 容器無法啟動
**解決方案**:
```bash
# 檢查 Docker 狀態
docker info

# 檢查容器日誌
docker-compose logs

# 重新構建容器
docker-compose build --no-cache
```

#### 3. 網絡連接問題

**問題**: 無法訪問容器服務
**解決方案**:
```bash
# 檢查端口映射
docker-compose ps

# 檢查防火牆設置
sudo ufw status

# 檢查網絡配置
docker network inspect bee_swarm_bee-swarm-network
```

#### 4. 資源不足

**問題**: 系統資源不足
**解決方案**:
```bash
# 檢查系統資源
htop
df -h

# 清理 Docker 資源
docker system prune -f

# 調整資源限制
# 編輯 docker-compose.yml 中的資源配置
```

### 性能優化

#### 1. 資源配置調整

根據實際需求調整容器資源配置：

```yaml
# docker-compose.yml
services:
  pm-01:
    deploy:
      resources:
        limits:
          memory: 1G    # 根據需要調整
          cpus: '0.5'   # 根據需要調整
```

#### 2. 日誌輪轉

配置日誌輪轉以避免磁盤空間不足：

```bash
# 創建日誌輪轉配置
sudo tee /etc/logrotate.d/bee-swarm << EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
EOF
```

## 安全配置

### 1. 防火牆配置

```bash
# 配置 UFW 防火牆
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 6080:6083/tcp  # VNC 端口
sudo ufw allow 7680:7683/tcp  # TTYD 端口
```

### 2. SSL/TLS 配置

如果需要 HTTPS 訪問，配置反向代理：

```nginx
# nginx 配置示例
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:6080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 訪問控制

```bash
# 設置強密碼
export VNC_PASSWORD_PM_01="StrongPassword123!"
export TTYD_PASSWORD_PM_01="StrongTerminalPassword123!"

# 限制訪問 IP
# 在防火牆中只允許特定 IP 訪問
sudo ufw allow from 192.168.1.0/24 to any port 6080:6083
```

## 擴展部署

### 多節點部署

對於大規模部署，可以將不同角色部署到不同節點：

```bash
# 節點 1: 產品經理
docker-compose up pm-01

# 節點 2: 後端開發
docker-compose up backend-01

# 節點 3: 前端開發
docker-compose up frontend-01

# 節點 4: DevOps
docker-compose up devops-01
```

### 負載均衡

使用 Nginx 進行負載均衡：

```nginx
upstream bee_swarm {
    server node1:6080;
    server node2:6081;
    server node3:6082;
    server node4:6083;
}

server {
    listen 80;
    location / {
        proxy_pass http://bee_swarm;
    }
}
```

## 更新和升級

### 1. 備份當前配置

```bash
# 備份配置文件
cp docker-compose.yml docker-compose.yml.backup
cp .env .env.backup
```

### 2. 更新代碼

```bash
# 拉取最新代碼
git pull origin main

# 驗證配置
python3 scripts/validate_config.py
```

### 3. 重新部署

```bash
# 停止當前環境
docker-compose down

# 重新構建和啟動
docker-compose up -d --build
```

## 支持

如果遇到部署問題，請：

1. 查看 [故障排除](#故障排除) 部分
2. 檢查 [GitHub Issues](../../issues)
3. 查看系統日誌
4. 聯繫維護團隊 