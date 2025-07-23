# Level 2: 角色池管理

## 角色池架构设计

### 2.1 角色池概览

#### 角色池组成
```
角色池 (Role Pool)：
├── 产品经理 (Product Manager) × 2
│   ├── PM-01: 专注于需求分析和项目规划
│   └── PM-02: 专注于产品设计和用户研究
├── 后端开发 (Backend Developer) × 3
│   ├── Backend-01: 全栈开发，擅长Python/Node.js
│   ├── Backend-02: 微服务专家，擅长Go/Rust
│   └── Backend-03: 数据库专家，擅长PHP/DevOps
├── 前端开发 (Frontend Developer) × 2
│   ├── Frontend-01: React/Vue专家，UI设计
│   └── Frontend-02: Angular/Svelte专家，响应式设计
├── QA工程师 (QA Engineer) × 2
│   ├── QA-01: 自动化测试专家
│   └── QA-02: 安全测试和API测试专家
└── DevOps工程师 (DevOps Engineer) × 1
    └── DevOps-01: CI/CD和云基础设施专家
```

#### 角色状态管理
```yaml
角色状态：
  role_id: "backend-01"
  status: "available"  # available, busy, offline
  current_project: "project-a"
  current_task: "issue-123"
  workload: 75  # 0-100
  skills: ["python", "nodejs", "api_design"]
  ai_tools: ["claude-code", "rovo-dev", "cursor"]
  last_activity: "2024-01-15T10:30:00Z"
  performance_metrics:
    tasks_completed: 45
    average_completion_time: "2.5h"
    success_rate: 0.95
```

### 2.2 角色配置管理

#### 产品经理配置
```python
PM_ROLES = {
    "pm-01": {
        "username": "pm_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["gemini-cli", "notion-api", "figma-api"],
        "skills": ["product_management", "requirements_analysis", "project_planning"],
        "max_workload": 80,
        "specializations": ["web_apps", "mobile_apps", "enterprise_software"]
    },
    "pm-02": {
        "username": "pm_ai_002",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["gemini-cli", "notion-api", "figma-api"],
        "skills": ["product_management", "user_research", "ux_design"],
        "max_workload": 80,
        "specializations": ["ui_ux", "user_experience", "market_research"]
    }
}
```

#### 后端开发配置
```python
BACKEND_ROLES = {
    "backend-01": {
        "username": "backend_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["claude-code", "rovo-dev", "cursor"],
        "skills": ["python", "nodejs", "java", "api_design"],
        "max_workload": 90,
        "specializations": ["rest_apis", "graphql", "microservices"]
    },
    "backend-02": {
        "username": "backend_ai_002",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["claude-code", "rovo-dev", "cursor"],
        "skills": ["python", "go", "rust", "microservices"],
        "max_workload": 90,
        "specializations": ["high_performance", "distributed_systems", "cloud_native"]
    },
    "backend-03": {
        "username": "backend_ai_003",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["claude-code", "rovo-dev", "cursor"],
        "skills": ["python", "php", "database", "devops"],
        "max_workload": 90,
        "specializations": ["database_design", "data_engineering", "infrastructure"]
    }
}
```

#### 前端开发配置
```python
FRONTEND_ROLES = {
    "frontend-01": {
        "username": "frontend_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["warp", "cursor", "figma-api"],
        "skills": ["react", "vue", "typescript", "ui_design"],
        "max_workload": 85,
        "specializations": ["component_libraries", "state_management", "pwa"]
    },
    "frontend-02": {
        "username": "frontend_ai_002",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["warp", "cursor", "figma-api"],
        "skills": ["angular", "svelte", "javascript", "responsive_design"],
        "max_workload": 85,
        "specializations": ["mobile_first", "accessibility", "performance"]
    }
}
```

#### QA工程师配置
```python
QA_ROLES = {
    "qa-01": {
        "username": "qa_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["playwright", "jest", "cypress"],
        "skills": ["automated_testing", "manual_testing", "performance_testing"],
        "max_workload": 75,
        "specializations": ["e2e_testing", "unit_testing", "load_testing"]
    },
    "qa-02": {
        "username": "qa_ai_002",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["playwright", "jest", "cypress"],
        "skills": ["security_testing", "api_testing", "mobile_testing"],
        "max_workload": 75,
        "specializations": ["penetration_testing", "api_security", "mobile_qa"]
    }
}
```

#### DevOps工程师配置
```python
DEVOPS_ROLES = {
    "devops-01": {
        "username": "devops_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["terraform", "kubernetes", "docker"],
        "skills": ["ci_cd", "kubernetes", "aws", "monitoring"],
        "max_workload": 70,
        "specializations": ["infrastructure_as_code", "cloud_architecture", "observability"]
    }
}
```

