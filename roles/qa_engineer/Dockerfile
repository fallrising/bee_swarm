# 基于VNC Lab的QA工程师角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装QA工程师专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 测试工具
    jmeter \
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

# 安装Node.js和npm (用于AI工具和前端测试)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装QA工程师专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装测试框架和工具
RUN npm install -g \
    # 测试框架
    jest \
    cypress \
    playwright \
    # 性能测试
    artillery \
    k6 \
    # 代码质量
    eslint \
    prettier \
    # 其他工具
    typescript \
    @types/node

# 安装Python和pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Python测试依赖
RUN pip3 install \
    # 测试框架
    pytest \
    pytest-asyncio \
    pytest-cov \
    pytest-html \
    pytest-xdist \
    # 自动化测试
    selenium \
    playwright \
    robotframework \
    robotframework-seleniumlibrary \
    # API测试
    requests \
    httpx \
    pytest-httpx \
    # 性能测试
    locust \
    # 数据验证
    jsonschema \
    cerberus \
    # 报告生成
    allure-pytest \
    # 其他工具
    beautifulsoup4 \
    pandas \
    matplotlib

# 安装Playwright浏览器
RUN playwright install chromium firefox webkit

# 安装Java (用于JMeter)
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# 设置Java环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# 创建QA工程师工作目录
RUN mkdir -p /app/qa_engineer \
    /app/projects \
    /app/test_cases \
    /app/test_reports \
    /app/test_data \
    /app/automation \
    /app/docs

# 复制QA工程师脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建QA工程师用户
RUN useradd -m -s /bin/bash qa_engineer \
    && chown -R qa_engineer:qa_engineer /app

# 切换到QA工程师用户
USER qa_engineer

# 设置环境变量
ENV ROLE_NAME=qa_engineer
ENV ROLE_TYPE=qa_engineer
ENV WORKSPACE=/app/projects
ENV TEST_CASE_WORKSPACE=/app/test_cases
ENV TEST_REPORT_WORKSPACE=/app/test_reports
ENV TEST_DATA_WORKSPACE=/app/test_data
ENV AUTOMATION_WORKSPACE=/app/automation

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 