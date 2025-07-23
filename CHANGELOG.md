# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub-Centric 架構設計
- 簡化的文檔結構
- 基於 GitHub Actions 的觸發機制
- 異步協作工作流
- 透明化協調機制

### Changed
- 架構從複雜的 coordinator 改為 GitHub-Centric
- 文檔結構從 5 層級簡化為 4 個核心文檔
- 協調機制從中央協調器改為 GitHub 平台
- 通信協議從自定義消息格式改為 GitHub 原生功能

### Deprecated
- 複雜的中央協調器架構
- 5 層級文檔結構
- 自定義通信協議
- 複雜的狀態管理系統

### Removed
- coordinator/ 目錄及其所有組件
- docs/level1/ 到 docs/level5/ 目錄
- 複雜的通信協議設計
- 過度詳細的實現細節文檔

### Fixed
- 架構複雜度問題
- 文檔維護困難問題
- 系統透明度問題
- 部署複雜度問題

### Security
- 簡化安全配置
- 利用 GitHub 原生安全機制
- 減少攻擊面

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

### Change Types
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes

### Release Plan
- **v0.1.0**: Basic architecture and documentation
- **v0.2.0**: Role pool architecture refactor ✅
- **v0.3.0**: Single VPS single role architecture ✅
- **v0.4.0**: GitHub-Centric architecture refactor ✅
- **v0.5.0**: Product Manager role implementation
- **v0.6.0**: Backend Developer role implementation
- **v0.7.0**: Frontend Developer role implementation
- **v0.8.0**: QA Engineer role implementation
- **v0.9.0**: DevOps Engineer role implementation
- **v1.0.0**: Production-ready version 