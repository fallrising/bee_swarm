# 基于VNC Lab的iOS开发者角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装iOS开发专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 构建工具
    cmake \
    ninja-build \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 其他工具
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装iOS开发者专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装Swift (Linux版本)
RUN wget https://download.swift.org/swift-5.8-release/ubuntu2204/swift-5.8-RELEASE-ubuntu22.04.tar.gz \
    && tar -xzf swift-5.8-RELEASE-ubuntu22.04.tar.gz -C /opt \
    && rm swift-5.8-RELEASE-ubuntu22.04.tar.gz \
    && ln -s /opt/swift-5.8-RELEASE-ubuntu22.04/usr/bin/swift /usr/local/bin/swift

# 设置Swift环境变量
ENV PATH=$PATH:/opt/swift-5.8-RELEASE-ubuntu22.04/usr/bin

# 安装Python和pip (用于辅助工具)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装Python iOS开发辅助依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    selenium \
    appium-python-client \
    fastlane

# 安装CocoaPods (Ruby gem)
RUN apt-get update && apt-get install -y \
    ruby \
    ruby-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN gem install cocoapods

# 安装Fastlane
RUN gem install fastlane

# 安装Xcode命令行工具 (模拟)
RUN mkdir -p /opt/xcode-command-line-tools \
    && echo "Xcode Command Line Tools (Linux模拟版本)" > /opt/xcode-command-line-tools/README.md

# 创建iOS开发工作目录
RUN mkdir -p /app/ios_developer \
    /app/projects \
    /app/ios_projects \
    /app/frameworks \
    /app/tests \
    /app/docs

# 复制iOS开发脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建iOS开发用户
RUN useradd -m -s /bin/bash ios_developer \
    && chown -R ios_developer:ios_developer /app

# 切换到iOS开发用户
USER ios_developer

# 设置环境变量
ENV ROLE_NAME=ios_developer
ENV ROLE_TYPE=ios_developer
ENV WORKSPACE=/app/projects
ENV IOS_WORKSPACE=/app/ios_projects
ENV FRAMEWORK_WORKSPACE=/app/frameworks
ENV TEST_WORKSPACE=/app/tests

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 