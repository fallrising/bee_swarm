# Level 4: 通信协议

## 业务面：角色间消息格式

### 4.1 消息类型定义

#### 任务分配消息
```json
{
  "type": "task_assigned",
  "role": "backend_developer",
  "issue_number": 123,
  "title": "实现用户认证API",
  "description": "创建JWT认证系统，包括登录、注册、token验证等功能",
  "priority": "high",
  "estimated_hours": 8,
  "labels": ["api", "backend", "security"],
  "assignee": "backend_ai_001",
  "created_at": "2024-01-15T10:30:00Z",
  "deadline": "2024-01-17T18:00:00Z"
}
```

#### 进度更新消息
```json
{
  "type": "progress_update",
  "role": "backend_developer",
  "issue_number": 123,
  "status": "in_progress",
  "progress_percentage": 60,
  "comment": "JWT token生成完成，正在实现验证逻辑。预计还需要2小时完成剩余工作。",
  "updated_at": "2024-01-16T14:30:00Z",
  "time_spent": 4.5,
  "remaining_estimate": 2.0
}
```

#### 协作请求消息
```json
{
  "type": "collaboration_request",
  "from_role": "backend_developer",
  "to_role": "frontend_developer",
  "request_type": "api_review",
  "api_docs_url": "https://api.example.com/docs",
  "message": "API设计完成，请审查接口设计是否符合前端需求。主要变更包括用户认证接口的响应格式调整。",
  "priority": "medium",
  "requested_at": "2024-01-16T15:00:00Z",
  "expected_response_time": "2024-01-16T17:00:00Z"
}
```

#### 代码审查消息
```json
{
  "type": "code_review",
  "reviewer_role": "qa_engineer",
  "pr_number": 456,
  "status": "changes_requested",
  "comments": [
    {
      "file": "src/auth/jwt.js",
      "line": 45,
      "comment": "建议添加输入验证，防止空值导致错误",
      "severity": "warning"
    },
    {
      "file": "tests/auth.test.js",
      "line": 23,
      "comment": "缺少边界条件测试用例",
      "severity": "info"
    }
  ],
  "overall_rating": 7,
  "reviewed_at": "2024-01-16T16:30:00Z"
}
```

#### 部署通知消息
```json
{
  "type": "deployment_notification",
  "role": "devops_engineer",
  "environment": "staging",
  "version": "v1.2.3",
  "status": "success",
  "deployment_url": "https://staging.example.com",
  "deployed_at": "2024-01-16T18:00:00Z",
  "rollback_available": true,
  "health_check_url": "https://staging.example.com/health"
}
```

#### 错误报告消息
```json
{
  "type": "error_report",
  "role": "qa_engineer",
  "issue_number": 789,
  "error_type": "api_error",
  "severity": "high",
  "description": "用户登录API在并发请求时出现500错误",
  "steps_to_reproduce": [
    "1. 同时发送多个登录请求",
    "2. 观察服务器响应",
    "3. 检查日志文件"
  ],
  "expected_behavior": "应该正常处理并发请求",
  "actual_behavior": "返回500内部服务器错误",
  "reported_at": "2024-01-16T19:00:00Z"
}
```

### 4.2 状态管理

#### Issue状态流转
```
open → assigned → in_progress → review_requested → approved → merged → closed
```

#### 角色状态定义
```json
{
  "idle": "空闲状态，等待新任务",
  "busy": "忙碌状态，正在处理任务",
  "reviewing": "审查状态，正在审查代码或文档",
  "collaborating": "协作状态，与其他角色协作",
  "deploying": "部署状态，正在部署或运维",
  "blocked": "阻塞状态，等待依赖或资源",
  "error": "错误状态，遇到问题需要处理"
}
```

#### 优先级定义
```json
{
  "critical": "紧急，需要立即处理",
  "high": "高优先级，需要优先处理",
  "medium": "中等优先级，正常处理",
  "low": "低优先级，空闲时处理"
}
```

## 技术面：API接口定义

### 4.1 角色间通信API

