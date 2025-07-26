# Bee Swarm 輔助腳本指南

本目錄包含 Bee Swarm 項目的各種輔助腳本，用於簡化容器管理、部署和運維操作。

## 📁 腳本列表

### 🤖 role-management.sh
**主要的角色容器管理腳本**

#### 功能特點
- 支持所有 AI 角色容器的編譯、推送、啟動、停止
- 區分核心角色（4個）和擴展角色（5個）
- 自動端口分配和健康檢查
- 批量操作和狀態監控

#### 使用方法

```bash
# 基本命令格式
./scripts/role-management.sh [命令] [選項]

# 查看幫助
./scripts/role-management.sh --help

# 列出所有可用角色
./scripts/role-management.sh list-roles

# 編譯指定角色容器
./scripts/role-management.sh build product_manager

# 編譯所有核心角色
./scripts/role-management.sh build --core-only

# 啟動指定角色
./scripts/role-management.sh start backend_developer

# 啟動所有核心角色
./scripts/role-management.sh start --core-only

# 查看容器狀態
./scripts/role-management.sh status

# 查看容器日誌
./scripts/role-management.sh logs product_manager

# 停止容器
./scripts/role-management.sh stop product_manager

# 重啟容器
./scripts/role-management.sh restart product_manager

# 清理未使用資源
./scripts/role-management.sh clean
```

#### 環境變量配置

```bash
# Docker 註冊表配置
export DOCKER_REGISTRY="your-registry.com"

# VNC 訪問密碼
export VNC_PASSWORD="your-vnc-password"

# 終端訪問密碼
export TTYD_PASSWORD="your-terminal-password"
```

#### 端口分配

| 角色 | VNC 端口 | 終端端口 | 容器名稱 |
|------|----------|----------|----------|
| Product Manager | 6080 | 7681 | bee-swarm-product_manager |
| Backend Developer | 6081 | 7682 | bee-swarm-backend_developer |
| Frontend Developer | 6082 | 7683 | bee-swarm-frontend_developer |
| DevOps Engineer | 6083 | 7684 | bee-swarm-devops_engineer |
| 其他角色 | 6090+ | 7690+ | bee-swarm-{role_name} |

## 🚀 快速開始指南

### 1. 初次設置

```bash
# 1. 設置執行權限
chmod +x scripts/role-management.sh

# 2. 查看可用角色
./scripts/role-management.sh list-roles

# 3. 編譯核心角色容器
./scripts/role-management.sh build --core-only
```

### 2. 啟動開發環境

```bash
# 啟動所有核心角色
./scripts/role-management.sh start --core-only

# 檢查運行狀態
./scripts/role-management.sh status
```

### 3. 訪問角色容器

```bash
# 通過瀏覽器訪問 VNC
# 產品經理：http://localhost:6080
# 後端開發者：http://localhost:6081
# 前端開發者：http://localhost:6082
# DevOps工程師：http://localhost:6083

# 通過瀏覽器訪問終端
# 產品經理：http://localhost:7681
# 後端開發者：http://localhost:7682
# 前端開發者：http://localhost:7683
# DevOps工程師：http://localhost:7684
```

### 4. 停止和清理

```bash
# 停止所有核心角色
./scripts/role-management.sh stop --core-only

# 清理未使用的資源
./scripts/role-management.sh clean
```

## 🛠️ 高級用法

### 批量操作

```bash
# 編譯所有角色（包括擴展角色）
./scripts/role-management.sh build --all

# 推送所有核心角色到註冊表
./scripts/role-management.sh push --core-only

# 重啟所有核心角色
./scripts/role-management.sh restart --core-only
```

### 開發調試

```bash
# 詳細輸出模式
./scripts/role-management.sh build product_manager --verbose

# 查看實時日誌
./scripts/role-management.sh logs product_manager

# 單獨重啟有問題的容器
./scripts/role-management.sh restart backend_developer
```

### 容器管理

```bash
# 檢查特定角色狀態
docker ps -f name=bee-swarm-product_manager

# 進入容器進行調試
docker exec -it bee-swarm-product_manager /bin/bash

# 查看容器資源使用
docker stats bee-swarm-product_manager
```

## 📊 監控和維護

### 健康檢查

```bash
# 定期檢查容器狀態
./scripts/role-management.sh status

# 查看系統資源使用情況
docker system df

# 檢查容器日誌中的錯誤
./scripts/role-management.sh logs product_manager | grep ERROR
```

### 備份和恢復

```bash
# 備份容器數據
docker run --rm \
  -v bee-swarm-data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/bee-swarm-backup-$(date +%Y%m%d).tar.gz /data

# 恢復容器數據
docker run --rm \
  -v bee-swarm-data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar xzf /backup/bee-swarm-backup-20241201.tar.gz -C /
```

### 性能優化

```bash
# 清理 Docker 系統
docker system prune -af

# 優化鏡像大小
docker image prune -f

# 重新構建優化後的鏡像
./scripts/role-management.sh build --core-only
```

## 🐛 故障排除

### 常見問題

#### 1. 容器啟動失敗
```bash
# 檢查 Docker 是否運行
docker version

# 檢查端口是否被占用
netstat -tlnp | grep 6080

# 查看詳細錯誤信息
./scripts/role-management.sh logs product_manager
```

#### 2. 無法訪問 VNC/終端
```bash
# 檢查容器是否正在運行
./scripts/role-management.sh status

# 檢查端口映射
docker port bee-swarm-product_manager

# 重啟容器
./scripts/role-management.sh restart product_manager
```

#### 3. 容器編譯失敗
```bash
# 檢查 Dockerfile 語法
docker build --no-cache -f roles/product_manager/Dockerfile .

# 清理緩存重新編譯
./scripts/role-management.sh clean
./scripts/role-management.sh build product_manager
```

### 日誌分析

```bash
# 查看容器啟動日誌
./scripts/role-management.sh logs product_manager --tail 50

# 查看 Docker 守護進程日誌
journalctl -u docker.service

# 查看系統資源使用
top
df -h
```

## 📝 腳本開發指南

### 添加新角色

1. 在 `roles/` 目錄創建新角色文件夾
2. 添加 `Dockerfile` 和 `prompt.md`
3. 在腳本中更新角色列表
4. 測試新角色的編譯和啟動

### 腳本擴展

```bash
# 添加新的管理功能
# 在 role-management.sh 中添加新的 case 分支

case "$command" in
    "new-command")
        new_function "$role"
        ;;
esac
```

### 貢獻指南

1. Fork 項目並創建功能分支
2. 在本地測試腳本功能
3. 添加適當的錯誤處理和日誌
4. 更新文檔和使用說明
5. 提交 Pull Request

---

## 📚 相關文檔

- [項目完整指南](../bee-swarm-complete-guide.md)
- [角色定義說明](../roles/README.md)
- [部署配置指南](../docs/07-部署運維/)
- [模擬工具使用](../docs/05-simulation/)

---

*這些腳本是 Bee Swarm 項目的重要組成部分，簡化了 AI 角色容器的管理和運維工作。* 