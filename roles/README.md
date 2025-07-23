# Bee Swarm AI Role System

## Overview

Bee Swarm AI is an AI team collaboration automated workflow system. This directory contains the definitions, configurations, and implementations of all AI roles in the system.

## Role Architecture

### Role List

| Role | Folder | Primary Responsibilities | Tech Stack |
|------|--------|------------------------|------------|
| **Product Manager** | `product_manager/` | Requirement management, product planning, project coordination | Project management tools, AI tools |
| **Project Manager** | `project_manager/` | Project planning, progress management, resource coordination | Project management tools, collaboration tools, AI tools |
| **Backend Developer** | `backend_developer/` | API design, database design, business logic | Python/Node.js/Go, databases, cloud services |
| **Frontend Developer** | `frontend_developer/` | UI development, user experience, frontend architecture | React/Vue/Angular, CSS, build tools |
| **QA Engineer** | `qa_engineer/` | Test planning, automated testing, quality assurance | Testing frameworks, automation tools, monitoring tools |
| **DevOps Engineer** | `devops_engineer/` | Infrastructure, CI/CD, monitoring operations | Containerization, cloud platforms, monitoring tools |
| **Android Developer** | `android_developer/` | Android app development, mobile development | Kotlin/Java, Android SDK, AI tools |
| **iOS Developer** | `ios_developer/` | iOS app development, mobile development | Swift/Objective-C, iOS SDK, AI tools |
| **Unity Developer** | `unity_developer/` | Game development, 3D applications, interactive experiences | C#, Unity Engine, AI tools |
| **Visual Designer** | `visual_designer/` | UI/UX design, brand design, design systems | Design tools, frontend technologies, AI tools |
| **Data Engineer** | `data_engineer/` | Data infrastructure, data pipelines, data quality | Big data technologies, Python/SQL, data platforms |

### Directory Structure

```
roles/
├── product_manager/
│   ├── Dockerfile          # Product manager container configuration
│   └── prompt.md           # Product manager role specification
├── project_manager/
│   ├── Dockerfile          # Project manager container configuration
│   └── prompt.md           # Project manager role specification
├── backend_developer/
│   ├── Dockerfile          # Backend developer container configuration
│   └── prompt.md           # Backend developer role specification
├── frontend_developer/
│   ├── Dockerfile          # Frontend developer container configuration
│   └── prompt.md           # Frontend developer role specification
├── qa_engineer/
│   ├── Dockerfile          # QA engineer container configuration
│   └── prompt.md           # QA engineer role specification
├── devops_engineer/
│   ├── Dockerfile          # DevOps engineer container configuration
│   └── prompt.md           # DevOps engineer role specification
├── android_developer/
│   ├── Dockerfile          # Android developer container configuration
│   └── prompt.md           # Android developer role specification
├── ios_developer/
│   ├── Dockerfile          # iOS developer container configuration
│   └── prompt.md           # iOS developer role specification
├── unity_developer/
│   ├── Dockerfile          # Unity developer container configuration
│   └── prompt.md           # Unity developer role specification
├── visual_designer/
│   ├── Dockerfile          # Visual designer container configuration
│   └── prompt.md           # Visual designer role specification
├── data_engineer/
│   ├── Dockerfile          # Data engineer container configuration
│   └── prompt.md           # Data engineer role specification
└── README.md               # This file
```

## Role Specification Format

Each role's `prompt.md` file follows a unified format containing the following sections:

### 1. Role Identity and Background
- Role positioning and core values
- Professional background and skill requirements

### 2. Primary Responsibilities and Scope
- Detailed responsibility descriptions
- Work scope and boundaries

### 3. Work Methods and Processes
- Workflow diagrams (Mermaid)
- Daily work and development principles

### 4. Collaboration Patterns with Other Roles
- Collaboration methods with various roles
- Communication and coordination mechanisms

### 5. Input and Output Definitions
- Received input content
- Produced output content

### 6. Tool Usage Standards
- Essential tools and AI tools
- Tool usage principles

### 7. Code and Documentation Standards
- Code standards and documentation requirements
- Quality requirements

### 8. Technology Stack and Frameworks
- Primary technology stack
- Related frameworks and tools

