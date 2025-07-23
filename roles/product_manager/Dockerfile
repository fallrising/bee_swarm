# 基于VNC Lab的产品经理角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装产品经理专用工具
RUN apt-get update && apt-get install -y \
    # 项目管理工具
    git \
    curl \
    wget \
    # 文档工具
    pandoc \
    markdown \
    # 设计工具
    inkscape \
    gimp \
    # 其他工具
    tree \
    htop \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装产品经理专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装Python和pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    pandas \
    matplotlib \
    jupyter \
    notebook

# 创建产品经理工作目录
RUN mkdir -p /app/product_manager \
    /app/projects \
    /app/templates \
    /app/docs

# 复制产品经理脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建产品经理用户
RUN useradd -m -s /bin/bash product_manager \
    && chown -R product_manager:product_manager /app

# 切换到产品经理用户
USER product_manager

# 设置环境变量
ENV ROLE_NAME=product_manager
ENV ROLE_TYPE=product_manager
ENV WORKSPACE=/app/projects
ENV TEMPLATES=/app/templates
ENV DOCS=/app/docs

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 