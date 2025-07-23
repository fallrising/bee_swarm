# Level 5: 实现细节

## 业务面：具体操作步骤

### 5.1 项目启动流程

#### 环境准备
1. **系统要求检查**
   ```bash
   # 检查Docker版本
   docker --version
   # 检查Docker Compose版本
   docker-compose --version
   # 检查可用内存
   free -h
   # 检查磁盘空间
   df -h
   ```

2. **网络配置**
   ```bash
   # 检查网络连接
   ping github.com
   # 检查DNS解析
   nslookup api.github.com
   # 检查防火墙设置
   sudo ufw status
   ```

3. **权限设置**
   ```bash
   # 创建项目目录
   mkdir -p /opt/bee-swarm
   cd /opt/bee-swarm
   
   # 设置目录权限
   sudo chown -R $USER:$USER /opt/bee-swarm
   chmod 755 /opt/bee-swarm
   ```

#### 配置文件设置
1. **环境变量配置**
   ```bash
   # 复制环境变量模板
   cp .env.example .env
   
   # 编辑环境变量
   nano .env
   ```

   ```env
   # GitHub配置
   GITHUB_TOKEN_PM=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_BACKEND=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_FRONTEND=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_QA=ghp_xxxxxxxxxxxxxxxxxxxx
   GITHUB_TOKEN_DEVOPS=ghp_xxxxxxxxxxxxxxxxxxxx
   
   # AI工具配置
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
   GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxx
   
   # 容器配置
   VNC_PASSWORD_PM=vnc123
   VNC_PASSWORD_BACKEND=vnc123
   VNC_PASSWORD_FRONTEND=vnc123
   VNC_PASSWORD_QA=vnc123
   VNC_PASSWORD_DEVOPS=vnc123
   
   # Cloudflare配置
   CLOUDFLARE_TUNNEL_URL=https://your-tunnel-url.trycloudflare.com
   
   # 数据库配置
   REDIS_URL=redis://localhost:6379
   POSTGRES_URL=postgresql://user:password@localhost:5432/beeswarm
   ```

2. **GitHub Webhook配置**
   ```bash
   # 在GitHub仓库设置中添加Webhook
   # URL: https://your-domain.com/webhook
   # Content type: application/json
   # Secret: your-webhook-secret
   # Events: Issues, Pull requests, Push
   ```

#### 容器构建和启动
1. **构建基础镜像**
   ```bash
   # 构建VNC基础镜像
   cd novnc_base
   docker build -t vnc-base .
   
   # 构建AI工具镜像
   cd ../novnc_llm_cli
   docker build -t vnc-llm-cli .
   ```

2. **构建角色镜像**
   ```bash
   # 构建所有角色镜像
   docker-compose build
   
   # 或者构建特定角色
   docker-compose build product-manager
   docker-compose build backend-developer
   ```

3. **启动服务**
   ```bash
   # 启动所有服务
   docker-compose up -d
   
   # 启动特定服务
   docker-compose up -d product-manager
   
   # 查看服务状态
   docker-compose ps
   ```

### 5.2 角色工作流程

#### 产品经理工作流程
1. **需求接收和分析**
   ```bash
   # 进入产品经理容器
   docker exec -it bee-swarm-product-manager-1 bash
   
   # 启动产品经理服务
   python /app/role_service.py
   ```

2. **任务创建和分配**
   ```python
   # 创建需求Issue
   issue_data = {
       'title': '实现用户登录功能',
       'body': '需要实现用户注册、登录、密码重置等功能',
       'labels': ['feature', 'high', 'backend'],
       'assignees': ['backend_ai_001']
   }
   
   github_client.create_issue('your-org/your-repo', **issue_data)
   ```

3. **进度跟踪**
   ```python
   # 更新Issue状态
   github_client.update_issue(
       'your-org/your-repo', 
       issue_number=123, 
       state='open',
       labels=['in_progress']
   )
   ```

#### 后端开发工作流程
1. **接收任务**
   ```bash
   # 进入后端开发容器
   docker exec -it bee-swarm-backend-developer-1 bash
   
   # 检查分配的任务
   python /app/check_assigned_tasks.py
   ```

