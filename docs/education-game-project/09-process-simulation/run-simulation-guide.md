# 真实世界项目仿真运行指南

## 概述

这个仿真展示了 AI 角色容器如何从项目启动到完成的完整流程，包括：
- 🚀 **项目启动**: 可行性分析和环境搭建
- 🎯 **MVP 开发**: 最小可行产品开发
- 📦 **Release 1.0**: 第一个正式版本发布
- 🔄 **Release 1.1**: 功能增强版本

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

# 运行真实世界项目仿真
python3 real-world-simulation.py
```

## 预期输出

### 控制台输出示例
```
============================================================
🐝 Bee Swarm 真实世界项目仿真
============================================================
仿真时间: 200 小时
AI 角色容器: 4 个
项目里程碑: 4 个
============================================================
生成任务: 12 个

[   0.0h] Product Manager AI: 开始规划里程碑: 项目启动
[   2.5h] Product Manager AI: 使用 Gemini CLI 进行里程碑规划
[   2.5h] Product Manager AI: 里程碑 项目启动 开始执行
[   2.5h] Product Manager AI: 分配任务: 项目可行性分析
[   8.2h] Product Manager AI: 完成任务: 项目可行性分析 (产出: 2 个文件)
[  12.1h] DevOps Engineer AI: 开始任务: 环境配置
[  18.3h] DevOps Engineer AI: 完成任务: 环境配置 (产出: 2 个文件)
[  20.5h] Product Manager AI: 开始任务: 需求分析
[  32.8h] Product Manager AI: 完成任务: 需求分析 (产出: 2 个文件)
[  32.8h] Product Manager AI: 里程碑 项目启动 完成!
[  32.8h] Product Manager AI: 进入下一个里程碑: MVP 开发
...
```

### 最终结果示例
```
============================================================
📊 仿真结果
============================================================
仿真时间: 200 小时
实际运行时间: 45.23 秒
总任务数: 12
完成任务数: 12
完成率: 100.0%

📈 项目活动:
  GitHub 提交: 36
  Pull Requests: 12
  部署次数: 2
  沟通事件: 24

🎯 里程碑状态:
  ✅ 项目启动: completed
    完成时间: 32.8 小时
  ✅ MVP 开发: completed
    完成时间: 85.2 小时
  ✅ Release 1.0: completed
    完成时间: 142.1 小时
  ✅ Release 1.1: completed
    完成时间: 178.9 小时

👥 角色工作量:
  Product Manager AI: 78.5% (3 个任务)
  Backend Developer AI: 85.2% (5 个任务)
  Frontend Developer AI: 82.1% (3 个任务)
  DevOps Engineer AI: 65.8% (3 个任务)
```

### 生成的文件
- `project_timeline.png` - 项目时间线可视化图表

## 仿真流程详解

### 1. 项目启动阶段 (M1: 0-32小时)
```
Product Manager AI:
├── 项目可行性分析 (8小时)
├── 需求分析 (12小时)
└── 任务分配和进度监控

DevOps Engineer AI:
└── 环境配置 (6小时)
```

### 2. MVP 开发阶段 (M2: 32-85小时)
```
Backend Developer AI:
├── 数据库设计 (10小时)
├── 用户注册 API (16小时)
└── 基础游戏功能 (20小时)

Frontend Developer AI:
└── 用户界面设计 (12小时)
```

### 3. Release 1.0 阶段 (M3: 85-142小时)
```
Backend Developer AI:
└── 学习系统开发 (18小时)

Frontend Developer AI:
└── 学习界面开发 (16小时)

DevOps Engineer AI:
└── 生产环境部署 (8小时)
```

### 4. Release 1.1 阶段 (M4: 142-179小时)
```
Backend Developer AI:
└── 家长监控功能 (14小时)

Frontend Developer AI:
└── 家长界面开发 (12小时)

DevOps Engineer AI:
└── 性能优化 (10小时)
```

## AI 角色容器运作机制

### 角色触发机制
1. **Product Manager**: 自动启动，负责里程碑规划和任务分配
2. **Developers**: 等待任务分配，收到任务后立即开始工作
3. **DevOps**: 监控里程碑完成情况，在需要时进行部署

### 数据获取方式
- **GitHub API**: 通过 GitHub Issues 和 Pull Requests 进行任务管理
- **AI 工具**: 使用 Gemini CLI、Claude Code、Rovo Dev CLI 辅助开发
- **容器通信**: 通过共享资源和事件日志进行协作

### 产出结果
每个任务完成后会生成具体的文件：
- **文档文件**: `.md` 文件（需求文档、设计文档等）
- **代码文件**: `.js`、`.jsx`、`.sql` 文件
- **配置文件**: `.yml`、`.conf` 文件

## 自定义配置

### 修改仿真时间
```python
# 在 real-world-simulation.py 中修改
SIMULATION_TIME = 100  # 改为 100 小时（更快）
SIMULATION_TIME = 300  # 改为 300 小时（更详细）
```

### 修改任务复杂度
```python
# 在 generate_project_tasks() 中添加更多任务
{
    'title': '新功能开发',
    'description': '添加新功能',
    'priority': 'medium',
    'estimated_hours': 15,
    'assigned_role': 'be-01',
    'milestone': 'M4',
    'output_files': ['new_feature.js', 'new_component.jsx']
}
```

### 修改角色效率
```python
# 在 __init__() 中修改角色效率
'pm-01': Role(
    name='Product Manager AI',
    container_id='pm-01',
    skills=['需求分析', '任务分解', '进度监控', '用户研究'],
    efficiency=0.95,  # 提高效率到 95%
    github_username='pm_ai_001'
)
```

## 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 使用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple simpy matplotlib pandas
```

#### 2. 图表显示问题
```bash
# 如果无法显示图表，保存为文件
# 在代码中注释掉 plt.show()，只保留 plt.savefig()
```

#### 3. 运行时间过长
```bash
# 减少仿真时间
sed -i '' 's/SIMULATION_TIME = 200/SIMULATION_TIME = 50/' real-world-simulation.py
```

#### 4. 内存不足
```bash
# 减少任务数量或简化仿真逻辑
# 在 generate_project_tasks() 中只保留部分任务
```

## 仿真结果解读

### 关键指标
- **完成率**: 100% 表示所有任务都完成了
- **里程碑完成时间**: 显示每个阶段的进度
- **角色利用率**: 显示各角色的工作量分布
- **项目活动**: 显示 GitHub 提交、PR、部署等实际活动

### 优化建议
- **角色利用率不均**: 考虑重新分配任务
- **里程碑延迟**: 分析瓶颈并优化流程
- **沟通事件过多**: 优化协作机制
- **部署次数少**: 增加自动化部署

## 下一步

1. **运行仿真**: 执行 `python3 real-world-simulation.py`
2. **观察输出**: 关注角色交互和里程碑完成
3. **分析结果**: 查看生成的图表和统计数据
4. **优化流程**: 根据结果调整角色配置和任务分配
5. **实际应用**: 将仿真结果应用到真实的 bee_swarm 项目中

---

*这个仿真让你直观地看到 AI 角色容器如何协作完成一个完整的项目！* 