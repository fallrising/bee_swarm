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
        "GITHUB_TOKEN_COORDINATOR"
        "GITHUB_REPOSITORY"
        "GITHUB_OWNER"
        "DATABASE_URL"
        "REDIS_URL"
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
    
    # 构建系统协调器
    log_info "Building coordinator image..."
    if [ -d "coordinator" ]; then
        cd coordinator
        docker build -t bee-swarm-coordinator . || {
            log_error "Failed to build coordinator image"
            exit 1
        }
        cd ..
    else
        log_warn "Coordinator directory not found, skipping coordinator build"
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
    
    # 启动基础服务
    log_info "Starting infrastructure services..."
    docker-compose up -d redis postgres prometheus grafana || {
        log_error "Failed to start infrastructure services"
        exit 1
    }
    
    # 等待基础服务启动
    log_info "Waiting for infrastructure services to start..."
    sleep 30
    
    # 启动系统协调器
    log_info "Starting coordinator..."
    docker-compose up -d coordinator || {
        log_error "Failed to start coordinator"
        exit 1
    }
    
    # 等待协调器启动
    log_info "Waiting for coordinator to start..."
    sleep 20
    
    # 启动角色池
    log_info "Starting role pool..."
    docker-compose up -d pm-01 pm-02 backend-01 backend-02 backend-03 frontend-01 frontend-02 qa-01 qa-02 devops-01 || {
        log_error "Failed to start role pool"
        exit 1
    }
    
    # 等待角色启动
    log_info "Waiting for roles to start..."
    sleep 60
    
    # 检查服务状态
    check_service_status
    
    log_info "Services started successfully"
}

# 检查服务状态
check_service_status() {
    log_step "Checking service status..."
    
    # 检查基础设施服务
    infrastructure_services=("redis" "postgres" "prometheus" "grafana")
    for service in "${infrastructure_services[@]}"; do
        if docker-compose ps | grep -q "$service.*Up"; then
            log_info "$service is running"
        else
            log_error "$service is not running"
            docker-compose logs "$service"
        fi
    done
    
    # 检查协调器
    if docker-compose ps | grep -q "coordinator.*Up"; then
        log_info "coordinator is running"
    else
        log_error "coordinator is not running"
        docker-compose logs coordinator
    fi
    
    # 检查角色池
    role_services=("pm-01" "pm-02" "backend-01" "backend-02" "backend-03" "frontend-01" "frontend-02" "qa-01" "qa-02" "devops-01")
    for service in "${role_services[@]}"; do
        if docker-compose ps | grep -q "$service.*Up"; then
            log_info "$service is running"
        else
            log_error "$service is not running"
            docker-compose logs "$service"
        fi
    done
}

# 配置GitHub仓库
setup_github_repository() {
    log_step "Setting up GitHub repository..."
    
    log_warn "Please manually configure GitHub repository:"
    log_warn "1. Create GitHub Projects board for task management"
    log_warn "2. Set up Labels for task classification:"
    log_warn "   - task types: feature, bugfix, refactor, documentation, testing, deployment, research, planning"
    log_warn "   - priorities: critical, high, medium, low"
    log_warn "   - skills: python, nodejs, java, go, rust, php, react, vue, angular, typescript, javascript"
    log_warn "   - projects: project-a, project-b, project-c"
    log_warn "3. Configure role GitHub accounts with appropriate permissions"
    log_warn "4. Set up repository webhooks (optional for future use)"
    
    # 提供自动配置的选项
    if command -v gh &> /dev/null && [ -n "$GITHUB_REPOSITORY" ]; then
        read -p "Do you want to configure GitHub repository automatically? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            configure_github_automatically
        fi
    fi
}