2. **代码开发**
   ```python
   # 使用AI工具生成代码
   from ai_tools import AITools
   
   ai_tools = AITools()
   code = ai_tools.generate_code(
       'claude-code',
       'Create a JWT authentication system with login and register endpoints',
       context='Node.js, Express, MongoDB'
   )
   ```

3. **创建PR**
   ```python
   # 创建分支
   github_client.create_branch('your-org/your-repo', 'feature/user-auth')
   
   # 创建PR
   pr_data = {
       'title': 'Add user authentication system',
       'body': 'Implements JWT-based authentication with login and register endpoints',
       'head': 'feature/user-auth',
       'base': 'main'
   }
   
   github_client.create_pull_request('your-org/your-repo', **pr_data)
   ```

#### 前端开发工作流程
1. **API对接**
   ```python
   # 获取API文档
   api_docs = github_client.get_file_content(
       'your-org/your-repo', 
       'docs/api.md', 
       ref='feature/user-auth'
   )
   ```

2. **UI开发**
   ```python
   # 使用AI工具生成前端代码
   ui_code = ai_tools.generate_code(
       'warp',
       'Create a login form with React and Tailwind CSS',
       context=api_docs
   )
   ```

3. **集成测试**
   ```python
   # 运行前端测试
   import subprocess
   subprocess.run(['npm', 'test'], cwd='/app/frontend')
   ```

#### QA工程师工作流程
1. **测试计划制定**
   ```python
   # 分析PR变更
   pr = github_client.get_pull_request('your-org/your-repo', 456)
   changed_files = pr.get('changed_files', [])
   
   # 生成测试用例
   test_cases = ai_tools.generate_code(
       'playwright',
       f'Generate test cases for files: {changed_files}',
       context=pr.get('body', '')
   )
   ```

2. **执行测试**
   ```bash
   # 运行自动化测试
   npx playwright test
   
   # 生成测试报告
   npx playwright show-report
   ```

3. **问题报告**
   ```python
   # 创建问题Issue
   if test_failed:
       issue_data = {
           'title': f'Test failed: {test_name}',
           'body': f'Test {test_name} failed with error: {error_message}',
           'labels': ['bug', 'test'],
           'assignees': [pr_author]
       }
       github_client.create_issue('your-org/your-repo', **issue_data)
   ```

#### DevOps工程师工作流程
1. **部署准备**
   ```python
   # 检查PR状态
   pr = github_client.get_pull_request('your-org/your-repo', 456)
   
   if pr.get('mergeable') and pr.get('review_approvals') >= 1:
       # 合并PR
       github_client.merge_pull_request('your-org/your-repo', 456)
   ```

2. **自动部署**
   ```bash
   # 触发CI/CD流水线
   curl -X POST https://api.github.com/repos/your-org/your-repo/dispatches \
     -H "Authorization: token $GITHUB_TOKEN" \
     -d '{"event_type": "deploy", "client_payload": {"environment": "staging"}}'
   ```

3. **监控部署**
   ```python
   # 检查部署状态
   deployment_status = check_deployment_status('staging')
   
   if deployment_status['status'] == 'success':
       # 发送部署成功通知
       communication_api.send_deployment_notification(
           'staging', 
           'v1.2.3', 
           'success',
           deployment_url='https://staging.example.com'
       )
   ```

## 技术面：代码实现细节

### 5.1 AI工具集成

