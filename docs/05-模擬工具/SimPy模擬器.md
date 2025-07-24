# SimPy 模擬器

## 本章概要

本章介紹 Bee Swarm 項目中使用的 SimPy 離散事件模擬器，用於模擬 AI 角色協作過程和評估協作效果。

- **章節目標**：理解 SimPy 模擬器的架構和功能
- **主要內容**：模擬器設計、核心組件、使用方法
- **閱讀收穫**：掌握如何使用模擬器驗證協作模式

## 🎯 模擬器概述

### 什麼是 SimPy
SimPy 是一個基於 Python 的離散事件模擬框架，特別適合模擬複雜系統中的異步流程和資源競爭。在 Bee Swarm 項目中，我們使用 SimPy 來：

- **模擬 AI 角色行為**：每個角色作為獨立的進程
- **模擬任務處理流程**：從需求到部署的完整生命週期
- **評估協作效率**：量化不同協作模式的效果
- **優化工作流程**：識別瓶頸和改進機會

### 為什麼選擇 SimPy
1. **事件驅動**：符合 GitHub-centric 的異步工作模式
2. **資源管理**：可以模擬開發者時間、服務器資源等約束
3. **統計分析**：內建豐富的數據收集和分析功能
4. **擴展性強**：易於添加新的角色類型和工作流程

## 🏗️ 模擬器架構

### 核心組件

```python
# 模擬器核心架構
class BeeSwarmSimulator:
    def __init__(self):
        self.env = simpy.Environment()
        self.roles = {}
        self.task_queue = simpy.Store(self.env)
        self.github_api = GitHubSimulator(self.env)
        self.metrics = MetricsCollector()
```

### 1. 環境管理器 (Environment)
```python
class SimulationEnvironment:
    """管理整個模擬環境"""
    def __init__(self, duration=1000):
        self.env = simpy.Environment()
        self.duration = duration
        self.clock = 0
        
    def run(self):
        """運行模擬"""
        self.env.run(until=self.duration)
```

### 2. 角色模擬器 (Role Simulators)
每個 AI 角色都有對應的模擬器類：

```python
class ProductManagerSimulator:
    """產品經理模擬器"""
    def __init__(self, env, github_api):
        self.env = env
        self.github = github_api
        self.workload = simpy.Resource(env, capacity=1)
        
    def process(self):
        """主要工作流程"""
        while True:
            # 創建需求
            yield self.env.timeout(random.exponential(2))
            issue = self.create_requirement()
            yield self.github.create_issue(issue)
            
    def create_requirement(self):
        """創建功能需求"""
        return {
            'type': 'feature_request',
            'priority': random.choice(['high', 'medium', 'low']),
            'complexity': random.normal(5, 2)
        }
```

### 3. GitHub API 模擬器
```python
class GitHubSimulator:
    """模擬 GitHub API 行為"""
    def __init__(self, env):
        self.env = env
        self.issues = []
        self.prs = []
        self.api_rate_limit = simpy.Resource(env, capacity=5000)
        
    def create_issue(self, issue_data):
        """模擬創建 Issue"""
        with self.api_rate_limit.request() as req:
            yield req
            yield self.env.timeout(0.1)  # API 延遲
            issue = Issue(issue_data)
            self.issues.append(issue)
            return issue
```

### 4. 任務處理流程
```python
class TaskProcessor:
    """任務處理流程模擬"""
    def __init__(self, env, roles):
        self.env = env
        self.roles = roles
        
    def process_feature(self, feature):
        """處理功能開發流程"""
        # Phase 1: 需求分析
        yield self.env.process(self.requirement_analysis(feature))
        
        # Phase 2: 設計階段
        design = yield self.env.process(self.design_phase(feature))
        
        # Phase 3: 開發階段
        implementation = yield self.env.process(
            self.development_phase(design)
        )
        
        # Phase 4: 部署階段
        yield self.env.process(self.deployment_phase(implementation))
```

## ⚙️ 模擬參數配置

### 角色工作特性
```yaml
roles:
  product_manager:
    capacity: 1.0
    focus_time: [2, 8]  # 專注工作時間範圍
    context_switch_cost: 0.5  # 上下文切換成本
    
  backend_developer:
    capacity: 1.0
    coding_speed: [0.5, 2.0]  # 編程速度範圍
    bug_rate: 0.1  # 缺陷率
    
  frontend_developer:
    capacity: 1.0
    ui_design_time: [1, 4]  # UI 設計時間
    browser_testing_time: 0.5
    
  devops_engineer:
    capacity: 1.0
    deployment_time: [0.2, 1.0]  # 部署時間範圍
    monitoring_overhead: 0.1
```

### 任務類型和複雜度
```yaml
task_types:
  feature_request:
    complexity_range: [1, 10]
    priority_distribution:
      high: 0.2
      medium: 0.6
      low: 0.2
      
  bug_fix:
    complexity_range: [0.5, 5]
    urgency_distribution:
      critical: 0.1
      high: 0.3
      medium: 0.4
      low: 0.2
      
  technical_debt:
    complexity_range: [2, 8]
    impact_range: [1, 5]
```

