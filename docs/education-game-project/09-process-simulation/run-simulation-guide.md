# Bee Swarm 事件驱动仿真运行指南

## 概述

这个事件驱动仿真展示了 AI 角色容器如何从项目启动到完成的完整流程，基于 SimPy 离散事件模拟，提供详细的事件日志和统计结果。

### 核心特性
- 🚀 **事件驱动**: 每个系统变化都是通过事件实现
- 📊 **详细记录**: 每个事件都有时间、类型、描述、耗时
- 🔄 **资源竞争**: GitHub API、AI 工具等资源的并发限制
- 📈 **完整统计**: 项目活动、角色工作量、事件类型分布
- 🎯 **质量保证**: Code Review + UAT 双重验证

## 快速运行

### 1. 安装依赖
```bash
# 安装必要的 Python 包
pip3 install simpy matplotlib pandas

# 验证安装
python3 -c "import simpy, matplotlib, pandas; print('依赖安装成功!')"
```

### 2. 运行仿真
```bash
cd docs/education-game-project/09-process-simulation

# 运行事件驱动仿真
python3 bee-swarm-event-driven-simulation.py
```

## 预期输出

### 控制台输出示例
```
================================================================================
🐝 Bee Swarm 事件驱动仿真
================================================================================
仿真时间: 100 小时
AI 角色容器: 4 个
资源限制: GitHub API(3), AI工具(2)
================================================================================
[   0.0h] Product Manager AI: 人类创建Issue - 人类 PO 发布任务: 开发教育游戏用户注册功能
[   0.0h] Product Manager AI: PM开始分析 - 开始处理任务: 开发教育游戏用户注册功能
[   3.1h] Product Manager AI: AI工具使用 - 使用 Gemini CLI 分析需求 (耗时: 3.1h)
[   3.1h] Product Manager AI: PM分析完成 - 完成需求分析: 开发教育游戏用户注册功能
[   3.2h] Product Manager AI: GitHub评论添加 - 在 Issue #ISSUE-001 添加 PRD 评论 (耗时: 0.1h)
[   3.5h] Product Manager AI: 任务分配 - 创建任务: 后端 API 设计 -> Backend Developer AI
[   4.6h] Frontend Developer AI: 开发者开始任务 - 开始任务: 前端注册界面
[   5.3h] Frontend Developer AI: AI工具使用 - 查看后端 API 文档 (耗时: 0.7h)
[   5.6h] Frontend Developer AI: GitHub评论添加 - 在 Issue #ISSUE-001 提出 API 疑问 (耗时: 0.3h)
[   7.6h] Backend Developer AI: AI工具使用 - 使用 Gemini CLI 辅助开发 (耗时: 2.9h)
[  18.6h] Backend Developer AI: API文档创建 - 创建 API 文档
[  18.8h] Backend Developer AI: PR创建 - 创建 PR: 实现 后端 API 设计 (耗时: 0.2h)
[  22.8h] Product Manager AI: 代码审查完成 - PR #PR-001 审查通过 (耗时: 1.8h)
[  26.3h] Product Manager AI: UAT开始 - 对 PR #PR-001 进行 UAT 测试 (耗时: 1.2h)
[  26.5h] Product Manager AI: UAT完成 - 完成 PR #PR-001 的 UAT 测试
[  31.9h] DevOps Engineer AI: 部署开始 - 开始部署 PR #PR-001
[  35.7h] DevOps Engineer AI: 部署完成 - PR #PR-001 部署完成! (耗时: 3.8h)
[  48.8h] Backend Developer AI: 日报生成 - 生成日报 #1 (耗时: 0.3h)
```

### 最终统计结果示例
```
================================================================================
📊 事件驱动仿真详细结果
================================================================================
仿真时间: 100 小时
实际运行时间: 0.00 秒

📈 项目活动统计:
  总事件数: 104
  GitHub Issues: 1
  Pull Requests: 3
  沟通事件: 11
  API 文档: 2
  日报数量: 5

🎯 任务执行统计:
  总任务数: 3
  完成任务数: 3
  完成率: 100.0%
  平均任务耗时: 15.1 小时

👥 角色工作量统计:
  Product Manager AI: 37.0% 利用率，AI工具使用 8.4%
  Backend Developer AI: 59.3% 利用率，AI工具使用 9.8%
  Frontend Developer AI: 45.2% 利用率，AI工具使用 5.1%
  DevOps Engineer AI: 35.1% 利用率

🔄 事件类型统计:
  默认任务执行: 57 次
  GitHub评论添加: 8 次
  AI工具使用: 5 次
  日报生成: 5 次
  任务分配: 3 次
  开发者开始任务: 3 次
  PR创建: 3 次
  代码审查完成: 3 次
  UAT开始/完成: 各 3 次
  部署开始/完成: 各 3 次
  API文档创建: 2 次
```