#### AI工具管理器
```python
# ai_tools.py
import subprocess
import json
import os
import time
from typing import Dict, Any, Optional
import logging

class AITools:
    def __init__(self):
        self.tools = {
            'gemini-cli': self._run_gemini_cli,
            'claude-code': self._run_claude_code,
            'rovo-dev': self._run_rovo_dev,
            'warp': self._run_warp,
            'cursor': self._run_cursor
        }
        
        self.logger = logging.getLogger(__name__)
        
        # 工具配置
        self.config = {
            'gemini-cli': {
                'timeout': 300,
                'max_retries': 3
            },
            'claude-code': {
                'timeout': 300,
                'max_retries': 3
            },
            'rovo-dev': {
                'timeout': 600,
                'max_retries': 2
            },
            'warp': {
                'timeout': 180,
                'max_retries': 3
            },
            'cursor': {
                'timeout': 180,
                'max_retries': 3
            }
        }
    
    def generate_code(self, tool: str, prompt: str, context: str = "", 
                     **kwargs) -> str:
        """使用指定AI工具生成代码"""
        if tool not in self.tools:
            raise ValueError(f"Unsupported tool: {tool}")
        
        self.logger.info(f"Generating code with {tool}")
        
        try:
            result = self.tools[tool](prompt, context, **kwargs)
            self.logger.info(f"Code generation successful with {tool}")
            return result
            
        except Exception as e:
            self.logger.error(f"Code generation failed with {tool}: {e}")
            raise
    
    def _run_gemini_cli(self, prompt: str, context: str = "", **kwargs) -> str:
        """运行Gemini CLI"""
        try:
            cmd = ['gemini', '--prompt', prompt]
            
            if context:
                cmd.extend(['--context', context])
            
            if kwargs.get('temperature'):
                cmd.extend(['--temperature', str(kwargs['temperature'])])
            
            if kwargs.get('max_tokens'):
                cmd.extend(['--max-tokens', str(kwargs['max_tokens'])])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config['gemini-cli']['timeout']
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"Gemini CLI error: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            raise Exception("Gemini CLI timeout")
        except Exception as e:
            raise Exception(f"Gemini CLI failed: {e}")
    
    def _run_claude_code(self, prompt: str, code_context: str = "", **kwargs) -> str:
        """运行Claude Code"""
        try:
            cmd = ['claude-code', '--prompt', prompt]
            
            if code_context:
                cmd.extend(['--code', code_context])
            
            if kwargs.get('model'):
                cmd.extend(['--model', kwargs['model']])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config['claude-code']['timeout']
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"Claude Code error: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            raise Exception("Claude Code timeout")
        except Exception as e:
            raise Exception(f"Claude Code failed: {e}")
    
    def _run_rovo_dev(self, prompt: str, context: str = "", **kwargs) -> str:
        """运行Rovo Dev"""
        try:
            cmd = ['rovo-dev', 'generate', '--prompt', prompt]
            
            if context:
                cmd.extend(['--context', context])
            
            if kwargs.get('framework'):
                cmd.extend(['--framework', kwargs['framework']])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config['rovo-dev']['timeout']
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"Rovo Dev error: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            raise Exception("Rovo Dev timeout")
        except Exception as e:
            raise Exception(f"Rovo Dev failed: {e}")
    
    def _run_warp(self, prompt: str, context: str = "", **kwargs) -> str:
        """运行Warp"""
        try:
            # Warp通常通过API调用
            api_key = os.getenv('WARP_API_KEY')
            if not api_key:
                raise Exception("WARP_API_KEY not set")
            
            # 这里需要根据Warp的实际API实现
            # 示例实现
            import requests
            
            response = requests.post(
                'https://api.warp.dev/v1/generate',
                headers={'Authorization': f'Bearer {api_key}'},
                json={
                    'prompt': prompt,
                    'context': context,
                    **kwargs
                },
                timeout=self.config['warp']['timeout']
            )
            
            if response.status_code == 200:
                return response.json()['code']
            else:
                raise Exception(f"Warp API error: {response.text}")
        
        except Exception as e:
            raise Exception(f"Warp failed: {e}")
    
    def _run_cursor(self, prompt: str, context: str = "", **kwargs) -> str:
        """运行Cursor"""
        try:
            # Cursor通常通过API调用
            api_key = os.getenv('CURSOR_API_KEY')
            if not api_key:
                raise Exception("CURSOR_API_KEY not set")
            
            # 这里需要根据Cursor的实际API实现
            # 示例实现
            import requests
            
            response = requests.post(
                'https://api.cursor.sh/v1/generate',
                headers={'Authorization': f'Bearer {api_key}'},
                json={
                    'prompt': prompt,
                    'context': context,
                    **kwargs
                },
                timeout=self.config['cursor']['timeout']
            )
            
            if response.status_code == 200:
                return response.json()['code']
            else:
                raise Exception(f"Cursor API error: {response.text}")
        
        except Exception as e:
            raise Exception(f"Cursor failed: {e}")
    
    def review_code(self, tool: str, code: str, requirements: str = "") -> Dict[str, Any]:
        """使用AI工具审查代码"""
        prompt = f"""
        请审查以下代码，并提供改进建议：
        
        代码：
        {code}
        
        要求：
        {requirements}
        
        请提供：
        1. 代码质量评分（1-10）
        2. 发现的问题
        3. 改进建议
        4. 安全性检查
        5. 性能优化建议
        """
        
        review_text = self.generate_code(tool, prompt)
        
        # 解析审查结果
        return self._parse_review_result(review_text)
    
    def _parse_review_result(self, review_text: str) -> Dict[str, Any]:
        """解析代码审查结果"""
        # 这里可以实现更复杂的解析逻辑
        # 示例实现
        lines = review_text.split('\n')
        
        score = 8  # 默认评分
        issues = []
        suggestions = []
        security_concerns = []
        performance_suggestions = []
        
        for line in lines:
            line = line.strip()
            if '评分' in line or 'score' in line.lower():
                # 提取评分
                import re
                score_match = re.search(r'(\d+)', line)
                if score_match:
                    score = int(score_match.group(1))
            
            elif '问题' in line or 'issue' in line.lower():
                issues.append(line)
            
            elif '建议' in line or 'suggestion' in line.lower():
                suggestions.append(line)
            
            elif '安全' in line or 'security' in line.lower():
                security_concerns.append(line)
            
            elif '性能' in line or 'performance' in line.lower():
                performance_suggestions.append(line)
        
        return {
            'score': score,
            'issues': issues,
            'suggestions': suggestions,
            'security_concerns': security_concerns,
            'performance_suggestions': performance_suggestions,
            'raw_text': review_text
        }
    
    def optimize_code(self, tool: str, code: str, optimization_type: str = "performance") -> str:
        """使用AI工具优化代码"""
        prompt = f"""
        请优化以下代码，重点优化{optimization_type}：
        
        代码：
        {code}
        
        优化要求：
        1. 提高{optimization_type}
        2. 保持代码可读性
        3. 不改变功能逻辑
        4. 添加必要的注释
        """
        
        return self.generate_code(tool, prompt)
    
    def generate_tests(self, tool: str, code: str, test_framework: str = "jest") -> str:
        """使用AI工具生成测试代码"""
        prompt = f"""
        请为以下代码生成{test_framework}测试用例：
        
        代码：
        {code}
        
        测试要求：
        1. 覆盖所有主要功能
        2. 包含边界条件测试
        3. 包含错误情况测试
        4. 测试用例命名清晰
        5. 使用{test_framework}语法
        """
        
        return self.generate_code(tool, prompt)
```

