# Manim 动画模板项目（含自动语音合成）

这是一个基于[Manim](https://www.manim.community/)的动画生成模板项目，用于创建高质量的数学和物理可视化动画。项目中已经包含一些创建好的动画脚本。


## 技术背景

Manim是一个由3Blue1Brown（Grant Sanderson）开发的Python库，用于创建精美的数学解释视频。本项目提供了一个简单的模板，帮助您快速开始使用Manim创建自己的动画。

本项目主要是建立了一个可以较好处理字幕和配音、便于使用的模板。


## 安装指南

### 前提条件

- Python 3.8+
- pip（Python包管理器）
- FFmpeg（用于视频渲染）


### 安装步骤

1. 安装系统级应用：

如果对系统级应用非常熟悉，这里可以自行安装必要的部分。
如果此前已经安装过系统级应用，可以跳过这一步。

首先，默认 apt 源速度在国内有可能速度太慢，可以先如下替换。
如果安装速度正常可以跳过该步骤。
```bash
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
sudo nano /etc/apt/sources.list
```
在 nano 编辑器打开后填入如下内容，保存然后退出
```
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-security main restricted universe multiverse
```

完成源替换后开始安装系统级应用
```bash
sudo apt update
sudo apt install -y \
    build-essential python3-dev python3-pip python3-venv git wget curl \
    texlive-full texlive-latex-extra texlive-fonts-extra texlive-xetex latexmk \
    ffmpeg sox libcairo2-dev libpango1.0-dev libpangocairo-1.0-0 libffi-dev \
    libgl1-mesa-dev libgles2-mesa-dev libegl1-mesa-dev libosmesa6-dev \
    libxi-dev libxrandr-dev libxinerama-dev libxcursor-dev libxext-dev \
    fonts-dejavu fonts-freefont-ttf fonts-noto fonts-roboto fonts-lmodern fonts-cmu \
    xclip xsel libopenmpi-dev libssl-dev \
    libavdevice-dev libavfilter-dev libavformat-dev libavcodec-dev \
    libswresample-dev libswscale-dev libpostproc-dev
sudo apt autoremove -y && sudo apt clean
```

2. 克隆代码仓库：

```bash
git clone https://github.com/liuhao-cn/manim_template.git
cd manim_template
```

3. 创建并激活虚拟环境（推荐）：

```bash
python -m venv manim
source manim/bin/activate
```

4. 安装 python 包：

和前面一样，如果默认的安装源速度太慢，可以先如下替换（速度正常可无需替换）：
```bash
python -m pip install --upgrade pip
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

替换后安装所需的 python 软件包
```bash
pip install -r requirements.txt
```


## API密钥设置

本项目的语音部分使用阿里云语音合成服务，请按以下方式设置API密钥或修改 tts_engine_aliyun 改用你偏好的API：
```bash
echo "export ALIYUNAPI='your_api_key_here'" >> ~/.bashrc
source ~/.bashrc
source manim/bin/activate
```
或者在项目目录下添加并编辑 .env 添加 ALIYUNAPI='your_api_key_here'

**重要安全提示**：
- 切勿将`.env`文件提交到版本控制系统
- 建议将`.env`添加到`.gitignore`

## 使用方法：

将 template.py 和合适的提示词一起喂给大模型进行代码生成。可以参考以下 AI 提示词，
```AI prompt
请基于我提供给你的模板设计一套动画用于展示 xxx，注意遵循以下要求：
- 生成结果应该是一份新的代码，例如 ai_code.py
- 注意使用新的类名并随之更新各输出文件名
- 使用模板自带的字幕和计时相关功能，根据场景需要选择 ThreeDScene 或 Scene 类
- 动画要丰富、深刻、生动、易懂，并添加充足的字幕说明
- 字幕说明的时间要精确计算，默认取 wait=0 即按字数计算
- 你要预估每个字幕的后续动画时间，如果这个时间很长，你应该适当削减字幕的 wait
- 设计字幕时要使用两套文本，一套包含 latex 格式公式用于显示，一套纯文本专用于 tts 阅读，注意 update_subtitle 已经支持两套字幕
- 每个动画动作都要明确地设定 run_time 参数，并相应维护动画计时器 animation_timer
- 先给出详细的策划，经我审核后再进行动画代码的生成
```

## 主要参数配置
在`template.py`中可调整：
```python
# 视频质量设置
quality = "l"  # 可选 l(480p), m(720p), h(1080p), k(4K)
preview = ""  # 改为 -p 可自动预览

# 语音合成设置
voice_name = "longlaotie"  # 推荐发音人：longlaotie/loongbella
self.time_per_char = 0.28  # 每个字符的默认持续时间
```


## FFmpeg 安装

manim 需要 FFmpeg 来处理音频和视频（根据文档，最新版本或可跳过）。请按照以下步骤安装：

### Windows 安装
1. 下载 FFmpeg：访问 [FFmpeg官网](https://ffmpeg.org/download.html) 或 [FFmpeg Windows 构建](https://www.gyan.dev/ffmpeg/builds/)
2. 下载 "FFmpeg Git Full Build" 压缩包并解压
3. 将解压后的 bin 文件夹路径添加到系统环境变量 PATH 中
4. 重启命令提示符或 PowerShell，输入 `ffmpeg -version` 验证安装

### macOS 安装
brew install ffmpeg

### Ubuntu 安装
```
sudo apt update
sudo apt install ffmpeg
```

## 项目结构

```
manim_template/
├── media/             # manim 场景和语音等缓存文件
├── template.py        # 主模板
├── generate_speech.py # 配音模块
├── requirements.txt   # 项目依赖
└── README.md          # 项目说明
```

## 贡献指南

欢迎提交问题和拉取请求！

## 许可证

MIT 