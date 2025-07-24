"""
Bee Swarm 详细事件仿真
参考仓库系统模式，详细记录每个离散事件的生命周期
"""

import simpy
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# 配置参数
SIMULATION_TIME = 80
RANDOM_SEED = 42

@dataclass
class Event:
    """离散事件"""
    id: str
    event_type: str
    actor: str
    target: str
    description: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    details: Dict = field(default_factory=dict)
    status: str = 'pending'

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
    duration: Optional[float] = None

@dataclass
class Role:
    """AI 角色"""
    name: str
    container_id: str
    github_username: str
    default_tasks: List[str] = field(default_factory=list)
    completed_tasks: List[Task] = field(default_factory=list)
    daily_reports: int = 0
    current_event: Optional[Event] = None

class BeeSwarmDetailedSimulation:
    """Bee Swarm 详细事件仿真"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.random = random.Random(RANDOM_SEED)
        
        # 创建资源
        self.github_api = simpy.Resource(self.env, capacity=10)
        self.ai_tools = simpy.Resource(self.env, capacity=5)
        
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
        self.events = []
        
        # 项目状态
        self.project_status = {
            'total_issues': 0,
            'total_prs': 0,
            'communication_events': 0,
            'api_docs_created': 0,
            'daily_reports': 0
        }
        
        # 控制标志
        self.issue_processed = False
        self.event_counter = 0
        
    def create_event(self, event_type: str, actor: str, target: str, description: str, details: Dict = None) -> Event:
        """创建新事件"""
        self.event_counter += 1
        event = Event(
            id=f"EVENT-{self.event_counter:03d}",
            event_type=event_type,
            actor=actor,
            target=target,
            description=description,
            start_time=self.env.now,
            details=details or {}
        )
        self.events.append(event)
        return event
    
    def start_event(self, event: Event):
        """开始事件"""
        event.status = 'running'
        role = self.roles.get(event.actor)
        if role:
            role.current_event = event
        
        print(f"[{self.env.now:6.1f}h] [START] {event.actor}: {event.description}")
        if event.details:
            for key, value in event.details.items():
                print(f"         └─ {key}: {value}")
    
    def complete_event(self, event: Event, result: str = "完成"):
        """完成事件"""
        event.status = 'completed'
        event.end_time = self.env.now
        event.duration = event.end_time - event.start_time
        
        role = self.roles.get(event.actor)
        if role and role.current_event == event:
            role.current_event = None
        
        print(f"[{self.env.now:6.1f}h] [COMPLETE] {event.actor}: {event.description} - {result} (耗时: {event.duration:.1f}h)")
    
    def log_comment(self, author: str, content: str, target_type: str, target_id: str):
        """记录评论事件"""
        event = self.create_event(
            'comment',
            author,
            f"{target_type}_{target_id}",
            f"在 {target_type} #{target_id} 添加评论",
            {'content': content[:50] + '...' if len(content) > 50 else content}
        )
        self.start_event(event)
        self.complete_event(event, f"评论内容: {content[:30]}...")
        self.project_status['communication_events'] += 1
    
    def human_po_process(self):
        """人类 PO 发布任务流程"""
        while True:
            if self.env.now < 15 and not self.issue_processed:
                # 创建 Issue 事件
                event = self.create_event(
                    'issue_creation',
                    'human_po',
                    'github_repository',
                    '发布新的开发任务',
                    {
                        'title': '开发教育游戏用户注册功能',
                        'description': '需要实现用户注册、登录、密码重置功能',
                        'priority': 'high'
                    }
                )
                self.start_event(event)
                
                # 模拟创建 Issue 的时间
                creation_time = self.random.uniform(0.5, 1.5)
                yield self.env.timeout(creation_time)
                
                # 创建 GitHub Issue
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
                
                self.complete_event(event, f"Issue #{issue.id} 创建成功")
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
                
                # 开始处理 Issue 事件
                event = self.create_event(
                    'issue_processing',
                    role_id,
                    issue.id,
                    f'开始处理 Issue #{issue.id}',
                    {'issue_title': issue.title}
                )
                self.start_event(event)
                
                # 分配 Issue
                issue.assigned_to = role_id
                issue.status = 'in_progress'
                
                # 使用 AI 工具分析需求
                ai_event = self.create_event(
                    'ai_analysis',
                    role_id,
                    'gemini_cli',
                    '使用 Gemini CLI 分析用户需求',
                    {
                        'tool': 'Gemini CLI',
                        'analysis_type': '需求分析',
                        'input': issue.description
                    }
                )
                self.start_event(ai_event)
                
                with self.ai_tools.request() as request:
                    yield request
                    analysis_time = self.random.uniform(2, 4)
                    yield self.env.timeout(analysis_time)
                    
                    analysis_result = {
                        'user_stories': 3,
                        'technical_requirements': 4
                    }
                    ai_event.details['output'] = analysis_result
                    self.complete_event(ai_event, f"分析完成，生成 {analysis_result['user_stories']} 个用户故事")
                
                # 生成 PRD 文档
                prd_event = self.create_event(
                    'prd_creation',
                    role_id,
                    'documentation',
                    '生成产品需求文档 (PRD)',
                    {
                        'document_type': 'PRD',
                        'sections': ['用户故事', '功能需求', '非功能需求', '验收标准']
                    }
                )
                self.start_event(prd_event)
                
                prd_time = self.random.uniform(1, 2)
                yield self.env.timeout(prd_time)
                
                prd_content = "产品需求文档包含用户故事、功能需求、非功能需求和验收标准"
                prd_event.details['content'] = prd_content
                self.complete_event(prd_event, "PRD 文档生成完成")
                
                # 添加 PRD 评论到 GitHub Issue
                self.log_comment(
                    role.github_username,
                    f"📋 PRD 已生成：{prd_content}",
                    'issue',
                    issue.id
                )
                
                # 创建开发任务
                yield from self.create_development_tasks(issue)
                
                self.complete_event(event, f"Issue #{issue.id} 处理完成，已分配 {len(self.tasks)} 个任务")
                
            # 检查 PR 状态，进行 UAT 测试
            pending_prs = [pr for pr in self.pull_requests if pr.status == 'open']
            for pr in pending_prs:
                if pr.review_status == 'approved':
                    # UAT 测试事件
                    uat_event = self.create_event(
                        'uat_testing',
                        role_id,
                        pr.id,
                        f'对 PR #{pr.id} 进行用户验收测试',
                        {
                            'pr_title': pr.title,
                            'test_scenarios': ['功能测试', '界面测试', '性能测试']
                        }
                    )
                    self.start_event(uat_event)
                    
                    uat_time = self.random.uniform(1, 2)
                    yield self.env.timeout(uat_time)
                    
                    test_results = {
                        '功能测试': '通过',
                        '界面测试': '通过', 
                        '性能测试': '通过'
                    }
                    uat_event.details['results'] = test_results
                    self.complete_event(uat_event, "UAT 测试全部通过")
                    
                    # 添加 UAT 结果评论
                    self.log_comment(
                        role.github_username,
                        "✅ UAT 测试通过，功能符合需求",
                        'pr',
                        pr.id
                    )
                    pr.status = 'merged'
            
            # 执行默认任务
            if not new_issues and not pending_prs:
                default_task = self.random.choice(role.default_tasks)
                default_event = self.create_event(
                    'default_task',
                    role_id,
                    'system',
                    f'执行默认任务: {default_task}',
                    {'task_type': default_task}
                )
                self.start_event(default_event)
                
                default_time = self.random.uniform(1, 3)
                yield self.env.timeout(default_time)
                
                self.complete_event(default_event, f"默认任务 '{default_task}' 执行完成")
            
            # 生成日报
            if int(self.env.now) % 24 == 0 and self.env.now > 0:
                yield from self.generate_daily_report(role_id)
            
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def create_development_tasks(self, issue: GitHubIssue):
        """创建开发任务"""
        task_templates = [
            {
                'title': '后端 API 设计',
                'assigned_role': 'be-01',
                'description': '设计用户注册、登录、密码重置的 REST API 接口',
                'estimated_hours': 8
            },
            {
                'title': '前端注册界面',
                'assigned_role': 'fe-01',
                'description': '开发用户注册和登录的前端界面',
                'estimated_hours': 10
            }
        ]
        
        for template in task_templates:
            # 创建任务事件
            task_event = self.create_event(
                'task_creation',
                'pm-01',
                template['assigned_role'],
                f"创建任务: {template['title']}",
                {
                    'task_title': template['title'],
                    'description': template['description'],
                    'estimated_hours': template['estimated_hours']
                }
            )
            self.start_event(task_event)
            
            # 创建任务对象
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
            self.log_comment(
                self.roles[template['assigned_role']].github_username,
                f"🎯 任务分配: {template['title']}",
                'issue',
                issue.id
            )
            
            self.complete_event(task_event, f"任务已分配给 {self.roles[template['assigned_role']].name}")
    
    def developer_process(self, role_id):
        """开发者工作流程"""
        role = self.roles[role_id]
        
        while True:
            # 检查分配给该角色的任务
            assigned_tasks = [task for task in self.tasks 
                            if task.assigned_role == role_id and task.status == 'pending']
            
            if assigned_tasks:
                task = assigned_tasks[0]
                
                # 开始任务事件
                task_event = self.create_event(
                    'task_execution',
                    role_id,
                    task.id,
                    f'开始执行任务: {task.title}',
                    {
                        'task_id': task.id,
                        'task_title': task.title,
                        'issue_id': task.issue_id
                    }
                )
                self.start_event(task_event)
                
                task.status = 'in_progress'
                task.started_time = self.env.now
                
                # 如果是前端开发者，查看 API 文档
                if role_id == 'fe-01':
                    api_review_event = self.create_event(
                        'api_review',
                        role_id,
                        'api_documentation',
                        '查看后端 API 文档',
                        {
                            'review_type': 'API 文档审查',
                            'focus_areas': ['接口规范', '错误码', '数据格式']
                        }
                    )
                    self.start_event(api_review_event)
                    
                    review_time = self.random.uniform(0.5, 1)
                    yield self.env.timeout(review_time)
                    
                    # 在 GitHub Issue 中提问
                    if self.random.random() < 0.3:
                        question = "❓ 关于 API 接口的疑问：错误码定义是否完整？"
                        self.log_comment(
                            role.github_username,
                            question,
                            'issue',
                            task.issue_id
                        )
                        
                        # 等待回复
                        wait_time = self.random.uniform(1, 3)
                        yield self.env.timeout(wait_time)
                        
                        # 模拟后端开发者回复
                        reply = "✅ 回复前端开发者：错误码已完整定义"
                        self.log_comment(
                            'backend_ai_001',
                            reply,
                            'issue',
                            task.issue_id
                        )
                    
                    self.complete_event(api_review_event, "API 文档审查完成")
                
                # 使用 AI 工具进行开发
                ai_dev_event = self.create_event(
                    'ai_development',
                    role_id,
                    'gemini_cli',
                    f'使用 Gemini CLI 辅助开发 {task.title}',
                    {
                        'tool': 'Gemini CLI',
                        'development_type': '代码生成',
                        'task': task.title
                    }
                )
                self.start_event(ai_dev_event)
                
                with self.ai_tools.request() as request:
                    yield request
                    ai_time = self.random.uniform(2, 4)
                    yield self.env.timeout(ai_time)
                    
                    # 模拟 AI 生成的代码
                    if role_id == 'be-01':
                        generated_code = "用户注册 API 代码"
                    else:
                        generated_code = "注册组件代码"
                    
                    ai_dev_event.details['generated_code'] = generated_code
                    self.complete_event(ai_dev_event, f"AI 辅助开发完成，生成代码")
                
                # 开发时间
                development_time = self.random.uniform(8, 16)
                yield self.env.timeout(development_time)
                
                # 如果是后端开发者，创建 API 文档
                if role_id == 'be-01':
                    api_doc_event = self.create_event(
                        'api_doc_creation',
                        role_id,
                        'documentation',
                        '创建 API 文档',
                        {
                            'doc_type': 'API 文档',
                            'endpoints': ['POST /api/auth/register', 'POST /api/auth/login']
                        }
                    )
                    self.start_event(api_doc_event)
                    
                    doc_time = self.random.uniform(1, 2)
                    yield self.env.timeout(doc_time)
                    
                    api_doc_content = "API 文档包含用户注册和登录接口"
                    api_doc_event.details['content'] = api_doc_content
                    self.complete_event(api_doc_event, "API 文档创建完成")
                    self.project_status['api_docs_created'] += 1
                
                # 创建 Pull Request
                pr_event = self.create_event(
                    'pr_creation',
                    role_id,
                    'github',
                    f'创建 Pull Request: {task.title}',
                    {
                        'pr_title': f"实现 {task.title}",
                        'files_changed': ['src/controllers/auth.js', 'src/models/user.js'],
                        'commit_message': f"feat: 实现 {task.title}"
                    }
                )
                self.start_event(pr_event)
                
                pr = PullRequest(
                    id=f"PR-{len(self.pull_requests)+1:03d}",
                    title=f"实现 {task.title}",
                    created_by=role_id,
                    created_time=self.env.now,
                    status='open'
                )
                self.pull_requests.append(pr)
                self.project_status['total_prs'] += 1
                
                self.complete_event(pr_event, f"PR #{pr.id} 创建成功")
                
                # 完成任务
                task.status = 'completed'
                task.completed_time = self.env.now
                task.duration = task.completed_time - task.started_time
                role.completed_tasks.append(task)
                
                self.complete_event(task_event, f"任务完成，耗时 {task.duration:.1f} 小时")
                
            else:
                # 执行默认任务
                default_task = self.random.choice(role.default_tasks)
                default_event = self.create_event(
                    'default_task',
                    role_id,
                    'system',
                    f'执行默认任务: {default_task}',
                    {'task_type': default_task}
                )
                self.start_event(default_event)
                
                default_time = self.random.uniform(1, 3)
                yield self.env.timeout(default_time)
                
                self.complete_event(default_event, f"默认任务 '{default_task}' 执行完成")
            
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
                # Code Review 事件
                review_event = self.create_event(
                    'code_review',
                    'copilot_ai',
                    pr.id,
                    f'对 PR #{pr.id} 进行代码审查',
                    {
                        'pr_title': pr.title,
                        'review_tools': ['Copilot', 'ESLint', 'SonarQube'],
                        'review_areas': ['代码质量', '安全性', '性能', '可维护性']
                    }
                )
                self.start_event(review_event)
                
                review_time = self.random.uniform(1, 3)
                yield self.env.timeout(review_time)
                
                with self.github_api.request() as request:
                    yield request
                    yield self.env.timeout(0.1)
                    
                    if self.random.random() < 0.7:  # 70% 概率通过
                        review_result = {
                            'status': 'approved',
                            'comments': ['代码质量良好', '符合编码规范', '测试覆盖充分']
                        }
                        
                        self.log_comment(
                            'copilot_ai',
                            "✅ 代码审查通过，建议合并",
                            'pr',
                            pr.id
                        )
                        pr.review_status = 'approved'
                        self.complete_event(review_event, "代码审查通过")
                    else:
                        review_result = {
                            'status': 'changes_requested',
                            'issues': ['缺少错误处理', '性能需要优化', '缺少单元测试']
                        }
                        
                        self.log_comment(
                            'copilot_ai',
                            "🔧 需要修改：添加错误处理、优化性能",
                            'pr',
                            pr.id
                        )
                        pr.review_status = 'changes_requested'
                        self.complete_event(review_event, "代码审查需要修改")
            
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
                    # 部署事件
                    deploy_event = self.create_event(
                        'deployment',
                        role_id,
                        pr.id,
                        f'开始部署 PR #{pr.id}',
                        {
                            'pr_title': pr.title,
                            'deployment_type': 'production',
                            'environment': 'staging -> production',
                            'tools': ['Docker', 'Kubernetes', 'GitHub Actions']
                        }
                    )
                    self.start_event(deploy_event)
                    
                    # 部署准备
                    prep_event = self.create_event(
                        'deployment_prep',
                        role_id,
                        'system',
                        '准备部署环境',
                        {'steps': ['构建镜像', '运行测试', '准备配置']}
                    )
                    self.start_event(prep_event)
                    
                    prep_time = self.random.uniform(1, 2)
                    yield self.env.timeout(prep_time)
                    self.complete_event(prep_event, "部署环境准备完成")
                    
                    # 执行部署
                    deployment_time = self.random.uniform(2, 4)
                    yield self.env.timeout(deployment_time)
                    
                    # 部署验证
                    verify_event = self.create_event(
                        'deployment_verify',
                        role_id,
                        'system',
                        '验证部署结果',
                        {'checks': ['健康检查', '功能测试', '性能监控']}
                    )
                    self.start_event(verify_event)
                    
                    verify_time = self.random.uniform(0.5, 1)
                    yield self.env.timeout(verify_time)
                    self.complete_event(verify_event, "部署验证通过")
                    
                    pr.deployed = True
                    self.complete_event(deploy_event, f"PR #{pr.id} 部署成功")
            
            # 执行默认任务
            default_task = self.random.choice(role.default_tasks)
            default_event = self.create_event(
                'default_task',
                role_id,
                'system',
                f'执行默认任务: {default_task}',
                {'task_type': default_task}
            )
            self.start_event(default_event)
            
            default_time = self.random.uniform(1, 3)
            yield self.env.timeout(default_time)
            
            self.complete_event(default_event, f"默认任务 '{default_task}' 执行完成")
            
            # 生成日报
            if int(self.env.now) % 24 == 0 and self.env.now > 0:
                yield from self.generate_daily_report(role_id)
            
            yield self.env.timeout(self.random.uniform(4, 6))
    
    def generate_daily_report(self, role_id):
        """生成日报"""
        role = self.roles[role_id]
        
        report_event = self.create_event(
            'daily_report',
            role_id,
            'github',
            f'生成日报 #{role.daily_reports + 1}',
            {
                'report_type': '日报',
                'date': f"Day {int(self.env.now // 24)}",
                'completed_tasks': len(role.completed_tasks),
                'ongoing_tasks': 1 if role.current_event else 0
            }
        )
        self.start_event(report_event)
        
        with self.github_api.request() as request:
            yield request
            yield self.env.timeout(0.1)
        
        role.daily_reports += 1
        self.project_status['daily_reports'] += 1
        
        report_content = f"日报包含今日完成的任务和明日计划"
        report_event.details['content'] = report_content
        self.complete_event(report_event, f"日报 #{role.daily_reports} 生成完成")
    
    def run_simulation(self):
        """运行仿真"""
        print("="*80)
        print("🐝 Bee Swarm 详细事件仿真")
        print("="*80)
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"AI 角色容器: {len(self.roles)} 个")
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
        self.print_results(end_time - start_time)
    
    def print_results(self, real_time):
        """输出仿真结果"""
        print("\n" + "="*80)
        print("📊 详细事件仿真结果")
        print("="*80)
        
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"实际运行时间: {real_time:.2f} 秒")
        print(f"总事件数: {len(self.events)}")
        
        print(f"\n📈 项目活动:")
        print(f"  GitHub Issues: {self.project_status['total_issues']}")
        print(f"  Pull Requests: {self.project_status['total_prs']}")
        print(f"  沟通事件: {self.project_status['communication_events']}")
        print(f"  API 文档: {self.project_status['api_docs_created']}")
        print(f"  日报数量: {self.project_status['daily_reports']}")
        
        print(f"\n🎯 任务状态:")
        completed_tasks = len([t for t in self.tasks if t.status == 'completed'])
        print(f"  总任务数: {len(self.tasks)}")
        print(f"  完成任务数: {completed_tasks}")
        print(f"  完成率: {completed_tasks/len(self.tasks)*100:.1f}%" if self.tasks else "0%")
        
        print(f"\n👥 角色工作量:")
        for role_id, role in self.roles.items():
            total_duration = sum(task.duration for task in role.completed_tasks if task.duration)
            print(f"  {role.name}: {len(role.completed_tasks)} 个任务, {role.daily_reports} 个日报, 总工时: {total_duration:.1f}h")
        
        print(f"\n📝 协作统计:")
        total_comments = sum(len(issue.comments) for issue in self.github_issues)
        total_pr_comments = sum(len(pr.comments) for pr in self.pull_requests)
        print(f"  Issue 评论: {total_comments}")
        print(f"  PR 评论: {total_pr_comments}")
        print(f"  总沟通次数: {total_comments + total_pr_comments}")
        
        print(f"\n🔄 事件类型统计:")
        event_types = {}
        for event in self.events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
        
        for event_type, count in sorted(event_types.items()):
            print(f"  {event_type}: {count} 次")
        
        print(f"\n⏱️ 平均事件耗时:")
        completed_events = [e for e in self.events if e.duration]
        if completed_events:
            avg_duration = sum(e.duration for e in completed_events) / len(completed_events)
            print(f"  平均事件耗时: {avg_duration:.1f} 小时")

def main():
    """主函数"""
    print("🚀 启动 Bee Swarm 详细事件仿真...")
    
    # 创建仿真实例
    simulation = BeeSwarmDetailedSimulation()
    
    # 运行仿真
    simulation.run_simulation()

if __name__ == "__main__":
    main() 