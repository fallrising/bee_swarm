"""
配置管理模块
"""
import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    app_name: str = "Bee Swarm Coordinator"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # GitHub配置
    github_token: str = Field(..., env="GITHUB_TOKEN_COORDINATOR")
    github_repository: str = Field(..., env="GITHUB_REPOSITORY")
    github_owner: str = Field(..., env="GITHUB_OWNER")
    
    # 数据库配置
    database_url: str = Field(..., env="DATABASE_URL")
    postgres_db: str = Field(default="beeswarm", env="POSTGRES_DB")
    postgres_user: str = Field(default="beeswarm", env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    
    # Redis配置
    redis_url: str = Field(..., env="REDIS_URL")
    
    # Celery配置
    celery_broker_url: str = Field(..., env="REDIS_URL")
    celery_result_backend: str = Field(..., env="REDIS_URL")
    
    # 任务调度配置
    task_scan_interval: int = Field(default=30, env="TASK_SCAN_INTERVAL")
    role_status_update_interval: int = Field(default=60, env="ROLE_STATUS_UPDATE_INTERVAL")
    max_concurrent_tasks: int = Field(default=10, env="MAX_CONCURRENT_TASKS")
    task_timeout: int = Field(default=3600, env="TASK_TIMEOUT")
    load_balance_strategy: str = Field(default="round_robin", env="LOAD_BALANCE_STRATEGY")
    
    # 日志配置
    log_level: str = Field(default="info", env="LOG_LEVEL")
    log_file: str = "/app/logs/coordinator.log"
    
    # 监控配置
    prometheus_url: str = Field(default="http://prometheus:9090", env="PROMETHEUS_URL")
    grafana_url: str = Field(default="http://grafana:3000", env="GRAFANA_URL")
    
    # 角色池配置
    role_pool_size: int = Field(default=10, env="ROLE_POOL_SIZE")
    
    # 健康检查配置
    health_check_url: str = Field(default="http://coordinator:8000/health", env="HEALTH_CHECK_URL")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 创建全局配置实例
settings = Settings()


# 角色配置
class RoleConfig:
    """角色配置"""
    
    # 产品经理配置
    PM_ROLES = {
        "pm-01": {
            "username": os.getenv("GITHUB_USERNAME_PM_01", "pm_ai_001"),
            "token": os.getenv("GITHUB_TOKEN_PM_01"),
            "ai_tools": ["gemini-cli", "notion-api", "figma-api"],
            "skills": ["product_management", "requirements_analysis", "project_planning"],
            "max_workload": 80
        },
        "pm-02": {
            "username": os.getenv("GITHUB_USERNAME_PM_02", "pm_ai_002"),
            "token": os.getenv("GITHUB_TOKEN_PM_02"),
            "ai_tools": ["gemini-cli", "notion-api", "figma-api"],
            "skills": ["product_management", "requirements_analysis", "project_planning"],
            "max_workload": 80
        }
    }
    
    # 后端开发配置
    BACKEND_ROLES = {
        "backend-01": {
            "username": os.getenv("GITHUB_USERNAME_BACKEND_01", "backend_ai_001"),
            "token": os.getenv("GITHUB_TOKEN_BACKEND_01"),
            "ai_tools": ["claude-code", "rovo-dev", "cursor"],
            "skills": ["python", "nodejs", "java", "api_design"],
            "max_workload": 90
        },
        "backend-02": {
            "username": os.getenv("GITHUB_USERNAME_BACKEND_02", "backend_ai_002"),
            "token": os.getenv("GITHUB_TOKEN_BACKEND_02"),
            "ai_tools": ["claude-code", "rovo-dev", "cursor"],
            "skills": ["python", "go", "rust", "microservices"],
            "max_workload": 90
        },
        "backend-03": {
            "username": os.getenv("GITHUB_USERNAME_BACKEND_03", "backend_ai_003"),
            "token": os.getenv("GITHUB_TOKEN_BACKEND_03"),
            "ai_tools": ["claude-code", "rovo-dev", "cursor"],
            "skills": ["python", "php", "database", "devops"],
            "max_workload": 90
        }
    }
    
    # 前端开发配置
    FRONTEND_ROLES = {
        "frontend-01": {
            "username": os.getenv("GITHUB_USERNAME_FRONTEND_01", "frontend_ai_001"),
            "token": os.getenv("GITHUB_TOKEN_FRONTEND_01"),
            "ai_tools": ["warp", "cursor", "figma-api"],
            "skills": ["react", "vue", "typescript", "ui_design"],
            "max_workload": 85
        },
        "frontend-02": {
            "username": os.getenv("GITHUB_USERNAME_FRONTEND_02", "frontend_ai_002"),
            "token": os.getenv("GITHUB_TOKEN_FRONTEND_02"),
            "ai_tools": ["warp", "cursor", "figma-api"],
            "skills": ["angular", "svelte", "javascript", "responsive_design"],
            "max_workload": 85
        }
    }
    
    # QA工程师配置
    QA_ROLES = {
        "qa-01": {
            "username": os.getenv("GITHUB_USERNAME_QA_01", "qa_ai_001"),
            "token": os.getenv("GITHUB_TOKEN_QA_01"),
            "ai_tools": ["playwright", "jest", "cypress"],
            "skills": ["automated_testing", "manual_testing", "performance_testing"],
            "max_workload": 75
        },
        "qa-02": {
            "username": os.getenv("GITHUB_USERNAME_QA_02", "qa_ai_002"),
            "token": os.getenv("GITHUB_TOKEN_QA_02"),
            "ai_tools": ["playwright", "jest", "cypress"],
            "skills": ["security_testing", "api_testing", "mobile_testing"],
            "max_workload": 75
        }
    }
    
    # DevOps工程师配置
    DEVOPS_ROLES = {
        "devops-01": {
            "username": os.getenv("GITHUB_USERNAME_DEVOPS_01", "devops_ai_001"),
            "token": os.getenv("GITHUB_TOKEN_DEVOPS_01"),
            "ai_tools": ["terraform", "kubernetes", "docker"],
            "skills": ["ci_cd", "kubernetes", "aws", "monitoring"],
            "max_workload": 70
        }
    }
    
    @classmethod
    def get_all_roles(cls):
        """获取所有角色配置"""
        return {
            **cls.PM_ROLES,
            **cls.BACKEND_ROLES,
            **cls.FRONTEND_ROLES,
            **cls.QA_ROLES,
            **cls.DEVOPS_ROLES
        }
    
    @classmethod
    def get_roles_by_type(cls, role_type: str):
        """根据类型获取角色配置"""
        role_mapping = {
            "product_manager": cls.PM_ROLES,
            "backend_developer": cls.BACKEND_ROLES,
            "frontend_developer": cls.FRONTEND_ROLES,
            "qa_engineer": cls.QA_ROLES,
            "devops_engineer": cls.DEVOPS_ROLES
        }
        return role_mapping.get(role_type, {})
    
    @classmethod
    def get_role_config(cls, role_id: str):
        """获取特定角色配置"""
        all_roles = cls.get_all_roles()
        return all_roles.get(role_id)


# 任务标签配置
class TaskLabels:
    """任务标签配置"""
    
    # 任务类型标签
    TASK_TYPES = [
        "feature",      # 新功能
        "bugfix",       # 修复bug
        "refactor",     # 重构
        "documentation", # 文档
        "testing",      # 测试
        "deployment",   # 部署
        "research",     # 调研
        "planning"      # 规划
    ]
    
    # 优先级标签
    PRIORITIES = [
        "critical",     # 紧急
        "high",         # 高
        "medium",       # 中
        "low"           # 低
    ]
    
    # 技能要求标签
    SKILLS = [
        "python", "nodejs", "java", "go", "rust", "php",
        "react", "vue", "angular", "typescript", "javascript",
        "api_design", "database", "microservices", "devops",
        "testing", "ui_design", "product_management"
    ]
    
    # 项目标签
    PROJECTS = [
        "project-a", "project-b", "project-c"
    ]
    
    @classmethod
    def get_all_labels(cls):
        """获取所有标签"""
        return {
            "task_types": cls.TASK_TYPES,
            "priorities": cls.PRIORITIES,
            "skills": cls.SKILLS,
            "projects": cls.PROJECTS
        } 