### 5.2 监控和日志

#### 监控系统
```python
# monitoring.py
import logging
import time
import psutil
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import threading

class Monitoring:
    def __init__(self, role_name: str):
        self.role_name = role_name
        self.logger = logging.getLogger(f"monitoring.{role_name}")
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 文件处理器
        file_handler = logging.FileHandler(f'/app/logs/{role_name}.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.setLevel(logging.INFO)
        
        # 性能指标
        self.performance_history = []
        self.error_history = []
        self.activity_history = []
        
        # 告警阈值
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'error_rate': 0.1
        }
        
        # 启动监控线程
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def log_activity(self, action: str, details: Dict[str, Any] = None):
        """记录角色活动"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'role': self.role_name,
            'action': action,
            'details': details or {}
        }
        
        self.logger.info(f"Activity: {action} - {details}")
        self.activity_history.append(log_data)
        
        # 发送到监控系统
        self._send_to_monitoring(log_data)
    
    def track_performance(self) -> Dict[str, Any]:
        """跟踪性能指标"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'role': self.role_name,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'memory_available': memory.available,
            'disk_free': disk.free,
            'load_average': psutil.getloadavg()
        }
        
        self.logger.info(f"Performance metrics: {metrics}")
        self.performance_history.append(metrics)
        
        # 检查告警阈值
        self._check_alert_thresholds(metrics)
        
        return metrics
    
    def alert_on_issues(self, issue_type: str, details: str):
        """问题告警"""
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'role': self.role_name,
            'issue_type': issue_type,
            'details': details,
            'severity': 'warning'
        }
        
        self.logger.warning(f"Alert: {issue_type} - {details}")
        self.error_history.append(alert_data)
        
        # 发送告警通知
        self._send_alert(alert_data)
    
    def track_api_calls(self, api_name: str, response_time: float, 
                       status_code: int, success: bool):
        """跟踪API调用"""
        api_data = {
            'timestamp': datetime.now().isoformat(),
            'role': self.role_name,
            'api_name': api_name,
            'response_time': response_time,
            'status_code': status_code,
            'success': success
        }
        
        self.logger.info(f"API call: {api_name} - {response_time}ms - {status_code}")
        
        # 检查API性能
        if response_time > 5000:  # 5秒
            self.alert_on_issues('slow_api_call', f"{api_name} took {response_time}ms")
        
        if not success:
            self.alert_on_issues('api_error', f"{api_name} failed with {status_code}")
    
    def track_github_operations(self, operation: str, success: bool, 
                               details: Dict[str, Any] = None):
        """跟踪GitHub操作"""
        github_data = {
            'timestamp': datetime.now().isoformat(),
            'role': self.role_name,
            'operation': operation,
            'success': success,
            'details': details or {}
        }
        
        self.logger.info(f"GitHub operation: {operation} - {'success' if success else 'failed'}")
        
        if not success:
            self.alert_on_issues('github_operation_failed', f"{operation} failed")
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """获取性能摘要"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_metrics = [
            m for m in self.performance_history 
            if datetime.fromisoformat(m['timestamp']) > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
        
        # 计算平均值
        avg_cpu = sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m['memory_percent'] for m in recent_metrics) / len(recent_metrics)
        avg_disk = sum(m['disk_percent'] for m in recent_metrics) / len(recent_metrics)
        
        # 计算最大值
        max_cpu = max(m['cpu_percent'] for m in recent_metrics)
        max_memory = max(m['memory_percent'] for m in recent_metrics)
        max_disk = max(m['disk_percent'] for m in recent_metrics)
        
        return {
            'period_hours': hours,
            'avg_cpu_percent': round(avg_cpu, 2),
            'avg_memory_percent': round(avg_memory, 2),
            'avg_disk_percent': round(avg_disk, 2),
            'max_cpu_percent': max_cpu,
            'max_memory_percent': max_memory,
            'max_disk_percent': max_disk,
            'total_metrics': len(recent_metrics)
        }
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """获取错误摘要"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_errors = [
            e for e in self.error_history 
            if datetime.fromisoformat(e['timestamp']) > cutoff_time
        ]
        
        error_types = {}
        for error in recent_errors:
            error_type = error['issue_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'period_hours': hours,
            'total_errors': len(recent_errors),
            'error_types': error_types,
            'recent_errors': recent_errors[-10:]  # 最近10个错误
        }
    
    def _check_alert_thresholds(self, metrics: Dict[str, Any]):
        """检查告警阈值"""
        if metrics['cpu_percent'] > self.alert_thresholds['cpu_percent']:
            self.alert_on_issues('high_cpu_usage', f"CPU usage: {metrics['cpu_percent']}%")
        
        if metrics['memory_percent'] > self.alert_thresholds['memory_percent']:
            self.alert_on_issues('high_memory_usage', f"Memory usage: {metrics['memory_percent']}%")
        
        if metrics['disk_percent'] > self.alert_thresholds['disk_percent']:
            self.alert_on_issues('high_disk_usage', f"Disk usage: {metrics['disk_percent']}%")
    
    def _monitoring_loop(self):
        """监控循环"""
        while True:
            try:
                # 跟踪性能
                self.track_performance()
                
                # 清理历史数据（保留最近7天）
                self._cleanup_history()
                
                # 等待下次检查
                time.sleep(300)  # 5分钟
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
    
    def _cleanup_history(self):
        """清理历史数据"""
        cutoff_time = datetime.now() - timedelta(days=7)
        
        # 清理性能历史
        self.performance_history = [
            m for m in self.performance_history 
            if datetime.fromisoformat(m['timestamp']) > cutoff_time
        ]
        
        # 清理错误历史
        self.error_history = [
            e for e in self.error_history 
            if datetime.fromisoformat(e['timestamp']) > cutoff_time
        ]
        
        # 清理活动历史
        self.activity_history = [
            a for a in self.activity_history 
            if datetime.fromisoformat(a['timestamp']) > cutoff_time
        ]
    
    def _send_to_monitoring(self, data: Dict[str, Any]):
        """发送数据到监控系统"""
        try:
            # 这里可以集成Prometheus、Grafana等监控系统
            # 示例：发送到Prometheus
            prometheus_url = os.getenv('PROMETHEUS_URL')
            if prometheus_url:
                requests.post(f"{prometheus_url}/metrics", json=data, timeout=5)
        except Exception as e:
            self.logger.error(f"Failed to send to monitoring: {e}")
    
    def _send_alert(self, alert_data: Dict[str, Any]):
        """发送告警通知"""
        try:
            # 这里可以集成Slack、邮件等通知系统
            # 示例：发送到Slack
            slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
            if slack_webhook:
                slack_message = {
                    'text': f"🚨 Alert from {self.role_name}: {alert_data['issue_type']}",
                    'attachments': [{
                        'text': alert_data['details'],
                        'color': 'danger'
                    }]
                }
                requests.post(slack_webhook, json=slack_message, timeout=5)
        except Exception as e:
            self.logger.error(f"Failed to send alert: {e}")
```

