"""
Bee Swarm 详细事件演示
参考仓库系统模式，详细记录每个离散事件的生命周期
"""

import simpy
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# 配置参数
SIMULATION_TIME = 60
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

class BeeSwarmDetailedDemo:
    """Bee Swarm 详细事件演示"""
    
    def __init__(self):
        self.env = simpy.Environment()
        self.random = random.Random(RANDOM_SEED)
        
        # 创建资源
        self.github_api = simpy.Resource(self.env, capacity=10)
        self.ai_tools = simpy.Resource(self.env, capacity=5)
        
        # 事件计数器
        self.event_counter = 0
        self.events = []
        
        # 控制标志
        self.issue_created = False
        
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
        print(f"[{self.env.now:6.1f}h] [START] {event.actor}: {event.description}")
        if event.details:
            for key, value in event.details.items():
                print(f"         └─ {key}: {value}")
    
    def complete_event(self, event: Event, result: str = "完成"):
        """完成事件"""
        event.status = 'completed'
        event.end_time = self.env.now
        event.duration = event.end_time - event.start_time
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
    
    def human_po_process(self):
        """人类 PO 发布任务流程"""
        while True:
            if self.env.now < 10 and not self.issue_created:
                # 创建 Issue 事件
                event = self.create_event(
                    'issue_creation',
                    'human_po',
                    'github_repository',
                    '发布新的开发任务',
                    {
                        'title': '开发教育游戏用户注册功能',
                        'description': '需要实现用户注册、登录、密码重置功能，支持邮箱验证',
                        'priority': 'high',
                        'labels': ['feature', 'backend', 'frontend']
                    }
                )
                self.start_event(event)
                
                # 模拟创建 Issue 的时间
                creation_time = self.random.uniform(0.5, 1.5)
                yield self.env.timeout(creation_time)
                
                self.complete_event(event, "Issue #001 创建成功")
                self.issue_created = True
            
            yield self.env.timeout(self.random.uniform(20, 30))
    
    def product_manager_process(self):
        """产品经理 AI 工作流程"""
        role_id = 'pm-01'
        
        while True:
            if self.issue_created and self.env.now < 20:
                # 开始处理 Issue 事件
                event = self.create_event(
                    'issue_processing',
                    role_id,
                    'ISSUE-001',
                    '开始处理 Issue #001',
                    {'issue_title': '开发教育游戏用户注册功能'}
                )
                self.start_event(event)
                
                # 使用 AI 工具分析需求
                ai_event = self.create_event(
                    'ai_analysis',
                    role_id,
                    'gemini_cli',
                    '使用 Gemini CLI 分析用户需求',
                    {
                        'tool': 'Gemini CLI',
                        'analysis_type': '需求分析',
                        'input': '需要实现用户注册、登录、密码重置功能，支持邮箱验证'
                    }
                )
                self.start_event(ai_event)
                
                with self.ai_tools.request() as request:
                    yield request
                    analysis_time = self.random.uniform(2, 4)
                    yield self.env.timeout(analysis_time)
                    
                    analysis_result = {
                        'user_stories': [
                            '作为用户，我希望能够注册新账户',
                            '作为用户，我希望能够登录系统',
                            '作为用户，我希望能够重置密码'
                        ],
                        'technical_requirements': [
                            '邮箱验证机制',
                            '密码加密存储',
                            'JWT token 认证'
                        ]
                    }
                    ai_event.details['output'] = analysis_result
                    self.complete_event(ai_event, f"分析完成，生成 {len(analysis_result['user_stories'])} 个用户故事")
                
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
                
                prd_content = """
# 产品需求文档 (PRD)

## 用户故事
1. 作为用户，我希望能够注册新账户
2. 作为用户，我希望能够登录系统  
3. 作为用户，我希望能够重置密码

## 功能需求
- 用户注册功能
- 用户登录功能
- 密码重置功能
- 邮箱验证机制

## 验收标准
- 注册流程完整可用
- 登录验证正确
- 密码重置邮件发送成功
                """
                prd_event.details['content'] = prd_content
                self.complete_event(prd_event, "PRD 文档生成完成")
                
                # 添加 PRD 评论到 GitHub Issue
                self.log_comment(
                    'pm_ai_001',
                    f"📋 PRD 已生成：\n{prd_content[:200]}...",
                    'issue',
                    '001'
                )
                
                # 创建开发任务
                yield from self.create_development_tasks()
                
                self.complete_event(event, "Issue #001 处理完成，已分配 2 个任务")
                
            # 执行默认任务
            else:
                default_task = self.random.choice(['热门新闻爬虫', '用户反馈分析', '竞品监控'])
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
            
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def create_development_tasks(self):
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
            
            # 在 GitHub Issue 中分配任务
            self.log_comment(
                template['assigned_role'],
                f"🎯 任务分配: {template['title']}\n描述: {template['description']}\n预估工时: {template['estimated_hours']} 小时",
                'issue',
                '001'
            )
            
            self.complete_event(task_event, f"任务已分配给 {template['assigned_role']}")
    
    def developer_process(self, role_id):
        """开发者工作流程"""
        
        while True:
            if self.issue_created and self.env.now < 30:
                # 开始任务事件
                task_event = self.create_event(
                    'task_execution',
                    role_id,
                    'TASK-001',
                    f'开始执行任务: {"后端 API 设计" if role_id == "be-01" else "前端注册界面"}',
                    {
                        'task_id': 'TASK-001',
                        'task_title': "后端 API 设计" if role_id == "be-01" else "前端注册界面",
                        'issue_id': 'ISSUE-001'
                    }
                )
                self.start_event(task_event)
                
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
                    question = "❓ 关于 API 接口的疑问：\n1. 错误码定义是否完整？\n2. 是否需要添加字段验证？\n3. 响应格式是否统一？"
                    self.log_comment(
                        'frontend_ai_001',
                        question,
                        'issue',
                        '001'
                    )
                    
                    # 等待回复
                    wait_time = self.random.uniform(1, 3)
                    yield self.env.timeout(wait_time)
                    
                    # 模拟后端开发者回复
                    reply = "✅ 回复前端开发者：\n1. 错误码已完整定义\n2. 已添加字段验证\n3. 响应格式统一为 JSON"
                    self.log_comment(
                        'backend_ai_001',
                        reply,
                        'issue',
                        '001'
                    )
                    
                    self.complete_event(api_review_event, "API 文档审查完成")
                
                # 使用 AI 工具进行开发
                ai_dev_event = self.create_event(
                    'ai_development',
                    role_id,
                    'gemini_cli',
                    f'使用 Gemini CLI 辅助开发',
                    {
                        'tool': 'Gemini CLI',
                        'development_type': '代码生成',
                        'task': "后端 API 设计" if role_id == "be-01" else "前端注册界面"
                    }
                )
                self.start_event(ai_dev_event)
                
                with self.ai_tools.request() as request:
                    yield request
                    ai_time = self.random.uniform(2, 4)
                    yield self.env.timeout(ai_time)
                    
                    # 模拟 AI 生成的代码
                    if role_id == 'be-01':
                        generated_code = """
// 用户注册 API
app.post('/api/auth/register', async (req, res) => {
  const { email, password, name } = req.body;
  // 验证逻辑
  // 密码加密
  // 保存用户
  res.status(201).json({ message: '注册成功' });
});
                        """
                    else:
                        generated_code = """
// 注册组件
function RegisterForm() {
  const [formData, setFormData] = useState({});
  // 表单处理逻辑
  return <form>...</form>;
}
                        """
                    
                    ai_dev_event.details['generated_code'] = generated_code
                    self.complete_event(ai_dev_event, f"AI 辅助开发完成，生成代码 {len(generated_code)} 字符")
                
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
                    
                    api_doc_content = """
# API 文档

## 用户注册
POST /api/auth/register
- 参数: email, password, name
- 响应: { message: '注册成功' }

## 用户登录  
POST /api/auth/login
- 参数: email, password
- 响应: { token: 'jwt_token' }
                    """
                    api_doc_event.details['content'] = api_doc_content
                    self.complete_event(api_doc_event, "API 文档创建完成")
                
                # 创建 Pull Request
                pr_event = self.create_event(
                    'pr_creation',
                    role_id,
                    'github',
                    f'创建 Pull Request',
                    {
                        'pr_title': f"实现 {'后端 API 设计' if role_id == 'be-01' else '前端注册界面'}",
                        'files_changed': ['src/controllers/auth.js', 'src/models/user.js'],
                        'commit_message': f"feat: 实现 {'后端 API 设计' if role_id == 'be-01' else '前端注册界面'}"
                    }
                )
                self.start_event(pr_event)
                
                self.complete_event(pr_event, f"PR #PR-00{1 if role_id == 'be-01' else 2} 创建成功")
                
                # 完成任务
                self.complete_event(task_event, f"任务完成，耗时 {development_time:.1f} 小时")
                
            else:
                # 执行默认任务
                default_tasks = {
                    'be-01': ['API性能优化', '数据库维护', '系统监控'],
                    'fe-01': ['UI组件库维护', '性能优化', '用户体验分析']
                }
                default_task = self.random.choice(default_tasks[role_id])
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
            
            yield self.env.timeout(self.random.uniform(2, 4))
    
    def run_simulation(self):
        """运行仿真"""
        print("="*80)
        print("🐝 Bee Swarm 详细事件演示")
        print("="*80)
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print("="*80)
        
        # 启动各个流程
        self.env.process(self.human_po_process())
        self.env.process(self.product_manager_process())
        self.env.process(self.developer_process('be-01'))
        self.env.process(self.developer_process('fe-01'))
        
        # 运行仿真
        start_time = time.time()
        self.env.run(until=SIMULATION_TIME)
        end_time = time.time()
        
        # 输出结果
        self.print_results(end_time - start_time)
    
    def print_results(self, real_time):
        """输出仿真结果"""
        print("\n" + "="*80)
        print("📊 详细事件演示结果")
        print("="*80)
        
        print(f"仿真时间: {SIMULATION_TIME} 小时")
        print(f"实际运行时间: {real_time:.2f} 秒")
        print(f"总事件数: {len(self.events)}")
        
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
            
            # 按事件类型统计平均耗时
            type_durations = {}
            for event in completed_events:
                if event.event_type not in type_durations:
                    type_durations[event.event_type] = []
                type_durations[event.event_type].append(event.duration)
            
            for event_type, durations in type_durations.items():
                avg = sum(durations) / len(durations)
                print(f"  {event_type}: {avg:.1f} 小时")

def main():
    """主函数"""
    print("🚀 启动 Bee Swarm 详细事件演示...")
    
    # 创建仿真实例
    simulation = BeeSwarmDetailedDemo()
    
    # 运行仿真
    simulation.run_simulation()

if __name__ == "__main__":
    main() 