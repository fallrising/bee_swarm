#!/bin/bash

# 互動式重寫 commit 消息腳本

echo "🔧 互動式 Commit 消息英文化工具"
echo "================================"
echo ""

# 檢查當前狀態
echo "📊 當前 Git 狀態："
git status --short

if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  警告：工作目錄有未提交的變更，請先處理這些變更再繼續"
    echo "運行 'git status' 查看詳情"
    exit 1
fi

echo ""
echo "📋 中文 Commit 消息列表："
echo "========================="

# 顯示所有中文 commit 消息
git log --pretty=format:"%h - %s" | head -20 | grep -E "[\u4e00-\u9fff]|🧹|🎯|📋|🔄|✨|🎮|📚"

echo ""
echo "❓ 您想要如何處理？"
echo "1. 自動批量重寫所有中文消息（推薦）"
echo "2. 逐個手動重寫每個 commit"
echo "3. 只查看預覽，不進行實際更改"
echo "4. 取消操作"

read -p "請選擇 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🔄 準備自動批量重寫..."
        read -p "⚠️  這將會改變所有 commit hash。確定繼續嗎？(y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo "🗂️  創建備份分支..."
            git branch backup-main-$(date +%Y%m%d-%H%M%S)
            echo "執行重寫腳本..."
            ./scripts/rewrite-commit-messages.sh
        else
            echo "❌ 操作已取消"
        fi
        ;;
    2)
        echo ""
        echo "📝 手動重寫模式 - 使用 git rebase -i"
        echo "這將打開互動式 rebase，您可以選擇要重寫的 commit"
        read -p "請輸入要重寫的 commit 數量（默認：20）: " commit_count
        commit_count=${commit_count:-20}
        
        echo "🗂️  創建備份分支..."
        git branch backup-main-$(date +%Y%m%d-%H%M%S)
        
        echo "🔧 啟動互動式 rebase..."
        git rebase -i HEAD~$commit_count
        ;;
    3)
        echo ""
        echo "👀 預覽模式 - 將要重寫的消息："
        echo "============================"
        
        # 顯示預覽
        git log --pretty=format:"%h - %s" | head -20 | while IFS= read -r line; do
            commit_msg=$(echo "$line" | cut -d'-' -f2- | xargs)
            case "$commit_msg" in
                "docs: 更新CHANGELOG記錄文件名英文化變更")
                    echo "$line → docs: update CHANGELOG for filename internationalization changes"
                    ;;
                "refactor: 文件名英文化和角色系統更新")
                    echo "$line → refactor: internationalize filenames and update role system"
                    ;;
                "🧹 完成項目重構最終清理和優化")
                    echo "$line → chore: complete project restructuring final cleanup and optimization"
                    ;;
                # 添加更多翻譯...
                *)
                    if [[ "$commit_msg" =~ [\u4e00-\u9fff] ]] || [[ "$commit_msg" =~ [🧹🎯📋🔄✨🎮📚] ]]; then
                        echo "$line → [需要翻譯]"
                    else
                        echo "$line → [保持不變]"
                    fi
                    ;;
            esac
        done
        ;;
    4)
        echo "❌ 操作已取消"
        exit 0
        ;;
    *)
        echo "❌ 無效選擇"
        exit 1
        ;;
esac

echo ""
echo "✅ 完成！"
echo ""
echo "📝 後續步驟："
echo "1. 檢查結果: git log --oneline"
echo "2. 如果滿意: git push --force-with-lease origin main"
echo "3. 如果需要回滾: git reset --hard backup-main-[timestamp]" 