#### 通信服务类
```python
# communication_api.py
from flask import Flask, request, jsonify
import requests
import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

app = Flask(__name__)

class CommunicationAPI:
    def __init__(self):
        self.role_name = os.getenv('ROLE_NAME')
        self.other_roles = {
            'product_manager': 'http://pm-container:5000',
            'backend_developer': 'http://backend-container:5000',
            'frontend_developer': 'http://frontend-container:5000',
            'qa_engineer': 'http://qa-container:5000',
            'devops_engineer': 'http://devops-container:5000'
        }
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"communication.{self.role_name}")
    
    def send_message(self, to_role: str, message: Dict[str, Any]) -> bool:
        """发送消息给其他角色"""
        if to_role not in self.other_roles:
            self.logger.error(f"Unknown role: {to_role}")
            return False
        
        try:
            # 添加发送者信息
            message['from_role'] = self.role_name
            message['sent_at'] = datetime.now().isoformat()
            
            response = requests.post(
                f"{self.other_roles[to_role]}/receive_message",
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"Message sent to {to_role}: {message['type']}")
                return True
            else:
                self.logger.error(f"Failed to send message to {to_role}: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending message to {to_role}: {e}")
            return False
    
    def broadcast_message(self, message: Dict[str, Any], 
                         exclude_self: bool = True) -> Dict[str, bool]:
        """广播消息给所有角色"""
        results = {}
        
        for role, url in self.other_roles.items():
            if exclude_self and role == self.role_name:
                continue
            
            results[role] = self.send_message(role, message)
        
        return results
    
    def send_task_assignment(self, to_role: str, issue_data: Dict[str, Any]) -> bool:
        """发送任务分配消息"""
        message = {
            'type': 'task_assigned',
            'role': to_role,
            'issue_number': issue_data.get('number'),
            'title': issue_data.get('title'),
            'description': issue_data.get('body'),
            'priority': self._extract_priority(issue_data.get('labels', [])),
            'labels': [label['name'] for label in issue_data.get('labels', [])],
            'assignee': issue_data.get('assignee', {}).get('login'),
            'created_at': issue_data.get('created_at'),
            'deadline': self._calculate_deadline(issue_data)
        }
        
        return self.send_message(to_role, message)
    
    def send_progress_update(self, issue_number: int, status: str, 
                           progress_percentage: int, comment: str) -> bool:
        """发送进度更新消息"""
        message = {
            'type': 'progress_update',
            'role': self.role_name,
            'issue_number': issue_number,
            'status': status,
            'progress_percentage': progress_percentage,
            'comment': comment,
            'updated_at': datetime.now().isoformat()
        }
        
        # 发送给产品经理
        return self.send_message('product_manager', message)
    
    def send_collaboration_request(self, to_role: str, request_type: str, 
                                 message: str, **kwargs) -> bool:
        """发送协作请求消息"""
        collaboration_message = {
            'type': 'collaboration_request',
            'from_role': self.role_name,
            'to_role': to_role,
            'request_type': request_type,
            'message': message,
            'requested_at': datetime.now().isoformat(),
            **kwargs
        }
        
        return self.send_message(to_role, collaboration_message)
    
    def send_code_review(self, pr_number: int, status: str, 
                        comments: List[Dict[str, Any]]) -> bool:
        """发送代码审查消息"""
        message = {
            'type': 'code_review',
            'reviewer_role': self.role_name,
            'pr_number': pr_number,
            'status': status,
            'comments': comments,
            'reviewed_at': datetime.now().isoformat()
        }
        
        # 发送给PR作者
        return self.send_message('backend_developer', message)
    
    def send_deployment_notification(self, environment: str, version: str, 
                                   status: str, **kwargs) -> bool:
        """发送部署通知消息"""
        message = {
            'type': 'deployment_notification',
            'role': self.role_name,
            'environment': environment,
            'version': version,
            'status': status,
            'deployed_at': datetime.now().isoformat(),
            **kwargs
        }
        
        # 广播给所有角色
        return self.broadcast_message(message)
    
    def send_error_report(self, issue_number: int, error_type: str, 
                         severity: str, description: str, **kwargs) -> bool:
        """发送错误报告消息"""
        message = {
            'type': 'error_report',
            'role': self.role_name,
            'issue_number': issue_number,
            'error_type': error_type,
            'severity': severity,
            'description': description,
            'reported_at': datetime.now().isoformat(),
            **kwargs
        }
        
        # 发送给相关角色
        if error_type == 'api_error':
            return self.send_message('backend_developer', message)
        elif error_type == 'ui_error':
            return self.send_message('frontend_developer', message)
        else:
            return self.send_message('devops_engineer', message)
    
    def _extract_priority(self, labels: List[Dict[str, Any]]) -> str:
        """从标签中提取优先级"""
        label_names = [label['name'] for label in labels]
        
        if 'critical' in label_names:
            return 'critical'
        elif 'high' in label_names:
            return 'high'
        elif 'low' in label_names:
            return 'low'
        else:
            return 'medium'
    
    def _calculate_deadline(self, issue_data: Dict[str, Any]) -> str:
        """计算截止时间"""
        created_at = datetime.fromisoformat(issue_data.get('created_at', '').replace('Z', '+00:00'))
        
        # 根据优先级设置不同的截止时间
        priority = self._extract_priority(issue_data.get('labels', []))
        
        if priority == 'critical':
            deadline = created_at.replace(hour=18, minute=0, second=0, microsecond=0)
        elif priority == 'high':
            deadline = created_at.replace(hour=18, minute=0, second=0, microsecond=0)
            deadline = deadline.replace(day=deadline.day + 1)
        else:
            deadline = created_at.replace(hour=18, minute=0, second=0, microsecond=0)
            deadline = deadline.replace(day=deadline.day + 2)
        
        return deadline.isoformat()

# 创建通信API实例
communication_api = CommunicationAPI()

@app.route('/receive_message', methods=['POST'])
def receive_message():
    """接收其他角色发送的消息"""
    try:
        data = request.json
        from_role = data.get('from_role')
        message_type = data.get('type')
        
        app.logger.info(f"Received message from {from_role}: {message_type}")
        
        # 处理接收到的消息
        handle_received_message(from_role, data)
        
        return jsonify({'status': 'received', 'message_type': message_type})
        
    except Exception as e:
        app.logger.error(f"Error receiving message: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    """发送消息给其他角色"""
    try:
        data = request.json
        to_role = data.get('to_role')
        message = data.get('message')
        
        success = communication_api.send_message(to_role, message)
        
        return jsonify({'success': success})
        
    except Exception as e:
        app.logger.error(f"Error sending message: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/broadcast_message', methods=['POST'])
def broadcast_message():
    """广播消息给所有角色"""
    try:
        data = request.json
        message = data.get('message')
        exclude_self = data.get('exclude_self', True)
        
        results = communication_api.broadcast_message(message, exclude_self)
        
        return jsonify({'results': results})
        
    except Exception as e:
        app.logger.error(f"Error broadcasting message: {e}")
        return jsonify({'error': str(e)}), 500

def handle_received_message(from_role: str, message: Dict[str, Any]):
    """处理接收到的消息"""
    message_type = message.get('type')
    
    app.logger.info(f"Handling message from {from_role}: {message_type}")
    
    if message_type == 'task_assigned':
        handle_task_assigned(message)
    elif message_type == 'progress_update':
        handle_progress_update(message)
    elif message_type == 'collaboration_request':
        handle_collaboration_request(message)
    elif message_type == 'code_review':
        handle_code_review(message)
    elif message_type == 'deployment_notification':
        handle_deployment_notification(message)
    elif message_type == 'error_report':
        handle_error_report(message)
    else:
        app.logger.warning(f"Unknown message type: {message_type}")

def handle_task_assigned(message: Dict[str, Any]):
    """处理任务分配消息"""
    app.logger.info(f"Task assigned: {message.get('title')}")
    # 实现任务分配处理逻辑

def handle_progress_update(message: Dict[str, Any]):
    """处理进度更新消息"""
    app.logger.info(f"Progress update: {message.get('progress_percentage')}%")
    # 实现进度更新处理逻辑

def handle_collaboration_request(message: Dict[str, Any]):
    """处理协作请求消息"""
    app.logger.info(f"Collaboration request: {message.get('request_type')}")
    # 实现协作请求处理逻辑

def handle_code_review(message: Dict[str, Any]):
    """处理代码审查消息"""
    app.logger.info(f"Code review: {message.get('status')}")
    # 实现代码审查处理逻辑

def handle_deployment_notification(message: Dict[str, Any]):
    """处理部署通知消息"""
    app.logger.info(f"Deployment notification: {message.get('status')}")
    # 实现部署通知处理逻辑

def handle_error_report(message: Dict[str, Any]):
    """处理错误报告消息"""
    app.logger.info(f"Error report: {message.get('error_type')}")
    # 实现错误报告处理逻辑

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 4.2 错误处理和重试机制

#### 错误处理类
```python
# error_handler.py
import time
import logging
import requests
from functools import wraps
from typing import Callable, Any, Dict, Optional
from datetime import datetime, timedelta

