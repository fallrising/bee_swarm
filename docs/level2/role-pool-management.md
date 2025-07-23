# Level 2: Role Pool Management

## Role Pool Architecture Design

### 2.1 Role Pool Overview

#### Role Pool Composition
```
Role Pool:
├── Product Manager × 2
│   ├── PM-01: Focus on requirements analysis and project planning
│   └── PM-02: Focus on product design and user research
├── Backend Developer × 3
│   ├── Backend-01: Full-stack development, expert in Python/Node.js
│   ├── Backend-02: Microservices expert, expert in Go/Rust
│   └── Backend-03: Database expert, expert in PHP/DevOps
├── Frontend Developer × 2
│   ├── Frontend-01: React/Vue expert, UI design
│   └── Frontend-02: Angular/Svelte expert, responsive design
├── QA Engineer × 2
│   ├── QA-01: Automated testing expert
│   └── QA-02: Security testing and API testing expert
└── DevOps Engineer × 1
    └── DevOps-01: CI/CD and cloud infrastructure expert
```

#### Role State Management
```yaml
Role State:
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

### 2.2 Role Configuration Management

#### Product Manager Configuration
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

#### Backend Developer Configuration
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

#### Frontend Developer Configuration
```python
FRONTEND_ROLES = {
    "frontend-01": {
        "username": "frontend_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["warp", "cursor", "figma-api"],
        "skills": ["react", "vue", "javascript", "typescript"],
        "max_workload": 85,
        "specializations": ["ui_design", "component_library", "state_management"]
    },
    "frontend-02": {
        "username": "frontend_ai_002",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["warp", "cursor", "figma-api"],
        "skills": ["angular", "svelte", "css", "responsive_design"],
        "max_workload": 85,
        "specializations": ["responsive_design", "accessibility", "performance_optimization"]
    }
}
```

#### QA Engineer Configuration
```python
QA_ROLES = {
    "qa-01": {
        "username": "qa_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["playwright", "jest", "cypress"],
        "skills": ["automated_testing", "manual_testing", "test_planning"],
        "max_workload": 80,
        "specializations": ["e2e_testing", "unit_testing", "integration_testing"]
    },
    "qa-02": {
        "username": "qa_ai_002",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["playwright", "jest", "cypress"],
        "skills": ["security_testing", "api_testing", "performance_testing"],
        "max_workload": 80,
        "specializations": ["security_audit", "penetration_testing", "load_testing"]
    }
}
```

#### DevOps Engineer Configuration
```python
DEVOPS_ROLES = {
    "devops-01": {
        "username": "devops_ai_001",
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
        "ai_tools": ["terraform", "kubernetes", "docker"],
        "skills": ["ci_cd", "cloud_infrastructure", "monitoring"],
        "max_workload": 85,
        "specializations": ["aws", "kubernetes", "terraform", "jenkins"]
    }
}
```

### 2.3 Workspace Management

#### Workspace Isolation
```python
class WorkspaceManager:
    def __init__(self):
        self.workspaces = {}
        self.base_path = "/workspace"
    
    def create_workspace(self, project_id: str, role_id: str):
        """Create isolated workspace for role"""
        workspace_path = f"{self.base_path}/{project_id}/{role_id}"
        os.makedirs(workspace_path, exist_ok=True)
        
        # Initialize git repository
        subprocess.run(["git", "init"], cwd=workspace_path)
        
        # Set up environment
        self._setup_environment(workspace_path, role_id)
        
        return workspace_path
    
    def _setup_environment(self, workspace_path: str, role_id: str):
        """Set up development environment for role"""
        # Create .env file
        env_file = f"{workspace_path}/.env"
        with open(env_file, "w") as f:
            f.write(f"ROLE_ID={role_id}\n")
            f.write(f"WORKSPACE_PATH={workspace_path}\n")
        
        # Create role-specific configuration
        self._create_role_config(workspace_path, role_id)
    
    def _create_role_config(self, workspace_path: str, role_id: str):
        """Create role-specific configuration files"""
        config_dir = f"{workspace_path}/.bee-swarm"
        os.makedirs(config_dir, exist_ok=True)
        
        # Create role configuration
        role_config = {
            "role_id": role_id,
            "created_at": datetime.now().isoformat(),
            "ai_tools": self._get_role_ai_tools(role_id),
            "skills": self._get_role_skills(role_id)
        }
        
        with open(f"{config_dir}/role.json", "w") as f:
            json.dump(role_config, f, indent=2)
