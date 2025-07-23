# 基于VNC Lab的DevOps工程师角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装DevOps工程师专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 容器工具
    docker.io \
    docker-compose \
    # 云平台CLI
    awscli \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 网络工具
    netcat \
    telnet \
    nmap \
    # 监控工具
    prometheus \
    grafana \
    # 其他工具
    jq \
    yq \
    kubectl \
    helm \
    terraform \
    ansible \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装DevOps工程师专用AI工具
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
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Python DevOps依赖
RUN pip3 install \
    # 云平台SDK
    boto3 \
    google-cloud-storage \
    azure-mgmt-compute \
    # 容器工具
    docker \
    kubernetes \
    # 配置管理
    ansible \
    salt \
    # 监控和日志
    prometheus-client \
    grafana-api \
    elasticsearch \
    # CI/CD
    jenkins \
    gitlab \
    github3.py \
    # 安全工具
    bandit \
    safety \
    # 其他工具
    requests \
    yaml \
    jinja2 \
    click

# 安装Go (用于云原生工具)
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz \
    && rm go1.21.0.linux-amd64.tar.gz

# 设置Go环境变量
ENV PATH=$PATH:/usr/local/go/bin
ENV GOPATH=/go
ENV GOROOT=/usr/local/go

# 安装Go DevOps工具
RUN go install github.com/hashicorp/terraform@latest \
    && go install github.com/helm/helm@latest \
    && go install github.com/kubernetes/kubectl@latest

# 创建DevOps工程师工作目录
RUN mkdir -p /app/devops_engineer \
    /app/projects \
    /app/infrastructure \
    /app/ci_cd \
    /app/monitoring \
    /app/security \
    /app/docs

# 复制DevOps工程师脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建DevOps工程师用户
RUN useradd -m -s /bin/bash devops_engineer \
    && chown -R devops_engineer:devops_engineer /app

# 将用户添加到docker组
RUN usermod -aG docker devops_engineer

# 切换到DevOps工程师用户
USER devops_engineer

# 设置环境变量
ENV ROLE_NAME=devops_engineer
ENV ROLE_TYPE=devops_engineer
ENV WORKSPACE=/app/projects
ENV INFRASTRUCTURE_WORKSPACE=/app/infrastructure
ENV CI_CD_WORKSPACE=/app/ci_cd
ENV MONITORING_WORKSPACE=/app/monitoring
ENV SECURITY_WORKSPACE=/app/security

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 