class ErrorHandler:
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        
        # 错误统计
        self.error_counts = {}
        self.last_error_time = {}
    
    def retry_on_failure(self, func: Callable) -> Callable:
        """失败重试装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < self.max_retries - 1:
                        # 指数退避
                        delay = self.retry_delay * (2 ** attempt)
                        time.sleep(delay)
            
            self.logger.error(
                f"All {self.max_retries} attempts failed for {func.__name__}"
            )
            raise last_exception
        
        return wrapper
    
    def handle_github_error(self, error: Exception) -> bool:
        """处理GitHub API错误"""
        if hasattr(error, 'response'):
            status_code = error.response.status_code
            
            if status_code == 401:
                self.logger.error("GitHub authentication failed")
                return False
            elif status_code == 403:
                self.logger.error("GitHub rate limit exceeded")
                time.sleep(60)  # 等待1分钟
                return True
            elif status_code == 404:
                self.logger.error("GitHub resource not found")
                return False
            elif status_code >= 500:
                self.logger.error("GitHub server error")
                time.sleep(30)  # 等待30秒
                return True
        
        return False
    
    def handle_network_error(self, error: Exception) -> bool:
        """处理网络错误"""
        if isinstance(error, requests.exceptions.ConnectionError):
            self.logger.error("Network connection error")
            time.sleep(10)  # 等待10秒
            return True
        elif isinstance(error, requests.exceptions.Timeout):
            self.logger.error("Request timeout")
            time.sleep(5)  # 等待5秒
            return True
        elif isinstance(error, requests.exceptions.RequestException):
            self.logger.error("Request exception")
            time.sleep(15)  # 等待15秒
            return True
        
        return False
    
    def track_error(self, error_type: str, error_message: str):
        """跟踪错误"""
        current_time = datetime.now()
        
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        
        self.error_counts[error_type] += 1
        self.last_error_time[error_type] = current_time
        
        self.logger.error(f"Error tracked: {error_type} - {error_message}")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """获取错误统计"""
        return {
            'error_counts': self.error_counts,
            'last_error_time': {
                error_type: time.isoformat() 
                for error_type, time in self.last_error_time.items()
            }
        }
    
    def should_alert(self, error_type: str, threshold: int = 5) -> bool:
        """判断是否应该告警"""
        count = self.error_counts.get(error_type, 0)
        return count >= threshold
    
    def reset_error_count(self, error_type: str):
        """重置错误计数"""
        if error_type in self.error_counts:
            del self.error_counts[error_type]
        if error_type in self.last_error_time:
            del self.last_error_time[error_type]

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """执行函数，带熔断器保护"""
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """成功时的处理"""
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def _on_failure(self):
        """失败时的处理"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
    
    def _should_attempt_reset(self) -> bool:
        """判断是否应该尝试重置"""
        if not self.last_failure_time:
            return True
        
        elapsed = datetime.now() - self.last_failure_time
        return elapsed.total_seconds() >= self.recovery_timeout
    
    def get_state(self) -> str:
        """获取当前状态"""
        return self.state
