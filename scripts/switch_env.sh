#!/bin/bash

# Bee Swarm 環境切換腳本
# 用於在測試和生產環境之間切換

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 顯示幫助信息
show_help() {
    echo "Bee Swarm 環境切換腳本"
    echo ""
    echo "用法: $0 [production|test|status|validate]"
    echo ""
    echo "選項:"
    echo "  production  切換到生產環境"
    echo "  test        切換到測試環境"
    echo "  status      顯示當前環境狀態"
    echo "  validate    驗證配置"
    echo "  help        顯示此幫助信息"
    echo ""
    echo "示例:"
    echo "  $0 production  # 啟動生產環境"
    echo "  $0 test        # 啟動測試環境"
    echo "  $0 status      # 檢查環境狀態"
    echo "  $0 validate    # 驗證配置"
}

# 檢查 Docker 是否運行
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker 未運行，請先啟動 Docker"
        exit 1
    fi
}

# 檢查 Docker Compose 是否可用
check_docker_compose() {
    if ! docker-compose version > /dev/null 2>&1; then
        log_error "Docker Compose 不可用，請檢查安裝"
        exit 1
    fi
}

# 停止所有容器
stop_all_containers() {
    log_info "停止所有運行中的容器..."
    
    # 停止生產環境容器
    if [ -f "docker-compose.yml" ]; then
        docker-compose down --remove-orphans 2>/dev/null || true
    fi
    
    # 停止測試環境容器
    if [ -f "docker-compose.test.yml" ]; then
        docker-compose -f docker-compose.test.yml down --remove-orphans 2>/dev/null || true
    fi
    
    log_success "所有容器已停止"
}

# 啟動生產環境
start_production() {
    log_info "🚀 切換到生產環境..."
    
    # 檢查配置文件
    if [ ! -f "docker-compose.yml" ]; then
        log_error "找不到 docker-compose.yml 文件"
        exit 1
    fi
    
    if [ ! -f ".env" ]; then
        log_warning "找不到 .env 文件，將使用 env.example"
        cp env.example .env
    fi
    
    # 驗證配置
    log_info "驗證生產環境配置..."
    python3 scripts/validate_config.py
    
    # 停止其他環境
    stop_all_containers
    
    # 啟動生產環境
    log_info "啟動生產環境容器..."
    docker-compose up -d
    
    # 檢查容器狀態
    sleep 5
    docker-compose ps
    
    log_success "生產環境啟動完成！"
    log_info "訪問地址:"
    log_info "  - 產品經理: http://localhost:6080"
    log_info "  - 後端開發: http://localhost:6081"
    log_info "  - 前端開發: http://localhost:6082"
    log_info "  - DevOps: http://localhost:6083"
}

# 啟動測試環境
start_test() {
    log_info "🧪 切換到測試環境..."
    
    # 檢查測試配置文件
    if [ ! -f "docker-compose.test.yml" ]; then
        log_error "找不到 docker-compose.test.yml 文件"
        log_info "請先創建測試環境配置文件"
        exit 1
    fi
    
    if [ ! -f ".env.test" ]; then
        log_warning "找不到 .env.test 文件，將使用 env.example"
        cp env.example .env.test
    fi
    
    # 停止其他環境
    stop_all_containers
    
    # 啟動測試環境
    log_info "啟動測試環境容器..."
    docker-compose -f docker-compose.test.yml --env-file .env.test up -d
    
    # 檢查容器狀態
    sleep 5
    docker-compose -f docker-compose.test.yml ps
    
    log_success "測試環境啟動完成！"
    log_info "訪問地址:"
    log_info "  - 產品經理: http://localhost:6080"
    log_info "  - 後端開發: http://localhost:6081"
    log_info "  - 前端開發: http://localhost:6082"
    log_info "  - DevOps: http://localhost:6083"
}

# 顯示環境狀態
show_status() {
    log_info "📊 當前環境狀態..."
    
    echo ""
    echo "=== 生產環境狀態 ==="
    if [ -f "docker-compose.yml" ]; then
        docker-compose ps 2>/dev/null || echo "生產環境未運行"
    else
        echo "生產環境配置文件不存在"
    fi
    
    echo ""
    echo "=== 測試環境狀態 ==="
    if [ -f "docker-compose.test.yml" ]; then
        docker-compose -f docker-compose.test.yml ps 2>/dev/null || echo "測試環境未運行"
    else
        echo "測試環境配置文件不存在"
    fi
    
    echo ""
    echo "=== 系統資源使用 ==="
    docker system df
    
    echo ""
    echo "=== 網絡狀態 ==="
    docker network ls | grep bee-swarm || echo "未找到 bee-swarm 網絡"
}

# 驗證配置
validate_config() {
    log_info "🔍 驗證系統配置..."
    
    # 檢查必需文件
    required_files=("docker-compose.yml" "env.example" "scripts/validate_config.py")
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "✓ $file 存在"
        else
            log_error "✗ $file 不存在"
        fi
    done
    
    # 檢查 Docker 環境
    check_docker
    check_docker_compose
    log_success "✓ Docker 環境正常"
    
    # 運行配置驗證腳本
    if [ -f "scripts/validate_config.py" ]; then
        log_info "運行配置驗證腳本..."
        python3 scripts/validate_config.py
    else
        log_warning "配置驗證腳本不存在"
    fi
}

# 清理環境
cleanup() {
    log_info "🧹 清理環境..."
    
    # 停止所有容器
    stop_all_containers
    
    # 清理未使用的資源
    docker system prune -f
    
    # 清理未使用的卷
    docker volume prune -f
    
    # 清理未使用的網絡
    docker network prune -f
    
    log_success "環境清理完成"
}

# 主函數
main() {
    local action=${1:-help}
    
    case $action in
        "production"|"prod")
            check_docker
            check_docker_compose
            start_production
            ;;
        "test")
            check_docker
            check_docker_compose
            start_test
            ;;
        "status")
            show_status
            ;;
        "validate")
            validate_config
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "無效的選項: $action"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 執行主函數
main "$@" 