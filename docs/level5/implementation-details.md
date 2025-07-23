# Level 5: Implementation Details

## Business Aspect: Specific Operation Steps

### 5.1 Project Startup Process

#### Environment Preparation
1. **System Requirements Check**
   ```bash
   # Check Docker version
   docker --version
   # Check Docker Compose version
   docker-compose --version
   # Check available memory
   free -h
   # Check disk space
   df -h
   ```

2. **Network Configuration**
   ```bash
   # Check network connectivity
   ping github.com
   # Check DNS resolution
   nslookup api.github.com
   # Check firewall settings
   sudo ufw status
   ```

3. **Permission Settings**
   ```bash
   # Create project directory
   mkdir -p /opt/bee-swarm
   cd /opt/bee-swarm
   
   # Set directory permissions
   sudo chown -R $USER:$USER /opt/bee-swarm
   chmod 755 /opt/bee-swarm
   ```

#### Configuration File Setup
1. **Environment Variable Configuration**
   ```bash
   # Copy environment variable template
   cp .env.example .env
   
   # Edit environment variables
   nano .env
   ```

   ```env
   # GitHub Configuration
   GITHUB_TOKEN_PM=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_BACKEND=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_FRONTEND=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_QA=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_DEVOPS=ghp_xxxxxxxxxxxxxxxxxxxx
   
   # AI Tool Configuration
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
   GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
   
   # Container Configuration
   VNC_PASSWORD_PM=vnc123
   VNC_PASSWORD_BACKEND=vnc123
   VNC_PASSWORD_FRONTEND=vnc123
   VNC_PASSWORD_QA=vnc123
   VNC_PASSWORD_DEVOPS=vnc123
   
   # Cloudflare Configuration
   CLOUDFLARE_TUNNEL_URL=https://your-tunnel-url.trycloudflare.com
   
   # Database Configuration
   REDIS_URL=redis://localhost:6379
   POSTGRES_URL=postgresql://user:password@localhost:5432/beeswarm
   ```

2. **GitHub Webhook Configuration**
   ```bash
   # Add webhook in GitHub repository settings
   # URL: https://your-domain.com/webhook
   # Content type: application/json
   # Secret: your-webhook-secret
   # Events: Issues, Pull requests, Push
   ```

#### Container Build and Startup
1. **Build Base Images**
   ```bash
   # Build VNC base image
   cd novnc_base
   docker build -t vnc-base .
   
   # Build AI tools image
   cd ../novnc_llm_cli
   docker build -t vnc-llm-cli .
   ```

2. **Build Role Images**
   ```bash
   # Build Product Manager image
   cd ../roles/product_manager
   docker build -t bee-swarm-pm .
   
   # Build Backend Developer image
   cd ../backend_developer
   docker build -t bee-swarm-backend .
   
   # Build Frontend Developer image
   cd ../frontend_developer
   docker build -t bee-swarm-frontend .
   
   # Build QA Engineer image
   cd ../qa_engineer
   docker build -t bee-swarm-qa .
   
   # Build DevOps Engineer image
   cd ../devops_engineer
   docker build -t bee-swarm-devops .
   ```

3. **Start Containers**
   ```bash
   # Start all containers
   docker-compose up -d
   
   # Check container status
   docker-compose ps
   
   # View container logs
   docker-compose logs -f
   ```

### 5.2 Role Container Implementation

#### Product Manager Container
```dockerfile
# roles/product_manager/Dockerfile
FROM vnc-llm-cli:latest

# Install product management tools
RUN apt-get update && apt-get install -y \
    pandoc \
    inkscape \
    graphviz \
    plantuml \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install \
    jira \
    notion-client \
    figma-api \
    miro-api \
    lucidchart-api

# Set up product management workspace
WORKDIR /workspace
RUN mkdir -p /workspace/projects /workspace/templates /workspace/docs

# Copy product management scripts
COPY scripts/ /opt/scripts/
RUN chmod +x /opt/scripts/*.py

# Set environment variables
ENV ROLE_TYPE=product_manager
ENV ROLE_ID=pm-01

# Start product management service
CMD ["python", "/opt/scripts/pm_service.py"]
```

