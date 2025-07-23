# Bee Swarm

An AI team collaboration automated workflow system.

## 📊 Project Status

**Last Updated**: 2025-07-23 22:59:08

### Repository Information
- **Stars**: 42 ⭐
- **Forks**: 15 🍴
- **Open Issues**: 3 📝
- **Open Pull Requests**: 2 🔄
- **Last Updated**: 2025-07-23T10:30:00Z

### Recent Activity
#### Recent Commits
- `abc123` feat: add new feature module (2025-07-23)
- `def456` fix: fix login issue (2025-07-22)
- `ghi789` docs: update documentation (2025-07-21)

#### Open Issues
- #1 Implement user authentication feature
- #2 Fix login page bug
- #3 Add database connection pool

#### Open Pull Requests
- #1 Add new feature functionality
- #2 Fix UI issues

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- GitHub account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/bee_swarm.git
cd bee_swarm
```

2. Copy environment variables file:
```bash
cp env.example .env
```

3. Start services:
```bash
docker-compose up -d
```

## 📋 Features

### 🤖 AI Team Collaboration
- Automatic task assignment and notification
- Intelligent workflow management
- Real-time status monitoring

### 🔄 Automated Workflows
- GitHub Actions integration
- Scheduled task execution
- Event-driven triggers

### 📊 System Monitoring
- Health status checks
- Performance metrics monitoring
- Automatic backups

### 📚 Documentation Management
- Automatic documentation updates
- Version control integration
- Project status tracking

## 🏗️ System Architecture

```
bee_swarm/
├── coordinator/          # Coordinator service
├── roles/               # AI role definitions
├── scripts/             # Workflow scripts
├── docs/                # Project documentation
└── .github/workflows/   # GitHub Actions
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file and configure the following variables:

```bash
# GitHub Configuration
GITHUB_TOKEN=your_github_token
GITHUB_REPOSITORY=your_username/bee_swarm

# Optional Configuration (Mock version doesn't require)
CLOUDFLARE_TUNNEL_URL=your_tunnel_url
PROMETHEUS_URL=your_prometheus_url
GRAFANA_URL=your_grafana_url
SLACK_WEBHOOK_URL=your_slack_webhook
```

### GitHub Secrets

Add the following secrets in your GitHub repository settings:

- `GITHUB_TOKEN`: GitHub API access token
- `CLOUDFLARE_TUNNEL_URL`: Cloudflare Tunnel URL (optional)
- `PROMETHEUS_URL`: Prometheus service URL (optional)
- `GRAFANA_URL`: Grafana service URL (optional)
- `SLACK_WEBHOOK_URL`: Slack Webhook URL (optional)

## 🧪 Mock Mode

Currently, all scripts run in **Mock Mode**, which means:

- ✅ No need to configure complex external services
- ✅ Workflows can run immediately
- ✅ All data is preset mock data
- ✅ Easy for development and testing

### Mock Script List

- `check_pending_tasks.py` - Check pending tasks
- `trigger_ai_containers.py` - Trigger AI containers
- `notify_role_assignment.py` - Notify role assignments
- `handle_pr_events.py` - Handle PR events
- `check_system_health.py` - Check system health status
- `create_backup.py` - Create system backups
- `update_documentation.py` - Update project documentation

### Test Mock Scripts

```bash
# Test all scripts
python3 scripts/test_scripts.py

# Test individual script
python3 scripts/check_pending_tasks.py
```

## 📖 Documentation

For detailed documentation, please check the [docs/](docs/) directory:

- [System Overview](docs/level1/system-overview.md)
- [Role System](docs/level2/role-system.md)
- [Workflow System](docs/level3/workflow-system.md)
- [Communication Protocol](docs/level4/communication-protocol.md)
- [Implementation Details](docs/level5/implementation-details.md)
- [Workflow Fixes Record](docs/workflow-fixes.md)

## 🤝 Contributing

1. Fork this project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues or have suggestions, please:

1. Check the [Issues](../../issues) page
2. Create a new Issue
3. Contact the maintenance team

---

*This project is automatically maintained by the AI team*

