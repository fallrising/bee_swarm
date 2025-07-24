"""
Bee Swarm 事件驱动仿真
基于 SimPy 离散事件模拟，提供详细的事件日志和统计
"""

import simpy
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
from enum import Enum

# 配置参数
SIMULATION_TIME = 100
RANDOM_SEED = 42

class EventType(Enum):
    """事件类型枚举"""
    HUMAN_ISSUE_CREATED = "人类创建Issue"
    PM_ANALYSIS_START = "PM开始分析"
    PM_ANALYSIS_COMPLETE = "PM分析完成"
    TASK_ASSIGNED = "任务分配"
    DEVELOPER_START_TASK = "开发者开始任务"
    AI_TOOL_USED = "AI工具使用"
    API_DOC_CREATED = "API文档创建"
    PR_CREATED = "PR创建"
    CODE_REVIEW_START = "代码审查开始"
    CODE_REVIEW_COMPLETE = "代码审查完成"
    UAT_START = "UAT开始"
    UAT_COMPLETE = "UAT完成"
    DEPLOYMENT_START = "部署开始"
    DEPLOYMENT_COMPLETE = "部署完成"
    DAILY_REPORT_GENERATED = "日报生成"
    GITHUB_COMMENT_ADDED = "GitHub评论添加"
    DEFAULT_TASK_EXECUTED = "默认任务执行"

@dataclass
class GitHubIssue:
    """GitHub Issue"""
    id: str
    title: str
    description: str
    created_by: str
    created_time: float
    status: str
    assigned_to: Optional[str] = None
    comments: List[Dict] = field(default_factory=list)
    
    def add_comment(self, author: str, content: str, time: float):
        """添加评论"""
        self.comments.append({
            'author': author,
            'content': content,
            'time': time
        })

@dataclass
class PullRequest:
    """Pull Request"""
    id: str
    title: str
    created_by: str
    created_time: float
    status: str
    comments: List[Dict] = field(default_factory=list)
    review_status: str = 'pending'
    
    def add_comment(self, author: str, content: str, time: float):
        """添加评论"""
        self.comments.append({
            'author': author,
            'content': content,
            'time': time
        })

@dataclass
class Task:
    """开发任务"""
    id: str
    title: str
    assigned_role: str
    status: str
    issue_id: str
    created_time: float
    started_time: Optional[float] = None
    completed_time: Optional[float] = None
    total_duration: Optional[float] = None

@dataclass
class Role:
    """AI 角色"""
    name: str
    container_id: str
    github_username: str
    default_tasks: List[str] = field(default_factory=list)
    completed_tasks: List[Task] = field(default_factory=list)
    daily_reports: int = 0
    total_work_time: float = 0.0
    ai_tool_usage_time: float = 0.0

@dataclass
class SimulationEvent:
    """仿真事件"""
    time: float
    event_type: EventType
    role_id: str
    description: str
    duration: Optional[float] = None
    resources_used: List[str] = field(default_factory=list)

