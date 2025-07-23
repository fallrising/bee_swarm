# Level 4: Communication Protocol

## Business Aspect: Inter-Role Message Format

### 4.1 Message Type Definitions

#### Task Assignment Message
```json
{
  "type": "task_assigned",
  "role": "backend_developer",
  "issue_number": 123,
  "title": "Implement User Authentication API",
  "description": "Create JWT authentication system including login, registration, token validation and other functions",
  "priority": "high",
  "estimated_hours": 8,
  "labels": ["api", "backend", "security"],
  "assignee": "backend_ai_001",
  "created_at": "2024-01-15T10:30:00Z",
  "deadline": "2024-01-17T18:00:00Z"
}
```

#### Progress Update Message
```json
{
  "type": "progress_update",
  "role": "backend_developer",
  "issue_number": 123,
  "status": "in_progress",
  "progress_percentage": 60,
  "comment": "JWT token generation completed, implementing validation logic. Estimated 2 more hours to complete remaining work.",
  "updated_at": "2024-01-16T14:30:00Z",
  "time_spent": 4.5,
  "remaining_estimate": 2.0
}
```

#### Collaboration Request Message
```json
{
  "type": "collaboration_request",
  "from_role": "backend_developer",
  "to_role": "frontend_developer",
  "request_type": "api_review",
  "api_docs_url": "https://api.example.com/docs",
  "message": "API design completed, please review if the interface design meets frontend requirements. Main changes include response format adjustments for user authentication interfaces.",
  "priority": "medium",
  "requested_at": "2024-01-16T15:00:00Z",
  "expected_response_time": "2024-01-16T17:00:00Z"
}
```

#### Code Review Message
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
      "comment": "Suggest adding input validation to prevent errors from null values",
      "severity": "warning"
    },
    {
      "file": "tests/auth.test.js",
      "line": 23,
      "comment": "Missing boundary condition test cases",
      "severity": "info"
    }
  ],
  "overall_rating": 7,
  "reviewed_at": "2024-01-16T16:30:00Z"
}
```

#### Deployment Notification Message
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

#### Error Report Message
```json
{
  "type": "error_report",
  "role": "qa_engineer",
  "issue_number": 789,
  "error_type": "functional_error",
  "severity": "high",
  "description": "User login fails when using special characters in password",
  "steps_to_reproduce": [
    "Navigate to login page",
    "Enter username: test@example.com",
    "Enter password: Test@123!",
    "Click login button"
  ],
  "expected_behavior": "User should be logged in successfully",
  "actual_behavior": "Login fails with 500 error",
  "environment": "staging",
  "browser": "Chrome 120.0",
  "reported_at": "2024-01-16T19:00:00Z"
}
```

### 4.2 Message Priority Levels

#### Priority Definition
```python
class MessagePriority:
    CRITICAL = 1    # Immediate attention required
    HIGH = 2        # Urgent, respond within 1 hour
    MEDIUM = 3      # Normal priority, respond within 4 hours
    LOW = 4         # Low priority, respond within 24 hours
    INFO = 5        # Informational only, no response required
```

#### Priority Assignment Rules
```python
class PriorityAssignment:
    def assign_priority(self, message_type: str, context: dict) -> int:
        """Assign priority based on message type and context"""
        
        # Critical priority
        if message_type in ["error_report", "deployment_failure", "security_alert"]:
            return MessagePriority.CRITICAL
        
        # High priority
        if message_type in ["task_assigned", "deadline_approaching", "blocking_issue"]:
            return MessagePriority.HIGH
        
        # Medium priority
        if message_type in ["collaboration_request", "code_review", "progress_update"]:
            return MessagePriority.MEDIUM
        
        # Low priority
        if message_type in ["status_update", "documentation_update"]:
            return MessagePriority.LOW
        
        # Info priority
        if message_type in ["deployment_notification", "system_notification"]:
            return MessagePriority.INFO
        
        return MessagePriority.MEDIUM  # Default priority
