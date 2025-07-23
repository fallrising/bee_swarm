# 基于VNC Lab的Unity开发者角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装Unity开发专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 图形库
    libgl1-mesa-glx \
    libglu1-mesa \
    libxrandr2 \
    libxinerama1 \
    libxcursor1 \
    libxi6 \
    # 音频库
    libasound2 \
    libpulse0 \
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

# 安装Unity开发者专用AI工具
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

# 安装Python Unity开发辅助依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    selenium \
    unity-python-api \
    blender-python-api

# 安装Mono (Unity脚本运行时)
RUN apt-get update && apt-get install -y \
    mono-complete \
    mono-devel \
    && rm -rf /var/lib/apt/lists/*

# 安装Unity Hub (简化版)
RUN mkdir -p /opt/unity-hub \
    && echo "Unity Hub (Linux模拟版本)" > /opt/unity-hub/README.md

# 安装Unity编辑器 (简化版)
RUN mkdir -p /opt/unity-editor \
    && echo "Unity Editor (Linux模拟版本)" > /opt/unity-editor/README.md

# 安装Blender (用于3D建模)
RUN apt-get update && apt-get install -y \
    blender \
    && rm -rf /var/lib/apt/lists/*

# 安装GIMP (用于图像编辑)
RUN apt-get update && apt-get install -y \
    gimp \
    && rm -rf /var/lib/apt/lists/*

# 安装Audacity (用于音频编辑)
RUN apt-get update && apt-get install -y \
    audacity \
    && rm -rf /var/lib/apt/lists/*

# 安装游戏开发工具
RUN apt-get update && apt-get install -y \
    # 物理引擎
    bullet \
    # 音频处理
    ffmpeg \
    # 图像处理
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# 创建Unity开发工作目录
RUN mkdir -p /app/unity_developer \
    /app/projects \
    /app/unity_projects \
    /app/assets \
    /app/scripts \
    /app/tests \
    /app/docs

# 复制Unity开发脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建Unity开发用户
RUN useradd -m -s /bin/bash unity_developer \
    && chown -R unity_developer:unity_developer /app

# 切换到Unity开发用户
USER unity_developer

# 设置环境变量
ENV ROLE_NAME=unity_developer
ENV ROLE_TYPE=unity_developer
ENV WORKSPACE=/app/projects
ENV UNITY_WORKSPACE=/app/unity_projects
ENV ASSET_WORKSPACE=/app/assets
ENV SCRIPT_WORKSPACE=/app/scripts
ENV TEST_WORKSPACE=/app/tests

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 