### 5.3 部署脚本

#### 自动化部署脚本
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查环境
check_environment() {
    log_info "Checking environment..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # 检查环境变量文件
    if [ ! -f .env ]; then
        log_error ".env file not found"
        exit 1
    fi
    
    log_info "Environment check passed"
}

# 构建镜像
build_images() {
    log_info "Building Docker images..."
    
    # 构建基础镜像
    log_info "Building base images..."
    cd novnc_base
    docker build -t vnc-base . || {
        log_error "Failed to build vnc-base image"
        exit 1
    }
    cd ..
    
    cd novnc_llm_cli
    docker build -t vnc-llm-cli . || {
        log_error "Failed to build vnc-llm-cli image"
        exit 1
    }
    cd ..
    
    # 构建角色镜像
    log_info "Building role images..."
    docker-compose build || {
        log_error "Failed to build role images"
        exit 1
    }
    
    log_info "Image build completed"
}

# 启动服务
start_services() {
    log_info "Starting services..."
    
    # 启动所有服务
    docker-compose up -d || {
        log_error "Failed to start services"
        exit 1
    }
    
    # 等待服务启动
    log_info "Waiting for services to start..."
    sleep 30
    
    # 检查服务状态
    check_service_status
    
    log_info "Services started successfully"
}

# 检查服务状态
check_service_status() {
    log_info "Checking service status..."
    
    services=("product-manager" "backend-developer" "frontend-developer" "qa-engineer" "devops-engineer")
    
    for service in "${services[@]}"; do
        if docker-compose ps | grep -q "$service.*Up"; then
            log_info "$service is running"
        else
            log_error "$service is not running"
            docker-compose logs "$service"
        fi
    done
}

