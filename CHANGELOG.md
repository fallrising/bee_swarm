# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 采用单VPS单角色架构设计
- 基于VNC Lab项目构建角色容器
- 实现AI工具轮换机制
- 添加详细的执行计划文档
- 设计逐步实现策略
- 创建角色专用Dockerfile模板

### Changed
- 架构从角色池改为单VPS单角色模式
- 容器基础从自定义改为基于VNC Lab
- 部署策略从集中式改为分布式
- 执行计划从并行改为逐步实现

### Deprecated
- 角色池架构
- 集中式部署模式
- 并行开发策略

### Removed
- 多角色容器配置
- 角色池管理逻辑
- 集中式负载均衡

### Fixed
- 资源隔离问题
- 维护复杂度问题
- 扩展性问题

### Security
- 改进VPS间通信安全
- 增强角色权限隔离
- 优化网络安全策略

## [0.3.0] - 2024-01-15

### Added
- 单VPS单角色架构设计
- 基于VNC Lab的容器构建
- AI工具轮换机制
- 详细执行计划文档
- 角色专用Dockerfile
- 分布式部署策略

### Changed
- 重构docker-compose.yml支持单VPS模式
- 更新README.md架构说明
- 优化环境变量配置
- 调整端口分配策略

## [0.2.0] - 2024-01-15

### Added
- 角色常驻容器架构设计
- 系统协调器基础框架
- GitHub驱动的协作机制
- 角色池管理文档
- 任务调度系统设计
- 负载均衡算法
- 健康检查机制
- 工作空间管理
- 动态扩缩容功能

### Changed
- 重构docker-compose.yml支持角色池
- 更新环境变量配置
- 重新设计文档结构
- 优化README.md架构说明

## [0.1.0] - 2024-01-10

### Added
- 项目初始化
- 基础文档结构
- Docker Compose配置
- 环境变量配置
- GitHub Actions工作流
- 部署脚本
- MIT许可证

---

## 版本说明

### 版本号格式
- MAJOR.MINOR.PATCH
- MAJOR: 不兼容的API变更
- MINOR: 向后兼容的功能性新增
- PATCH: 向后兼容的问题修复

### 变更类型
- **Added**: 新功能
- **Changed**: 现有功能的变更
- **Deprecated**: 即将移除的功能
- **Removed**: 已移除的功能
- **Fixed**: 问题修复
- **Security**: 安全相关变更

### 发布计划
- **v0.1.0**: 基础架构和文档
- **v0.2.0**: 角色池架构重构 ✅
- **v0.3.0**: 单VPS单角色架构 ✅
- **v0.4.0**: 产品经理角色实现
- **v0.5.0**: 后端开发角色实现
- **v0.6.0**: 前端开发角色实现
- **v0.7.0**: QA工程师角色实现
- **v0.8.0**: DevOps工程师角色实现
- **v0.9.0**: 团队协作验证
- **v1.0.0**: 生产就绪版本 