# 自动配置GitHub
configure_github_automatically() {
    log_info "Configuring GitHub repository automatically..."
    
    # 创建Labels
    log_info "Creating labels..."
    labels=(
        "feature:新功能:0366d6"
        "bugfix:修复bug:d73a4a"
        "refactor:重构:7057ff"
        "documentation:文档:0075ca"
        "testing:测试:0e8a16"
        "deployment:部署:5319e7"
        "research:调研:fbca04"
        "planning:规划:1d76db"
        "critical:紧急:d93f0b"
        "high:高:fb8c00"
        "medium:中:fbca04"
        "low:低:0e8a16"
        "python:Python:3776ab"
        "nodejs:Node.js:339933"
        "java:Java:ed8b00"
        "go:Go:00add8"
        "rust:Rust:dea584"
        "php:PHP:777bb4"
        "react:React:61dafb"
        "vue:Vue:4fc08d"
        "angular:Angular:dd0031"
        "typescript:TypeScript:3178c6"
        "javascript:JavaScript:f7df1e"
    )
    
    for label in "${labels[@]}"; do
        IFS=':' read -r name description color <<< "$label"
        gh api repos/$GITHUB_REPOSITORY/labels \
            -f name="$name" \
            -f description="$description" \
            -f color="$color" || {
            log_warn "Failed to create label $name"
        }
    done
    
    log_info "GitHub repository configured successfully"
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
    ports=(8000 5555 6080 6081 6082 6083 6084 6085 6086 6087 6088 6089 6379 5432 9090 3000)
    for port in "${ports[@]}"; do
        if netstat -tuln 2>/dev/null | grep -q ":$port " || ss -tuln 2>/dev/null | grep -q ":$port "; then
            log_info "Port $port is listening"
        else
            log_warn "Port $port is not listening"
        fi
    done
    
    # 检查协调器API
    if curl -s http://localhost:8000/health > /dev/null; then
        log_info "Coordinator API is responding"
    else
        log_warn "Coordinator API is not responding"
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
        docker run --rm -v bee-swarm_coordinator_data:/data -v "$(pwd)/$backup_dir":/backup alpine tar czf /backup/coordinator_data.tar.gz -C /data . 2>/dev/null || true
        docker run --rm -v bee-swarm_shared_workspace:/data -v "$(pwd)/$backup_dir":/backup alpine tar czf /backup/workspace_data.tar.gz -C /data . 2>/dev/null || true
    fi
    
    log_info "Backup saved to $backup_dir"
}

# 显示访问信息
show_access_info() {
    log_step "Deployment completed successfully!"
    echo
    log_info "Access URLs:"
    log_info "  Coordinator API: http://localhost:8000"
    log_info "  Coordinator Docs: http://localhost:8000/docs"
    log_info "  Flower (Celery): http://localhost:5555"
    echo
    log_info "Role VNC Access:"
    log_info "  Product Manager 1: http://localhost:6080"
    log_info "  Product Manager 2: http://localhost:6081"
    log_info "  Backend Developer 1: http://localhost:6082"
    log_info "  Backend Developer 2: http://localhost:6083"
    log_info "  Backend Developer 3: http://localhost:6084"
    log_info "  Frontend Developer 1: http://localhost:6085"
    log_info "  Frontend Developer 2: http://localhost:6086"
    log_info "  QA Engineer 1: http://localhost:6087"
    log_info "  QA Engineer 2: http://localhost:6088"
    log_info "  DevOps Engineer 1: http://localhost:6089"
    echo
    log_info "Management URLs:"
    log_info "  Prometheus: http://localhost:9090"
    log_info "  Grafana: http://localhost:3000 (admin/admin)"
    echo
    log_info "Useful commands:"
    log_info "  View logs: docker-compose logs -f [service-name]"
    log_info "  Stop services: docker-compose down"
    log_info "  Restart services: docker-compose restart"
    log_info "  Update services: docker-compose pull && docker-compose up -d"
    echo
    log_info "Next steps:"
    log_info "  1. Configure GitHub repository settings"
    log_info "  2. Set up GitHub Projects board"
    log_info "  3. Create initial issues for testing"
    log_info "  4. Monitor coordinator logs for task processing"
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
    
    # 配置GitHub仓库
    setup_github_repository
    
    # 显示访问信息
    show_access_info
}

# 运行主函数
main "$@" 