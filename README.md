# 🐝 **Bee Swarm - AI自动化开发团队系统**

## 📋 **项目概述**

Bee Swarm是一个基于**单VPS单角色**的AI开发团队协作系统，通过**GitHub作为中央数据源**，实现完全异步的AI驱动软件开发流程。每个VPS运行一个专门的AI角色容器，基于[VNC Lab](https://github.com/fallrising/vnc_lab)项目构建。

### 🎯 **核心概念**
- **单VPS单角色**：每个VPS只运行一个AI角色容器，确保资源隔离和稳定性
- **基于VNC Lab**：使用预装AI工具的VNC桌面环境，支持多种AI编程助手
- **GitHub驱动协作**：所有信息交换通过GitHub功能实现（Issues、Projects、Comments、Labels）
- **异步协作模式**：角色通过定期扫描GitHub状态进行异步协作
- **智能任务调度**：根据角色负载和技能自动分配任务

### 🏗️ **系统架构**
```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub 平台                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Issues    │ │  Projects   │ │  Comments   │ │   Labels    │ │
│  │   (任务)    │ │  (看板)     │ │  (通信)     │ │  (分类)     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    系统协调器 (Coordinator)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ 任务调度器  │ │ 状态管理器  │ │ GitHub同步器│ │ 通信协调器  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VPS集群 (单VPS单角色)                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   VPS-01    │ │   VPS-02    │ │   VPS-03    │ │   VPS-04    │ │
│  │ 产品经理    │ │ 后端开发    │ │ 前端开发    │ │ QA工程师    │ │
│  │ PM-01       │ │ Backend-01  │ │ Frontend-01 │ │ QA-01       │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│  ┌─────────────┐                                                 │
│  │   VPS-05    │                                                 │
│  │ DevOps工程师│                                                 │
│  │ DevOps-01   │                                                 │
│  └─────────────┘                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🖥️ **VPS部署架构**
```
每个VPS包含：
├── 角色容器 (基于VNC Lab)
│   ├── noVNC桌面环境
│   ├── AI工具集成 (Gemini CLI, Claude Code, Rovo Dev, Cursor)
│   ├── Web终端 (ttyd)
│   └── Firefox浏览器
├── 基础设施服务
│   ├── Redis (消息队列)
│   ├── PostgreSQL (状态数据库)
│   ├── Prometheus (监控)
│   └── Grafana (可视化)
└── 系统协调器 (可选，通常独立部署)
```

## 🚀 **快速开始**

### 环境要求
- Docker 20.10+
- 每个VPS至少4GB可用内存
- GitHub账号和Personal Access Token
- Python 3.9+

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-org/bee-swarm.git
   cd bee-swarm
   ```

2. **配置环境变量**
   ```bash
   cp env.example .env
   # 编辑.env文件，配置GitHub tokens等
   ```

3. **构建VNC Lab基础镜像**
   ```bash
   # 基于VNC Lab构建基础镜像
   cd roles/base
   docker build -t vnc-llm-cli .
   ```

4. **启动单个角色VPS**
   ```bash
   # 启动产品经理VPS
   docker-compose up pm-01
   
   # 启动后端开发VPS
   docker-compose up backend-01
   ```

5. **配置GitHub仓库**
   - 创建GitHub Projects看板
   - 设置Labels（任务类型、优先级、技能要求）
   - 配置角色GitHub账号

## 📚 **文档结构**

- `docs/level1/` - 系统概览文档
- `docs/level2/` - 角色池管理文档
- `docs/level3/` - GitHub协作流程文档
- `docs/level4/` - 任务调度系统文档
- `docs/level5/` - 实现细节文档

## 🛠️ **技术栈**

- **容器化**：Docker + VNC Lab + noVNC
- **系统协调**：Python + FastAPI + Redis
- **GitHub集成**：PyGithub + GitHub API
- **任务调度**：Celery + Redis
- **状态管理**：SQLAlchemy + PostgreSQL
- **AI工具**：Gemini CLI, Claude Code, Rovo Dev, Cursor
- **监控**：Prometheus + Grafana

## 🔄 **工作流程**

### 需求发布流程
```
人类用户 → GitHub Issues → 系统协调器 → 任务分析 → 角色分配
```

### 任务执行流程
```
角色接收任务 → 更新状态 → 执行开发 → 创建PR → 代码审查 → 合并部署
```

### 协作通信流程
```
角色间通信 → GitHub Comments → 状态同步 → 进度更新 → 任务完成
```

## 🖥️ **VPS访问信息**

### 角色VNC访问
- **产品经理**: `http://vps-01:6080` (VNC密码: 环境变量设置)
- **后端开发**: `http://vps-02:6080` (VNC密码: 环境变量设置)
- **前端开发**: `http://vps-03:6080` (VNC密码: 环境变量设置)
- **QA工程师**: `http://vps-04:6080` (VNC密码: 环境变量设置)
- **DevOps工程师**: `http://vps-05:6080` (VNC密码: 环境变量设置)

### Web终端访问
- **产品经理**: `http://vps-01:7680` (终端密码: 环境变量设置)
- **后端开发**: `http://vps-02:7681` (终端密码: 环境变量设置)
- **前端开发**: `http://vps-03:7682` (终端密码: 环境变量设置)
- **QA工程师**: `http://vps-04:7683` (终端密码: 环境变量设置)
- **DevOps工程师**: `http://vps-05:7684` (终端密码: 环境变量设置)

### 管理界面
- **系统协调器**: `http://coordinator:8000`
- **API文档**: `http://coordinator:8000/docs`
- **Celery监控**: `http://coordinator:5555`
- **Prometheus**: `http://vps-01:9090`
- **Grafana**: `http://vps-01:3000` (admin/admin)

## 📄 **许可证**

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 **贡献**

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 **联系方式**

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 参与讨论