class BeeSwarmEventDrivenSimulation:
    """Bee Swarm 事件驱动仿真"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.random = random.Random(RANDOM_SEED)
        
        # 创建资源 - 模拟真实限制
        self.github_api = simpy.Resource(self.env, capacity=3)
        self.ai_tools = simpy.Resource(self.env, capacity=2)
        self.deployment_env = simpy.Resource(self.env, capacity=1)
        self.code_reviewers = simpy.Resource(self.env, capacity=2)
        
        # 创建 AI 角色容器
        self.roles = {
            'pm-01': Role(
                name='Product Manager AI',
                container_id='pm-01',
                github_username='pm_ai_001',
                default_tasks=['热门新闻爬虫', '用户反馈分析', '竞品监控']
            ),
            'be-01': Role(
                name='Backend Developer AI',
                container_id='be-01',
                github_username='backend_ai_001',
                default_tasks=['API性能优化', '数据库维护', '系统监控']
            ),
            'fe-01': Role(
                name='Frontend Developer AI',
                container_id='fe-01',
                github_username='frontend_ai_001',
                default_tasks=['UI组件库维护', '性能优化', '用户体验分析']
            ),
            'de-01': Role(
                name='DevOps Engineer AI',
                container_id='de-01',
                github_username='devops_ai_001',
                default_tasks=['系统监控', '安全扫描', '性能分析']
            )
        }
        
        # 数据存储
        self.github_issues = []
        self.pull_requests = []
        self.tasks = []
        self.event_log = []
        
        # 项目状态
        self.project_status = {
            'total_issues': 0,
            'total_prs': 0,
            'communication_events': 0,
            'api_docs_created': 0,
            'daily_reports': 0,
            'total_events': 0
        }
        
        # 控制标志
        self.issue_processed = False
        
    def log_event(self, event_type: EventType, role_id: str, description: str, 
                  duration: Optional[float] = None, resources: Optional[List[str]] = None):
        """记录详细事件"""
        event = SimulationEvent(
            time=self.env.now,
            event_type=event_type,
            role_id=role_id,
            description=description,
            duration=duration,
            resources_used=resources or []
        )
        self.event_log.append(event)
        self.project_status['total_events'] += 1
        
        # 格式化输出
        time_str = f"[{self.env.now:6.1f}h]"
        role_str = f"{self.roles[role_id].name}"
        event_str = f"{event_type.value}"
        desc_str = f"{description}"
        
        if duration:
            print(f"{time_str} {role_str}: {event_str} - {desc_str} (耗时: {duration:.1f}h)")
        else:
            print(f"{time_str} {role_str}: {event_str} - {desc_str}")
    
    def human_po_process(self):
        """人类 PO 发布任务流程"""
        while True:
            if self.env.now < 15 and not self.issue_processed:
                issue = GitHubIssue(
                    id=f"ISSUE-{len(self.github_issues)+1:03d}",
                    title="开发教育游戏用户注册功能",
                    description="需要实现用户注册、登录、密码重置功能",
                    created_by="human_po",
                    created_time=self.env.now,
                    status="open"
                )
                self.github_issues.append(issue)
                self.project_status['total_issues'] += 1
                
                self.log_event(EventType.HUMAN_ISSUE_CREATED, 'pm-01', 
                              f"人类 PO 发布任务: {issue.title}")
                self.issue_processed = True
            
            yield self.env.timeout(self.random.uniform(20, 30))
    
    def product_manager_process(self):
        """产品经理 AI 工作流程"""
        role_id = 'pm-01'
        role = self.roles[role_id]
        
        while True:
            # 检查新的 GitHub Issues
            new_issues = [issue for issue in self.github_issues 
                         if issue.status == 'open' and not issue.assigned_to]
            
            if new_issues:
                issue = new_issues[0]
                issue.assigned_to = role_id
                issue.status = 'in_progress'
                
                self.log_event(EventType.PM_ANALYSIS_START, role_id, 
                              f"开始处理任务: {issue.title}")
                
                # 使用 AI 工具分析需求
                with self.ai_tools.request() as request:
                    yield request
                    analysis_time = self.random.uniform(2, 4)
                    yield self.env.timeout(analysis_time)
                    role.ai_tool_usage_time += analysis_time
                    role.total_work_time += analysis_time
                    
                    self.log_event(EventType.AI_TOOL_USED, role_id, 
                                  f"使用 Gemini CLI 分析需求", analysis_time, ['ai_tools'])
                
                self.log_event(EventType.PM_ANALYSIS_COMPLETE, role_id, 
                              f"完成需求分析: {issue.title}")
                
                # 生成 PRD 并添加评论
                with self.github_api.request() as request:
                    yield request
                    comment_time = self.random.uniform(0.1, 0.3)
                    yield self.env.timeout(comment_time)
                    role.total_work_time += comment_time
                    
                    issue.add_comment(
                        role.github_username,
                        "📋 PRD 已生成：用户注册流程设计、邮箱验证机制、密码安全策略",
                        self.env.now
                    )
                    self.project_status['communication_events'] += 1
                    
                    self.log_event(EventType.GITHUB_COMMENT_ADDED, role_id, 
                                  f"在 Issue #{issue.id} 添加 PRD 评论", comment_time, ['github_api'])
                
                # 创建开发任务
                yield from self.create_development_tasks(issue)
                
            # 检查 PR 状态，进行 UAT 测试
            pending_prs = [pr for pr in self.pull_requests if pr.status == 'open']
            for pr in pending_prs:
                if pr.review_status == 'approved':
                    uat_time = self.random.uniform(1, 2)
                    yield self.env.timeout(uat_time)
                    role.total_work_time += uat_time
                    
                    self.log_event(EventType.UAT_START, role_id, 
                                  f"对 PR #{pr.id} 进行 UAT 测试", uat_time)
                    
                    with self.github_api.request() as request:
                        yield request
                        comment_time = self.random.uniform(0.1, 0.3)
                        yield self.env.timeout(comment_time)
                        role.total_work_time += comment_time
                        
                        pr.add_comment(
                            role.github_username,
                            "✅ UAT 测试通过，功能符合需求",
                            self.env.now
                        )
                        pr.status = 'merged'
                        self.project_status['communication_events'] += 1
                        
                        self.log_event(EventType.GITHUB_COMMENT_ADDED, role_id, 
                                      f"在 PR #{pr.id} 添加 UAT 结果", comment_time, ['github_api'])
                    
                    self.log_event(EventType.UAT_COMPLETE, role_id, 
                                  f"完成 PR #{pr.id} 的 UAT 测试")
            
            # 执行默认任务
            if not new_issues and not pending_prs:
                default_task = self.random.choice(role.default_tasks)
                default_time = self.random.uniform(1, 3)
                yield self.env.timeout(default_time)
                role.total_work_time += default_time
                
                self.log_event(EventType.DEFAULT_TASK_EXECUTED, role_id, 
                              f"执行默认任务: {default_task}", default_time)
            
            # 生成日报
            if int(self.env.now) % 24 == 0 and self.env.now > 0:
                yield from self.generate_daily_report(role_id)
            
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def create_development_tasks(self, issue: GitHubIssue):
        """创建开发任务"""
        task_templates = [
            {'title': '后端 API 设计', 'assigned_role': 'be-01'},
            {'title': '数据库设计', 'assigned_role': 'be-01'},
            {'title': '前端注册界面', 'assigned_role': 'fe-01'}
        ]
        
        for template in task_templates:
            task = Task(
                id=f"TASK-{len(self.tasks)+1:03d}",
                title=template['title'],
                assigned_role=template['assigned_role'],
                status='pending',
                issue_id=issue.id,
                created_time=self.env.now
            )
            self.tasks.append(task)
            
            # 在 GitHub Issue 中分配任务
            with self.github_api.request() as request:
                yield request
                comment_time = self.random.uniform(0.1, 0.3)
                yield self.env.timeout(comment_time)
                
                issue.add_comment(
                    self.roles[template['assigned_role']].github_username,
                    f"🎯 任务分配: {template['title']}",
                    self.env.now
                )
                self.project_status['communication_events'] += 1
                
                self.log_event(EventType.GITHUB_COMMENT_ADDED, 'pm-01', 
                              f"分配任务 {template['title']} 给 {self.roles[template['assigned_role']].name}", 
                              comment_time, ['github_api'])
            
            self.log_event(EventType.TASK_ASSIGNED, 'pm-01', 
                          f"创建任务: {template['title']} -> {self.roles[template['assigned_role']].name}")
    
    def developer_process(self, role_id):
        """开发者工作流程"""
        role = self.roles[role_id]
        
        while True:
            # 检查分配给该角色的任务
            assigned_tasks = [task for task in self.tasks 
                            if task.assigned_role == role_id and task.status == 'pending']
            
            if assigned_tasks:
                task = assigned_tasks[0]
                task.status = 'in_progress'
                task.started_time = self.env.now
                
                self.log_event(EventType.DEVELOPER_START_TASK, role_id, 
                              f"开始任务: {task.title}")
                
                # 如果是前端开发者，查看 API 文档
                if role_id == 'fe-01':
                    review_time = self.random.uniform(0.5, 1)
                    yield self.env.timeout(review_time)
                    role.total_work_time += review_time
                    
                    self.log_event(EventType.AI_TOOL_USED, role_id, 
                                  "查看后端 API 文档", review_time)
                    
                    # 在 GitHub Issue 中提问
                    if self.random.random() < 0.3:
                        with self.github_api.request() as request:
                            yield request
                            comment_time = self.random.uniform(0.1, 0.3)
                            yield self.env.timeout(comment_time)
                            role.total_work_time += comment_time
                            
                            issue = next(i for i in self.github_issues if i.id == task.issue_id)
                            issue.add_comment(
                                role.github_username,
                                "❓ 关于 API 接口的疑问：错误码定义是否完整？",
                                self.env.now
                            )
                            self.project_status['communication_events'] += 1
                            
                            self.log_event(EventType.GITHUB_COMMENT_ADDED, role_id, 
                                          f"在 Issue #{issue.id} 提出 API 疑问", comment_time, ['github_api'])
                            
                            yield self.env.timeout(self.random.uniform(1, 3))
                
                # 使用 AI 工具进行开发
                with self.ai_tools.request() as request:
                    yield request
                    ai_time = self.random.uniform(2, 4)
                    yield self.env.timeout(ai_time)
                    role.ai_tool_usage_time += ai_time
                    role.total_work_time += ai_time
                    
                    self.log_event(EventType.AI_TOOL_USED, role_id, 
                                  f"使用 Gemini CLI 辅助开发", ai_time, ['ai_tools'])
                
                # 开发时间
                development_time = self.random.uniform(8, 16)
                yield self.env.timeout(development_time)
                role.total_work_time += development_time
                
                # 如果是后端开发者，创建 API 文档
                if role_id == 'be-01':
                    self.project_status['api_docs_created'] += 1
                    self.log_event(EventType.API_DOC_CREATED, role_id, 
                                  "创建 API 文档")
                
                # 创建 Pull Request
                with self.github_api.request() as request:
                    yield request
                    pr_time = self.random.uniform(0.2, 0.5)
                    yield self.env.timeout(pr_time)
                    role.total_work_time += pr_time
                    
                    pr = PullRequest(
                        id=f"PR-{len(self.pull_requests)+1:03d}",
                        title=f"实现 {task.title}",
                        created_by=role_id,
                        created_time=self.env.now,
                        status='open'
                    )
                    self.pull_requests.append(pr)
                    self.project_status['total_prs'] += 1
                    
                    self.log_event(EventType.PR_CREATED, role_id, 
                                  f"创建 PR: {pr.title}", pr_time, ['github_api'])
                
                task.status = 'completed'
                task.completed_time = self.env.now
                task.total_duration = task.completed_time - task.started_time
                role.completed_tasks.append(task)
                
            else:
                # 执行默认任务
                default_task = self.random.choice(role.default_tasks)
                default_time = self.random.uniform(1, 3)
                yield self.env.timeout(default_time)
                role.total_work_time += default_time
                
                self.log_event(EventType.DEFAULT_TASK_EXECUTED, role_id, 
                              f"执行默认任务: {default_task}", default_time)
            
            # 生成日报
            if int(self.env.now) % 24 == 0 and self.env.now > 0:
                yield from self.generate_daily_report(role_id)
            
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def code_review_process(self):
        """Code Review 流程"""
        while True:
            # 检查待审查的 PR
            pending_reviews = [pr for pr in self.pull_requests if pr.status == 'open']
            
            for pr in pending_reviews:
                with self.code_reviewers.request() as request:
                    yield request
                    
                    review_time = self.random.uniform(1, 3)
                    yield self.env.timeout(review_time)
                    
                    with self.github_api.request() as request2:
                        yield request2
                        comment_time = self.random.uniform(0.1, 0.3)
                        yield self.env.timeout(comment_time)
                        
                        if self.random.random() < 0.7:  # 70% 概率通过
                            pr.add_comment(
                                'copilot_ai',
                                "✅ 代码审查通过，建议合并",
                                self.env.now
                            )
                            pr.review_status = 'approved'
                            self.log_event(EventType.CODE_REVIEW_COMPLETE, 'pm-01', 
                                          f"PR #{pr.id} 审查通过", review_time, ['code_reviewers', 'github_api'])
                        else:
                            pr.add_comment(
                                'copilot_ai',
                                "🔧 需要修改：添加错误处理、优化性能",
                                self.env.now
                            )
                            pr.review_status = 'changes_requested'
                            self.log_event(EventType.CODE_REVIEW_COMPLETE, 'pm-01', 
                                          f"PR #{pr.id} 需要修改", review_time, ['code_reviewers', 'github_api'])
                        
                        self.project_status['communication_events'] += 1
            
            yield self.env.timeout(self.random.uniform(4, 6))
    
    def devops_process(self):
        """DevOps 工程师工作流程"""
        role_id = 'de-01'
        role = self.roles[role_id]
        
        while True:
            # 检查是否有已合并的 PR 需要部署
            merged_prs = [pr for pr in self.pull_requests if pr.status == 'merged']
            
            for pr in merged_prs:
                if not hasattr(pr, 'deployed'):
                    with self.deployment_env.request() as request:
                        yield request
                        
                        self.log_event(EventType.DEPLOYMENT_START, role_id, 
                                      f"开始部署 PR #{pr.id}")
                        
                        deployment_time = self.random.uniform(2, 4)
                        yield self.env.timeout(deployment_time)
                        role.total_work_time += deployment_time
                        
                        pr.deployed = True
                        self.log_event(EventType.DEPLOYMENT_COMPLETE, role_id, 
                                      f"PR #{pr.id} 部署完成!", deployment_time, ['deployment_env'])
            
            # 执行默认任务
            default_task = self.random.choice(role.default_tasks)
            default_time = self.random.uniform(1, 3)
            yield self.env.timeout(default_time)
            role.total_work_time += default_time
            
            self.log_event(EventType.DEFAULT_TASK_EXECUTED, role_id, 
                          f"执行默认任务: {default_task}", default_time)
            
            # 生成日报
            if int(self.env.now) % 24 == 0 and self.env.now > 0:
                yield from self.generate_daily_report(role_id)
            
            yield self.env.timeout(self.random.uniform(4, 6))
    
    def generate_daily_report(self, role_id):
        """生成日报"""
        role = self.roles[role_id]
        role.daily_reports += 1
        self.project_status['daily_reports'] += 1
        
        with self.github_api.request() as request:
            yield request
            report_time = self.random.uniform(0.1, 0.3)
            yield self.env.timeout(report_time)
            role.total_work_time += report_time
        
        self.log_event(EventType.DAILY_REPORT_GENERATED, role_id, 
                      f"生成日报 #{role.daily_reports}", report_time, ['github_api'])
    
    def run_simulation(self):
        """运行仿真"""
        print("="*80)
        print("🐝 Bee Swarm 事件驱动仿真")
        print("="*80)
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"AI 角色容器: {len(self.roles)} 个")
        print(f"资源限制: GitHub API({self.github_api.capacity}), AI工具({self.ai_tools.capacity})")
        print("="*80)
        
        # 启动各个流程
        self.env.process(self.human_po_process())
        self.env.process(self.product_manager_process())
        self.env.process(self.developer_process('be-01'))
        self.env.process(self.developer_process('fe-01'))
        self.env.process(self.code_review_process())
        self.env.process(self.devops_process())
        
        # 运行仿真
        start_time = time.time()
        self.env.run(until=SIMULATION_TIME)
        end_time = time.time()
        
        # 输出结果
        self.print_detailed_results(end_time - start_time)
    
    def print_detailed_results(self, real_time):
        """输出详细仿真结果"""
        print("\n" + "="*80)
        print("📊 事件驱动仿真详细结果")
        print("="*80)
        
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"实际运行时间: {real_time:.2f} 秒")
        
        print(f"\n📈 项目活动统计:")
        print(f"  总事件数: {self.project_status['total_events']}")
        print(f"  GitHub Issues: {self.project_status['total_issues']}")
        print(f"  Pull Requests: {self.project_status['total_prs']}")
        print(f"  沟通事件: {self.project_status['communication_events']}")
        print(f"  API 文档: {self.project_status['api_docs_created']}")
        print(f"  日报数量: {self.project_status['daily_reports']}")
        
        print(f"\n🎯 任务执行统计:")
        completed_tasks = len([t for t in self.tasks if t.status == 'completed'])
        print(f"  总任务数: {len(self.tasks)}")
        print(f"  完成任务数: {completed_tasks}")
        print(f"  完成率: {completed_tasks/len(self.tasks)*100:.1f}%" if self.tasks else "0%")
        
        if completed_tasks > 0:
            avg_task_duration = sum(t.total_duration for t in self.tasks if t.total_duration) / completed_tasks
            print(f"  平均任务耗时: {avg_task_duration:.1f} 小时")
        
        print(f"\n👥 角色工作量统计:")
        for role_id, role in self.roles.items():
            utilization = role.total_work_time / SIMULATION_TIME * 100
            ai_usage_ratio = role.ai_tool_usage_time / role.total_work_time * 100 if role.total_work_time > 0 else 0
            print(f"  {role.name}:")
            print(f"    完成任务: {len(role.completed_tasks)} 个")
            print(f"    总工作时间: {role.total_work_time:.1f} 小时")
            print(f"    利用率: {utilization:.1f}%")
            print(f"    AI工具使用: {role.ai_tool_usage_time:.1f} 小时 ({ai_usage_ratio:.1f}%)")
            print(f"    日报数量: {role.daily_reports} 个")
        
        print(f"\n📝 协作统计:")
        total_comments = sum(len(issue.comments) for issue in self.github_issues)
        total_pr_comments = sum(len(pr.comments) for pr in self.pull_requests)
        print(f"  Issue 评论: {total_comments}")
        print(f"  PR 评论: {total_pr_comments}")
        print(f"  总沟通次数: {total_comments + total_pr_comments}")
        
        print(f"\n🔄 事件类型统计:")
        event_counts = {}
        for event in self.event_log:
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {event_type}: {count} 次")
        
        print(f"\n⚡ 资源使用统计:")
        print(f"  GitHub API 最大并发: {self.github_api.capacity}")
        print(f"  AI 工具最大并发: {self.ai_tools.capacity}")
        print(f"  代码审查员最大并发: {self.code_reviewers.capacity}")
        print(f"  部署环境最大并发: {self.deployment_env.capacity}")

def main():
    """主函数"""
    print("🚀 启动 Bee Swarm 事件驱动仿真...")
    
    # 创建仿真实例
    simulation = BeeSwarmEventDrivenSimulation()
    
    # 运行仿真
    simulation.run_simulation()

if __name__ == "__main__":
    main() 