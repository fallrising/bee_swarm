# Level 1: System Overview

## Business Aspect: Overall Project Operation Mode

### 1.1 Project Lifecycle

#### Requirements Phase
1. **Requirements Reception**: Human users create Issues on GitHub to describe requirements
2. **Requirements Analysis**: Product Manager role analyzes feasibility and technical complexity of requirements
3. **Task Breakdown**: Break down large requirements into specific development tasks
4. **Priority Sorting**: Sort by business value and urgency
5. **Task Assignment**: System coordinator intelligently assigns to appropriate roles

#### Development Phase
1. **Task Reception**: Roles receive assigned tasks from GitHub
2. **Context Switching**: Roles switch to corresponding project workspace
3. **AI Tool Execution**: Use pre-installed AI tools for development
4. **Code Generation**: AI tools generate code based on requirements
5. **PR Creation**: Create Pull Requests for code review

#### Testing Phase
1. **Automated Testing**: QA Engineer executes automated tests
2. **Issue Discovery**: Discover and record code issues
3. **Issue Feedback**: Provide feedback through GitHub Comments
4. **Issue Resolution**: Developers fix issues based on feedback
5. **Regression Testing**: Verify functionality after fixes

#### Deployment Phase
1. **Code Merge**: Merge to main branch after code review
2. **Automated Deployment**: DevOps Engineer triggers automated deployment process
3. **Environment Monitoring**: Monitor production environment status
4. **Issue Handling**: Handle issues in production environment
5. **Performance Optimization**: Optimize based on runtime data

### 1.2 Role Collaboration Mode

#### Role Pool Management
```
Role Pool:
├── Product Manager × 2 (PM-01, PM-02)
├── Backend Developer × 3 (Backend-01, Backend-02, Backend-03)
├── Frontend Developer × 2 (Frontend-01, Frontend-02)
├── QA Engineer × 2 (QA-01, QA-02)
└── DevOps Engineer × 1 (DevOps-01)
```

#### Task Assignment Process
```
GitHub Issue → System Coordinator → Task Analysis → Role Matching → Task Assignment
     ↓              ↓           ↓         ↓         ↓
Requirement Description → Skill Matching → Load Check → Role Selection → Status Update
```

#### Asynchronous Collaboration Process
```
Role A → GitHub Comments → Role B
  ↓           ↓           ↓
Execute Task → Status Update → Receive Notification
  ↓           ↓           ↓
Complete Task → Create PR → Code Review
```

### 1.3 Communication Mechanism

#### GitHub-Driven Communication
- **Issues**: Task management and status tracking
- **Comments**: Inter-role discussions and issue feedback
- **Labels**: Task categorization, priorities, and skill requirements
- **Projects**: Project kanban and role load management
- **Pull Requests**: Code review and discussions
- **Mentions**: Inter-role notifications and collaboration

#### Status Synchronization Mechanism
- **Periodic Scanning**: Scan GitHub status every 30 seconds
- **Event Triggering**: Update immediately when important events occur
- **Load Balancing**: Dynamically assign tasks based on role load
- **Progress Tracking**: Real-time task progress updates

#### Issue Feedback Process
1. **Issue Discovery**: QA or developers discover issues
2. **Issue Recording**: Create Issues or Comments on GitHub
3. **Issue Assignment**: System automatically assigns to appropriate handlers
4. **Issue Resolution**: Relevant personnel resolve issues
5. **Issue Verification**: Verify if issues are resolved

## Technical Aspect: System Architecture Overview

### 1.1 Overall Architecture

#### System Hierarchy
```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Platform                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Issues    │ │  Projects   │ │  Comments   │ │   Labels    │ │
│  │  (Tasks)    │ │  (Kanban)   │ │ (Communication)│ │ (Categories) │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 System Coordinator (Coordinator)                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ Task Scheduler│ │ State Manager│ │ GitHub Sync│ │ Communication│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Role Pool (Role Pool)                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ PM-01       │ │ Backend-01  │ │ Frontend-01 │ │ QA-01       │ │
│  │ PM-02       │ │ Backend-02  │ │ Frontend-02 │ │ QA-02       │ │
│  │             │ │ Backend-03  │ │             │ │             │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│  ┌─────────────┐                                                 │
│  │ DevOps-01   │                                                 │
│  └─────────────┘                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Network Architecture
```
Internet
    │
    ▼
┌─────────────────┐
│   Docker Host   │
└─────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│                Docker Network                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │Coordinator│ │ PM-01  │ │Backend-01│ │Frontend-01│ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │ PM-02   │ │Backend-02│ │Frontend-02│ │ QA-01   │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │Backend-03│ │ QA-02   │ │DevOps-01│ │ Redis   │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

#### System Coordinator
- **FastAPI**: Web framework and API services
- **Celery**: Asynchronous task processing
- **Redis**: Message queue and caching
- **PostgreSQL**: State database
- **PyGithub**: GitHub API integration

#### Role Containers
- **Docker**: Container runtime
- **VNC Lab**: noVNC-based desktop environment
- **Supervisor**: Process management
- **Python**: Role logic implementation

#### AI Tool Integration
- **Gemini CLI**: Google's AI programming assistant
- **Claude Code**: Anthropic's code generation tool
- **Rovo Dev**: AI-driven development tool
- **Warp**: AI terminal
- **Cursor**: AI code editor

#### Monitoring and Logging
- **Prometheus**: Metrics collection
- **Grafana**: Data visualization
- **Loguru**: Log management

### 1.3 Deployment Strategy

#### Development Environment
- **Local Deployment**: Use Docker Compose
- **Single Machine**: All services run on the same machine
- **Rapid Iteration**: Easy for development and testing

#### Testing Environment
- **Container Cluster**: Use Docker Swarm or Kubernetes
- **Load Balancing**: Test high availability
- **Performance Testing**: Verify system performance

#### Production Environment
- **Container Orchestration**: Use Kubernetes
- **Auto Scaling**: Automatically adjust based on load
- **Multi-Region Deployment**: Improve availability

#### Deployment Process
1. **Code Build**: Docker image building
2. **Image Push**: Push to image registry
3. **Service Update**: Rolling service updates
4. **Health Check**: Verify service status
5. **Traffic Switch**: Switch to new version

### 1.4 Security Strategy

#### Network Security
- **Container Isolation**: Each role runs in independent container
- **Network Policies**: Limit inter-container communication
- **Port Management**: Only open necessary ports

#### Container Security
- **Image Scanning**: Scan for security vulnerabilities
- **Minimal Permissions**: Containers run with minimal privileges
- **Resource Limits**: Limit container resource usage

#### Data Security
- **Data Encryption**: Encrypt data in transit and at rest
- **Backup Strategy**: Regular data backups
- **Access Control**: Role-based access control

### 1.5 Performance Optimization

#### Resource Optimization
- **CPU Allocation**: Allocate CPU based on role requirements
- **Memory Management**: Reasonably allocate memory resources
- **Storage Optimization**: Use shared workspace

#### Network Optimization
- **Connection Pooling**: Reuse database connections
- **Caching Strategy**: Multi-level caching
- **Asynchronous Processing**: Reduce blocking operations

#### Application Optimization
- **Code Optimization**: Optimize AI-generated code
- **Database Optimization**: Query and index optimization
- **Cache Optimization**: Application-level caching 