```

### 4.3 消息队列集成

#### Redis消息队列
```python
# message_queue.py
import redis
import json
import threading
import time
from typing import Callable, Dict, Any, Optional
from datetime import datetime

class MessageQueue:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.subscribers = {}
        self.running = False
        self.thread = None
    
    def publish(self, channel: str, message: Dict[str, Any]):
        """发布消息"""
        message['timestamp'] = datetime.now().isoformat()
        self.redis_client.publish(channel, json.dumps(message))
    
    def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], None]):
        """订阅消息"""
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        
        self.subscribers[channel].append(callback)
    
    def start_listening(self):
        """开始监听消息"""
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.start()
    
    def stop_listening(self):
        """停止监听消息"""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _listen_loop(self):
        """监听循环"""
        pubsub = self.redis_client.pubsub()
        
        # 订阅所有频道
        for channel in self.subscribers.keys():
            pubsub.subscribe(channel)
        
        while self.running:
            try:
                message = pubsub.get_message(timeout=1)
                if message and message['type'] == 'message':
                    channel = message['channel'].decode('utf-8')
                    data = json.loads(message['data'].decode('utf-8'))
                    
                    # 调用回调函数
                    if channel in self.subscribers:
                        for callback in self.subscribers[channel]:
                            try:
                                callback(data)
                            except Exception as e:
                                print(f"Error in callback: {e}")
                                
            except Exception as e:
                print(f"Error in listen loop: {e}")
                time.sleep(1)
    
    def send_task_message(self, to_role: str, message: Dict[str, Any]):
        """发送任务消息"""
        channel = f"tasks:{to_role}"
        self.publish(channel, message)
    
    def send_collaboration_message(self, to_role: str, message: Dict[str, Any]):
        """发送协作消息"""
        channel = f"collaboration:{to_role}"
        self.publish(channel, message)
    
    def send_notification_message(self, message: Dict[str, Any]):
        """发送通知消息"""
        channel = "notifications"
        self.publish(channel, message)
