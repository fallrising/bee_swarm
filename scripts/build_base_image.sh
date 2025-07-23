#!/bin/bash

# 構建基礎 VNC Lab 鏡像腳本
# 用於構建 MCP Server 架構的基礎鏡像

set -e

echo "🚀 開始構建 VNC Lab 基礎鏡像..."

# 檢查是否克隆了 VNC Lab 倉庫
if [ ! -d "vnc_lab" ]; then
    echo "📥 克隆 VNC Lab 倉庫..."
    git clone https://github.com/fallrising/vnc_lab.git
fi

cd vnc_lab

# 構建 novnc_llm_cli 基礎鏡像
echo "🔨 構建 novnc_llm_cli 基礎鏡像..."
cd novnc_llm_cli
docker build -t fallrising/novnc_llm_cli:latest .

# 構建 vnc-llm-cli 別名（向後兼容）
docker tag fallrising/novnc_llm_cli:latest vnc-llm-cli:latest

echo "✅ 基礎鏡像構建完成！"
echo "📋 可用的鏡像："
echo "  - fallrising/novnc_llm_cli:latest"
echo "  - vnc-llm-cli:latest"

# 返回原目錄
cd ../..

echo "🎉 基礎鏡像準備就緒，可以開始構建角色容器了！" 