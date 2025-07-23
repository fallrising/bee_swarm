# 🐝 **Bee Swarm - AI Automated Development Team System**

## 📋 **Project Overview**

Bee Swarm is an AI development team collaboration system based on **single VPS single role** architecture, using **GitHub as the central data source** to achieve completely asynchronous AI-driven software development workflow. Each VPS runs a dedicated AI role container, built on the [VNC Lab](https://github.com/fallrising/vnc_lab) project.

### 🎯 **Core Concepts**
- **Single VPS Single Role**: Each VPS runs only one AI role container, ensuring resource isolation and stability
- **Based on VNC Lab**: Uses VNC desktop environment with pre-installed AI tools, supporting multiple AI programming assistants
- **GitHub-Driven Collaboration**: All information exchange through GitHub features (Issues, Projects, Comments, Labels)
- **Asynchronous Collaboration Mode**: Roles collaborate asynchronously by periodically scanning GitHub status
- **Intelligent Task Scheduling**: Automatically assign tasks based on role workload and skills

### 🏗️ **System Architecture**
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
│                VPS Cluster (Single VPS Single Role)             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   VPS-01    │ │   VPS-02    │ │   VPS-03    │ │   VPS-04    │ │
│  │ Product Mgr │ │ Backend Dev │ │ Frontend Dev│ │ QA Engineer │ │
│  │ PM-01       │ │ Backend-01  │ │ Frontend-01 │ │ QA-01       │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│  ┌─────────────┐                                                 │
│  │   VPS-05    │                                                 │
│  │ DevOps Eng  │                                                 │
│  │ DevOps-01   │                                                 │
│  └─────────────┘                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🖥️ **VPS Deployment Architecture**
```
Each VPS contains:
├── Role Container (Based on VNC Lab)
│   ├── noVNC Desktop Environment
│   ├── AI Tools Integration (Gemini CLI, Claude Code, Rovo Dev, Cursor)
│   ├── Web Terminal (ttyd)
│   └── Firefox Browser
├── Infrastructure Services
│   ├── Redis (Message Queue)
│   ├── PostgreSQL (State Database)
│   ├── Prometheus (Monitoring)
│   └── Grafana (Visualization)
└── System Coordinator (Optional, usually deployed independently)
```

## 🚀 **Quick Start**

### Requirements
- Docker 20.10+
- At least 4GB available memory per VPS
- GitHub account and Personal Access Token
- Python 3.9+

### Installation Steps

1. **Clone the project**
   ```bash
   git clone https://github.com/your-org/bee-swarm.git
   cd bee-swarm
   ```

2. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env file to configure GitHub tokens, etc.
   ```

3. **Build VNC Lab base image**
   ```bash
   # Build base image based on VNC Lab
   cd roles/base
   docker build -t vnc-llm-cli .
   ```

4. **Start single role VPS**
   ```bash
   # Start Product Manager VPS
   docker-compose up pm-01
   
   # Start Backend Developer VPS
   docker-compose up backend-01
   ```

5. **Configure GitHub repository**
   - Create GitHub Projects kanban board
   - Set up Labels (task types, priorities, skill requirements)
   - Configure role GitHub accounts

## 📚 **Documentation Structure**

- `docs/level1/` - System overview documentation
- `docs/level2/` - Role pool management documentation
- `docs/level3/` - GitHub collaboration workflow documentation
- `docs/level4/` - Task scheduling system documentation
- `docs/level5/` - Implementation details documentation

## 🛠️ **Technology Stack**

- **Containerization**: Docker + VNC Lab + noVNC
- **System Coordination**: Python + FastAPI + Redis
- **GitHub Integration**: PyGithub + GitHub API
- **Task Scheduling**: Celery + Redis
- **State Management**: SQLAlchemy + PostgreSQL
- **AI Tools**: Gemini CLI, Claude Code, Rovo Dev, Cursor
- **Monitoring**: Prometheus + Grafana

## 🔄 **Workflow**

### Requirements Release Process
```
Human User → GitHub Issues → System Coordinator → Task Analysis → Role Assignment
```

### Task Execution Process
```
Role Receives Task → Updates Status → Executes Development → Creates PR → Code Review → Merge & Deploy
```

### Collaboration Communication Process
```
Inter-Role Communication → GitHub Comments → Status Sync → Progress Update → Task Completion
```

## 🖥️ **VPS Access Information**

### Role VNC Access
- **Product Manager**: `http://vps-01:6080` (VNC Password: Set in environment variables)
- **Backend Developer**: `http://vps-02:6080` (VNC Password: Set in environment variables)
- **Frontend Developer**: `http://vps-03:6080` (VNC Password: Set in environment variables)
- **QA Engineer**: `http://vps-04:6080` (VNC Password: Set in environment variables)
- **DevOps Engineer**: `http://vps-05:6080` (VNC Password: Set in environment variables)

### Web Terminal Access
- **Product Manager**: `http://vps-01:7680` (Terminal Password: Set in environment variables)
- **Backend Developer**: `http://vps-02:7681` (Terminal Password: Set in environment variables)
- **Frontend Developer**: `http://vps-03:7682` (Terminal Password: Set in environment variables)
- **QA Engineer**: `http://vps-04:7683` (Terminal Password: Set in environment variables)
- **DevOps Engineer**: `http://vps-05:7684` (Terminal Password: Set in environment variables)

### Management Interfaces
- **System Coordinator**: `http://coordinator:8000`
- **API Documentation**: `http://coordinator:8000/docs`
- **Celery Monitoring**: `http://coordinator:5555`
- **Prometheus**: `http://vps-01:9090`
- **Grafana**: `http://vps-01:3000` (admin/admin)

## 📄 **License**

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🤝 **Contributing**

Welcome to submit Issues and Pull Requests to improve this project!

## 📞 **Contact**

For questions or suggestions, please contact us through:
- Submit an Issue
- Send email
- Join discussions

