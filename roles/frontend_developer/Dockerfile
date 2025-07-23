# 基于VNC Lab的前端开发者角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装前端开发专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 设计工具
    inkscape \
    gimp \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 其他工具
    jq \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于前端开发和AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装前端开发专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli \
    @warp/cli

# 安装前端开发框架和工具
RUN npm install -g \
    # 包管理器
    yarn \
    pnpm \
    # 构建工具
    webpack \
    vite \
    # 框架CLI
    @vue/cli \
    @angular/cli \
    create-react-app \
    # 代码质量工具
    eslint \
    prettier \
    stylelint \
    # 测试工具
    jest \
    cypress \
    # 其他工具
    typescript \
    @types/node

# 安装Python和pip (用于辅助工具)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装Python前端开发辅助依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    selenium \
    playwright

# 安装Playwright浏览器
RUN playwright install chromium firefox webkit

# 创建前端开发工作目录
RUN mkdir -p /app/frontend_developer \
    /app/projects \
    /app/components \
    /app/pages \
    /app/styles \
    /app/tests \
    /app/docs

# 复制前端开发脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建前端开发用户
RUN useradd -m -s /bin/bash frontend_developer \
    && chown -R frontend_developer:frontend_developer /app

# 切换到前端开发用户
USER frontend_developer

# 设置环境变量
ENV ROLE_NAME=frontend_developer
ENV ROLE_TYPE=frontend_developer
ENV WORKSPACE=/app/projects
ENV COMPONENT_WORKSPACE=/app/components
ENV PAGE_WORKSPACE=/app/pages
ENV STYLE_WORKSPACE=/app/styles
ENV TEST_WORKSPACE=/app/tests

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 