"""
Bee Swarm 真实世界项目仿真
展示 AI 角色容器从项目启动到完成的完整流程
"""

import simpy
import random
import time
from dataclasses import dataclass
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# 配置参数 - 快速测试版本
SIMULATION_TIME = 200  # 仿真时间（小时）
RANDOM_SEED = 42

@dataclass
class Milestone:
    """项目里程碑"""
    id: str
    name: str
    description: str
    target_date: float
    status: str  # planned, in_progress, completed
    completed_date: float = None
    tasks: List[str] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []

@dataclass
class Task:
    """开发任务"""
    id: str
    title: str
    description: str
    priority: str
    estimated_hours: float
    assigned_role: str
    status: str
    milestone: str
    created_time: float
    started_time: float = None
    completed_time: float = None
    output_files: List[str] = None
    
    def __post_init__(self):
        if self.output_files is None:
            self.output_files = []

@dataclass
class Role:
    """AI 角色"""
    name: str
    container_id: str
    skills: List[str]
    efficiency: float
    current_task: Task = None
    completed_tasks: List[Task] = None
    github_username: str = ""
    ai_tools: List[str] = None
    
    def __post_init__(self):
        if self.completed_tasks is None:
            self.completed_tasks = []
        if self.ai_tools is None:
            self.ai_tools = ["Gemini CLI", "Claude Code", "Rovo Dev CLI"]

