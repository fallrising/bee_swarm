#!/bin/bash

# Bee Swarm 角色容器管理腳本
# 用於編譯、推送、啟動和管理 AI 角色容器

set -e

# 配置變量
DOCKER_REGISTRY="your-registry"
PROJECT_NAME="bee-swarm"
ROLES_DIR="./roles"

# 顏色輸出
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

# 顯示使用說明
show_usage() {
    cat << EOF
Bee Swarm 角色容器管理工具

用法: $0 [命令] [選項]

命令:
  build [role]     - 編譯指定角色容器（不指定則編譯所有）
  push [role]      - 推送指定角色容器到註冊表
  start [role]     - 啟動指定角色容器
  stop [role]      - 停止指定角色容器
  restart [role]   - 重啟指定角色容器
  logs [role]      - 查看指定角色容器日誌
  status           - 查看所有角色容器狀態
  clean            - 清理未使用的容器和映像
  list-roles       - 列出所有可用角色

選項:
  -h, --help       - 顯示此幫助信息
  -v, --verbose    - 詳細輸出
  --core-only      - 僅操作核心角色（4個）
  --all            - 操作所有角色（包括擴展角色）

範例:
  $0 build product_manager           # 編譯產品經理角色
  $0 start --core-only              # 啟動所有核心角色
  $0 status                         # 查看容器狀態
  $0 clean                          # 清理未使用資源

EOF
}

# 獲取所有角色列表
get_roles() {
    local core_only=$1
    local roles=()
    
    # 核心角色
    local core_roles=("product_manager" "backend_developer" "frontend_developer" "devops_engineer")
    
    # 擴展角色
    local extended_roles=("android_developer" "ios_developer" "unity_developer" "visual_designer" "data_engineer")
    
    if [[ "$core_only" == "true" ]]; then
        roles=("${core_roles[@]}")
    else
        roles=("${core_roles[@]}" "${extended_roles[@]}")
    fi
    
    echo "${roles[@]}"
}

# 檢查角色是否存在
check_role_exists() {
    local role=$1
    if [[ ! -d "$ROLES_DIR/$role" ]]; then
        log_error "角色 '$role' 不存在"
        return 1
    fi
    
    if [[ ! -f "$ROLES_DIR/$role/Dockerfile" ]]; then
        log_error "角色 '$role' 缺少 Dockerfile"
        return 1
    fi
    
    return 0
}

# 編譯角色容器
build_role() {
    local role=$1
    
    if ! check_role_exists "$role"; then
        return 1
    fi
    
    log_info "正在編譯角色容器: $role"
    
    local image_name="$PROJECT_NAME/$role:latest"
    local dockerfile_path="$ROLES_DIR/$role/Dockerfile"
    
    if docker build -t "$image_name" -f "$dockerfile_path" "$ROLES_DIR/$role/"; then
        log_success "角色 '$role' 編譯完成"
        return 0
    else
        log_error "角色 '$role' 編譯失敗"
        return 1
    fi
}

# 推送角色容器
push_role() {
    local role=$1
    local image_name="$PROJECT_NAME/$role:latest"
    
    if [[ -z "$DOCKER_REGISTRY" ]]; then
        log_error "請設置 DOCKER_REGISTRY 環境變量"
        return 1
    fi
    
    local registry_image="$DOCKER_REGISTRY/$image_name"
    
    log_info "正在推送角色容器: $role"
    
    # 標記映像
    docker tag "$image_name" "$registry_image"
    
    # 推送映像
    if docker push "$registry_image"; then
        log_success "角色 '$role' 推送完成"
        return 0
    else
        log_error "角色 '$role' 推送失敗"
        return 1
    fi
}

# 啟動角色容器
start_role() {
    local role=$1
    local container_name="$PROJECT_NAME-$role"
    local image_name="$PROJECT_NAME/$role:latest"
    
    # 檢查容器是否已存在
    if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
        log_warning "容器 '$container_name' 已存在"
        
        # 檢查是否正在運行
        if docker ps --format '{{.Names}}' | grep -q "^$container_name$"; then
            log_info "容器 '$container_name' 已在運行"
            return 0
        else
            log_info "正在啟動現有容器: $container_name"
            docker start "$container_name"
            return $?
        fi
    fi
    
    log_info "正在創建並啟動新容器: $container_name"
    
    # 分配端口（基於角色索引）
    local vnc_port
    local ttyd_port
    
    case "$role" in
        "product_manager")     vnc_port=6080; ttyd_port=7681 ;;
        "backend_developer")   vnc_port=6081; ttyd_port=7682 ;;
        "frontend_developer")  vnc_port=6082; ttyd_port=7683 ;;
        "devops_engineer")     vnc_port=6083; ttyd_port=7684 ;;
        *)                     vnc_port=6090; ttyd_port=7690 ;;
    esac
    
    # 啟動容器
    docker run -d \
        --name "$container_name" \
        --restart unless-stopped \
        -p "$vnc_port:6080" \
        -p "$ttyd_port:7681" \
        -e "ROLE_NAME=$role" \
        -e "VNC_PASSWORD=${VNC_PASSWORD:-beeswarm}" \
        -e "TTYD_PASSWORD=${TTYD_PASSWORD:-beeswarm}" \
        -v "$(pwd)/workspace:/app/workspace" \
        "$image_name"
    
    if [[ $? -eq 0 ]]; then
        log_success "容器 '$container_name' 啟動成功"
        log_info "VNC 訪問地址: http://localhost:$vnc_port"
        log_info "終端訪問地址: http://localhost:$ttyd_port"
        return 0
    else
        log_error "容器 '$container_name' 啟動失敗"
        return 1
    fi
}