#### Backend Developer Container
```dockerfile
# roles/backend_developer/Dockerfile
FROM vnc-llm-cli:latest

# Install development tools
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    python3-pip \
    python3-venv \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install \
    fastapi \
    uvicorn \
    sqlalchemy \
    alembic \
    pytest \
    black \
    flake8 \
    mypy

# Install Node.js packages
RUN npm install -g \
    typescript \
    ts-node \
    nodemon \
    jest \
    eslint

# Set up development workspace
WORKDIR /workspace
RUN mkdir -p /workspace/backend /workspace/api /workspace/tests

# Copy backend development scripts
COPY scripts/ /opt/scripts/
RUN chmod +x /opt/scripts/*.py

# Set environment variables
ENV ROLE_TYPE=backend_developer
ENV ROLE_ID=backend-01

# Start backend development service
CMD ["python", "/opt/scripts/backend_service.py"]
```

#### Frontend Developer Container
```dockerfile
# roles/frontend_developer/Dockerfile
FROM vnc-llm-cli:latest

# Install frontend development tools
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    yarn \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js packages
RUN npm install -g \
    create-react-app \
    create-vue-app \
    @angular/cli \
    svelte-cli \
    typescript \
    ts-node \
    nodemon \
    jest \
    cypress \
    eslint \
    prettier

# Set up frontend workspace
WORKDIR /workspace
RUN mkdir -p /workspace/frontend /workspace/components /workspace/assets

# Copy frontend development scripts
COPY scripts/ /opt/scripts/
RUN chmod +x /opt/scripts/*.py

# Set environment variables
ENV ROLE_TYPE=frontend_developer
ENV ROLE_ID=frontend-01

# Start frontend development service
CMD ["python", "/opt/scripts/frontend_service.py"]
```

### 5.3 System Coordinator Implementation

#### FastAPI Application
```python
# coordinator/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bee Swarm Coordinator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Task(BaseModel):
    id: str
    title: str
    description: str
    role_id: str
    priority: str
    status: str
    created_at: datetime
    deadline: Optional[datetime] = None

class Role(BaseModel):
    id: str
    type: str
    status: str
    workload: int
    current_task: Optional[str] = None
    last_activity: datetime

# In-memory storage (replace with database in production)
tasks: Dict[str, Task] = {}
roles: Dict[str, Role] = {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Bee Swarm Coordinator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "tasks_count": len(tasks),
        "roles_count": len(roles)
    }

@app.get("/tasks")
async def get_tasks(status: Optional[str] = None, role_id: Optional[str] = None):
    """Get all tasks with optional filtering"""
    filtered_tasks = list(tasks.values())
    
    if status:
        filtered_tasks = [t for t in filtered_tasks if t.status == status]
    
    if role_id:
        filtered_tasks = [t for t in filtered_tasks if t.role_id == role_id]
    
    return filtered_tasks

@app.post("/tasks")
async def create_task(task: Task, background_tasks: BackgroundTasks):
    """Create new task"""
    try:
        tasks[task.id] = task
        
        # Notify assigned role
        background_tasks.add_task(notify_role, task.role_id, {
            "type": "task_assigned",
            "task": task.dict()
        })
        
        logger.info(f"Created task {task.id} assigned to {task.role_id}")
        return {"success": True, "task_id": task.id}
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task_update: Dict[str, Any]):
    """Update task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        task = tasks[task_id]
        for key, value in task_update.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        tasks[task_id] = task
        logger.info(f"Updated task {task_id}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roles")
async def get_roles():
    """Get all roles"""
    return list(roles.values())

@app.get("/roles/{role_id}")
async def get_role(role_id: str):
    """Get specific role"""
    if role_id not in roles:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return roles[role_id]

@app.post("/roles")
async def create_role(role: Role):
    """Create new role"""
    try:
        roles[role.id] = role
        logger.info(f"Created role {role.id}")
        return {"success": True, "role_id": role.id}
    except Exception as e:
        logger.error(f"Error creating role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/roles/{role_id}")
async def update_role(role_id: str, role_update: Dict[str, Any]):
    """Update role"""
    if role_id not in roles:
        raise HTTPException(status_code=404, detail="Role not found")
    
    try:
        role = roles[role_id]
        for key, value in role_update.items():
            if hasattr(role, key):
                setattr(role, key, value)
        
        roles[role_id] = role
        logger.info(f"Updated role {role_id}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error updating role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notify")
async def notify_role(role_id: str, message: Dict[str, Any]):
    """Send notification to role"""
    try:
        # Send notification via message queue or HTTP
        logger.info(f"Notifying role {role_id}: {message}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error notifying role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def notify_role(role_id: str, message: Dict[str, Any]):
    """Background task to notify role"""
    try:
        # Implementation would send message to role container
        logger.info(f"Background notification to {role_id}: {message}")
    except Exception as e:
        logger.error(f"Background notification error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Celery Task Queue
```python
# coordinator/celery_app.py
from celery import Celery
from celery.schedules import crontab
import os