class RealWorldSimulation:
    """真实世界项目仿真"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.random = random.Random(RANDOM_SEED)
        self.current_time = 0
        
        # 创建资源
        self.github_api = simpy.Resource(self.env, capacity=10)
        self.ai_tools = simpy.Resource(self.env, capacity=5)
        self.deployment_env = simpy.Resource(self.env, capacity=2)
        
        # 创建 AI 角色容器
        self.roles = {
            'pm-01': Role(
                name='Product Manager AI',
                container_id='pm-01',
                skills=['需求分析', '任务分解', '进度监控', '用户研究'],
                efficiency=0.9,
                github_username='pm_ai_001'
            ),
            'be-01': Role(
                name='Backend Developer AI',
                container_id='be-01',
                skills=['API开发', '数据库设计', '业务逻辑', '系统架构'],
                efficiency=0.85,
                github_username='backend_ai_001'
            ),
            'fe-01': Role(
                name='Frontend Developer AI',
                container_id='fe-01',
                skills=['界面开发', '用户体验', '响应式设计', '前端架构'],
                efficiency=0.85,
                github_username='frontend_ai_001'
            ),
            'de-01': Role(
                name='DevOps Engineer AI',
                container_id='de-01',
                skills=['部署', '监控', '运维', '安全'],
                efficiency=0.8,
                github_username='devops_ai_001'
            )
        }
        
        # 项目里程碑
        self.milestones = [
            Milestone(
                id="M1",
                name="项目启动",
                description="项目可行性分析和环境搭建",
                target_date=20,
                status="planned"
            ),
            Milestone(
                id="M2", 
                name="MVP 开发",
                description="最小可行产品开发",
                target_date=80,
                status="planned"
            ),
            Milestone(
                id="M3",
                name="Release 1.0",
                description="第一个正式版本发布",
                target_date=140,
                status="planned"
            ),
            Milestone(
                id="M4",
                name="Release 1.1",
                description="功能增强版本",
                target_date=180,
                status="planned"
            )
        ]
        
        # 任务队列和完成的任务
        self.task_queue = []
        self.completed_tasks = []
        
        # 项目状态
        self.project_status = {
            'current_milestone': 0,
            'total_tasks': 0,
            'completed_tasks': 0,
            'github_commits': 0,
            'pull_requests': 0,
            'deployments': 0,
            'communication_events': 0
        }
        
        # 事件日志
        self.event_log = []
        
    def log_event(self, role_id: str, event_type: str, description: str, duration: float = 0):
        """记录事件"""
        event = {
            'time': self.env.now,
            'role_id': role_id,
            'event_type': event_type,
            'description': description,
            'duration': duration
        }
        self.event_log.append(event)
        print(f"[{self.env.now:6.1f}h] {self.roles[role_id].name}: {description}")
    
    def generate_project_tasks(self):
        """生成项目任务"""
        task_templates = [
            # 项目启动阶段 (M1)
            {
                'title': '项目可行性分析',
                'description': '分析教育游戏项目的可行性',
                'priority': 'high',
                'estimated_hours': 8,
                'assigned_role': 'pm-01',
                'milestone': 'M1',
                'output_files': ['feasibility_report.md', 'market_analysis.md']
            },
            {
                'title': '环境配置',
                'description': '配置开发环境和容器',
                'priority': 'high',
                'estimated_hours': 6,
                'assigned_role': 'de-01',
                'milestone': 'M1',
                'output_files': ['docker-compose.yml', 'env.config']
            },
            {
                'title': '需求分析',
                'description': '详细分析用户需求',
                'priority': 'high',
                'estimated_hours': 12,
                'assigned_role': 'pm-01',
                'milestone': 'M1',
                'output_files': ['requirements.md', 'user_stories.md']
            },
            
            # MVP 开发阶段 (M2)
            {
                'title': '数据库设计',
                'description': '设计用户和游戏数据表',
                'priority': 'high',
                'estimated_hours': 10,
                'assigned_role': 'be-01',
                'milestone': 'M2',
                'output_files': ['database_schema.sql', 'api_design.md']
            },
            {
                'title': '用户注册 API',
                'description': '实现用户注册和登录 API',
                'priority': 'high',
                'estimated_hours': 16,
                'assigned_role': 'be-01',
                'milestone': 'M2',
                'output_files': ['auth_controller.js', 'user_model.js']
            },
            {
                'title': '用户界面设计',
                'description': '设计注册和登录界面',
                'priority': 'high',
                'estimated_hours': 12,
                'assigned_role': 'fe-01',
                'milestone': 'M2',
                'output_files': ['login_component.jsx', 'register_component.jsx']
            },
            {
                'title': '基础游戏功能',
                'description': '实现基础的角色养成功能',
                'priority': 'high',
                'estimated_hours': 20,
                'assigned_role': 'be-01',
                'milestone': 'M2',
                'output_files': ['game_controller.js', 'character_model.js']
            },
            
            # Release 1.0 阶段 (M3)
            {
                'title': '学习系统开发',
                'description': '实现学习进度和成绩系统',
                'priority': 'high',
                'estimated_hours': 18,
                'assigned_role': 'be-01',
                'milestone': 'M3',
                'output_files': ['study_controller.js', 'progress_model.js']
            },
            {
                'title': '学习界面开发',
                'description': '开发学习界面和进度展示',
                'priority': 'high',
                'estimated_hours': 16,
                'assigned_role': 'fe-01',
                'milestone': 'M3',
                'output_files': ['study_page.jsx', 'progress_chart.jsx']
            },
            {
                'title': '生产环境部署',
                'description': '部署到生产环境',
                'priority': 'high',
                'estimated_hours': 8,
                'assigned_role': 'de-01',
                'milestone': 'M3',
                'output_files': ['deployment.yml', 'monitoring.conf']
            },
            
            # Release 1.1 阶段 (M4)
            {
                'title': '家长监控功能',
                'description': '实现家长监控孩子学习进度',
                'priority': 'medium',
                'estimated_hours': 14,
                'assigned_role': 'be-01',
                'milestone': 'M4',
                'output_files': ['parent_controller.js', 'report_model.js']
            },
            {
                'title': '家长界面开发',
                'description': '开发家长监控界面',
                'priority': 'medium',
                'estimated_hours': 12,
                'assigned_role': 'fe-01',
                'milestone': 'M4',
                'output_files': ['parent_dashboard.jsx', 'report_view.jsx']
            },
            {
                'title': '性能优化',
                'description': '优化系统性能',
                'priority': 'medium',
                'estimated_hours': 10,
                'assigned_role': 'de-01',
                'milestone': 'M4',
                'output_files': ['performance_report.md', 'optimization.conf']
            }
        ]
        
        for i, template in enumerate(task_templates):
            task = Task(
                id=f"TASK-{i+1:03d}",
                title=template['title'],
                description=template['description'],
                priority=template['priority'],
                estimated_hours=template['estimated_hours'],
                assigned_role=template['assigned_role'],
                status='pending',
                milestone=template['milestone'],
                created_time=self.env.now,
                output_files=template['output_files']
            )
            self.task_queue.append(task)
            self.project_status['total_tasks'] += 1
    
    def product_manager_process(self):
        """产品经理工作流程"""
        role_id = 'pm-01'
        role = self.roles[role_id]
        
        while True:
            # 检查当前里程碑
            current_milestone = self.milestones[self.project_status['current_milestone']]
            
            # 里程碑规划
            if current_milestone.status == 'planned':
                self.log_event(role_id, 'milestone_planning', f'开始规划里程碑: {current_milestone.name}')
                
                # 使用 AI 工具进行规划
                with self.ai_tools.request() as request:
                    yield request
                    planning_time = self.random.uniform(2, 4)
                    yield self.env.timeout(planning_time)
                    self.log_event(role_id, 'ai_planning', f'使用 {role.ai_tools[0]} 进行里程碑规划', planning_time)
                
                current_milestone.status = 'in_progress'
                self.log_event(role_id, 'milestone_start', f'里程碑 {current_milestone.name} 开始执行')
            
            # 任务分配
            pending_tasks = [task for task in self.task_queue 
                           if task.milestone == current_milestone.id and task.status == 'pending']
            
            if pending_tasks:
                task = pending_tasks[0]
                self.log_event(role_id, 'task_assignment', f'分配任务: {task.title}')
                
                # 创建 GitHub Issue
                with self.github_api.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.1, 0.3))
                    self.project_status['github_commits'] += 1
                
                self.project_status['communication_events'] += 1
            
            # 进度监控
            yield self.env.timeout(self.random.uniform(4, 6))
            
            # 检查里程碑完成情况
            milestone_tasks = [task for task in self.completed_tasks 
                             if task.milestone == current_milestone.id]
            if len(milestone_tasks) >= 3:  # 假设每个里程碑需要完成3个任务
                current_milestone.status = 'completed'
                current_milestone.completed_date = self.env.now
                self.log_event(role_id, 'milestone_complete', f'里程碑 {current_milestone.name} 完成!')
                
                # 移动到下一个里程碑
                if self.project_status['current_milestone'] < len(self.milestones) - 1:
                    self.project_status['current_milestone'] += 1
                    self.log_event(role_id, 'milestone_transition', f'进入下一个里程碑: {self.milestones[self.project_status["current_milestone"]].name}')
    
    def developer_process(self, role_id):
        """开发者工作流程"""
        role = self.roles[role_id]
        
        while True:
            # 查找分配给该角色的任务
            assigned_tasks = [task for task in self.task_queue 
                            if task.assigned_role == role_id and task.status == 'pending']
            
            if assigned_tasks:
                task = assigned_tasks[0]
                task.status = 'in_progress'
                task.started_time = self.env.now
                role.current_task = task
                
                self.log_event(role_id, 'task_start', f'开始任务: {task.title}')
                
                # 使用 AI 工具进行开发
                with self.ai_tools.request() as request:
                    yield request
                    ai_time = self.random.uniform(1, 3)
                    yield self.env.timeout(ai_time)
                    self.log_event(role_id, 'ai_development', f'使用 {role.ai_tools[0]} 辅助开发', ai_time)
                
                # 开发时间
                development_time = task.estimated_hours / role.efficiency
                development_time += self.random.uniform(-1, 2)
                yield self.env.timeout(development_time)
                
                # 代码质量检查
                quality_check = self.random.random()
                if quality_check < 0.9:  # 90% 通过率
                    fix_time = self.random.uniform(1, 3)
                    yield self.env.timeout(fix_time)
                    self.log_event(role_id, 'quality_fix', f'修复代码质量问题', fix_time)
                
                # 提交代码到 GitHub
                with self.github_api.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.1, 0.3))
                    self.project_status['github_commits'] += 1
                
                # 创建 Pull Request
                with self.github_api.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.2, 0.5))
                    self.project_status['pull_requests'] += 1
                
                # 代码审查
                review_time = self.random.uniform(1, 2)
                yield self.env.timeout(review_time)
                
                # 完成任务
                task.status = 'completed'
                task.completed_time = self.env.now
                role.completed_tasks.append(task)
                self.completed_tasks.append(task)
                self.task_queue.remove(task)
                
                self.project_status['completed_tasks'] += 1
                self.log_event(role_id, 'task_complete', f'完成任务: {task.title} (产出: {len(task.output_files)} 个文件)')
                
                role.current_task = None
            else:
                # 等待新任务
                yield self.env.timeout(self.random.uniform(2, 4))
    
    def devops_process(self):
        """DevOps 工程师工作流程"""
        role_id = 'de-01'
        role = self.roles[role_id]
        
        while True:
            # 检查是否有需要部署的里程碑
            completed_milestones = [m for m in self.milestones if m.status == 'completed']
            
            for milestone in completed_milestones:
                if milestone.id in ['M3', 'M4']:  # 只有 M3 和 M4 需要部署
                    self.log_event(role_id, 'deployment_start', f'开始部署里程碑: {milestone.name}')
                    
                    # 准备部署环境
                    with self.deployment_env.request() as request:
                        yield request
                        
                        # 环境配置
                        config_time = self.random.uniform(1, 2)
                        yield self.env.timeout(config_time)
                        self.log_event(role_id, 'env_config', '配置部署环境', config_time)
                        
                        # 部署过程
                        deployment_time = self.random.uniform(2, 4)
                        yield self.env.timeout(deployment_time)
                        self.log_event(role_id, 'deployment_process', '执行部署流程', deployment_time)
                        
                        # 部署验证
                        verify_time = self.random.uniform(0.5, 1)
                        yield self.env.timeout(verify_time)
                        self.log_event(role_id, 'deployment_verify', '验证部署结果', verify_time)
                        
                        # 监控配置
                        monitor_time = self.random.uniform(1, 2)
                        yield self.env.timeout(monitor_time)
                        self.log_event(role_id, 'monitor_setup', '配置监控系统', monitor_time)
                        
                        self.project_status['deployments'] += 1
                        self.log_event(role_id, 'deployment_complete', f'里程碑 {milestone.name} 部署完成!')
            
            # 系统监控
            yield self.env.timeout(self.random.uniform(4, 6))
    
    def run_simulation(self):
        """运行仿真"""
        print("="*60)
        print("🐝 Bee Swarm 真实世界项目仿真")
        print("="*60)
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"AI 角色容器: {len(self.roles)} 个")
        print(f"项目里程碑: {len(self.milestones)} 个")
        print("="*60)
        
        # 生成项目任务
        self.generate_project_tasks()
        print(f"生成任务: {self.project_status['total_tasks']} 个")
        
        # 启动各个角色的工作流程
        self.env.process(self.product_manager_process())
        self.env.process(self.developer_process('be-01'))
        self.env.process(self.developer_process('fe-01'))
        self.env.process(self.devops_process())
        
        # 运行仿真
        start_time = time.time()
        self.env.run(until=SIMULATION_TIME)
        end_time = time.time()
        
        # 输出结果
        self.print_results(end_time - start_time)
        self.generate_project_timeline()
    
    def print_results(self, real_time):
        """输出仿真结果"""
        print("\n" + "="*60)
        print("📊 仿真结果")
        print("="*60)
        
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"实际运行时间: {real_time:.2f} 秒")
        print(f"总任务数: {self.project_status['total_tasks']}")
        print(f"完成任务数: {self.project_status['completed_tasks']}")
        print(f"完成率: {self.project_status['completed_tasks']/self.project_status['total_tasks']*100:.1f}%")
        
        print(f"\n📈 项目活动:")
        print(f"  GitHub 提交: {self.project_status['github_commits']}")
        print(f"  Pull Requests: {self.project_status['pull_requests']}")
        print(f"  部署次数: {self.project_status['deployments']}")
        print(f"  沟通事件: {self.project_status['communication_events']}")
        
        print(f"\n🎯 里程碑状态:")
        for milestone in self.milestones:
            status_icon = "✅" if milestone.status == 'completed' else "🔄" if milestone.status == 'in_progress' else "⏳"
            print(f"  {status_icon} {milestone.name}: {milestone.status}")
            if milestone.completed_date:
                print(f"    完成时间: {milestone.completed_date:.1f} 小时")
        
        print(f"\n👥 角色工作量:")
        for role_id, role in self.roles.items():
            work_time = sum(task.completed_time - task.started_time for task in role.completed_tasks)
            utilization = work_time / SIMULATION_TIME * 100
            print(f"  {role.name}: {utilization:.1f}% ({len(role.completed_tasks)} 个任务)")
    
    def generate_project_timeline(self):
        """生成项目时间线图表"""
        plt.figure(figsize=(15, 10))
        
        # 创建时间线
        plt.subplot(2, 1, 1)
        
        # 绘制里程碑
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, milestone in enumerate(self.milestones):
            if milestone.completed_date:
                plt.axvline(x=milestone.completed_date, color=colors[i], linestyle='--', alpha=0.7)
                plt.text(milestone.completed_date, 0.8, milestone.name, rotation=90, 
                        color=colors[i], fontweight='bold')
        
        # 绘制任务完成时间
        task_times = [task.completed_time for task in self.completed_tasks]
        task_names = [task.title[:20] + '...' if len(task.title) > 20 else task.title 
                     for task in self.completed_tasks]
        
        plt.scatter(task_times, [0.5] * len(task_times), alpha=0.6, s=50)
        for i, (time, name) in enumerate(zip(task_times, task_names)):
            plt.annotate(name, (time, 0.5), xytext=(5, 5), textcoords='offset points', 
                        fontsize=8, alpha=0.8)
        
        plt.xlabel('时间 (小时)')
        plt.ylabel('项目进度')
        plt.title('项目时间线 - 里程碑和任务完成')
        plt.grid(True, alpha=0.3)
        
        # 角色工作量分布
        plt.subplot(2, 1, 2)
        role_names = [role.name for role in self.roles.values()]
        role_tasks = [len(role.completed_tasks) for role in self.roles.values()]
        
        bars = plt.bar(role_names, role_tasks, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        plt.xlabel('AI 角色')
        plt.ylabel('完成任务数')
        plt.title('角色工作量分布')
        
        # 添加数值标签
        for bar, value in zip(bars, role_tasks):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('project_timeline.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """主函数"""
    print("🚀 启动 Bee Swarm 真实世界项目仿真...")
    
    # 创建仿真实例
    simulation = RealWorldSimulation()
    
    # 运行仿真
    simulation.run_simulation()

if __name__ == "__main__":
    main() 