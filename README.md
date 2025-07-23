# 🐝 **Bee Swarm - AI自动化开发团队系统**

## 📋 **项目概述**

Bee Swarm是一个基于容器化虚拟角色的AI开发团队协作系统，利用现有的AI工具（Gemini CLI, Rovo Dev, Claude Code, Warp, Cursor）和GitHub工作流，实现完全自动化的软件开发流程。

### 🎯 **核心概念**
- **虚拟角色容器**：每个开发角色运行在独立的VNC容器中，拥有完整的桌面环境
- **AI工具集成**：每个角色容器预装相应的AI编程工具
- **异步协作**：通过GitHub Issues、PR、Actions实现角色间协作
- **按需触发**：通过GitHub Actions定时触发容器工作流程

### 🏗️ **系统架构**
```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub 平台                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Issues    │ │ Pull Request│ │   Actions   │ │   Webhooks  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Cloudflare Tunnel                            │
│                    远程访问网关                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    20台 VPS 集群                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ VPS-01      │ │ VPS-02      │ │ VPS-03      │ │ VPS-04      │ │
│  │ PM Container│ │ Backend     │ │ Frontend    │ │ QA          │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ VPS-05      │ │ VPS-06      │ │ VPS-07      │ │ VPS-08      │ │
│  │ DevOps      │ │ Project Mgr │ │ Operations  │ │ Data Analyst│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 **快速开始**

### 环境要求
- Docker 20.10+
- 至少2GB可用内存
- GitHub账号和Personal Access Token
- Cloudflare账号（用于Tunnel）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-org/bee-swarm.git
   cd bee-swarm
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑.env文件，配置GitHub tokens等
   ```

3. **构建角色容器**
   ```bash
   docker-compose build
   ```

4. **启动特定角色**
   ```bash
   docker-compose up product-manager
   ```

5. **配置GitHub Webhook**
   - 在GitHub仓库设置中添加Webhook
   - URL: `https://your-domain.com/webhook`
   - 选择事件: Issues, Pull requests

## 📚 **文档结构**

- `docs/level1/` - 系统概览文档
- `docs/level2/` - 角色系统文档
- `docs/level3/` - 工作流程文档
- `docs/level4/` - 通信协议文档
- `docs/level5/` - 实现细节文档

## 🛠️ **技术栈**

- **容器化**：基于VNC Lab的Docker容器
- **AI工具**：Gemini CLI, Rovo Dev, Claude Code, Warp, Cursor
- **协作平台**：GitHub (Issues, PR, Actions, Webhooks)
- **远程访问**：Cloudflare Tunnel + noVNC
- **调度系统**：GitHub Actions + Cron
- **监控**：Prometheus + Grafana

## 📄 **许可证**

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 **贡献**

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 **联系方式**

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 参与讨论