# Create Celery app
celery_app = Celery(
    "bee_swarm",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    include=["coordinator.tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periodic tasks
celery_app.conf.beat_schedule = {
    "sync-github-status": {
        "task": "coordinator.tasks.sync_github_status",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
    "health-check": {
        "task": "coordinator.tasks.health_check",
        "schedule": crontab(minute="*/2"),  # Every 2 minutes
    },
    "load-balance": {
        "task": "coordinator.tasks.load_balance",
        "schedule": crontab(minute="*/10"),  # Every 10 minutes
    },
}

# coordinator/tasks.py
from celery_app import celery_app
import requests
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

@celery_app.task
def sync_github_status():
    """Sync GitHub status with local state"""
    try:
        # Get GitHub issues
        github_issues = get_github_issues()
        
        # Update local task status
        for issue in github_issues:
            update_task_status(issue)
        
        logger.info("GitHub status sync completed")
        return {"success": True, "issues_synced": len(github_issues)}
    except Exception as e:
        logger.error(f"GitHub sync error: {e}")
        return {"success": False, "error": str(e)}

@celery_app.task
def health_check():
    """Check health of all role containers"""
    try:
        role_status = {}
        
        # Check each role container
        for role_id in ["pm-01", "backend-01", "frontend-01", "qa-01", "devops-01"]:
            status = check_role_health(role_id)
            role_status[role_id] = status
        
        # Log health status
        logger.info(f"Health check completed: {role_status}")
        
        return {"success": True, "role_status": role_status}
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"success": False, "error": str(e)}

@celery_app.task
def load_balance():
    """Perform load balancing across roles"""
    try:
        # Get current workload
        workload = get_role_workload()
        
        # Calculate optimal distribution
        optimal_distribution = calculate_optimal_distribution(workload)
        
        # Reassign tasks if needed
        reassignments = reassign_tasks(optimal_distribution)
        
        logger.info(f"Load balancing completed: {reassignments} reassignments")
        return {"success": True, "reassignments": reassignments}
    except Exception as e:
        logger.error(f"Load balancing error: {e}")
        return {"success": False, "error": str(e)}

@celery_app.task
def assign_task_to_role(task_id: str, role_id: str):
    """Assign specific task to role"""
    try:
        # Get task details
        task = get_task(task_id)
        
        # Assign to role
        result = assign_task(task, role_id)
        
        # Notify role
        notify_role(role_id, {
            "type": "task_assigned",
            "task": task
        })
        
        logger.info(f"Task {task_id} assigned to {role_id}")
        return {"success": True, "task_id": task_id, "role_id": role_id}
    except Exception as e:
        logger.error(f"Task assignment error: {e}")
        return {"success": False, "error": str(e)}

def get_github_issues() -> List[Dict[str, Any]]:
    """Get issues from GitHub API"""
    # Implementation would call GitHub API
    return []

def update_task_status(issue: Dict[str, Any]):
    """Update local task status based on GitHub issue"""
    # Implementation would update local task database
    pass

def check_role_health(role_id: str) -> Dict[str, Any]:
    """Check health of specific role container"""
    try:
        response = requests.get(f"http://{role_id}:8000/health", timeout=5)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds()
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

def get_role_workload() -> Dict[str, int]:
    """Get current workload for each role"""
    # Implementation would query role status
    return {}

def calculate_optimal_distribution(workload: Dict[str, int]) -> Dict[str, List[str]]:
    """Calculate optimal task distribution"""
    # Implementation would use load balancing algorithm
    return {}

def reassign_tasks(distribution: Dict[str, List[str]]) -> int:
    """Reassign tasks based on optimal distribution"""
    # Implementation would reassign tasks
    return 0

def get_task(task_id: str) -> Dict[str, Any]:
    """Get task details"""
    # Implementation would query task database
    return {}

def assign_task(task: Dict[str, Any], role_id: str) -> bool:
    """Assign task to role"""
    # Implementation would update task assignment
    return True

def notify_role(role_id: str, message: Dict[str, Any]):
    """Notify role about task assignment"""
    # Implementation would send notification
    pass
```

### 5.4 Database Schema

#### PostgreSQL Schema
```sql
-- Database schema for Bee Swarm system

-- Create database
CREATE DATABASE beeswarm;
\c beeswarm;

-- Roles table
CREATE TABLE roles (
    id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available',
    workload INTEGER NOT NULL DEFAULT 0,
    current_task_id VARCHAR(50),
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    role_id VARCHAR(50) REFERENCES roles(id),
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    issue_number INTEGER,
    pr_number INTEGER,
    estimated_hours DECIMAL(5,2),
    actual_hours DECIMAL(5,2),
    progress_percentage INTEGER DEFAULT 0,
    labels TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    sender_id VARCHAR(50) REFERENCES roles(id),
    recipient_id VARCHAR(50) REFERENCES roles(id),
    content JSONB NOT NULL,
    priority INTEGER DEFAULT 3,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    read_at TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    github_repo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project tasks relationship
CREATE TABLE project_tasks (
    project_id VARCHAR(50) REFERENCES projects(id),
    task_id VARCHAR(50) REFERENCES tasks(id),
    PRIMARY KEY (project_id, task_id)
);

-- Performance metrics table
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    role_id VARCHAR(50) REFERENCES roles(id),
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_roles_type ON roles(type);
CREATE INDEX idx_roles_status ON roles(status);
CREATE INDEX idx_tasks_role_id ON tasks(role_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_performance_metrics_role_id ON performance_metrics(role_id);
CREATE INDEX idx_performance_metrics_recorded_at ON performance_metrics(recorded_at);

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_roles_updated_at BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### SQLAlchemy Models
```python
# coordinator/models.py
from sqlalchemy import Column, String, Integer, Text, DateTime, DECIMAL, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(String(50), primary_key=True)
    type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="available")
    workload = Column(Integer, nullable=False, default=0)
    current_task_id = Column(String(50))
    last_activity = Column(DateTime, default=func.current_timestamp())
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    role_id = Column(String(50))
    priority = Column(String(20), nullable=False, default="medium")
    status = Column(String(20), nullable=False, default="open")
    issue_number = Column(Integer)
    pr_number = Column(Integer)
    estimated_hours = Column(DECIMAL(5, 2))
    actual_hours = Column(DECIMAL(5, 2))
    progress_percentage = Column(Integer, default=0)
    labels = Column(ARRAY(String))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deadline = Column(DateTime)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    sender_id = Column(String(50))
    recipient_id = Column(String(50))
    content = Column(JSON, nullable=False)
    priority = Column(Integer, default=3)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=func.current_timestamp())
    sent_at = Column(DateTime)
    read_at = Column(DateTime)

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="active")
    github_repo = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(String(50))
    metric_type = Column(String(50), nullable=False)
    metric_value = Column(DECIMAL(10, 2), nullable=False)
    recorded_at = Column(DateTime, default=func.current_timestamp())
```

### 5.5 Monitoring and Logging

#### Prometheus Metrics
```python
# coordinator/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Summary
import time

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Task metrics
TASK_CREATED = Counter(
    'tasks_created_total',
    'Total tasks created',
    ['priority', 'role_type']
)

TASK_COMPLETED = Counter(
    'tasks_completed_total',
    'Total tasks completed',
    ['role_type', 'status']
)

TASK_DURATION = Histogram(
    'task_duration_hours',
    'Task completion duration',
    ['role_type', 'priority']
)

# Role metrics
ROLE_WORKLOAD = Gauge(
    'role_workload_percentage',
    'Current workload percentage',
    ['role_id', 'role_type']
)

ROLE_STATUS = Gauge(
    'role_status',
    'Role status (0=offline, 1=available, 2=busy)',
    ['role_id', 'role_type']
)

# System metrics
ACTIVE_TASKS = Gauge(
    'active_tasks_total',
    'Total active tasks',
    ['status']
)

SYSTEM_HEALTH = Gauge(
    'system_health',
    'System health status (0=unhealthy, 1=healthy)',
    ['component']
)

# Performance metrics
AI_TOOL_USAGE = Counter(
    'ai_tool_usage_total',
    'AI tool usage count',
    ['tool_name', 'role_type']
)

AI_TOOL_RESPONSE_TIME = Histogram(
    'ai_tool_response_time_seconds',
    'AI tool response time',
    ['tool_name']
)

# Middleware for request metrics
class PrometheusMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            method = scope["method"]
            path = scope["path"]
            
            start_time = time.time()
            
            # Track request
            REQUEST_COUNT.labels(method=method, endpoint=path, status="pending").inc()
            
            try:
                await self.app(scope, receive, send)
                
                # Record success
                REQUEST_COUNT.labels(method=method, endpoint=path, status="success").inc()
                
            except Exception as e:
                # Record error
                REQUEST_COUNT.labels(method=method, endpoint=path, status="error").inc()
                raise
            finally:
                # Record duration
                duration = time.time() - start_time
                REQUEST_DURATION.labels(method=method, endpoint=path).observe(duration)
        else:
            await self.app(scope, receive, send)
```

#### Logging Configuration
```python
# coordinator/logging_config.py
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                "logs/coordinator.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            
            # Error file handler
            logging.handlers.RotatingFileHandler(
                "logs/coordinator_error.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                level=logging.ERROR
            )
        ]
    )
    
    # Configure specific loggers
    loggers = {
        "coordinator": logging.getLogger("coordinator"),
        "coordinator.tasks": logging.getLogger("coordinator.tasks"),
        "coordinator.api": logging.getLogger("coordinator.api"),
        "coordinator.github": logging.getLogger("coordinator.github"),
    }
    
    for logger_name, logger_obj in loggers.items():
        logger_obj.setLevel(logging.INFO)
    
    return loggers

# Custom formatter for structured logging
class StructuredFormatter(logging.Formatter):
    def format(self, record):
        # Add structured fields
        record.timestamp = datetime.utcnow().isoformat()
        record.service = "bee-swarm-coordinator"
        
        # Format as JSON-like structure
        return (
            f'{{"timestamp": "{record.timestamp}", '
            f'"level": "{record.levelname}", '
            f'"service": "{record.service}", '
            f'"logger": "{record.name}", '
            f'"message": "{record.getMessage()}"}}'
        )

# Setup structured logging
def setup_structured_logging():
    """Setup structured logging for production"""
    
    # Create structured formatter
    formatter = StructuredFormatter()
    
    # Configure handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    file_handler = logging.handlers.RotatingFileHandler(
        "logs/coordinator_structured.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
```

### 5.6 Deployment Scripts

#### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  # System Coordinator
  coordinator:
    build: ./coordinator
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
      - POSTGRES_URL=postgresql://user:password@postgres:5432/beeswarm
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    depends_on:
      - redis
      - postgres
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # Product Manager
  pm-01:
    build: ./roles/product_manager
    environment:
      - ROLE_ID=pm-01
      - GITHUB_TOKEN=${GITHUB_TOKEN_PM}
      - VNC_PASSWORD=${VNC_PASSWORD_PM}
    ports:
      - "6080:6080"  # VNC
      - "7680:7680"  # Terminal
    volumes:
      - pm-workspace:/workspace
    restart: unless-stopped

  # Backend Developer
  backend-01:
    build: ./roles/backend_developer
    environment:
      - ROLE_ID=backend-01
      - GITHUB_TOKEN=${GITHUB_TOKEN_BACKEND}
      - VNC_PASSWORD=${VNC_PASSWORD_BACKEND}
    ports:
      - "6081:6080"  # VNC
      - "7681:7680"  # Terminal
    volumes:
      - backend-workspace:/workspace
    restart: unless-stopped

  # Frontend Developer
  frontend-01:
    build: ./roles/frontend_developer
    environment:
      - ROLE_ID=frontend-01
      - GITHUB_TOKEN=${GITHUB_TOKEN_FRONTEND}
      - VNC_PASSWORD=${VNC_PASSWORD_FRONTEND}
    ports:
      - "6082:6080"  # VNC
      - "7682:7680"  # Terminal
    volumes:
      - frontend-workspace:/workspace
    restart: unless-stopped

  # QA Engineer
  qa-01:
    build: ./roles/qa_engineer
    environment:
      - ROLE_ID=qa-01
      - GITHUB_TOKEN=${GITHUB_TOKEN_QA}
      - VNC_PASSWORD=${VNC_PASSWORD_QA}
    ports:
      - "6083:6080"  # VNC
      - "7683:7680"  # Terminal
    volumes:
      - qa-workspace:/workspace
    restart: unless-stopped

  # DevOps Engineer
  devops-01:
    build: ./roles/devops_engineer
    environment:
      - ROLE_ID=devops-01
      - GITHUB_TOKEN=${GITHUB_TOKEN_DEVOPS}
      - VNC_PASSWORD=${VNC_PASSWORD_DEVOPS}
    ports:
      - "6084:6080"  # VNC
      - "7684:7680"  # Terminal
    volumes:
      - devops-workspace:/workspace
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=beeswarm
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    restart: unless-stopped

  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    restart: unless-stopped

volumes:
  pm-workspace:
  backend-workspace:
  frontend-workspace:
  qa-workspace:
  devops-workspace:
  redis-data:
  postgres-data:
  prometheus-data:
  grafana-data:
```

#### Deployment Script
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "Starting Bee Swarm deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env and configure it"
    exit 1
fi

# Load environment variables
source .env

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p data/prometheus
mkdir -p data/grafana

# Build base images
echo "Building base images..."
docker build -t vnc-base ./novnc_base
docker build -t vnc-llm-cli ./novnc_llm_cli

# Build role images
echo "Building role images..."
docker build -t bee-swarm-pm ./roles/product_manager
docker build -t bee-swarm-backend ./roles/backend_developer
docker build -t bee-swarm-frontend ./roles/frontend_developer
docker build -t bee-swarm-qa ./roles/qa_engineer
docker build -t bee-swarm-devops ./roles/devops_engineer

# Build coordinator
echo "Building coordinator..."
docker build -t bee-swarm-coordinator ./coordinator

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Check service health
echo "Checking service health..."
docker-compose ps

# Initialize database
echo "Initializing database..."
docker-compose exec coordinator python -c "
from coordinator.database import init_db
init_db()
"

# Run migrations
echo "Running database migrations..."
docker-compose exec coordinator alembic upgrade head

# Start Celery workers
echo "Starting Celery workers..."
docker-compose exec -d coordinator celery -A coordinator.celery_app worker --loglevel=info

# Start Celery beat
echo "Starting Celery beat..."
docker-compose exec -d coordinator celery -A coordinator.celery_app beat --loglevel=info

echo "Deployment completed successfully!"
echo ""
echo "Access URLs:"
echo "  Coordinator API: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/docs"
echo "  Product Manager VNC: http://localhost:6080"
echo "  Backend Developer VNC: http://localhost:6081"
echo "  Frontend Developer VNC: http://localhost:6082"
echo "  QA Engineer VNC: http://localhost:6083"
echo "  DevOps Engineer VNC: http://localhost:6084"
echo "  Prometheus: http://localhost:9090"
echo "  Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
```

This implementation details document provides comprehensive technical specifications for deploying and operating the Bee Swarm AI development team system. 