### 9. Performance and Standards
- Performance metrics
- Quality standards

### 10. Communication and Reporting Mechanisms
- Daily communication methods
- Reporting and feedback mechanisms

### 11. Continuous Learning and Improvement
- Skill enhancement plans
- Process improvement methods

## Dockerfile Configuration

Each role's Dockerfile is based on the `vnc-llm-cli:latest` image and includes:

### Basic Configuration
- Working directory setup
- User creation and permission settings
- Environment variable configuration

### Tool Installation
- System tools and development tools
- Role-specific professional tools
- AI tool integration

### Dependency Management
- Python dependency packages
- Node.js package management
- Other language tools

### Workspace
- Role-specific directory structure
- Scripts and configuration files
- Data and log directories

## Role Collaboration Model

### Workflow
```mermaid
graph TD
    A[Product Manager] --> B[Requirement Analysis]
    B --> C[Project Manager]
    C --> D[Task Breakdown]
    D --> E[Visual Design]
    D --> F[Backend Development]
    D --> G[Frontend Development]
    D --> H[Mobile Development]
    D --> I[Game Development]
    D --> J[Data Engineering]
    E --> K[Design Delivery]
    F --> L[API Integration]
    G --> L
    H --> M[Mobile Integration]
    I --> N[Game Testing]
    J --> O[Data Pipeline]
    K --> P[UI Implementation]
    L --> Q[Full-stack Integration]
    M --> Q
    P --> Q
    O --> R[Data Analysis]
    Q --> S[QA Testing]
    N --> S
    R --> T[Data Reports]
    S --> U[DevOps Deployment]
    U --> V[Monitoring Verification]
    T --> V
    V --> W[User Feedback]
    W --> A
```

### Communication Mechanisms
- **Real-time Communication**: Use Slack/Teams for real-time collaboration
- **Document Collaboration**: Use Notion/Confluence for document management
- **Code Collaboration**: Use GitHub for code management and review
- **Project Management**: Use Jira/Trello for task management

## Deployment Configuration

### Environment Variables
Each role requires configuration of the following environment variables:

```bash
# Role Identity
ROLE_NAME=role_name
ROLE_ID=role_id
ROLE_TYPE=role_type

# GitHub Configuration
GITHUB_USERNAME=github_username
GITHUB_TOKEN=github_token

# System Configuration
COORDINATOR_URL=coordinator_url
REDIS_URL=redis_url

# VNC Configuration
VNC_PASSWORD=vnc_password
TTYD_PASSWORD=ttyd_password

# AI Tools
AI_TOOLS=gemini-cli,claude-code,rovo-dev,cursor
```

### Port Configuration
- **VNC Port**: 6080 (noVNC)
- **Terminal Port**: 7681 (ttyd)
- **API Port**: 8000 (FastAPI)

### Resource Limits
- **Memory Limit**: 2-4GB
- **CPU Limit**: 1-2 cores
- **Storage Space**: 10-20GB

## Monitoring and Maintenance

### Health Checks
- Regularly check role container status
- Monitor resource usage
- Check service availability

### Log Management
- Centralized collection of role logs
- Set up log rotation and cleanup
- Configure log monitoring and alerts

### Backup Strategy
- Regular backup of role configurations
- Backup important data and documents
- Test recovery procedures

## Extension and Customization

### Adding New Roles
1. Create role folder
2. Write Dockerfile
3. Create role specification
4. Update docker-compose.yml
5. Configure environment variables

### Custom Configuration
- Modify Dockerfile to add specific tools
- Update prompt.md to adjust role responsibilities
- Configure custom environment variables
- Add role-specific scripts

## Best Practices

### Role Design
- Clear role boundaries and responsibilities
- Maintain balance between roles
- Consider dependencies between roles
- Design clear communication mechanisms

### Technical Implementation
- Use containerized deployment
- Implement automated configuration
- Establish monitoring and alerts
- Keep code and documentation synchronized

### Operations Management
- Regular updates and maintenance
- Monitor system performance
- Address issues promptly
- Continuous process improvement

---

*This document is an overview of the Bee Swarm AI role system. For detailed role specifications, please refer to each role's prompt.md file.* 