### 環境約束
```yaml
constraints:
  github_api:
    rate_limit: 5000  # 每小時請求數
    response_time: [0.1, 0.5]  # 響應時間範圍
    
  ci_cd:
    build_time: [2, 10]  # 構建時間（分鐘）
    test_time: [1, 5]   # 測試時間
    deployment_time: [0.5, 2]  # 部署時間
    
  communication:
    notification_delay: [0, 2]  # 通知延遲
    response_time: [0.5, 24]   # 響應時間（小時）
```

## 📊 數據收集與分析

### 關鍵指標收集
```python
class MetricsCollector:
    def __init__(self):
        self.metrics = {
            'task_completion_time': [],
            'role_utilization': {},
            'communication_efficiency': [],
            'quality_metrics': []
        }
    
    def record_task_completion(self, task, start_time, end_time):
        """記錄任務完成時間"""
        duration = end_time - start_time
        self.metrics['task_completion_time'].append({
            'task_id': task.id,
            'type': task.type,
            'complexity': task.complexity,
            'duration': duration
        })
    
    def record_role_activity(self, role, activity, timestamp):
        """記錄角色活動"""
        if role not in self.metrics['role_utilization']:
            self.metrics['role_utilization'][role] = []
        
        self.metrics['role_utilization'][role].append({
            'activity': activity,
            'timestamp': timestamp
        })
```

### 性能分析工具
```python
class PerformanceAnalyzer:
    def __init__(self, metrics):
        self.metrics = metrics
        
    def calculate_throughput(self):
        """計算系統吞吐量"""
        completed_tasks = len(self.metrics['task_completion_time'])
        total_time = max(task['timestamp'] for task in completed_tasks)
        return completed_tasks / total_time
        
    def analyze_bottlenecks(self):
        """分析系統瓶頸"""
        role_workloads = {}
        for role, activities in self.metrics['role_utilization'].items():
            workload = sum(1 for activity in activities if activity['type'] == 'working')
            role_workloads[role] = workload
            
        return max(role_workloads, key=role_workloads.get)
```

## 🚀 使用實例

### 基本模擬運行
```python
# 創建模擬環境
simulator = BeeSwarmSimulator()

# 添加角色
simulator.add_role('pm', ProductManagerSimulator)
simulator.add_role('backend', BackendDeveloperSimulator)
simulator.add_role('frontend', FrontendDeveloperSimulator)
simulator.add_role('devops', DevOpsEngineerSimulator)

# 配置工作負載
simulator.configure_workload({
    'feature_requests_per_day': 2,
    'bug_reports_per_day': 1,
    'urgent_requests_rate': 0.1
})

# 運行模擬
results = simulator.run(duration=30)  # 30天模擬
```

### 場景比較分析
```python
# 比較不同協作模式
scenarios = [
    {'name': 'waterfall', 'parallel_development': False},
    {'name': 'agile', 'parallel_development': True, 'sprint_length': 7},
    {'name': 'continuous', 'continuous_deployment': True}
]

comparison_results = []
for scenario in scenarios:
    simulator.configure_scenario(scenario)
    result = simulator.run(duration=90)
    comparison_results.append({
        'scenario': scenario['name'],
        'throughput': result.throughput,
        'lead_time': result.average_lead_time,
        'quality': result.defect_rate
    })
```

## 實踐指南

### 設置模擬環境
1. **安裝依賴**
```bash
pip install simpy pandas matplotlib seaborn
```

2. **初始化模擬器**
```python
from bee_swarm_simulator import BeeSwarmSimulator

sim = BeeSwarmSimulator()
sim.load_config('config/default.yaml')
```

3. **運行基本模擬**
```python
results = sim.run_simulation(
    duration=30,
    output_dir='results/',
    verbose=True
)
```

### 自定義模擬場景
1. **創建自定義角色**
```python
class CustomDeveloper(DeveloperSimulator):
    def __init__(self, env, skills):
        super().__init__(env)
        self.skills = skills
        
    def estimate_task_time(self, task):
        skill_multiplier = self.skills.get(task.technology, 1.0)
        return task.complexity / skill_multiplier
```

2. **添加新的任務類型**
```python
class SecurityAuditTask(Task):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope
        self.required_skills = ['security', 'analysis']
```

### 分析模擬結果
```python
# 生成報告
analyzer = ResultAnalyzer(results)
analyzer.generate_report('output/simulation_report.html')

# 創建可視化
plotter = SimulationPlotter(results)
plotter.plot_throughput_trend()
plotter.plot_role_utilization()
plotter.plot_lead_time_distribution()
```

## 本章小結

### 關鍵要點
- **SimPy 框架**提供強大的離散事件模擬能力
- **模塊化設計**支持靈活的場景配置
- **數據驅動**的性能分析和優化
- **可視化工具**幫助理解模擬結果

### 與其他章節的關聯
- 第4章：角色定義為模擬器提供行為模型
- 第6章：模擬結果指導實際使用策略
- 第8章：真實案例驗證模擬準確性

### 下一步建議
1. 學習第6章的具體使用方法
2. 查看 scripts/ 目錄中的實際模擬腳本
3. 參考第8章的案例分析

## 參考資料

- [SimPy 官方文檔](https://simpy.readthedocs.io/)
- [離散事件模擬原理](https://en.wikipedia.org/wiki/Discrete-event_simulation)
- [軟件開發過程模擬](https://ieeexplore.ieee.org/document/software-simulation)
- [敏捷開發效率評估](https://agilealliance.org/agile101/) 