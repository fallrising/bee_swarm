# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced Bee Swarm documentation system and feature expansion
- Added enhanced bee swarm simulation system for educational game project (`enhanced-bee-swarm-simulation.py`)
- Added GitHub agile development workflow guides (`github-agile-methodology.md`, `github-agile-advanced.md`)
- Added bee swarm simulation system integration guide (`integration-guide.md`)
- Added project context documentation (`bee-swarm-context.md`)
- Added unified version bee swarm simulation program (`bee-swarm-unified-simulation.py`)
- Added comprehensive role system with 11 professional AI agents
- Added workflow simulation scripts supporting GitHub Actions workflows
- Added MCP Server architecture documentation (`docs/02-architecture/hybrid-architecture.md`)
- Added Dockerfile migration summary documentation (`dockerfile-migration-summary.md`)
- Added base image build script (`build_base_image.sh`)
- Added Dockerfile template (`Dockerfile.template`)
- Added CI environment configuration validation
- Configuration validation script (`scripts/validate_config.py`)
- Environment switching script (`scripts/switch_env.sh`)
- Test environment configuration (`docker-compose.test.yml`)
- Automated configuration validation mechanism
- Environment separation management functionality
- Resource usage monitoring functionality

### Changed
- 🎯 **Project repositioning**: Changed from production system to concept design framework, focusing on AI agent collaboration concept design and simulation
- ✨ **Enhanced multi-role multi-account containerized architecture description**, added visual system architecture diagrams and collaboration workflow diagrams
- Updated DockerHub user configuration (fallrising)
- Unified bee swarm simulation program, implemented product manager priority mechanism, conforming to GitHub-Centric architecture design
- Migrated all Dockerfiles to MCP Server architecture, using `fallrising/novnc_llm_cli:latest` base image
- Completed architecture simplification and role refactoring, improving system efficiency
- Simplified simulation files, retained core event-driven simulation
- Fixed GitHub Actions workflows, ensuring all workflows run properly
- Refactored project architecture and documentation structure
- Translated all documentation from Chinese to English, improving international accessibility
- Significantly simplified docker-compose.yml, removed all infrastructure services
- Optimized container resource configuration, adjusted according to role requirements
- Simplified environment variable configuration, reduced from 254 lines to 50 lines
- Redefined role responsibilities, simplified from 5 roles to 4 core roles
- Updated README.md to reflect new architecture and usage
- Improved role definition documentation, clarified responsibility boundaries

### Removed
- Deleted `.github/workflows` directory and all workflow files
- Deleted all deployment-related files: scripts/ folder (13 deployment scripts), docker-compose.yml, monitoring/ configuration files
- Deleted old version simulation files to keep codebase clean
- Removed coordinator module and old documentation structure
- Removed complex monitoring and backup configurations
- Redis service (state management changed to GitHub API)
- PostgreSQL service (data storage changed to GitHub Issues/Projects)
- Prometheus service (monitoring changed to GitHub Actions)
- Grafana service (visualization changed to GitHub Projects)
- QA Engineer role (responsibilities merged into DevOps Engineer)
- All third-party service configurations (Notion, Figma, Jira, Slack, etc.)
- Complex monitoring and backup configurations

### Fixed
- Fixed GitHub Actions workflow failure issues, added CI_ENVIRONMENT environment variable marker
- Fixed docker-compose command not found error in GitHub Actions
- Fixed GitHub Workflow files, ensuring all workflows run properly
- Architecture design contradiction issues
- Configuration complexity issues
- Role responsibility overlap issues
- Resource configuration issues
- Security configuration issues

### Security
- Implemented configuration validation mechanism
- Support for GitHub Secrets integration
- Environment separation management
- Password strength checking

## [0.4.0] - 2024-01-20

### Added
- GitHub-Centric architecture design
- Simplified documentation structure
- GitHub Actions-based trigger mechanism
- Asynchronous collaboration workflows
- Transparent coordination mechanism

### Changed
- Architecture changed from complex coordinator to GitHub-Centric
- Documentation structure simplified from 5 levels to 4 core documents
- Coordination mechanism changed from central coordinator to GitHub platform
- Communication protocol changed from custom message format to GitHub native features

### Deprecated
- Complex central coordinator architecture
- 5-level documentation structure
- Custom communication protocols
- Complex state management system

### Removed
- coordinator/ directory and all its components
- docs/level1/ to docs/level5/ directories
- Complex communication protocol design
- Overly detailed implementation documentation

### Fixed
- Architecture complexity issues
- Documentation maintenance difficulty issues
- System transparency issues
- Deployment complexity issues

### Security
- Simplified security configuration
- Leveraged GitHub native security mechanisms
- Reduced attack surface

## [0.3.0] - 2024-01-15

### Added
- Single VPS single role architecture design
- VNC Lab-based container construction
- AI tool rotation mechanism
- Detailed execution plan documentation
- Role-specific Dockerfiles
- Distributed deployment strategy

### Changed
- Refactored docker-compose.yml for single VPS mode
- Updated README.md architecture description
- Optimized environment variable configuration
- Adjusted port allocation strategy

## [0.2.0] - 2024-01-15

### Added
- Role persistent container architecture design
- System coordinator base framework
- GitHub-driven collaboration mechanism
- Role pool management documentation
- Task scheduling system design
- Load balancing algorithms
- Health check mechanisms
- Workspace management
- Dynamic scaling functionality

### Changed
- Refactored docker-compose.yml for role pool support
- Updated environment variable configuration
- Redesigned documentation structure
- Optimized README.md architecture description

## [0.1.0] - 2024-01-10

### Added
- Project initialization
- Basic documentation structure
- Docker Compose configuration
- Environment variable configuration
- GitHub Actions workflow
- Deployment scripts
- MIT License

---

## Version Notes

### Version Number Format
- MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible functional additions
- PATCH: Backward-compatible bug fixes

### Recent Major Changes (v0.4.0+)
- **Architecture Simplification**: Removed complex infrastructure components, truly implemented GitHub-Centric
- **Configuration Optimization**: Significantly simplified environment variable configuration, improved usability
- **Role Refactoring**: Redefined role responsibilities, avoided overlaps
- **Security Hardening**: Implemented configuration validation and environment separation
- **Performance Improvement**: Optimized resource configuration, improved system efficiency 