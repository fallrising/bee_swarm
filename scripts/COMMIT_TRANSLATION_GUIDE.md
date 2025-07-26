# Git Commit 消息英文化指南

## 概述

本指南提供將 Git 歷史中的中文 commit 消息轉換為英文的解決方案。

## ⚠️ 重要警告

**在執行任何操作前，請仔細閱讀以下警告：**

1. **這會改變所有相關 commit 的 hash 值**
2. **需要使用 force push 更新遠程倉庫**
3. **如果其他開發者已經基於這些 commit 工作，會造成協作問題**
4. **建議在個人項目或與團隊充分溝通後執行**

## 準備工作

### 1. 確保工作目錄乾淨

```bash
git status
```

如果有未提交的變更，請先處理：

```bash
git add .
git commit -m "save work in progress"
```

### 2. 備份當前倉庫

```bash
# 創建本地備份分支
git branch backup-main-$(date +%Y%m%d)

# 或者克隆整個倉庫作為備份
cd ..
git clone bee_swarm bee_swarm_backup
cd bee_swarm
```

## 使用方法

### 方法一：自動批量重寫（推薦）

**適用於：** 大量 commit 需要處理，且翻譯映射已經預定義

```bash
# 運行自動重寫腳本
./scripts/rewrite-commit-messages.sh
```

這個腳本會：
- 自動創建備份分支
- 批量重寫所有預定義的中文 commit 消息
- 保留其他消息不變

### 方法二：互動式處理

**適用於：** 想要更精確地控制過程

```bash
# 運行互動式腳本
./scripts/rewrite-commit-messages-interactive.sh
```

這個腳本提供四個選項：
1. **自動批量重寫** - 執行方法一
2. **手動逐個重寫** - 使用 `git rebase -i` 手動編輯
3. **預覽模式** - 只查看將要改變的內容
4. **取消操作** - 安全退出

### 方法三：手動使用 git rebase

**適用於：** 只需要修改少數幾個 commit

```bash
# 創建備份
git branch backup-main-$(date +%Y%m%d)

# 開始互動式 rebase（修改最近10個commit）
git rebase -i HEAD~10
```

在編輯器中：
1. 將要修改的 commit 前的 `pick` 改為 `reword`
2. 保存並關閉編輯器
3. 為每個標記的 commit 重新編寫消息

## 當前支持的翻譯映射

腳本目前支持以下中文消息的自動翻譯：

| 中文原文 | 英文翻譯 |
|---------|---------|
| `docs: 更新CHANGELOG記錄文件名英文化變更` | `docs: update CHANGELOG for filename internationalization changes` |
| `refactor: 文件名英文化和角色系統更新` | `refactor: internationalize filenames and update role system` |
| `🧹 完成項目重構最終清理和優化` | `chore: complete project restructuring final cleanup and optimization` |
| `docs(translation): 完成Bee Swarm項目完整英文翻譯` | `docs(translation): complete English translation for Bee Swarm project` |
| ... | *更多映射請查看腳本文件* |

## 執行後操作

### 1. 檢查結果

```bash
# 查看重寫後的 commit 歷史
git log --oneline -n 20

# 比較差異
git log --oneline backup-main-$(date +%Y%m%d)..HEAD
```

### 2. 推送到遠程倉庫

**如果滿意重寫結果：**

```bash
# 使用 force-with-lease 安全推送
git push --force-with-lease origin main
```

**`--force-with-lease` 比 `--force` 更安全，會檢查遠程分支是否有其他人的提交**

### 3. 如果需要回滾

```bash
# 回滾到備份分支
git reset --hard backup-main-$(date +%Y%m%d)

# 如果已經推送，需要 force push 回滾
git push --force-with-lease origin main
```

## 協作注意事項

### 通知團隊成員

如果是團隊項目，請在執行前通知所有成員：

```bash
# 發送通知消息示例
echo "計劃於 $(date) 重寫 Git 歷史中的中文 commit 消息為英文。
這會改變所有 commit hash。
請確保在此時間前推送所有本地變更，並在操作完成後重新克隆倉庫。"
```

### 團隊成員需要的操作

**操作完成後，其他開發者需要：**

```bash
# 刪除本地分支並重新獲取
git fetch origin
git reset --hard origin/main

# 或者重新克隆倉庫
cd ..
rm -rf bee_swarm
git clone <repository-url> bee_swarm
```

## 故障排除

### 如果 filter-branch 失敗

```bash
# 清理 filter-branch 殘留文件
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 如果需要添加新的翻譯映射

編輯 `scripts/rewrite-commit-messages.sh`，在 case 語句中添加新的映射：

```bash
"你的中文消息")
    echo "Your English message"
    ;;
```

## 最佳實踐

1. **測試先行**：在測試分支上先試運行
2. **小批次處理**：如果歷史很長，考慮分批處理
3. **文檔記錄**：在 CHANGELOG 中記錄這次歷史重寫
4. **團隊溝通**：確保所有相關人員都了解變更

## 相關命令參考

```bash
# 查看所有包含中文的 commit
git log --grep="[\u4e00-\u9fff]" --oneline

# 查看最近的 commit 消息
git log --pretty=format:"%s" -n 20

# 強制垃圾回收
git gc --prune=now --aggressive

# 查看分支歷史
git log --graph --oneline --all
``` 