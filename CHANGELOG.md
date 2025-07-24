# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 配置驗證腳本 (`scripts/validate_config.py`)
- 環境切換腳本 (`scripts/switch_env.sh`)
- 測試環境配置 (`docker-compose.test.yml`)
- 自動化配置驗證機制
- 環境分離管理功能
- 資源使用監控功能

### Changed
- 大幅簡化 docker-compose.yml，移除所有基礎設施服務
- 優化容器資源配置，根據角色需求調整
- 簡化環境變量配置，從 254 行減少到 50 行
- 重新定義角色職責，從 5 個角色簡化為 4 個核心角色
- 更新 README.md，反映新的架構和使用方式
- 改進角色定義文檔，明確職責邊界

### Removed
- Redis 服務（狀態管理改用 GitHub API）
- PostgreSQL 服務（數據存儲改用 GitHub Issues/Projects）
- Prometheus 服務（監控改用 GitHub Actions）
- Grafana 服務（可視化改用 GitHub Projects）
- QA Engineer 角色（職責合併到 DevOps Engineer）
- 所有第三方服務配置（Notion、Figma、Jira、Slack 等）
- 複雜的監控和備份配置

### Fixed
- 架構設計矛盾問題
- 配置複雜度過高問題
- 角色職責重疊問題
- 資源配置不合理問題
- 安全配置問題

### Security
- 實現配置驗證機制
- 支持 GitHub Secrets 集成
- 環境分離管理
- 密碼強度檢查

## [0.4.0] - 2024-01-20

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

### Recent Major Changes (v0.4.0+)
- **架構簡化**: 移除複雜的基礎設施組件，真正實現 GitHub-Centric
- **配置優化**: 大幅簡化環境變量配置，提高易用性
- **角色重構**: 重新定義角色職責，避免重疊
- **安全加固**: 實現配置驗證和環境分離
- **性能提升**: 優化資源配置，提高系統效率 