# 配置GitHub Webhook
setup_webhook() {
    log_info "Setting up GitHub webhook..."
    
    # 这里需要根据实际情况配置
    # 可以使用GitHub API自动配置webhook
    
    log_warn "Please manually configure GitHub webhook:"
    log_warn "URL: https://your-domain.com/webhook"
    log_warn "Content type: application/json"
    log_warn "Secret: your-webhook-secret"
    log_warn "Events: Issues, Pull requests, Push"
}

# 健康检查
health_check() {
    log_info "Performing health check..."
    
    # 检查容器健康状态
    unhealthy_containers=$(docker-compose ps | grep "unhealthy" | wc -l)
    
    if [ "$unhealthy_containers" -gt 0 ]; then
        log_error "Found $unhealthy_containers unhealthy containers"
        docker-compose ps
        exit 1
    fi
    
    # 检查端口监听
    ports=(6080 6081 6082 6083 6084)
    for port in "${ports[@]}"; do
        if netstat -tuln | grep -q ":$port "; then
            log_info "Port $port is listening"
        else
            log_warn "Port $port is not listening"
        fi
    done
    
    log_info "Health check completed"
}

# 清理旧容器
cleanup_old_containers() {
    log_info "Cleaning up old containers..."
    
    # 停止并删除旧容器
    docker-compose down --remove-orphans || true
    
    # 清理未使用的镜像
    docker image prune -f || true
    
    log_info "Cleanup completed"
}

# 备份数据
backup_data() {
    log_info "Backing up data..."
    
    backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # 备份配置文件
    cp .env "$backup_dir/"
    cp docker-compose.yml "$backup_dir/"
    
    # 备份日志
    if [ -d "logs" ]; then
        cp -r logs "$backup_dir/"
    fi
    
    log_info "Backup saved to $backup_dir"
}