### 2.3 工作空间管理

#### 共享工作空间结构
```
/workspace/
├── shared/                    # 共享资源
│   ├── tools/                # 共享工具
│   ├── templates/            # 项目模板
│   └── docs/                 # 共享文档
├── project-a/                # 项目A工作空间
│   ├── backend/              # 后端代码
│   ├── frontend/             # 前端代码
│   ├── tests/                # 测试代码
│   └── config/               # 项目配置
├── project-b/                # 项目B工作空间
│   ├── backend/
│   ├── frontend/
│   ├── tests/
│   └── config/
└── temp/                     # 临时文件
    ├── downloads/
    ├── uploads/
    └── cache/
```

#### 上下文切换机制
```python
class ContextManager:
    """上下文管理器"""
    
    def switch_context(self, role_id: str, project_id: str):
        """切换角色到指定项目上下文"""
        # 1. 保存当前工作状态
        self.save_current_state(role_id)
        
        # 2. 切换到项目工作空间
        self.switch_workspace(role_id, project_id)
        
        # 3. 加载项目配置
        self.load_project_config(project_id)
        
        # 4. 设置环境变量
        self.set_environment_variables(project_id)
        
        # 5. 更新角色状态
        self.update_role_status(role_id, project_id)
    
    def save_current_state(self, role_id: str):
        """保存当前工作状态"""
        # 保存当前工作目录
        # 保存打开的文件
        # 保存终端会话
        # 保存环境变量
        pass
    
    def switch_workspace(self, role_id: str, project_id: str):
        """切换到项目工作空间"""
        workspace_path = f"/workspace/{project_id}"
        # 确保工作空间存在
        # 设置工作目录
        # 初始化项目环境
        pass
```

### 2.4 负载均衡策略

#### 负载计算算法
```python
class LoadBalancer:
    """负载均衡器"""
    
    def calculate_workload(self, role_id: str) -> float:
        """计算角色当前负载"""
        role = self.get_role_status(role_id)
        
        # 基础负载：当前任务数量
        base_load = len(role.current_tasks) * 20
        
        # 任务复杂度负载
        complexity_load = sum(task.complexity for task in role.current_tasks)
        
        # 时间负载：任务持续时间
        time_load = sum(task.duration_hours for task in role.current_tasks) * 5
        
        # 总负载
        total_load = min(base_load + complexity_load + time_load, 100)
        
        return total_load
    
    def select_best_role(self, task_requirements: dict) -> str:
        """选择最适合的角色"""
        available_roles = self.get_available_roles()
        
        # 技能匹配度
        skill_scores = {}
        for role_id, role in available_roles.items():
            skill_match = self.calculate_skill_match(role.skills, task_requirements.skills)
            workload_score = 100 - role.workload  # 负载越低分数越高
            performance_score = role.performance_metrics.success_rate * 100
            
            # 综合评分
            total_score = skill_match * 0.5 + workload_score * 0.3 + performance_score * 0.2
            skill_scores[role_id] = total_score
        
        # 返回评分最高的角色
        return max(skill_scores, key=skill_scores.get)
```

#### 负载均衡策略
```python
class LoadBalanceStrategy:
    """负载均衡策略"""
    
    def round_robin(self, available_roles: list) -> str:
        """轮询策略"""
        # 按角色类型轮询分配
        pass
    
    def least_loaded(self, available_roles: list) -> str:
        """最少负载策略"""
        # 选择当前负载最低的角色
        return min(available_roles, key=lambda r: r.workload)
    
    def skill_based(self, task_requirements: dict, available_roles: list) -> str:
        """基于技能的策略"""
        # 根据任务技能要求选择最匹配的角色
        best_match = None
        best_score = 0
        
        for role in available_roles:
            score = self.calculate_skill_match(role.skills, task_requirements.skills)
            if score > best_score:
                best_score = score
                best_match = role
        
        return best_match.role_id
```

### 2.5 角色监控和健康检查

