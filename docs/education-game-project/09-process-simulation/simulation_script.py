"""
Bee Swarm 软件开发流程仿真脚本
使用 SimPy 模拟 AI 角色协作的软件开发流程
"""

import simpy
import random
import statistics
from dataclasses import dataclass
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import pandas as pd

# 配置参数
SIMULATION_TIME = 1000  # 仿真时间（小时）
RANDOM_SEED = 42

@dataclass
class Task:
    """任务数据类"""
    id: str
    title: str
    description: str
    priority: str  # high, medium, low
    estimated_hours: float
    assigned_role: str
    status: str  # pending, in_progress, review, completed
    created_time: float
    started_time: float = None
    completed_time: float = None

@dataclass
class Role:
    """AI 角色数据类"""
    name: str
    skills: List[str]
    efficiency: float  # 0.0-1.0
    current_task: Task = None
    completed_tasks: List[Task] = None
    
    def __post_init__(self):
        if self.completed_tasks is None:
            self.completed_tasks = []

class BeeSwarmSimulation:
    """Bee Swarm 软件开发流程仿真"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.random = random.Random(RANDOM_SEED)
        
        # 创建资源
        self.github_api = simpy.Resource(self.env, capacity=10)  # GitHub API 限制
        self.ai_tools = simpy.Resource(self.env, capacity=5)     # AI 工具池
        self.deployment_env = simpy.Resource(self.env, capacity=2)  # 部署环境
        
        # 创建 AI 角色
        self.roles = {
            'product_manager': Role(
                name='Product Manager',
                skills=['需求分析', '任务分解', '进度监控'],
                efficiency=0.9
            ),
            'backend_dev': Role(
                name='Backend Developer',
                skills=['API开发', '数据库设计', '业务逻辑'],
                efficiency=0.85
            ),
            'frontend_dev': Role(
                name='Frontend Developer',
                skills=['界面开发', '用户体验', '响应式设计'],
                efficiency=0.85
            ),
            'devops_engineer': Role(
                name='DevOps Engineer',
                skills=['部署', '监控', '运维'],
                efficiency=0.8
            )
        }
        
        # 任务队列
        self.task_queue = []
        self.completed_tasks = []
        
        # 统计数据
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'total_time': 0,
            'role_utilization': {},
            'task_duration': [],
            'communication_events': 0,
            'quality_issues': 0
        }
    
    def generate_tasks(self):
        """生成项目任务"""
        task_templates = [
            {
                'title': '用户注册功能',
                'description': '实现用户注册、登录、密码重置功能',
                'priority': 'high',
                'estimated_hours': 12,
                'assigned_role': 'backend_dev'
            },
            {
                'title': '用户界面设计',
                'description': '设计用户注册和登录界面',
                'priority': 'high',
                'estimated_hours': 8,
                'assigned_role': 'frontend_dev'
            },
            {
                'title': '数据库设计',
                'description': '设计用户表和相关索引',
                'priority': 'high',
                'estimated_hours': 6,
                'assigned_role': 'backend_dev'
            },
            {
                'title': '部署配置',
                'description': '配置生产环境部署',
                'priority': 'medium',
                'estimated_hours': 4,
                'assigned_role': 'devops_engineer'
            },
            {
                'title': '需求分析',
                'description': '分析用户需求并创建需求文档',
                'priority': 'high',
                'estimated_hours': 6,
                'assigned_role': 'product_manager'
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
                created_time=self.env.now
            )
            self.task_queue.append(task)
            self.stats['total_tasks'] += 1
    
    def product_manager_process(self):
        """产品经理工作流程"""
        while True:
            # 等待新任务或检查进度
            if self.task_queue:
                # 分析需求
                yield self.env.timeout(self.random.uniform(2, 4))
                
                # 使用 AI 工具
                with self.ai_tools.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.5, 2))
                
                # 创建 GitHub Issues
                with self.github_api.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.1, 0.5))
                
                self.stats['communication_events'] += 1
                
                # 任务分解
                yield self.env.timeout(self.random.uniform(1, 3))
            
            # 进度监控
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def developer_process(self, role_name):
        """开发者工作流程"""
        role = self.roles[role_name]
        
        while True:
            # 查找分配给该角色的任务
            assigned_tasks = [task for task in self.task_queue 
                            if task.assigned_role == role_name and task.status == 'pending']
            
            if assigned_tasks:
                task = assigned_tasks[0]
                task.status = 'in_progress'
                task.started_time = self.env.now
                role.current_task = task
                
                # 开发时间（考虑效率因素）
                development_time = task.estimated_hours / role.efficiency
                development_time += self.random.uniform(-1, 1)  # 添加随机性
                
                yield self.env.timeout(development_time)
                
                # 使用 AI 工具辅助开发
                with self.ai_tools.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.5, 2))
                
                # 代码质量检查
                quality_check = self.random.random()
                if quality_check < 0.9:  # 90% 通过率
                    # 需要修复问题
                    self.stats['quality_issues'] += 1
                    fix_time = self.random.uniform(1, 4)
                    yield self.env.timeout(fix_time)
                
                # 提交代码到 GitHub
                with self.github_api.request() as request:
                    yield request
                    yield self.env.timeout(self.random.uniform(0.1, 0.5))
                
                # 代码审查
                review_time = self.random.uniform(1, 3)
                yield self.env.timeout(review_time)
                
                # 完成任务
                task.status = 'completed'
                task.completed_time = self.env.now
                role.completed_tasks.append(task)
                self.completed_tasks.append(task)
                self.task_queue.remove(task)
                
                self.stats['completed_tasks'] += 1
                self.stats['task_duration'].append(task.completed_time - task.started_time)
                
                role.current_task = None
            else:
                # 等待新任务
                yield self.env.timeout(self.random.uniform(1, 3))
    
    def devops_process(self):
        """DevOps 工程师工作流程"""
        while True:
            # 检查是否有需要部署的代码
            completed_backend = [task for task in self.completed_tasks 
                               if task.assigned_role == 'backend_dev' and task.status == 'completed']
            completed_frontend = [task for task in self.completed_tasks 
                                if task.assigned_role == 'frontend_dev' and task.status == 'completed']
            
            if completed_backend or completed_frontend:
                # 准备部署环境
                with self.deployment_env.request() as request:
                    yield request
                    
                    # 环境配置
                    yield self.env.timeout(self.random.uniform(1, 2))
                    
                    # 部署过程
                    deployment_time = self.random.uniform(2, 4)
                    yield self.env.timeout(deployment_time)
                    
                    # 部署验证
                    yield self.env.timeout(self.random.uniform(0.5, 1))
                    
                    # 监控配置
                    yield self.env.timeout(self.random.uniform(1, 2))
            
            # 系统监控
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def communication_process(self):
        """角色间沟通流程"""
        while True:
            # 模拟角色间的沟通事件
            communication_interval = self.random.uniform(4, 8)
            yield self.env.timeout(communication_interval)
            
            # 使用 GitHub API 进行沟通
            with self.github_api.request() as request:
                yield request
                yield self.env.timeout(self.random.uniform(0.1, 0.3))
            
            self.stats['communication_events'] += 1
    
    def run_simulation(self):
        """运行仿真"""
        print("开始 Bee Swarm 软件开发流程仿真...")
        
        # 生成初始任务
        self.generate_tasks()
        
        # 启动各个角色的工作流程
        self.env.process(self.product_manager_process())
        self.env.process(self.developer_process('backend_dev'))
        self.env.process(self.developer_process('frontend_dev'))
        self.env.process(self.devops_process())
        self.env.process(self.communication_process())
        
        # 运行仿真
        self.env.run(until=SIMULATION_TIME)
        
        # 计算统计数据
        self.calculate_statistics()
        
        # 输出结果
        self.print_results()
        
        # 生成可视化图表
        self.generate_visualizations()
    
    def calculate_statistics(self):
        """计算统计数据"""
        self.stats['total_time'] = SIMULATION_TIME
        
        # 计算角色利用率
        for role_name, role in self.roles.items():
            total_work_time = sum(task.completed_time - task.started_time 
                                for task in role.completed_tasks)
            utilization = total_work_time / SIMULATION_TIME
            self.stats['role_utilization'][role_name] = utilization
    
    def print_results(self):
        """输出仿真结果"""
        print("\n" + "="*50)
        print("仿真结果")
        print("="*50)
        
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"总任务数: {self.stats['total_tasks']}")
        print(f"完成任务数: {self.stats['completed_tasks']}")
        print(f"完成率: {self.stats['completed_tasks']/self.stats['total_tasks']*100:.1f}%")
        
        if self.stats['task_duration']:
            avg_duration = statistics.mean(self.stats['task_duration'])
            print(f"平均任务时长: {avg_duration:.2f} 小时")
        
        print(f"沟通事件数: {self.stats['communication_events']}")
        print(f"质量问题数: {self.stats['quality_issues']}")
        
        print("\n角色利用率:")
        for role_name, utilization in self.stats['role_utilization'].items():
            print(f"  {role_name}: {utilization*100:.1f}%")
    
    def generate_visualizations(self):
        """生成可视化图表"""
        # 角色利用率饼图
        plt.figure(figsize=(10, 6))
        
        plt.subplot(1, 2, 1)
        role_names = list(self.stats['role_utilization'].keys())
        utilizations = list(self.stats['role_utilization'].values())
        plt.pie(utilizations, labels=role_names, autopct='%1.1f%%')
        plt.title('角色利用率')
        
        # 任务完成时间分布
        plt.subplot(1, 2, 2)
        if self.stats['task_duration']:
            plt.hist(self.stats['task_duration'], bins=10, alpha=0.7)
            plt.xlabel('任务时长 (小时)')
            plt.ylabel('任务数量')
            plt.title('任务完成时间分布')
        
        plt.tight_layout()
        plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """主函数"""
    # 创建仿真实例
    simulation = BeeSwarmSimulation()
    
    # 运行仿真
    simulation.run_simulation()

if __name__ == "__main__":
    main() 