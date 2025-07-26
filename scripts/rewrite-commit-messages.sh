#!/bin/bash

# 備份當前分支
echo "正在創建備份分支..."
git branch backup-main-$(date +%Y%m%d)

# 定義中文到英文的映射
declare -A translations=(
    ["docs: 更新CHANGELOG記錄文件名英文化變更"]="docs: update CHANGELOG for filename internationalization changes"
    ["refactor: 文件名英文化和角色系統更新"]="refactor: internationalize filenames and update role system"
    ["🧹 完成項目重構最終清理和優化"]="chore: complete project restructuring final cleanup and optimization"
    ["docs(translation): 完成Bee Swarm項目完整英文翻譯"]="docs(translation): complete English translation for Bee Swarm project"
    ["📋 更新重構狀態記錄：階段2完成"]="docs: update restructuring status record - phase 2 completed"
    ["🎯 階段2重構完成：清理舊中文目錄，建立精簡結構"]="refactor: phase 2 restructuring completed - clean old Chinese directories and establish streamlined structure"
    ["🧹 完成重構清理工作：移除重複文件並更新引用"]="chore: complete restructuring cleanup - remove duplicate files and update references"
    ["🔄 重構文檔結構：建立清晰的docs/01-05分類體系"]="refactor: restructure documentation - establish clear docs/01-05 categorization system"
    ["feat: 完成文檔重組 - 創建新目錄結構和角色專屬指南"]="feat: complete documentation reorganization - create new directory structure and role-specific guides"
    ["feat: 建立混合架構文檔體系和項目索引"]="feat: establish hybrid architecture documentation system and project index"
    ["fix: 重寫教育遊戲項目案例，使其與 Bee Swarm 核心理念保持一致"]="fix: rewrite education game project case to align with Bee Swarm core concepts"
    ["docs: 更新 CHANGELOG.md 記錄最新功能擴展和架構改進"]="docs: update CHANGELOG.md to record latest feature expansions and architecture improvements"
    ["feat: 完善 Bee Swarm 文檔系統與功能擴展"]="feat: enhance Bee Swarm documentation system and feature expansion"
    ["🎯 重新定位項目：專注 AI 角色協作概念設計與模擬"]="feat: reposition project focus on AI role collaboration concept design and simulation"
    ["✨ 更新 README: 強化多角色多帳號容器化架構說明"]="docs: update README - strengthen multi-role multi-account containerized architecture description"
    ["🎮 新增教育遊戲項目增強版蜂群模擬系統"]="feat: add enhanced bee swarm simulation system for education game project"
    ["📚 新增 GitHub 敏捷開發工作流指南"]="docs: add GitHub agile development workflow guide"
    ["feat: 合并模拟程序为统一版本，符合Bee Swarm核心思想"]="feat: merge simulation programs into unified version aligned with Bee Swarm core philosophy"
)

echo "正在重寫 commit 消息..."

# 使用 git filter-branch 重寫 commit 消息
git filter-branch --msg-filter '
read MSG
case "$MSG" in
    "docs: 更新CHANGELOG記錄文件名英文化變更")
        echo "docs: update CHANGELOG for filename internationalization changes"
        ;;
    "refactor: 文件名英文化和角色系統更新")
        echo "refactor: internationalize filenames and update role system"
        ;;
    "🧹 完成項目重構最終清理和優化")
        echo "chore: complete project restructuring final cleanup and optimization"
        ;;
    "docs(translation): 完成Bee Swarm項目完整英文翻譯")
        echo "docs(translation): complete English translation for Bee Swarm project"
        ;;
    "📋 更新重構狀態記錄：階段2完成")
        echo "docs: update restructuring status record - phase 2 completed"
        ;;
    "🎯 階段2重構完成：清理舊中文目錄，建立精簡結構")
        echo "refactor: phase 2 restructuring completed - clean old Chinese directories and establish streamlined structure"
        ;;
    "🧹 完成重構清理工作：移除重複文件並更新引用")
        echo "chore: complete restructuring cleanup - remove duplicate files and update references"
        ;;
    "🔄 重構文檔結構：建立清晰的docs/01-05分類體系")
        echo "refactor: restructure documentation - establish clear docs/01-05 categorization system"
        ;;
    "feat: 完成文檔重組 - 創建新目錄結構和角色專屬指南")
        echo "feat: complete documentation reorganization - create new directory structure and role-specific guides"
        ;;
    "feat: 建立混合架構文檔體系和項目索引")
        echo "feat: establish hybrid architecture documentation system and project index"
        ;;
    "fix: 重寫教育遊戲項目案例，使其與 Bee Swarm 核心理念保持一致")
        echo "fix: rewrite education game project case to align with Bee Swarm core concepts"
        ;;
    "docs: 更新 CHANGELOG.md 記錄最新功能擴展和架構改進")
        echo "docs: update CHANGELOG.md to record latest feature expansions and architecture improvements"
        ;;
    "feat: 完善 Bee Swarm 文檔系統與功能擴展")
        echo "feat: enhance Bee Swarm documentation system and feature expansion"
        ;;
    "🎯 重新定位項目：專注 AI 角色協作概念設計與模擬")
        echo "feat: reposition project focus on AI role collaboration concept design and simulation"
        ;;
    "✨ 更新 README: 強化多角色多帳號容器化架構說明")
        echo "docs: update README - strengthen multi-role multi-account containerized architecture description"
        ;;
    "🎮 新增教育遊戲項目增強版蜂群模擬系統")
        echo "feat: add enhanced bee swarm simulation system for education game project"
        ;;
    "📚 新增 GitHub 敏捷開發工作流指南")
        echo "docs: add GitHub agile development workflow guide"
        ;;
    "feat: 合并模拟程序为统一版本，符合Bee Swarm核心思想")
        echo "feat: merge simulation programs into unified version aligned with Bee Swarm core philosophy"
        ;;
    "refactor: 精简仿真文件，保留核心事件驱动仿真")
        echo "refactor: streamline simulation files and retain core event-driven simulation"
        ;;
    "fix(ci): 修复 GitHub Actions workflow 失败问题")
        echo "fix(ci): resolve GitHub Actions workflow failure issues"
        ;;
    "feat: 完成架構簡化和角色重構")
        echo "feat: complete architecture simplification and role restructuring"
        ;;
    "fix(workflows): 修复 GitHub Workflow 文件，确保所有 workflow 都能正常运行")
        echo "fix(workflows): resolve GitHub workflow files to ensure all workflows run properly"
        ;;
    *)
        echo "$MSG"
        ;;
esac
' -- --all

echo "Commit 消息重寫完成！"
echo "備份分支已創建：backup-main-$(date +%Y%m%d)"
echo ""
echo "下一步操作："
echo "1. 檢查重寫結果: git log --oneline"
echo "2. 如果滿意，推送到遠程: git push --force-with-lease origin main"
echo "3. 如果不滿意，恢復: git reset --hard backup-main-$(date +%Y%m%d)" 