```

### 4.3 Message Routing

#### Routing Rules
```python
class MessageRouter:
    def __init__(self):
        self.routing_rules = {
            "task_assigned": self._route_task_assignment,
            "collaboration_request": self._route_collaboration_request,
            "code_review": self._route_code_review,
            "error_report": self._route_error_report,
            "deployment_notification": self._route_deployment_notification
        }
    
    def route_message(self, message: dict) -> list:
        """Route message to appropriate recipients"""
        message_type = message.get("type")
        
        if message_type in self.routing_rules:
            return self.routing_rules[message_type](message)
        else:
            return self._route_default(message)
    
    def _route_task_assignment(self, message: dict) -> list:
        """Route task assignment messages"""
        assignee = message.get("assignee")
        if assignee:
            return [assignee]
        return []
    
    def _route_collaboration_request(self, message: dict) -> list:
        """Route collaboration request messages"""
        to_role = message.get("to_role")
        if to_role:
            # Map role to specific AI instances
            role_mapping = {
                "frontend_developer": ["frontend_ai_001", "frontend_ai_002"],
                "backend_developer": ["backend_ai_001", "backend_ai_002", "backend_ai_003"],
                "qa_engineer": ["qa_ai_001", "qa_ai_002"],
                "product_manager": ["pm_ai_001", "pm_ai_002"],
                "devops_engineer": ["devops_ai_001"]
            }
            return role_mapping.get(to_role, [])
        return []
    
    def _route_code_review(self, message: dict) -> list:
        """Route code review messages"""
        reviewer_role = message.get("reviewer_role")
        if reviewer_role:
            role_mapping = {
                "qa_engineer": ["qa_ai_001", "qa_ai_002"],
                "backend_developer": ["backend_ai_001", "backend_ai_002", "backend_ai_003"],
                "frontend_developer": ["frontend_ai_001", "frontend_ai_002"]
            }
            return role_mapping.get(reviewer_role, [])
        return []
    
    def _route_error_report(self, message: dict) -> list:
        """Route error report messages"""
        error_type = message.get("error_type")
        
        if error_type == "functional_error":
            # Route to QA and relevant developers
            return ["qa_ai_001", "qa_ai_002", "backend_ai_001", "frontend_ai_001"]
        elif error_type == "deployment_error":
            # Route to DevOps
            return ["devops_ai_001"]
        elif error_type == "security_error":
            # Route to all relevant roles
            return ["devops_ai_001", "backend_ai_001", "qa_ai_001"]
        else:
            return ["qa_ai_001"]  # Default to QA
    
    def _route_deployment_notification(self, message: dict) -> list:
        """Route deployment notification messages"""
        # Notify all roles about deployment
        return [
            "pm_ai_001", "pm_ai_002",
            "backend_ai_001", "backend_ai_002", "backend_ai_003",
            "frontend_ai_001", "frontend_ai_002",
            "qa_ai_001", "qa_ai_002",
            "devops_ai_001"
        ]
    
    def _route_default(self, message: dict) -> list:
        """Default routing for unknown message types"""
        return ["pm_ai_001"]  # Default to product manager
```

## Technical Aspect: Communication Implementation

### 4.1 Message Queue System

#### Redis-based Message Queue
```python
import redis
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime

