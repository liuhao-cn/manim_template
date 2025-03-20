# 阶段一：构建环境（基于 Ubuntu 22.04）
FROM ubuntu:22.04 as builder

# 基础配置
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APT_SOURCE="http://mirrors.aliyun.com/ubuntu/" \
    UBUNTU_CODENAME="jammy" \
    PY_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple/"

WORKDIR /manim_template

COPY . /manim_template

# 配置APT镜像源（阿里云）
RUN echo "deb ${APT_SOURCE} ${UBUNTU_CODENAME} main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb ${APT_SOURCE} ${UBUNTU_CODENAME}-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb ${APT_SOURCE} ${UBUNTU_CODENAME}-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb ${APT_SOURCE} ${UBUNTU_CODENAME}-proposed main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb ${APT_SOURCE} ${UBUNTU_CODENAME}-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb-src ${APT_SOURCE} ${UBUNTU_CODENAME} main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb-src ${APT_SOURCE} ${UBUNTU_CODENAME}-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb-src ${APT_SOURCE} ${UBUNTU_CODENAME}-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb-src ${APT_SOURCE} ${UBUNTU_CODENAME}-proposed main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb-src ${APT_SOURCE} ${UBUNTU_CODENAME}-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y git sudo lsb-release apt-utils \
    build-essential python3-dev python3-pip python3-venv git \
    ffmpeg libavdevice-dev sox \
    libcairo2-dev libpango1.0-dev \
    libgl1-mesa-dev libxi-dev libxrandr-dev \
    libgles2-mesa-dev libosmesa6-dev \
    fonts-dejavu fonts-freefont-ttf fonts-noto-cjk \
    texlive-latex-base texlive-fonts-recommended \
    texlive-latex-extra texlive-fonts-recommended \
    texlive-lang-chinese texlive-lang-cyrillic cm-super \
    texlive-xetex

RUN pip config set global.index-url ${PY_MIRROR} && \
    cd manim_template && \
    python3 -m venv ./manim && \
    . ./manim/bin/activate && \
    pip install -r requirements.txt && \
    python -m pip install --upgrade pip

# 设置工作目录和PATH
WORKDIR /manim_template
ENV PATH="/manim_template/manim/bin:$PATH"

# 启动时自动进入项目目录并激活虚拟环境
CMD ["/bin/bash", "-c", "cd /manim_template && source /manim_template/manim/bin/activate && /bin/bash"]
