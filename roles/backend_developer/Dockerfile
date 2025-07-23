# 基于VNC Lab的后端开发者角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装后端开发专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 数据库工具
    postgresql-client \
    mysql-client \
    redis-tools \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 网络工具
    netcat \
    telnet \
    # 其他工具
    jq \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装后端开发专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli \
    @warp/cli

# 安装Python和pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Python后端开发依赖
RUN pip3 install \
    fastapi \
    uvicorn \
    sqlalchemy \
    alembic \
    psycopg2-binary \
    redis \
    requests \
    pydantic \
    pytest \
    pytest-asyncio \
    black \
    flake8 \
    mypy \
    pre-commit

# 安装Go (用于高性能后端开发)
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz \
    && rm go1.21.0.linux-amd64.tar.gz

# 设置Go环境变量
ENV PATH=$PATH:/usr/local/go/bin
ENV GOPATH=/go
ENV GOROOT=/usr/local/go

# 创建后端开发工作目录
RUN mkdir -p /app/backend_developer \
    /app/projects \
    /app/apis \
    /app/databases \
    /app/tests \
    /app/docs

# 复制后端开发脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建后端开发用户
RUN useradd -m -s /bin/bash backend_developer \
    && chown -R backend_developer:backend_developer /app

# 切换到后端开发用户
USER backend_developer

# 设置环境变量
ENV ROLE_NAME=backend_developer
ENV ROLE_TYPE=backend_developer
ENV WORKSPACE=/app/projects
ENV API_WORKSPACE=/app/apis
ENV DB_WORKSPACE=/app/databases
ENV TEST_WORKSPACE=/app/tests

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 