class MessageQueue:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.queue_prefix = "bee_swarm:queue:"
        self.dlq_prefix = "bee_swarm:dlq:"
    
    def publish_message(self, message: Dict[str, Any], priority: int = 3) -> bool:
        """Publish message to queue"""
        try:
            # Add metadata
            message["id"] = self._generate_message_id()
            message["timestamp"] = datetime.now().isoformat()
            message["priority"] = priority
            message["retry_count"] = 0
            
            # Serialize message
            message_json = json.dumps(message)
            
            # Add to priority queue
            queue_name = f"{self.queue_prefix}{priority}"
            self.redis_client.lpush(queue_name, message_json)
            
            return True
        except Exception as e:
            print(f"Error publishing message: {e}")
            return False
    
    def consume_message(self, role_id: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """Consume message from queue"""
        try:
            # Check queues in priority order
            for priority in range(1, 6):
                queue_name = f"{self.queue_prefix}{priority}"
                
                # Try to get message from this priority queue
                result = self.redis_client.brpop(queue_name, timeout=timeout)
                
                if result:
                    queue, message_json = result
                    message = json.loads(message_json)
                    
                    # Check if message is for this role
                    if self._is_message_for_role(message, role_id):
                        return message
                    else:
                        # Put message back in queue
                        self.redis_client.lpush(queue_name, message_json)
            
            return None
        except Exception as e:
            print(f"Error consuming message: {e}")
            return None
    
    def acknowledge_message(self, message_id: str) -> bool:
        """Acknowledge message processing"""
        try:
            # Remove from processing queue
            self.redis_client.hdel("bee_swarm:processing", message_id)
            return True
        except Exception as e:
            print(f"Error acknowledging message: {e}")
            return False
    
    def move_to_dlq(self, message: Dict[str, Any], error: str) -> bool:
        """Move failed message to dead letter queue"""
        try:
            # Add error information
            message["error"] = error
            message["failed_at"] = datetime.now().isoformat()
            
            # Serialize and add to DLQ
            message_json = json.dumps(message)
            dlq_name = f"{self.dlq_prefix}{message.get('type', 'unknown')}"
            self.redis_client.lpush(dlq_name, message_json)
            
            return True
        except Exception as e:
            print(f"Error moving message to DLQ: {e}")
            return False
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        return f"msg_{int(time.time() * 1000)}_{id(self)}"
    
    def _is_message_for_role(self, message: Dict[str, Any], role_id: str) -> bool:
        """Check if message is intended for specific role"""
        # Check direct assignee
        if message.get("assignee") == role_id:
            return True
        
        # Check role-based routing
        if message.get("to_role"):
            role_mapping = {
                "frontend_developer": ["frontend_ai_001", "frontend_ai_002"],
                "backend_developer": ["backend_ai_001", "backend_ai_002", "backend_ai_003"],
                "qa_engineer": ["qa_ai_001", "qa_ai_002"],
                "product_manager": ["pm_ai_001", "pm_ai_002"],
                "devops_engineer": ["devops_ai_001"]
            }
            
            target_role = message["to_role"]
            if target_role in role_mapping:
                return role_id in role_mapping[target_role]
        
        return False
```

### 4.2 WebSocket Communication

#### WebSocket Server
```python
import asyncio
import websockets
import json
import logging
from typing import Dict, Set, Any

class WebSocketServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.role_clients: Dict[str, Set[str]] = {}
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start WebSocket server"""
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        self.logger.info(f"WebSocket server started on {self.host}:{self.port}")
        
        await server.wait_closed()
    
    async def handle_client(self, websocket, path):
        """Handle client connection"""
        client_id = None
        
        try:
            # Wait for client identification
            async for message in websocket:
                data = json.loads(message)
                
                if data.get("type") == "identify":
                    client_id = data.get("client_id")
                    role_id = data.get("role_id")
                    
                    if client_id and role_id:
                        # Register client
                        self.clients[client_id] = websocket
                        
                        if role_id not in self.role_clients:
                            self.role_clients[role_id] = set()
                        self.role_clients[role_id].add(client_id)
                        
                        self.logger.info(f"Client {client_id} (role: {role_id}) connected")
                        
                        # Send confirmation
                        await websocket.send(json.dumps({
                            "type": "identified",
                            "client_id": client_id,
                            "role_id": role_id
                        }))
                        break
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": "Invalid identification data"
                        }))
                        return
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Expected identification message"
                    }))
                    return
            
            # Handle regular messages
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(client_id, data)
                
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            self.logger.error(f"Error handling client {client_id}: {e}")
        finally:
            # Clean up client registration
            if client_id:
                self._remove_client(client_id)
    
    async def handle_message(self, client_id: str, data: Dict[str, Any]):
        """Handle incoming message from client"""
        message_type = data.get("type")
        
        if message_type == "ping":
            # Respond to ping
            await self.send_to_client(client_id, {
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            })
        
        elif message_type == "status_update":
            # Handle status update
            await self.broadcast_to_role(data.get("role_id"), {
                "type": "status_update",
                "client_id": client_id,
                "status": data.get("status"),
                "timestamp": datetime.now().isoformat()
            })
        
        elif message_type == "task_complete":
            # Handle task completion
            await self.notify_task_completion(data)
        
        else:
            # Unknown message type
            await self.send_to_client(client_id, {
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            })
    
    async def send_to_client(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client"""
        if client_id in self.clients:
            try:
                await self.clients[client_id].send(json.dumps(message))
            except Exception as e:
                self.logger.error(f"Error sending message to {client_id}: {e}")
                self._remove_client(client_id)
    
    async def send_to_role(self, role_id: str, message: Dict[str, Any]):
        """Send message to all clients of a specific role"""
        if role_id in self.role_clients:
            for client_id in self.role_clients[role_id].copy():
                await self.send_to_client(client_id, message)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        for client_id in list(self.clients.keys()):
            await self.send_to_client(client_id, message)
    
    def _remove_client(self, client_id: str):
        """Remove client from registrations"""
        if client_id in self.clients:
            del self.clients[client_id]
        
        # Remove from role clients
        for role_id, clients in self.role_clients.items():
            if client_id in clients:
                clients.remove(client_id)
                if not clients:
                    del self.role_clients[role_id]
                break
    
    async def notify_task_completion(self, data: Dict[str, Any]):
        """Notify relevant roles about task completion"""
        task_type = data.get("task_type")
        role_id = data.get("role_id")
        
        # Determine notification targets based on task type
        if task_type == "api_development":
            # Notify frontend developers
            await self.send_to_role("frontend_developer", {
                "type": "api_ready",
                "api_docs": data.get("api_docs"),
                "completed_by": role_id,
                "timestamp": datetime.now().isoformat()
            })
        
        elif task_type == "frontend_development":
            # Notify QA engineers
            await self.send_to_role("qa_engineer", {
                "type": "frontend_ready",
                "feature": data.get("feature"),
                "completed_by": role_id,
                "timestamp": datetime.now().isoformat()
            })
        
        # Always notify product manager
        await self.send_to_role("product_manager", {
            "type": "task_completed",
            "task": data.get("task"),
            "completed_by": role_id,
            "timestamp": datetime.now().isoformat()
        })
```

### 4.3 HTTP API Communication

#### RESTful API Server
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import asyncio

app = FastAPI(title="Bee Swarm Communication API")

class Message(BaseModel):
    type: str
    content: Dict[str, Any]
    priority: int = 3
    recipients: List[str]
    sender: str

class StatusUpdate(BaseModel):
    role_id: str
    status: str
    workload: int
    current_task: Optional[str] = None

class TaskUpdate(BaseModel):
    task_id: str
    status: str
    progress: int
    comment: Optional[str] = None

# In-memory storage for demonstration
messages = []
status_updates = {}
role_endpoints = {
    "pm_ai_001": "http://pm-01:8000",
    "backend_ai_001": "http://backend-01:8000",
    "frontend_ai_001": "http://frontend-01:8000",
    "qa_ai_001": "http://qa-01:8000",
    "devops_ai_001": "http://devops-01:8000"
}

@app.post("/messages/send")
async def send_message(message: Message, background_tasks: BackgroundTasks):
    """Send message to recipients"""
    try:
        # Store message
        message_data = {
            "id": f"msg_{len(messages) + 1}",
            "type": message.type,
            "content": message.content,
            "priority": message.priority,
            "sender": message.sender,
            "timestamp": datetime.now().isoformat()
        }
        messages.append(message_data)
        
        # Send to recipients in background
        background_tasks.add_task(send_to_recipients, message_data, message.recipients)
        
        return {"success": True, "message_id": message_data["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages/{role_id}")
async def get_messages(role_id: str, limit: int = 10):
    """Get messages for specific role"""
    try:
        # Filter messages for this role
        role_messages = [
            msg for msg in messages
            if role_id in msg.get("recipients", [])
        ]
        
        # Return latest messages
        return {
            "messages": role_messages[-limit:],
            "total": len(role_messages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/status/update")
async def update_status(status: StatusUpdate):
    """Update role status"""
    try:
        status_updates[status.role_id] = {
            "status": status.status,
            "workload": status.workload,
            "current_task": status.current_task,
            "updated_at": datetime.now().isoformat()
        }
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{role_id}")
async def get_status(role_id: str):
    """Get status of specific role"""
    try:
        return status_updates.get(role_id, {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_all_status():
    """Get status of all roles"""
    try:
        return status_updates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/update")
async def update_task(task_update: TaskUpdate):
    """Update task status"""
    try:
        # Update task status
        task_data = {
            "task_id": task_update.task_id,
            "status": task_update.status,
            "progress": task_update.progress,
            "comment": task_update.comment,
            "updated_at": datetime.now().isoformat()
        }
        
        # Notify relevant roles
        await notify_task_update(task_data)
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def send_to_recipients(message_data: Dict[str, Any], recipients: List[str]):
    """Send message to recipients via HTTP"""
    async with httpx.AsyncClient() as client:
        for recipient in recipients:
            if recipient in role_endpoints:
                try:
                    response = await client.post(
                        f"{role_endpoints[recipient]}/messages/receive",
                        json=message_data,
                        timeout=10.0
                    )
                    
                    if response.status_code != 200:
                        print(f"Failed to send message to {recipient}: {response.status_code}")
                        
                except Exception as e:
                    print(f"Error sending message to {recipient}: {e}")

async def notify_task_update(task_data: Dict[str, Any]):
    """Notify relevant roles about task update"""
    # Determine which roles to notify based on task type
    task_id = task_data["task_id"]
    
    # For now, notify all roles
    notification = {
        "type": "task_update",
        "task": task_data,
        "timestamp": datetime.now().isoformat()
    }
    
    async with httpx.AsyncClient() as client:
        for role_id, endpoint in role_endpoints.items():
            try:
                response = await client.post(
                    f"{endpoint}/notifications/receive",
                    json=notification,
                    timeout=5.0
                )
            except Exception as e:
                print(f"Error notifying {role_id}: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### 4.4 Message Validation

#### Message Schema Validation
```python
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class TaskAssignmentMessage(BaseModel):
    type: str = "task_assigned"
    role: str
    issue_number: int
    title: str
    description: str
    priority: str
    estimated_hours: float
    labels: List[str]
    assignee: str
    created_at: str
    deadline: str
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if v not in valid_priorities:
            raise ValueError(f'Priority must be one of {valid_priorities}')
        return v
    
    @validator('estimated_hours')
    def validate_estimated_hours(cls, v):
        if v <= 0:
            raise ValueError('Estimated hours must be positive')
        return v

class ProgressUpdateMessage(BaseModel):
    type: str = "progress_update"
    role: str
    issue_number: int
    status: str
    progress_percentage: int
    comment: str
    updated_at: str
    time_spent: float
    remaining_estimate: float
    
    @validator('progress_percentage')
    def validate_progress_percentage(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Progress percentage must be between 0 and 100')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['not_started', 'in_progress', 'review_requested', 'completed', 'blocked']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of {valid_statuses}')
        return v

class CollaborationRequestMessage(BaseModel):
    type: str = "collaboration_request"
    from_role: str
    to_role: str
    request_type: str
    api_docs_url: Optional[str] = None
    message: str
    priority: str
    requested_at: str
    expected_response_time: str
    
    @validator('request_type')
    def validate_request_type(cls, v):
        valid_types = ['api_review', 'design_review', 'code_review', 'testing_request', 'deployment_request']
        if v not in valid_types:
            raise ValueError(f'Request type must be one of {valid_types}')
        return v

class MessageValidator:
    def __init__(self):
        self.validators = {
            "task_assigned": TaskAssignmentMessage,
            "progress_update": ProgressUpdateMessage,
            "collaboration_request": CollaborationRequestMessage
        }
    
    def validate_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Validate message against schema"""
        message_type = message.get("type")
        
        if message_type not in self.validators:
            return {
                "valid": False,
                "error": f"Unknown message type: {message_type}"
            }
        
        try:
            validator_class = self.validators[message_type]
            validated_message = validator_class(**message)
            
            return {
                "valid": True,
                "message": validated_message.dict()
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def validate_required_fields(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Validate required fields are present"""
        required_fields = {
            "task_assigned": ["role", "issue_number", "title", "description", "assignee"],
            "progress_update": ["role", "issue_number", "status", "progress_percentage"],
            "collaboration_request": ["from_role", "to_role", "request_type", "message"]
        }
        
        message_type = message.get("type")
        
        if message_type not in required_fields:
            return {
                "valid": False,
                "error": f"Unknown message type: {message_type}"
            }
        
        missing_fields = []
        for field in required_fields[message_type]:
            if field not in message or message[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "valid": False,
                "error": f"Missing required fields: {missing_fields}"
            }
        
        return {"valid": True}
```

### 4.5 Error Handling and Retry Logic

#### Retry Mechanism
```python
import asyncio
import time
from typing import Callable, Any, Dict

class RetryHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def retry_async(self, func: Callable, *args, **kwargs) -> Any:
        """Retry async function with exponential backoff"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    print(f"All {self.max_retries + 1} attempts failed. Last error: {e}")
        
        raise last_exception
    
    def retry_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Retry sync function with exponential backoff"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"All {self.max_retries + 1} attempts failed. Last error: {e}")
        
        raise last_exception

class MessageErrorHandler:
    def __init__(self, dlq_client):
        self.dlq_client = dlq_client
        self.retry_handler = RetryHandler()
    
    async def handle_message_error(self, message: Dict[str, Any], error: Exception, context: Dict[str, Any]):
        """Handle message processing errors"""
        error_info = {
            "message_id": message.get("id"),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        # Log error
        print(f"Message error: {error_info}")
        
        # Check if message should be retried
        retry_count = message.get("retry_count", 0)
        max_retries = message.get("max_retries", 3)
        
        if retry_count < max_retries:
            # Increment retry count and retry
            message["retry_count"] = retry_count + 1
            message["last_error"] = error_info
            
            # Add delay before retry
            await asyncio.sleep(self.retry_handler.base_delay * (2 ** retry_count))
            
            return {"action": "retry", "message": message}
        else:
            # Move to dead letter queue
            await self.dlq_client.add_to_dlq(message, error_info)
            
            return {"action": "dlq", "error": error_info}
    
    def should_retry(self, error: Exception) -> bool:
        """Determine if error should be retried"""
        # Don't retry on validation errors
        if isinstance(error, ValueError):
            return False
        
        # Don't retry on authentication errors
        if "unauthorized" in str(error).lower() or "forbidden" in str(error).lower():
            return False
        
        # Retry on network errors, timeouts, etc.
        return True
```

This communication protocol provides comprehensive message handling, routing, validation, and error recovery mechanisms for the AI development team system. 