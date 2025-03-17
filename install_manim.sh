#!/bin/bash

# Manim 模板项目自动化安装脚本（兼容多版本）

# -------------------------------
# 配置区（可按需修改）
REPO_URL="https://github.com/liuhao-cn/manim_template.git"
PY_MIRROR="https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
APT_MIRROR_FILE="/etc/apt/sources.list"
# -------------------------------

# 获取系统版本信息
UBUNTU_CODENAME=$(lsb_release -cs)  # 动态获取系统代号

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "检测到需要管理员权限，请输入密码："
    sudo -v
fi

# 函数：显示带颜色的状态消息
status_msg() {
    echo -e "\033[1;34m[*] $1\033[0m"
}

success_msg() {
    echo -e "\033[1;32m[✓] $1\033[0m"
}

error_msg() {
    echo -e "\033[1;31m[!] $1\033[0m"
    exit 1
}

# 步骤 1：替换 APT 源（动态适配系统版本）
replace_apt_source() {
    status_msg "正在更换APT镜像源（适配$UBUNTU_CODENAME）..."
    
    # 备份原配置文件
    sudo cp "$APT_MIRROR_FILE" "${APT_MIRROR_FILE}.bak" || error_msg "备份原APT源失败"
    
    # 生成新版源配置
    sudo tee "$APT_MIRROR_FILE" > /dev/null <<EOF
# 国内 Ubuntu 镜像源（自动适配系统版本）
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME} main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-proposed main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME} main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-proposed main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ ${UBUNTU_CODENAME}-backports main restricted universe multiverse
EOF

    # 优化更新流程
    sudo rm -rf /var/lib/apt/lists/*
    sudo apt clean
    sudo apt update || {
        echo -e "\n\033[1;33m[!] 检测到镜像源更新失败，尝试备用方案...\033[0m"
        # 尝试恢复为官方源
        sudo cp "${APT_MIRROR_FILE}.bak" "$APT_MIRROR_FILE" || {
            echo -e "\033[1;33m[!] 无法恢复备份，手动配置官方源\033[0m"
            sudo tee "$APT_MIRROR_FILE" > /dev/null <<EOF
# Ubuntu 官方源
deb http://archive.ubuntu.com/ubuntu/ ${UBUNTU_CODENAME} main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ ${UBUNTU_CODENAME}-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ ${UBUNTU_CODENAME}-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ ${UBUNTU_CODENAME}-backports main restricted universe multiverse
EOF
        }
        sudo apt update || error_msg "APT 更新失败，请手动检查网络连接和源配置"
    }
    success_msg "APT 源配置完成"
}

# 步骤 2：安装系统依赖（适配多版本）
install_dependencies() {
    status_msg "正在安装系统依赖..."
    
    # 基础编译工具链
    sudo apt install -y build-essential python3-dev python3-pip python3-venv git
    
    # 多媒体处理相关
    sudo apt install -y ffmpeg libavdevice-dev sox
    
    # 图形渲染依赖
    sudo apt install -y libcairo2-dev libpango1.0-dev \
        libgl1-mesa-dev libxi-dev libxrandr-dev \
        libgles2-mesa-dev libosmesa6-dev
    
    # 字体支持
    sudo apt install -y fonts-dejavu fonts-freefont-ttf fonts-noto-cjk
    
    # TeXLive 组件（动态适配版本）
    if [[ "$UBUNTU_CODENAME" == "focal" || "$UBUNTU_CODENAME" == "jammy" ]]; then
        # 执行 tex 最小化安装组合
        sudo apt install -y --ignore-missing texlive-base texlive-latex-recommended \
            texlive-latex-extra texlive-fonts-recommended \
            texlive-lang-chinese texlive-lang-cyrillic cm-super \
            texlive-xetex && \
        sudo apt-mark hold texlive-context
    else
        # 原有轻量安装已不含 context
        sudo apt install -y texlive texlive-xetex texlive-lang-chinese
    fi

    
    # 清理系统
    sudo apt autoremove -y && sudo apt clean
    success_msg "系统依赖安装完成"
}

# 步骤 3：克隆项目仓库
clone_repo() {
    status_msg "正在克隆项目仓库..."
    if [ -d "manim_template" ]; then
        read -p "检测到已存在 manim_template 目录，是否覆盖？[y/N] " choice
        case "$choice" in
            y|Y) rm -rf manim_template ;;
            *) exit 0 ;;
        esac
    fi
    
    git clone "$REPO_URL" || error_msg "克隆仓库失败"
    cd manim_template || error_msg "进入项目目录失败"
    success_msg "项目克隆完成"
}

# 步骤 4：配置虚拟环境
setup_venv() {
    status_msg "正在配置 Python 虚拟环境..."
    python3 -m venv manim || error_msg "创建虚拟环境失败"
    source manim/bin/activate || error_msg "激活虚拟环境失败"
    
    python -m pip install --upgrade pip || error_msg "升级 pip 失败"
    pip config set global.index-url "$PY_MIRROR" || error_msg "配置 PyPI 镜像失败"
    success_msg "虚拟环境配置完成"
}

# 步骤 5：安装 Python 依赖
install_python_deps() {
    status_msg "正在安装 Python 依赖..."
    pip install -r requirements.txt || error_msg "安装依赖失败"
    success_msg "Python 依赖安装完成"
}

# 步骤 6：配置 API 密钥
setup_api_key() {
    status_msg "正在配置 API 密钥..."
    read -p "请输入阿里云语音合成 API 密钥（留空可跳过）：" api_key
    if [ -n "$api_key" ]; then
        # 将 API 密钥写入 .bashrc
        echo "export ALIYUNAPI='$api_key'" >> ~/.bashrc || error_msg "写入密钥失败"
        success_msg "API 密钥已保存至 ~/.bashrc"
    else
        echo "跳过 API 密钥配置"
    fi
}

# 主安装流程
main() {
    replace_apt_source
    install_dependencies
    clone_repo
    setup_venv
    install_python_deps
    setup_api_key
    
    echo
    success_msg "安装完成！"
    echo -e "后续操作指南：\n1. 激活 API 密钥：source ~/.bashrc\n2.进入项目目录：cd manim_template\n3. 激活虚拟环境：source manim/bin/activate\n4. 测试动画模板：python3 template.py\n"
}

# 执行主流程
main
