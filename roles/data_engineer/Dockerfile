# 基于VNC Lab的数据工程师角色容器
FROM vnc-llm-cli:latest

# 设置工作目录
WORKDIR /app

# 安装数据工程专用工具
RUN apt-get update && apt-get install -y \
    # 开发工具
    git \
    curl \
    wget \
    # 数据库工具
    postgresql-client \
    mysql-client \
    sqlite3 \
    # 系统工具
    tree \
    htop \
    nano \
    vim \
    # 其他工具
    jq \
    unzip \
    # 数据处理工具
    csvkit \
    xmlstarlet \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm (用于AI工具)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装数据工程师专用AI工具
RUN npm install -g \
    @google/gemini-cli \
    @anthropic-ai/claude-code \
    @rovo-dev/cli \
    @cursor/cli

# 安装Python和pip (主要数据工具)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Python数据工程核心依赖
RUN pip3 install \
    # 数据处理
    pandas \
    numpy \
    scipy \
    # 数据可视化
    matplotlib \
    seaborn \
    plotly \
    bokeh \
    # 机器学习
    scikit-learn \
    tensorflow \
    pytorch \
    # 数据库连接
    psycopg2-binary \
    pymysql \
    sqlalchemy \
    # 大数据处理
    pyspark \
    dask \
    vaex \
    # 数据质量
    great-expectations \
    pandas-profiling \
    # 工作流管理
    apache-airflow \
    prefect \
    # 数据存储
    h5py \
    parquet-tools \
    # 网络请求
    requests \
    beautifulsoup4 \
    selenium \
    # 其他工具
    jupyter \
    jupyterlab \
    ipython

# 安装Go (用于高性能数据处理)
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz \
    && rm go1.21.0.linux-amd64.tar.gz

# 设置Go环境变量
ENV PATH=$PATH:/usr/local/go/bin
ENV GOPATH=/go
ENV GOROOT=/usr/local/go

# 安装Go数据工具
RUN go install github.com/go-delve/delve/cmd/dlv@latest \
    && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# 安装数据库和数据处理工具
RUN apt-get update && apt-get install -y \
    # 数据库
    postgresql \
    mysql-server \
    redis-server \
    mongodb \
    # 大数据工具
    hadoop \
    spark \
    kafka \
    # 数据仓库
    clickhouse-server \
    # 监控工具
    prometheus \
    grafana \
    && rm -rf /var/lib/apt/lists/*

# 安装数据可视化工具
RUN apt-get update && apt-get install -y \
    # 图表工具
    gnuplot \
    # 地理数据处理
    gdal-bin \
    # 统计工具
    r-base \
    rstudio \
    && rm -rf /var/lib/apt/lists/*

# 安装R数据科学包
RUN R -e "install.packages(c('tidyverse', 'ggplot2', 'dplyr', 'tidyr', 'readr', 'purrr', 'tibble', 'stringr', 'forcats'), repos='https://cran.rstudio.com/')"

# 安装数据工程前端工具
RUN npm install -g \
    # 数据可视化
    d3 \
    chart.js \
    # 数据处理
    lodash \
    moment \
    # 数据分析
    mathjs \
    statistics

# 安装Apache Airflow (工作流管理)
RUN pip3 install apache-airflow[postgres,redis,celery]

# 创建数据工程工作目录
RUN mkdir -p /app/data_engineer \
    /app/data \
    /app/pipelines \
    /app/models \
    /app/reports \
    /app/notebooks \
    /app/docs

# 复制数据工程脚本
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# 设置权限
RUN chmod +x /app/scripts/*.sh

# 创建数据工程用户
RUN useradd -m -s /bin/bash data_engineer \
    && chown -R data_engineer:data_engineer /app

# 切换到数据工程用户
USER data_engineer

# 设置环境变量
ENV ROLE_NAME=data_engineer
ENV ROLE_TYPE=data_engineer
ENV WORKSPACE=/app/data
ENV PIPELINE_WORKSPACE=/app/pipelines
ENV MODEL_WORKSPACE=/app/models
ENV REPORT_WORKSPACE=/app/reports
ENV NOTEBOOK_WORKSPACE=/app/notebooks

# 暴露端口
EXPOSE 6080 7681

# 启动命令
CMD ["/app/scripts/start.sh"] 