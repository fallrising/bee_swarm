#!/bin/bash

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查环境
check_environment() {
    log_step "Checking environment..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # 检查环境变量文件
    if [ ! -f .env ]; then
        log_error ".env file not found"
        log_info "Please copy env.example to .env and configure it"
        exit 1
    fi
    
    # 检查必要的环境变量
    required_vars=(
        "GITHUB_TOKEN_PM"
        "GITHUB_TOKEN_BACKEND"
        "GITHUB_TOKEN_FRONTEND"
        "GITHUB_TOKEN_QA"
        "GITHUB_TOKEN_DEVOPS"
        "GITHUB_WEBHOOK_SECRET"
    )
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    log_info "Environment check passed"
}

# 构建镜像
build_images() {
    log_step "Building Docker images..."
    
    # 构建基础镜像
    log_info "Building base images..."
    if [ -d "novnc_base" ]; then
        cd novnc_base
        docker build -t vnc-base . || {
            log_error "Failed to build vnc-base image"
            exit 1
        }
        cd ..
    fi
    
    if [ -d "novnc_llm_cli" ]; then
        cd novnc_llm_cli
        docker build -t vnc-llm-cli . || {
            log_error "Failed to build vnc-llm-cli image"
            exit 1
        }
        cd ..
    fi
    
    # 构建角色镜像
    log_info "Building role images..."
    docker-compose build || {
        log_error "Failed to build role images"
        exit 1
    }
    
    log_info "Image build completed"
}

# 启动服务
start_services() {
    log_step "Starting services..."
    
    # 启动所有服务
    docker-compose up -d || {
        log_error "Failed to start services"
        exit 1
    }
    
    # 等待服务启动
    log_info "Waiting for services to start..."
    sleep 30
    
    # 检查服务状态
    check_service_status
    
    log_info "Services started successfully"
}

# 检查服务状态
check_service_status() {
    log_step "Checking service status..."
    
    services=("product-manager" "backend-developer" "frontend-developer" "qa-engineer" "devops-engineer")
    
    for service in "${services[@]}"; do
        if docker-compose ps | grep -q "$service.*Up"; then
            log_info "$service is running"
        else
            log_error "$service is not running"
            docker-compose logs "$service"
        fi
    done
}

# 配置GitHub Webhook
setup_webhook() {
    log_step "Setting up GitHub webhook..."
    
    # 检查是否有外部域名配置
    if [ -n "$EXTERNAL_DOMAIN" ]; then
        webhook_url="https://$EXTERNAL_DOMAIN/webhook"
    else
        webhook_url="http://localhost:5000/webhook"
        log_warn "No external domain configured, using localhost"
    fi
    
    log_warn "Please manually configure GitHub webhook:"
    log_warn "URL: $webhook_url"
    log_warn "Content type: application/json"
    log_warn "Secret: $GITHUB_WEBHOOK_SECRET"
    log_warn "Events: Issues, Pull requests, Push"
    
    # 提供自动配置的选项
    if command -v gh &> /dev/null && [ -n "$GITHUB_REPOSITORY" ]; then
        read -p "Do you want to configure webhook automatically? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            configure_webhook_automatically "$webhook_url"
        fi
    fi
}

# 自动配置webhook
configure_webhook_automatically() {
    local webhook_url="$1"
    
    log_info "Configuring webhook automatically..."
    
    # 使用GitHub CLI配置webhook
    gh api repos/$GITHUB_REPOSITORY/hooks \
        -f name="bee-swarm-webhook" \
        -f active=true \
        -f events='["issues", "pull_request", "push"]' \
        -f config="{\"url\": \"$webhook_url\", \"content_type\": \"json\", \"secret\": \"$GITHUB_WEBHOOK_SECRET\"}" || {
        log_error "Failed to configure webhook automatically"
        return 1
    }
    
    log_info "Webhook configured successfully"
}

# 健康检查
health_check() {
    log_step "Performing health check..."
    
    # 检查容器健康状态
    unhealthy_containers=$(docker-compose ps | grep "unhealthy" | wc -l)
    
    if [ "$unhealthy_containers" -gt 0 ]; then
        log_error "Found $unhealthy_containers unhealthy containers"
        docker-compose ps
        exit 1
    fi
    
    # 检查端口监听
    ports=(6080 6081 6082 6083 6084 5000 6379 9090 3000)
    for port in "${ports[@]}"; do
        if netstat -tuln 2>/dev/null | grep -q ":$port " || ss -tuln 2>/dev/null | grep -q ":$port "; then
            log_info "Port $port is listening"
        else
            log_warn "Port $port is not listening"
        fi
    done
    
    # 检查webhook端点
    if curl -s http://localhost:5000/health > /dev/null; then
        log_info "Webhook handler is responding"
    else
        log_warn "Webhook handler is not responding"
    fi
    
    log_info "Health check completed"
}

