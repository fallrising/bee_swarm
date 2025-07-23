# 基于VNC Lab的安卓开发者角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装安卓开发专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # Java开发环境
    openjdk-11-jdk \
    # 构建工具
    gradle \
    maven \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 其他工具
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 设置Java环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# 安装Node.js和npm (用于AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装安卓开发者专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# 下载并安装Android SDK
RUN mkdir -p $ANDROID_HOME && cd $ANDROID_HOME \
    && wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip \
    && unzip commandlinetools-linux-8512546_latest.zip \
    && rm commandlinetools-linux-8512546_latest.zip \
    && mkdir -p $ANDROID_HOME/cmdline-tools/latest \
    && mv cmdline-tools/* $ANDROID_HOME/cmdline-tools/latest/ \
    && rm -rf cmdline-tools

# 安装Android SDK组件
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses \
    && $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
        "platform-tools" \
        "platforms;android-33" \
        "platforms;android-32" \
        "platforms;android-31" \
        "build-tools;33.0.0" \
        "build-tools;32.0.0" \
        "build-tools;31.0.0" \
        "extras;android;m2repository" \
        "extras;google;m2repository" \
        "extras;intel;Hardware_Accelerated_Execution_Manager"

# 安装Python和pip (用于辅助工具)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装Python安卓开发辅助依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    selenium \
    appium-python-client \
    uiautomator2

# 安装Android Studio (简化版)
RUN wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2022.3.1.20/android-studio-2022.3.1.20-linux.tar.gz \
    && tar -xzf android-studio-2022.3.1.20-linux.tar.gz -C /opt \
    && rm android-studio-2022.3.1.20-linux.tar.gz \
    && ln -s /opt/android-studio/bin/studio.sh /usr/local/bin/android-studio

# 创建安卓开发工作目录
RUN mkdir -p /app/android_developer \
    /app/projects \
    /app/android_projects \
    /app/libraries \
    /app/tests \
    /app/docs

# 复制安卓开发脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建安卓开发用户
RUN useradd -m -s /bin/bash android_developer \
    && chown -R android_developer:android_developer /app

# 切换到安卓开发用户
USER android_developer

# 设置环境变量
ENV ROLE_NAME=android_developer
ENV ROLE_TYPE=android_developer
ENV WORKSPACE=/app/projects
ENV ANDROID_WORKSPACE=/app/android_projects
ENV LIBRARY_WORKSPACE=/app/libraries
ENV TEST_WORKSPACE=/app/tests

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 