## 仿真流程详解

### 1. 人类 PO 触发 (0小时)
```
[   0.0h] Product Manager AI: 人类创建Issue - 人类 PO 发布任务: 开发教育游戏用户注册功能
```

### 2. 产品经理分析需求 (0-3小时)
```
[   0.0h] Product Manager AI: PM开始分析 - 开始处理任务: 开发教育游戏用户注册功能
[   3.1h] Product Manager AI: AI工具使用 - 使用 Gemini CLI 分析需求 (耗时: 3.1h)
[   3.1h] Product Manager AI: PM分析完成 - 完成需求分析: 开发教育游戏用户注册功能
[   3.2h] Product Manager AI: GitHub评论添加 - 在 Issue #ISSUE-001 添加 PRD 评论 (耗时: 0.1h)
```

### 3. 任务分配 (3-4小时)
```
[   3.5h] Product Manager AI: 任务分配 - 创建任务: 后端 API 设计 -> Backend Developer AI
[   3.7h] Product Manager AI: 任务分配 - 创建任务: 数据库设计 -> Backend Developer AI
[   3.9h] Product Manager AI: 任务分配 - 创建任务: 前端注册界面 -> Frontend Developer AI
```

### 4. 开发者开始工作 (4-20小时)
```
[   4.6h] Frontend Developer AI: 开发者开始任务 - 开始任务: 前端注册界面
[   4.7h] Backend Developer AI: 开发者开始任务 - 开始任务: 后端 API 设计
[   5.3h] Frontend Developer AI: AI工具使用 - 查看后端 API 文档 (耗时: 0.7h)
[   5.6h] Frontend Developer AI: GitHub评论添加 - 在 Issue #ISSUE-001 提出 API 疑问 (耗时: 0.3h)
[   7.6h] Backend Developer AI: AI工具使用 - 使用 Gemini CLI 辅助开发 (耗时: 2.9h)
```

### 5. API 文档创建 (18-37小时)
```
[  18.6h] Backend Developer AI: API文档创建 - 创建 API 文档
[  37.1h] Backend Developer AI: API文档创建 - 创建 API 文档
```

### 6. PR 创建和代码审查 (18-25小时)
```
[  18.8h] Backend Developer AI: PR创建 - 创建 PR: 实现 后端 API 设计 (耗时: 0.2h)
[  19.6h] Frontend Developer AI: PR创建 - 创建 PR: 实现 前端注册界面 (耗时: 0.3h)
[  22.8h] Product Manager AI: 代码审查完成 - PR #PR-001 审查通过 (耗时: 1.8h)
[  25.4h] Product Manager AI: 代码审查完成 - PR #PR-002 审查通过 (耗时: 2.4h)
```

### 7. UAT 测试 (26-28小时)
```
[  26.3h] Product Manager AI: UAT开始 - 对 PR #PR-001 进行 UAT 测试 (耗时: 1.2h)
[  26.5h] Product Manager AI: UAT完成 - 完成 PR #PR-001 的 UAT 测试
[  28.3h] Product Manager AI: UAT开始 - 对 PR #PR-002 进行 UAT 测试 (耗时: 1.8h)
[  28.5h] Product Manager AI: UAT完成 - 完成 PR #PR-002 的 UAT 测试
```

### 8. 部署流程 (31-38小时)
```
[  31.9h] DevOps Engineer AI: 部署开始 - 开始部署 PR #PR-001
[  35.7h] DevOps Engineer AI: 部署完成 - PR #PR-001 部署完成! (耗时: 3.8h)
[  35.7h] DevOps Engineer AI: 部署开始 - 开始部署 PR #PR-002
[  38.2h] DevOps Engineer AI: 部署完成 - PR #PR-002 部署完成! (耗时: 2.5h)
```

### 9. 日报生成 (48-96小时)
```
[  48.8h] Backend Developer AI: 日报生成 - 生成日报 #1 (耗时: 0.3h)
[  72.2h] DevOps Engineer AI: 日报生成 - 生成日报 #1 (耗时: 0.1h)
[  72.9h] Product Manager AI: 日报生成 - 生成日报 #1 (耗时: 0.3h)
[  96.7h] Backend Developer AI: 日报生成 - 生成日报 #2 (耗时: 0.1h)
[  96.9h] Frontend Developer AI: 日报生成 - 生成日报 #1 (耗时: 0.1h)
```