#### 健康检查机制
```python
class HealthChecker:
    """健康检查器"""
    
    def check_role_health(self, role_id: str) -> dict:
        """检查角色健康状态"""
        health_status = {
            "role_id": role_id,
            "status": "healthy",
            "checks": {}
        }
        
        # 检查容器状态
        container_status = self.check_container_status(role_id)
        health_status["checks"]["container"] = container_status
        
        # 检查VNC连接
        vnc_status = self.check_vnc_connection(role_id)
        health_status["checks"]["vnc"] = vnc_status
        
        # 检查GitHub连接
        github_status = self.check_github_connection(role_id)
        health_status["checks"]["github"] = github_status
        
        # 检查AI工具状态
        ai_tools_status = self.check_ai_tools_status(role_id)
        health_status["checks"]["ai_tools"] = ai_tools_status
        
        # 综合状态判断
        if any(check["status"] == "unhealthy" for check in health_status["checks"].values()):
            health_status["status"] = "unhealthy"
        
        return health_status
    
    def check_container_status(self, role_id: str) -> dict:
        """检查容器状态"""
        # 检查Docker容器是否运行
        # 检查资源使用情况
        # 检查日志是否有错误
        pass
    
    def check_vnc_connection(self, role_id: str) -> dict:
        """检查VNC连接状态"""
        # 检查noVNC服务是否响应
        # 检查VNC密码是否正确
        # 检查桌面环境是否正常
        pass
    
    def check_github_connection(self, role_id: str) -> dict:
        """检查GitHub连接状态"""
        # 检查GitHub API连接
        # 检查Token是否有效
        # 检查权限是否足够
        pass
    
    def check_ai_tools_status(self, role_id: str) -> dict:
        """检查AI工具状态"""
        # 检查各个AI工具是否可用
        # 检查API密钥是否有效
        # 检查工具响应时间
        pass
```

#### 性能监控
```python
class PerformanceMonitor:
    """性能监控器"""
    
    def track_role_performance(self, role_id: str):
        """跟踪角色性能指标"""
        metrics = {
            "role_id": role_id,
            "timestamp": datetime.now(),
            "task_completion_rate": self.calculate_completion_rate(role_id),
            "average_task_duration": self.calculate_average_duration(role_id),
            "error_rate": self.calculate_error_rate(role_id),
            "resource_usage": self.get_resource_usage(role_id),
            "ai_tool_usage": self.get_ai_tool_usage(role_id)
        }
        
        # 存储性能指标
        self.store_metrics(metrics)
        
        # 检查是否需要调整
        self.check_performance_alerts(metrics)
    
    def calculate_completion_rate(self, role_id: str) -> float:
        """计算任务完成率"""
        # 统计最近24小时的任务完成情况
        pass
    
    def calculate_average_duration(self, role_id: str) -> float:
        """计算平均任务持续时间"""
        # 计算最近完成任务的平均时间
        pass
    
    def calculate_error_rate(self, role_id: str) -> float:
        """计算错误率"""
        # 统计任务失败和错误的比例
        pass
```

### 2.6 角色扩展和缩容

#### 动态扩缩容
```python
class RoleScaler:
    """角色扩缩容管理器"""
    
    def scale_up(self, role_type: str, count: int = 1):
        """扩容角色"""
        # 1. 检查资源可用性
        if not self.check_resource_availability(role_type, count):
            raise InsufficientResourcesError(f"Insufficient resources for {role_type}")
        
        # 2. 创建新角色容器
        new_roles = []
        for i in range(count):
            role_id = self.generate_role_id(role_type)
            role_config = self.create_role_config(role_type, role_id)
            
            # 启动新容器
            container_id = self.start_role_container(role_config)
            
            # 初始化角色
            self.initialize_role(role_id, role_config)
            
            new_roles.append(role_id)
        
        # 3. 更新角色池配置
        self.update_role_pool_config(role_type, new_roles)
        
        # 4. 通知系统协调器
        self.notify_coordinator_new_roles(new_roles)
        
        return new_roles
    
    def scale_down(self, role_type: str, count: int = 1):
        """缩容角色"""
        # 1. 选择要移除的角色
        roles_to_remove = self.select_roles_to_remove(role_type, count)
        
        # 2. 迁移正在进行的任务
        for role_id in roles_to_remove:
            self.migrate_tasks(role_id)
        
        # 3. 停止角色容器
        for role_id in roles_to_remove:
            self.stop_role_container(role_id)
        
        # 4. 清理角色数据
        for role_id in roles_to_remove:
            self.cleanup_role_data(role_id)
        
        # 5. 更新角色池配置
        self.update_role_pool_config(role_type, remove_roles=roles_to_remove)
        
        return roles_to_remove
    
    def auto_scale(self):
        """自动扩缩容"""
        # 1. 分析当前负载
        current_load = self.analyze_current_load()
        
        # 2. 预测未来负载
        predicted_load = self.predict_future_load()
        
        # 3. 计算需要的角色数量
        required_roles = self.calculate_required_roles(predicted_load)
        
        # 4. 执行扩缩容
        current_roles = self.get_current_role_count()
        
        if required_roles > current_roles:
            # 需要扩容
            self.scale_up(required_roles - current_roles)
        elif required_roles < current_roles:
            # 需要缩容
            self.scale_down(current_roles - required_roles)
```

这个角色池管理系统提供了完整的角色生命周期管理、负载均衡、健康检查和动态扩缩容功能，确保系统能够高效地分配和管理AI开发角色。 