# 主函数
main() {
    log_info "Starting Bee Swarm deployment..."
    
    # 检查环境
    check_environment
    
    # 备份数据
    backup_data
    
    # 清理旧容器
    cleanup_old_containers
    
    # 构建镜像
    build_images
    
    # 启动服务
    start_services
    
    # 健康检查
    health_check
    
    # 配置webhook
    setup_webhook
    
    log_info "Deployment completed successfully!"
    log_info "Access URLs:"
    log_info "  Product Manager: http://localhost:6080"
    log_info "  Backend Developer: http://localhost:6081"
    log_info "  Frontend Developer: http://localhost:6082"
    log_info "  QA Engineer: http://localhost:6083"
    log_info "  DevOps Engineer: http://localhost:6084"
}

# 运行主函数
main "$@"
```

#### 生产环境部署脚本
```bash
#!/bin/bash
# scripts/deploy-prod.sh

set -e

# 生产环境配置
ENVIRONMENT="production"
VPS_COUNT=20
REGION="us-west-2"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 部署到VPS集群
deploy_to_vps_cluster() {
    log_info "Deploying to VPS cluster..."
    
    for i in $(seq 1 $VPS_COUNT); do
        vps_name="vps-$i"
        log_info "Deploying to $vps_name..."
        
        # 这里需要根据实际的VPS管理方式实现
        # 示例：使用SSH部署
        ssh "user@$vps_name" << 'EOF'
            cd /opt/bee-swarm
            git pull origin main
            docker-compose down
            docker-compose pull
            docker-compose up -d
            docker system prune -f
EOF
        
        log_info "$vps_name deployment completed"
    done
}

# 配置负载均衡
setup_load_balancer() {
    log_info "Setting up load balancer..."
    
    # 这里需要根据实际的负载均衡器实现
    # 示例：使用Nginx配置
    
    cat > /etc/nginx/sites-available/bee-swarm << 'EOF'
upstream bee_swarm_backend {
    server vps-1:6080;
    server vps-2:6081;
    server vps-3:6082;
    server vps-4:6083;
    server vps-5:6084;
    # ... 更多VPS
}

server {
    listen 80;
    server_name bee-swarm.example.com;
    
    location / {
        proxy_pass http://bee_swarm_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
    
    ln -sf /etc/nginx/sites-available/bee-swarm /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
    
    log_info "Load balancer configured"
}

# 配置监控
setup_monitoring() {
    log_info "Setting up monitoring..."
    
    # 部署Prometheus
    docker run -d \
        --name prometheus \
        -p 9090:9090 \
        -v /opt/prometheus.yml:/etc/prometheus/prometheus.yml \
        prom/prometheus
    
    # 部署Grafana
    docker run -d \
        --name grafana \
        -p 3000:3000 \
        -e GF_SECURITY_ADMIN_PASSWORD=admin \
        grafana/grafana
    
    log_info "Monitoring setup completed"
}

# 配置备份
setup_backup() {
    log_info "Setting up backup..."
    
    # 创建备份脚本
    cat > /opt/backup-bee-swarm.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/bee-swarm/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份数据卷
docker run --rm -v bee-swarm_pm_data:/data -v "$BACKUP_DIR":/backup alpine tar czf /backup/pm_data.tar.gz -C /data .
docker run --rm -v bee-swarm_backend_data:/data -v "$BACKUP_DIR":/backup alpine tar czf /backup/backend_data.tar.gz -C /data .
# ... 更多数据卷

# 清理旧备份（保留7天）
find /backup/bee-swarm -type d -mtime +7 -exec rm -rf {} \;
EOF
    
    chmod +x /opt/backup-bee-swarm.sh
    
    # 添加到crontab
    echo "0 2 * * * /opt/backup-bee-swarm.sh" | crontab -
    
    log_info "Backup setup completed"
}

# 主函数
main() {
    log_info "Starting production deployment..."
    
    # 部署到VPS集群
    deploy_to_vps_cluster
    
    # 配置负载均衡
    setup_load_balancer
    
    # 配置监控
    setup_monitoring
    
    # 配置备份
    setup_backup
    
    log_info "Production deployment completed!"
}

main "$@"
``` 