```

#### Context Switching
```python
class ContextManager:
    def __init__(self):
        self.active_contexts = {}
    
    def switch_context(self, role_id: str, project_id: str):
        """Switch role to different project context"""
        context_key = f"{role_id}:{project_id}"
        
        if context_key in self.active_contexts:
            # Resume existing context
            context = self.active_contexts[context_key]
            self._restore_context(context)
        else:
            # Create new context
            context = self._create_context(role_id, project_id)
            self.active_contexts[context_key] = context
        
        return context
    
    def _create_context(self, role_id: str, project_id: str):
        """Create new project context for role"""
        context = {
            "role_id": role_id,
            "project_id": project_id,
            "workspace_path": f"/workspace/{project_id}/{role_id}",
            "current_task": None,
            "task_history": [],
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        
        # Initialize workspace
        workspace_manager = WorkspaceManager()
        workspace_manager.create_workspace(project_id, role_id)
        
        return context
    
    def _restore_context(self, context: dict):
        """Restore previous context state"""
        context["last_accessed"] = datetime.now().isoformat()
        
        # Restore working directory
        os.chdir(context["workspace_path"])
        
        # Restore environment variables
        self._load_environment(context["workspace_path"])
    
    def _load_environment(self, workspace_path: str):
        """Load environment variables from workspace"""
        env_file = f"{workspace_path}/.env"
        if os.path.exists(env_file):
            load_dotenv(env_file)
```

### 2.4 Load Balancing Algorithm

#### Task Assignment Algorithm
```python
class LoadBalancer:
    def __init__(self):
        self.role_states = {}
        self.task_queue = []
    
    def assign_task(self, task: dict) -> str:
        """Assign task to best available role"""
        available_roles = self._get_available_roles(task["required_skills"])
        
        if not available_roles:
            raise Exception("No available roles for task")
        
        # Score each role based on multiple factors
        role_scores = {}
        for role_id in available_roles:
            score = self._calculate_role_score(role_id, task)
            role_scores[role_id] = score
        
        # Select role with highest score
        best_role = max(role_scores, key=role_scores.get)
        
        # Assign task to role
        self._assign_task_to_role(best_role, task)
        
        return best_role
    
    def _get_available_roles(self, required_skills: list) -> list:
        """Get roles that have required skills and are available"""
        available_roles = []
        
        for role_id, state in self.role_states.items():
            if (state["status"] == "available" and 
                state["workload"] < state["max_workload"] and
                self._has_required_skills(role_id, required_skills)):
                available_roles.append(role_id)
        
        return available_roles
    
    def _calculate_role_score(self, role_id: str, task: dict) -> float:
        """Calculate score for role-task assignment"""
        state = self.role_states[role_id]
        
        # Base score from skill match
        skill_score = self._calculate_skill_match(role_id, task["required_skills"])
        
        # Workload factor (prefer less loaded roles)
        workload_factor = 1.0 - (state["workload"] / 100.0)
        
        # Performance factor
        performance_factor = state["performance_metrics"]["success_rate"]
        
        # Specialization bonus
        specialization_bonus = self._calculate_specialization_bonus(role_id, task)
        
        # Calculate final score
        score = (skill_score * 0.4 + 
                workload_factor * 0.3 + 
                performance_factor * 0.2 + 
                specialization_bonus * 0.1)
        
        return score
    
    def _calculate_skill_match(self, role_id: str, required_skills: list) -> float:
        """Calculate skill match percentage"""
        role_skills = self.role_states[role_id]["skills"]
        
        matched_skills = set(role_skills) & set(required_skills)
        total_required = len(required_skills)
        
        if total_required == 0:
            return 1.0
        
        return len(matched_skills) / total_required
    
    def _calculate_specialization_bonus(self, role_id: str, task: dict) -> float:
        """Calculate specialization bonus for task"""
        role_specializations = self.role_states[role_id]["specializations"]
        task_type = task.get("type", "")
        
        if task_type in role_specializations:
            return 0.2  # 20% bonus for specialization match
        
        return 0.0
    
    def _assign_task_to_role(self, role_id: str, task: dict):
        """Assign task to specific role"""
        # Update role state
        self.role_states[role_id]["status"] = "busy"
        self.role_states[role_id]["current_task"] = task["id"]
        self.role_states[role_id]["workload"] += task.get("estimated_effort", 10)
        
        # Add task to role's queue
        if "task_queue" not in self.role_states[role_id]:
            self.role_states[role_id]["task_queue"] = []
        
        self.role_states[role_id]["task_queue"].append(task)
```

### 2.5 Health Check and Monitoring

#### Role Health Monitoring
```python
class HealthMonitor:
    def __init__(self):
        self.health_checks = {}
        self.alert_thresholds = {
            "cpu_usage": 90,
            "memory_usage": 85,
            "disk_usage": 80,
            "response_time": 5000  # ms
        }
    
    def check_role_health(self, role_id: str) -> dict:
        """Perform comprehensive health check for role"""
        health_status = {
            "role_id": role_id,
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {}
        }
        
        # System resource checks
        health_status["checks"]["system"] = self._check_system_resources(role_id)
        
        # Application health checks
        health_status["checks"]["application"] = self._check_application_health(role_id)
        
        # AI tool availability checks
        health_status["checks"]["ai_tools"] = self._check_ai_tools(role_id)
        
        # Network connectivity checks
        health_status["checks"]["network"] = self._check_network_connectivity(role_id)
        
        # Determine overall status
        health_status["overall_status"] = self._determine_overall_status(health_status["checks"])
        
        return health_status
    
    def _check_system_resources(self, role_id: str) -> dict:
        """Check system resource usage"""
        try:
            # Get container stats
            container_stats = self._get_container_stats(role_id)
            
            checks = {
                "cpu_usage": {
                    "status": "healthy" if container_stats["cpu_percent"] < self.alert_thresholds["cpu_usage"] else "warning",
                    "value": container_stats["cpu_percent"],
                    "threshold": self.alert_thresholds["cpu_usage"]
                },
                "memory_usage": {
                    "status": "healthy" if container_stats["memory_percent"] < self.alert_thresholds["memory_usage"] else "warning",
                    "value": container_stats["memory_percent"],
                    "threshold": self.alert_thresholds["memory_usage"]
                },
                "disk_usage": {
                    "status": "healthy" if container_stats["disk_percent"] < self.alert_thresholds["disk_usage"] else "warning",
                    "value": container_stats["disk_percent"],
                    "threshold": self.alert_thresholds["disk_usage"]
                }
            }
            
            return checks
        except Exception as e:
            return {"error": str(e)}
    
    def _check_application_health(self, role_id: str) -> dict:
        """Check application health endpoints"""
        try:
            # Check role API endpoint
            response = requests.get(f"http://{role_id}:8000/health", timeout=5)
            
            checks = {
                "api_endpoint": {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": response.elapsed.total_seconds() * 1000,
                    "status_code": response.status_code
                }
            }
            
            return checks
        except Exception as e:
            return {"api_endpoint": {"status": "unhealthy", "error": str(e)}}
    
    def _check_ai_tools(self, role_id: str) -> dict:
        """Check AI tool availability"""
        role_config = self._get_role_config(role_id)
        ai_tools = role_config.get("ai_tools", [])
        
        checks = {}
        for tool in ai_tools:
            try:
                # Check if AI tool is available
                tool_status = self._check_ai_tool_status(tool)
                checks[tool] = {
                    "status": "healthy" if tool_status else "unhealthy",
                    "available": tool_status
                }
            except Exception as e:
                checks[tool] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        return checks
    
    def _check_network_connectivity(self, role_id: str) -> dict:
        """Check network connectivity"""
        checks = {}
        
        # Check GitHub connectivity
        try:
            response = requests.get("https://api.github.com", timeout=5)
            checks["github"] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            checks["github"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Check coordinator connectivity
        try:
            response = requests.get("http://coordinator:8000/health", timeout=5)
            checks["coordinator"] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            checks["coordinator"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        return checks
    
    def _determine_overall_status(self, checks: dict) -> str:
        """Determine overall health status"""
        all_checks = []
        
        # Flatten all check results
        for category, category_checks in checks.items():
            if isinstance(category_checks, dict):
                for check_name, check_result in category_checks.items():
                    if isinstance(check_result, dict) and "status" in check_result:
                        all_checks.append(check_result["status"])
        
        # Determine overall status
        if "unhealthy" in all_checks:
            return "unhealthy"
        elif "warning" in all_checks:
            return "warning"
        else:
            return "healthy"
```

### 2.6 Performance Monitoring

#### Performance Metrics Collection
```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.performance_history = {}
    
    def collect_metrics(self, role_id: str) -> dict:
        """Collect performance metrics for role"""
        metrics = {
            "role_id": role_id,
            "timestamp": datetime.now().isoformat(),
            "task_metrics": self._collect_task_metrics(role_id),
            "ai_tool_metrics": self._collect_ai_tool_metrics(role_id),
            "system_metrics": self._collect_system_metrics(role_id)
        }
        
        # Store metrics
        self.metrics[role_id] = metrics
        
        # Update performance history
        if role_id not in self.performance_history:
            self.performance_history[role_id] = []
        
        self.performance_history[role_id].append(metrics)
        
        # Keep only last 100 entries
        if len(self.performance_history[role_id]) > 100:
            self.performance_history[role_id] = self.performance_history[role_id][-100:]
        
        return metrics
    
    def _collect_task_metrics(self, role_id: str) -> dict:
        """Collect task-related performance metrics"""
        role_state = self._get_role_state(role_id)
        
        return {
            "tasks_completed": role_state.get("tasks_completed", 0),
            "tasks_failed": role_state.get("tasks_failed", 0),
            "average_completion_time": role_state.get("average_completion_time", "0h"),
            "success_rate": role_state.get("success_rate", 0.0),
            "current_workload": role_state.get("workload", 0),
            "queue_length": len(role_state.get("task_queue", []))
        }
    
    def _collect_ai_tool_metrics(self, role_id: str) -> dict:
        """Collect AI tool usage metrics"""
        role_config = self._get_role_config(role_id)
        ai_tools = role_config.get("ai_tools", [])
        
        tool_metrics = {}
        for tool in ai_tools:
            tool_metrics[tool] = {
                "usage_count": self._get_tool_usage_count(role_id, tool),
                "success_rate": self._get_tool_success_rate(role_id, tool),
                "average_response_time": self._get_tool_response_time(role_id, tool)
            }
        
        return tool_metrics
    
    def _collect_system_metrics(self, role_id: str) -> dict:
        """Collect system performance metrics"""
        try:
            container_stats = self._get_container_stats(role_id)
            
            return {
                "cpu_usage": container_stats.get("cpu_percent", 0),
                "memory_usage": container_stats.get("memory_percent", 0),
                "disk_usage": container_stats.get("disk_percent", 0),
                "network_io": container_stats.get("network_io", {}),
                "uptime": container_stats.get("uptime", 0)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_performance_report(self, role_id: str, time_range: str = "24h") -> dict:
        """Generate performance report for role"""
        if role_id not in self.performance_history:
            return {"error": "No performance data available"}
        
        history = self.performance_history[role_id]
        
        # Filter by time range
        cutoff_time = datetime.now() - timedelta(hours=24 if time_range == "24h" else 168)
        filtered_history = [
            entry for entry in history 
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
        ]
        
        if not filtered_history:
            return {"error": "No data in specified time range"}
        
        # Calculate aggregated metrics
        report = {
            "role_id": role_id,
            "time_range": time_range,
            "total_tasks": sum(entry["task_metrics"]["tasks_completed"] for entry in filtered_history),
            "average_success_rate": sum(entry["task_metrics"]["success_rate"] for entry in filtered_history) / len(filtered_history),
            "average_workload": sum(entry["task_metrics"]["current_workload"] for entry in filtered_history) / len(filtered_history),
            "system_performance": self._aggregate_system_metrics(filtered_history)
        }
        
        return report
    
    def _aggregate_system_metrics(self, history: list) -> dict:
        """Aggregate system metrics from history"""
        if not history:
            return {}
        
        cpu_usage = [entry["system_metrics"].get("cpu_usage", 0) for entry in history]
        memory_usage = [entry["system_metrics"].get("memory_usage", 0) for entry in history]
        
        return {
            "average_cpu_usage": sum(cpu_usage) / len(cpu_usage),
            "max_cpu_usage": max(cpu_usage),
            "average_memory_usage": sum(memory_usage) / len(memory_usage),
            "max_memory_usage": max(memory_usage)
        }
```

### 2.7 Dynamic Scaling

#### Auto-scaling Algorithm
```python
class AutoScaler:
    def __init__(self):
        self.scaling_rules = {
            "cpu_threshold": 80,
            "memory_threshold": 85,
            "queue_length_threshold": 10,
            "response_time_threshold": 5000
        }
        self.scaling_cooldown = 300  # 5 minutes
    
    def evaluate_scaling_needs(self) -> dict:
        """Evaluate if scaling is needed"""
        scaling_decisions = {
            "scale_up": [],
            "scale_down": [],
            "reasons": []
        }
        
        # Check each role type
        role_types = ["product_manager", "backend_developer", "frontend_developer", "qa_engineer", "devops_engineer"]
        
        for role_type in role_types:
            decision = self._evaluate_role_type_scaling(role_type)
            
            if decision["action"] == "scale_up":
                scaling_decisions["scale_up"].append({
                    "role_type": role_type,
                    "count": decision["count"],
                    "reason": decision["reason"]
                })
            elif decision["action"] == "scale_down":
                scaling_decisions["scale_down"].append({
                    "role_type": role_type,
                    "count": decision["count"],
                    "reason": decision["reason"]
                })
            
            scaling_decisions["reasons"].extend(decision["reasons"])
        
        return scaling_decisions
    
    def _evaluate_role_type_scaling(self, role_type: str) -> dict:
        """Evaluate scaling needs for specific role type"""
        roles = self._get_roles_by_type(role_type)
        
        if not roles:
            return {"action": "none", "count": 0, "reason": "No roles found", "reasons": []}
        
        reasons = []
        scale_up_factors = 0
        scale_down_factors = 0
        
        # Check average workload
        avg_workload = sum(role["workload"] for role in roles) / len(roles)
        if avg_workload > 90:
            scale_up_factors += 1
            reasons.append(f"High average workload: {avg_workload:.1f}%")
        elif avg_workload < 30:
            scale_down_factors += 1
            reasons.append(f"Low average workload: {avg_workload:.1f}%")
        
        # Check queue length
        total_queue_length = sum(len(role.get("task_queue", [])) for role in roles)
        if total_queue_length > self.scaling_rules["queue_length_threshold"]:
            scale_up_factors += 1
            reasons.append(f"Long task queue: {total_queue_length} tasks")
        
        # Check response time
        avg_response_time = self._get_average_response_time(roles)
        if avg_response_time > self.scaling_rules["response_time_threshold"]:
            scale_up_factors += 1
            reasons.append(f"Slow response time: {avg_response_time}ms")
        
        # Determine action
        if scale_up_factors >= 2:
            return {
                "action": "scale_up",
                "count": 1,
                "reason": "Multiple scaling factors triggered",
                "reasons": reasons
            }
        elif scale_down_factors >= 2 and len(roles) > 1:
            return {
                "action": "scale_down",
                "count": 1,
                "reason": "Low utilization detected",
                "reasons": reasons
            }
        else:
            return {
                "action": "none",
                "count": 0,
                "reason": "No scaling needed",
                "reasons": reasons
            }
    
    def execute_scaling(self, scaling_decisions: dict):
        """Execute scaling decisions"""
        results = {
            "scaled_up": [],
            "scaled_down": [],
            "errors": []
        }
        
        # Execute scale up
        for decision in scaling_decisions["scale_up"]:
            try:
                new_role = self._create_new_role(decision["role_type"])
                results["scaled_up"].append({
                    "role_type": decision["role_type"],
                    "role_id": new_role["id"],
                    "reason": decision["reason"]
                })
            except Exception as e:
                results["errors"].append({
                    "action": "scale_up",
                    "role_type": decision["role_type"],
                    "error": str(e)
                })
        
        # Execute scale down
        for decision in scaling_decisions["scale_down"]:
            try:
                removed_role = self._remove_role(decision["role_type"])
                results["scaled_down"].append({
                    "role_type": decision["role_type"],
                    "role_id": removed_role["id"],
                    "reason": decision["reason"]
                })
            except Exception as e:
                results["errors"].append({
                    "action": "scale_down",
                    "role_type": decision["role_type"],
                    "error": str(e)
                })
        
        return results
    
    def _create_new_role(self, role_type: str) -> dict:
        """Create new role instance"""
        # Generate unique role ID
        role_id = f"{role_type}-{int(time.time())}"
        
        # Create role configuration
        role_config = self._get_role_type_config(role_type)
        role_config["id"] = role_id
        role_config["created_at"] = datetime.now().isoformat()
        
        # Deploy role container
        container_id = self._deploy_role_container(role_config)
        
        # Update role registry
        self._register_role(role_config)
        
        return {
            "id": role_id,
            "type": role_type,
            "container_id": container_id,
            "status": "starting"
        }
    
    def _remove_role(self, role_type: str) -> dict:
        """Remove role instance"""
        # Find least loaded role of this type
        roles = self._get_roles_by_type(role_type)
        if not roles:
            raise Exception(f"No roles found for type: {role_type}")
        
        # Select role with lowest workload
        target_role = min(roles, key=lambda r: r["workload"])
        
        # Stop and remove container
        self._stop_role_container(target_role["id"])
        
        # Unregister role
        self._unregister_role(target_role["id"])
        
        return target_role
``` 