## 事件类型说明

### 核心事件类型
- **人类创建Issue**: 人类 PO 发布新任务
- **PM开始分析**: 产品经理开始分析需求
- **AI工具使用**: 使用 Gemini CLI、Claude Code 等 AI 工具
- **任务分配**: 产品经理分配任务给开发者
- **开发者开始任务**: 开发者开始执行分配的任务
- **API文档创建**: 后端开发者创建 API 文档
- **PR创建**: 开发者创建 Pull Request
- **代码审查完成**: AI 代码审查员完成审查
- **UAT开始/完成**: 产品经理进行用户验收测试
- **部署开始/完成**: DevOps 工程师进行部署
- **日报生成**: 各角色生成日报
- **GitHub评论添加**: 在 Issue 或 PR 中添加评论
- **默认任务执行**: 角色在没有分配任务时执行默认任务

### 资源使用
- **GitHub API**: 限制并发数为 3
- **AI 工具**: 限制并发数为 2
- **代码审查员**: 限制并发数为 2
- **部署环境**: 限制并发数为 1

## 自定义配置

### 修改仿真时间
```python
# 在 bee-swarm-event-driven-simulation.py 中修改
SIMULATION_TIME = 50   # 改为 50 小时（更快）
SIMULATION_TIME = 200  # 改为 200 小时（更详细）
```

### 修改资源限制
```python
# 在 __init__() 中修改资源容量
self.github_api = simpy.Resource(self.env, capacity=5)      # 增加 GitHub API 并发
self.ai_tools = simpy.Resource(self.env, capacity=3)        # 增加 AI 工具并发
self.code_reviewers = simpy.Resource(self.env, capacity=3)  # 增加代码审查员
```

### 修改角色配置
```python
# 在 __init__() 中修改角色默认任务
'pm-01': Role(
    name='Product Manager AI',
    container_id='pm-01',
    github_username='pm_ai_001',
    default_tasks=['热门新闻爬虫', '用户反馈分析', '竞品监控', '新任务']  # 添加新任务
)
```

### 修改任务模板
```python
# 在 create_development_tasks() 中添加新任务
task_templates = [
    {'title': '后端 API 设计', 'assigned_role': 'be-01'},
    {'title': '数据库设计', 'assigned_role': 'be-01'},
    {'title': '前端注册界面', 'assigned_role': 'fe-01'},
    {'title': '新功能开发', 'assigned_role': 'be-01'},  # 添加新任务
]
```

## 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 使用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple simpy matplotlib pandas
```

#### 2. 运行时间过长
```bash
# 减少仿真时间
sed -i '' 's/SIMULATION_TIME = 100/SIMULATION_TIME = 50/' bee-swarm-event-driven-simulation.py
```

#### 3. 输出信息过多
```bash
# 可以重定向输出到文件
python3 bee-swarm-event-driven-simulation.py > simulation_output.log 2>&1
```

#### 4. 内存不足
```bash
# 减少事件记录或简化仿真逻辑
# 在 log_event() 中减少记录的事件类型
```

## 仿真结果解读

### 关键指标
- **总事件数**: 显示系统活跃度
- **任务完成率**: 100% 表示所有任务都完成了
- **角色利用率**: 显示各角色的工作量分布
- **AI工具使用率**: 显示 AI 工具的使用情况
- **沟通事件数**: 显示团队协作频率

### 优化建议
- **角色利用率不均**: 考虑重新分配任务
- **AI工具使用率低**: 增加 AI 工具的使用场景
- **沟通事件过多**: 优化协作机制
- **部署次数少**: 增加自动化部署
- **事件类型单一**: 增加更多事件类型

## 下一步

1. **运行仿真**: 执行 `python3 bee-swarm-event-driven-simulation.py`
2. **观察事件流**: 关注事件的时间序列和类型分布
3. **分析统计**: 查看角色工作量和资源使用情况
4. **优化配置**: 根据结果调整角色配置和资源限制
5. **实际应用**: 将仿真结果应用到真实的 bee_swarm 项目中

---

*这个事件驱动仿真让你清楚地看到每个事件的发生时间、类型和影响，提供了 bee_swarm 系统运作的详细视图！* 