```

### 4.4 消息格式验证

#### 消息验证器
```python
# message_validator.py
from typing import Dict, Any, List, Optional
import re
from datetime import datetime

class MessageValidator:
    def __init__(self):
        self.required_fields = {
            'task_assigned': ['type', 'role', 'issue_number', 'title'],
            'progress_update': ['type', 'role', 'issue_number', 'status', 'progress_percentage'],
            'collaboration_request': ['type', 'from_role', 'to_role', 'request_type', 'message'],
            'code_review': ['type', 'reviewer_role', 'pr_number', 'status'],
            'deployment_notification': ['type', 'role', 'environment', 'version', 'status'],
            'error_report': ['type', 'role', 'issue_number', 'error_type', 'severity', 'description']
        }
        
        self.field_validators = {
            'issue_number': self._validate_issue_number,
            'pr_number': self._validate_pr_number,
            'progress_percentage': self._validate_percentage,
            'priority': self._validate_priority,
            'severity': self._validate_severity,
            'status': self._validate_status
        }
    
    def validate_message(self, message: Dict[str, Any]) -> List[str]:
        """验证消息格式"""
        errors = []
        
        # 检查消息类型
        message_type = message.get('type')
        if not message_type:
            errors.append("Missing message type")
            return errors
        
        if message_type not in self.required_fields:
            errors.append(f"Unknown message type: {message_type}")
            return errors
        
        # 检查必需字段
        for field in self.required_fields[message_type]:
            if field not in message:
                errors.append(f"Missing required field: {field}")
        
        # 验证字段值
        for field, value in message.items():
            if field in self.field_validators:
                field_errors = self.field_validators[field](value)
                errors.extend(field_errors)
        
        return errors
    
    def _validate_issue_number(self, value: Any) -> List[str]:
        """验证issue编号"""
        errors = []
        if not isinstance(value, int) or value <= 0:
            errors.append("Issue number must be a positive integer")
        return errors
    
    def _validate_pr_number(self, value: Any) -> List[str]:
        """验证PR编号"""
        errors = []
        if not isinstance(value, int) or value <= 0:
            errors.append("PR number must be a positive integer")
        return errors
    
    def _validate_percentage(self, value: Any) -> List[str]:
        """验证百分比"""
        errors = []
        if not isinstance(value, int) or value < 0 or value > 100:
            errors.append("Progress percentage must be an integer between 0 and 100")
        return errors
    
    def _validate_priority(self, value: Any) -> List[str]:
        """验证优先级"""
        errors = []
        valid_priorities = ['critical', 'high', 'medium', 'low']
        if value not in valid_priorities:
            errors.append(f"Priority must be one of: {valid_priorities}")
        return errors
    
    def _validate_severity(self, value: Any) -> List[str]:
        """验证严重程度"""
        errors = []
        valid_severities = ['critical', 'high', 'medium', 'low']
        if value not in valid_severities:
            errors.append(f"Severity must be one of: {valid_severities}")
        return errors
    
    def _validate_status(self, value: Any) -> List[str]:
        """验证状态"""
        errors = []
        valid_statuses = ['open', 'in_progress', 'review_requested', 'approved', 'merged', 'closed']
        if value not in valid_statuses:
            errors.append(f"Status must be one of: {valid_statuses}")
        return errors
    
    def sanitize_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """清理消息数据"""
        sanitized = message.copy()
        
        # 移除HTML标签
        for key, value in sanitized.items():
            if isinstance(value, str):
                sanitized[key] = re.sub(r'<[^>]+>', '', value)
        
        # 限制字符串长度
        for key, value in sanitized.items():
            if isinstance(value, str) and len(value) > 1000:
                sanitized[key] = value[:1000] + "..."
        
        return sanitized
``` 