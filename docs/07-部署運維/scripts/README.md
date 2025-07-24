# 部署運維腳本

本資料夾包含 Bee Swarm 項目的部署和運維相關腳本。

## 腳本目錄

### 部署腳本
- `deploy.sh` - 主要部署腳本
- `rollback.sh` - 回滾部署腳本
- `build-images.sh` - Docker 映像構建腳本

### 運維腳本
- `backup.sh` - 資料備份腳本
- `maintenance.sh` - 系統維護腳本
- `health-check.sh` - 健康檢查腳本
- `auto-recovery.sh` - 自動恢復腳本

### 監控腳本
- `setup-monitoring.sh` - 監控系統安裝腳本
- `alert-handler.py` - 告警處理腳本

## 使用方法

### 部署應用程式
```bash
# 部署到開發環境
./deploy.sh development

# 部署到生產環境
./deploy.sh production
```

### 執行備份
```bash
# 手動執行備份
./backup.sh

# 檢查備份狀態
./backup.sh --status
```

### 系統維護
```bash
# 執行系統維護
./maintenance.sh

# 檢查系統健康狀態
./health-check.sh
```

## 配置要求

執行這些腳本前，請確保：

1. 安裝了必要的依賴項（Docker、kubectl、aws-cli 等）
2. 設置了正確的環境變數
3. 具有適當的系統權限
4. 網路連線正常

## 注意事項

- 生產環境操作前請務必測試
- 重要操作建議進行二次確認
- 定期檢查腳本的執行日誌
- 保持腳本和配置的版本同步

---

*這些腳本是 Bee Swarm 項目運維的重要組成部分，請謹慎使用。* 