# 停止角色容器
stop_role() {
    local role=$1
    local container_name="$PROJECT_NAME-$role"
    
    if docker ps --format '{{.Names}}' | grep -q "^$container_name$"; then
        log_info "正在停止容器: $container_name"
        docker stop "$container_name"
        log_success "容器 '$container_name' 已停止"
    else
        log_warning "容器 '$container_name' 未在運行"
    fi
}

# 重啟角色容器
restart_role() {
    local role=$1
    stop_role "$role"
    start_role "$role"
}

# 查看角色容器日誌
show_logs() {
    local role=$1
    local container_name="$PROJECT_NAME-$role"
    
    if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
        log_info "顯示容器日誌: $container_name"
        docker logs -f "$container_name"
    else
        log_error "容器 '$container_name' 不存在"
        return 1
    fi
}

# 查看所有容器狀態
show_status() {
    log_info "Bee Swarm 角色容器狀態:"
    echo ""
    
    local roles
    roles=($(get_roles false))
    
    printf "%-20s %-15s %-10s %-15s\n" "角色" "容器名" "狀態" "端口"
    printf "%-20s %-15s %-10s %-15s\n" "----" "------" "----" "----"
    
    for role in "${roles[@]}"; do
        local container_name="$PROJECT_NAME-$role"
        local status="不存在"
        local ports=""
        
        if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
            status=$(docker ps -a --filter "name=$container_name" --format '{{.Status}}' | head -1)
            ports=$(docker ps --filter "name=$container_name" --format '{{.Ports}}' | head -1)
        fi
        
        printf "%-20s %-15s %-10s %-15s\n" "$role" "$container_name" "$status" "$ports"
    done
}

# 清理未使用資源
clean_resources() {
    log_info "清理未使用的 Docker 資源"
    
    # 清理停止的容器
    log_info "清理停止的容器..."
    docker container prune -f
    
    # 清理未使用的映像
    log_info "清理未使用的映像..."
    docker image prune -f
    
    # 清理未使用的網絡
    log_info "清理未使用的網絡..."
    docker network prune -f
    
    # 清理未使用的卷
    log_info "清理未使用的卷..."
    docker volume prune -f
    
    log_success "清理完成"
}

# 列出所有角色
list_roles() {
    log_info "可用的 AI 角色:"
    echo ""
    
    echo "核心角色 (Core Roles):"
    local core_roles=("product_manager" "backend_developer" "frontend_developer" "devops_engineer")
    for role in "${core_roles[@]}"; do
        echo "  - $role"
    done
    
    echo ""
    echo "擴展角色 (Extended Roles):"
    local extended_roles=("android_developer" "ios_developer" "unity_developer" "visual_designer" "data_engineer")
    for role in "${extended_roles[@]}"; do
        echo "  - $role"
    done
}

# 批量操作
batch_operation() {
    local operation=$1
    local core_only=$2
    local roles
    
    roles=($(get_roles "$core_only"))
    
    log_info "執行批量操作: $operation"
    log_info "目標角色: ${roles[*]}"
    
    for role in "${roles[@]}"; do
        case "$operation" in
            "build")
                build_role "$role" || log_error "角色 '$role' 操作失敗"
                ;;
            "start")
                start_role "$role" || log_error "角色 '$role' 操作失敗"
                ;;
            "stop")
                stop_role "$role" || log_error "角色 '$role' 操作失敗"
                ;;
            "push")
                push_role "$role" || log_error "角色 '$role' 操作失敗"
                ;;
        esac
    done
}

# 主函數
main() {
    local command=$1
    local role=$2
    local core_only=false
    local all_roles=false
    
    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            --core-only)
                core_only=true
                shift
                ;;
            --all)
                all_roles=true
                shift
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            *)
                if [[ -z "$command" ]]; then
                    command=$1
                elif [[ -z "$role" ]]; then
                    role=$1
                fi
                shift
                ;;
        esac
    done
    
    # 檢查 Docker 是否可用
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安裝或不可用"
        exit 1
    fi
    
    # 執行命令
    case "$command" in
        "build")
            if [[ -n "$role" ]]; then
                build_role "$role"
            else
                batch_operation "build" "$core_only"
            fi
            ;;
        "push")
            if [[ -n "$role" ]]; then
                push_role "$role"
            else
                batch_operation "push" "$core_only"
            fi
            ;;
        "start")
            if [[ -n "$role" ]]; then
                start_role "$role"
            else
                batch_operation "start" "$core_only"
            fi
            ;;
        "stop")
            if [[ -n "$role" ]]; then
                stop_role "$role"
            else
                batch_operation "stop" "$core_only"
            fi
            ;;
        "restart")
            if [[ -n "$role" ]]; then
                restart_role "$role"
            else
                batch_operation "stop" "$core_only"
                sleep 2
                batch_operation "start" "$core_only"
            fi
            ;;
        "logs")
            if [[ -n "$role" ]]; then
                show_logs "$role"
            else
                log_error "請指定要查看日誌的角色"
                exit 1
            fi
            ;;
        "status")
            show_status
            ;;
        "clean")
            clean_resources
            ;;
        "list-roles")
            list_roles
            ;;
        *)
            log_error "未知命令: $command"
            show_usage
            exit 1
            ;;
    esac
}

# 執行主函數
main "$@" 