# 基于VNC Lab的视觉设计师角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装视觉设计专用工具
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
    # 字体工具
    fonts-liberation \
    fonts-dejavu \
    fonts-noto \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 其他工具
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具和前端工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装视觉设计师专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装设计工具
RUN apt-get update && apt-get install -y \
    # 图像编辑
    gimp \
    inkscape \
    # 矢量图形
    inkscape \
    # 3D建模
    blender \
    # 视频编辑
    kdenlive \
    # 音频编辑
    audacity \
    # 截图工具
    flameshot \
    # 颜色管理
    gcolor2 \
    # 字体管理
    font-manager \
    && rm -rf /var/lib/apt/lists/*

# 安装Python和pip (用于辅助工具)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 安装Python设计辅助依赖
RUN pip3 install \
    requests \
    beautifulsoup4 \
    selenium \
    pillow \
    matplotlib \
    seaborn \
    plotly \
    bokeh \
    # 图像处理
    opencv-python \
    scikit-image \
    # 颜色处理
    colorthief \
    # 字体处理
    fonttools \
    # 设计工具
    svglib \
    reportlab

# 安装前端设计工具
RUN npm install -g \
    # 设计系统工具
    storybook \
    # 原型工具
    figma-cli \
    # 图标工具
    svgo \
    # 颜色工具
    color2k \
    # 字体工具
    fontmin \
    # 图像优化
    imagemin \
    imagemin-pngquant \
    imagemin-mozjpeg \
    imagemin-gifsicle \
    imagemin-svgo

# 安装设计资源管理工具
RUN apt-get update && apt-get install -y \
    # 文件管理器
    nautilus \
    # 压缩工具
    p7zip-full \
    # 批量重命名
    rename \
    && rm -rf /var/lib/apt/lists/*

# 安装设计参考工具
RUN apt-get update && apt-get install -y \
    # 浏览器
    firefox \
    chromium-browser \
    # 文档查看器
    evince \
    # 媒体播放器
    vlc \
    && rm -rf /var/lib/apt/lists/*

# 创建视觉设计工作目录
RUN mkdir -p /app/visual_designer \
    /app/projects \
    /app/designs \
    /app/assets \
    /app/templates \
    /app/resources \
    /app/docs

# 复制视觉设计脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建视觉设计用户
RUN useradd -m -s /bin/bash visual_designer \
    && chown -R visual_designer:visual_designer /app

# 切换到视觉设计用户
USER visual_designer

# 设置环境变量
ENV ROLE_NAME=visual_designer
ENV ROLE_TYPE=visual_designer
ENV WORKSPACE=/app/projects
ENV DESIGN_WORKSPACE=/app/designs
ENV ASSET_WORKSPACE=/app/assets
ENV TEMPLATE_WORKSPACE=/app/templates
ENV RESOURCE_WORKSPACE=/app/resources

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 