# 清理旧容器
cleanup_old_containers() {
    log_step "Cleaning up old containers..."
    
    # 停止并删除旧容器
    docker-compose down --remove-orphans || true
    
    # 清理未使用的镜像
    docker image prune -f || true
    
    log_info "Cleanup completed"
}

# 备份数据
backup_data() {
    log_step "Backing up data..."
    
    backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # 备份配置文件
    cp .env "$backup_dir/" 2>/dev/null || true
    cp docker-compose.yml "$backup_dir/" 2>/dev/null || true
    
    # 备份日志
    if [ -d "logs" ]; then
        cp -r logs "$backup_dir/" 2>/dev/null || true
    fi
    
    # 备份数据卷（如果存在）
    if docker volume ls | grep -q "bee-swarm"; then
        docker run --rm -v bee-swarm_pm_data:/data -v "$(pwd)/$backup_dir":/backup alpine tar czf /backup/pm_data.tar.gz -C /data . 2>/dev/null || true
        docker run --rm -v bee-swarm_backend_data:/data -v "$(pwd)/$backup_dir":/backup alpine tar czf /backup/backend_data.tar.gz -C /data . 2>/dev/null || true
    fi
    
    log_info "Backup saved to $backup_dir"
}

# 显示访问信息
show_access_info() {
    log_step "Deployment completed successfully!"
    echo
    log_info "Access URLs:"
    log_info "  Product Manager: http://localhost:6080"
    log_info "  Backend Developer: http://localhost:6081"
    log_info "  Frontend Developer: http://localhost:6082"
    log_info "  QA Engineer: http://localhost:6083"
    log_info "  DevOps Engineer: http://localhost:6084"
    echo
    log_info "Management URLs:"
    log_info "  Webhook Handler: http://localhost:5000"
    log_info "  Prometheus: http://localhost:9090"
    log_info "  Grafana: http://localhost:3000 (admin/admin)"
    echo
    log_info "Useful commands:"
    log_info "  View logs: docker-compose logs -f [service-name]"
    log_info "  Stop services: docker-compose down"
    log_info "  Restart services: docker-compose restart"
    log_info "  Update services: docker-compose pull && docker-compose up -d"
}

# 显示帮助信息
show_help() {
    echo "Bee Swarm Deployment Script"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -c, --check-only    Only check environment, don't deploy"
    echo "  -b, --build-only    Only build images, don't start services"
    echo "  -s, --start-only    Only start services, don't build"
    echo "  -f, --force         Force deployment without confirmation"
    echo "  -e, --env ENV_FILE  Use specific environment file"
    echo
    echo "Examples:"
    echo "  $0                  Full deployment"
    echo "  $0 -c               Environment check only"
    echo "  $0 -b               Build images only"
    echo "  $0 -s               Start services only"
    echo "  $0 -f               Force deployment"
}

# 主函数
main() {
    local check_only=false
    local build_only=false
    local start_only=false
    local force=false
    local env_file=".env"
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--check-only)
                check_only=true
                shift
                ;;
            -b|--build-only)
                build_only=true
                shift
                ;;
            -s|--start-only)
                start_only=true
                shift
                ;;
            -f|--force)
                force=true
                shift
                ;;
            -e|--env)
                env_file="$2"
                shift 2
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 加载环境变量
    if [ -f "$env_file" ]; then
        export $(cat "$env_file" | grep -v '^#' | xargs)
    else
        log_error "Environment file $env_file not found"
        exit 1
    fi
    
    log_info "Starting Bee Swarm deployment..."
    
    # 检查环境
    check_environment
    
    if [ "$check_only" = true ]; then
        log_info "Environment check completed"
        exit 0
    fi
    
    # 确认部署
    if [ "$force" = false ]; then
        echo
        read -p "Do you want to proceed with deployment? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Deployment cancelled"
            exit 0
        fi
    fi
    
    # 备份数据
    backup_data
    
    # 清理旧容器
    cleanup_old_containers
    
    # 构建镜像
    if [ "$start_only" = false ]; then
        build_images
    fi
    
    if [ "$build_only" = true ]; then
        log_info "Image build completed"
        exit 0
    fi
    
    # 启动服务
    start_services
    
    # 健康检查
    health_check
    
    # 配置webhook
    setup_webhook
    
    # 显示访问信息
    show_access_info
}

# 运行主函数
main "$@" 