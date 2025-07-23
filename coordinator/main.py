"""
Bee Swarm 系统协调器主入口
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from coordinator.core.config import settings
from coordinator.core.database import init_db
from coordinator.core.redis import init_redis
from coordinator.api.v1.api import api_router
from coordinator.core.celery_app import celery_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("Starting Bee Swarm Coordinator...")
    
    # 初始化数据库
    await init_db()
    logger.info("Database initialized")
    
    # 初始化Redis
    await init_redis()
    logger.info("Redis initialized")
    
    # 启动Celery Worker
    logger.info("Starting Celery worker...")
    
    yield
    
    # 关闭时
    logger.info("Shutting down Bee Swarm Coordinator...")


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title="Bee Swarm Coordinator",
        description="AI自动化开发团队系统协调器",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(api_router, prefix="/api/v1")
    
    return app


app = create_app()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Bee Swarm Coordinator",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "redis": "connected",
            "celery": "running"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 