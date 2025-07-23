# 基于VNC Lab的项目管理师角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装项目管理专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 文档工具
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 其他工具
    jq \
    unzip \
    # 协作工具
    slack-desktop \
    zoom \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具和项目管理工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装项目管理师专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装Python和pip (用于辅助工具)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装Python项目管理辅助依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    selenium \
    pandas \
    matplotlib \
    seaborn \
    plotly \
    # 项目管理工具
    jira \
    confluence \
    trello \
    asana \
    # 数据分析
    numpy \
    scipy \
    # 报告生成
    reportlab \
    jinja2

# 安装项目管理工具
RUN apt-get update && apt-get install -y \
    # 甘特图工具
    projectlibre \
    # 思维导图工具
    freemind \
    # 流程图工具
    draw.io \
    # 时间管理
    taskwarrior \
    # 笔记工具
    joplin \
    && rm -rf /var/lib/apt/lists/*

# 安装协作和沟通工具
RUN apt-get update && apt-get install -y \
    # 即时通讯
    telegram-desktop \
    discord \
    # 视频会议
    teams \
    # 邮件客户端
    thunderbird \
    # 日历工具
    evolution \
    && rm -rf /var/lib/apt/lists/*

# 安装文档和报告工具
RUN apt-get update && apt-get install -y \
    # 办公套件
    libreoffice \
    # PDF工具
    okular \
    # 图表工具
    dia \
    # 演示工具
    impress \
    && rm -rf /var/lib/apt/lists/*

# 安装项目管理前端工具
RUN npm install -g \
    # 项目管理工具
    @atlassian/jira-cli \
    # 时间跟踪
    timewarrior \
    # 任务管理
    task-cli \
    # 项目分析
    project-analytics

# 创建项目管理工作目录
RUN mkdir -p /app/project_manager \
    /app/projects \
    /app/documents \
    /app/reports \
    /app/meetings \
    /app/templates \
    /app/docs

# 复制项目管理脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建项目管理用户
RUN useradd -m -s /bin/bash project_manager \
    && chown -R project_manager:project_manager /app

# 切换到项目管理用户
USER project_manager

# 设置环境变量
ENV ROLE_NAME=project_manager
ENV ROLE_TYPE=project_manager
ENV WORKSPACE=/app/projects
ENV DOCUMENT_WORKSPACE=/app/documents
ENV REPORT_WORKSPACE=/app/reports
ENV MEETING_WORKSPACE=/app/meetings
ENV TEMPLATE_WORKSPACE=/app/templates

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 