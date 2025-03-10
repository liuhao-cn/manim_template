# Manim 动画模板项目（含自动语音合成）

这是一个基于[Manim](https://www.manim.community/)的动画生成模板项目，用于创建高质量的数学和物理可视化动画。

## 项目简介

Manim是一个由3Blue1Brown（Grant Sanderson）开发的Python库，用于创建精美的数学解释视频。本项目提供了一个简单的模板，帮助您快速开始使用Manim创建自己的动画。

## 安装指南

### 前提条件

- Python 3.7+
- pip（Python包管理器）
- FFmpeg（用于视频渲染）

### 安装步骤

1. 克隆此仓库：

```bash
git clone https://github.com/liuhao-cn/manim_template.git
cd manim_template
```

2. 创建并激活虚拟环境（推荐）：

```bash
# 在Windows上
python -m venv venv
venv\Scripts\activate

# 在Linux/MacOS上
python -m venv venv
source venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

## API密钥设置

本项目使用阿里云Dashscope的语音合成服务，请按以下步骤设置API密钥或修改 tts_engine_aliyun 改用你偏好的API：

1. 在项目根目录创建`.env`文件
2. 添加阿里云API密钥：
```env
ALIYUNAPI=your_api_key_here
```


**重要安全提示**：
- 切勿将`.env`文件提交到版本控制系统
- 建议将`.env`添加到`.gitignore`

## 使用方法：

可参考以下 AI 提示词：
```AI prompt
请基于这里的模板设计一套动画用于展示 xxx，注意遵循以下要求：
- 将 template.py 拷贝一份为 ai_code.py，在新文件中进行生成。
- 注意使用新的类名并随之更新结果文件名
- 使用模板自带的字幕和计时相关功能，按需切换 ThreeDScene 或 Scene 类
- 展示说明要深刻、生动、易懂并添加充足的字幕说明
- 字幕说明的时间要精确计算，默认按每个字 0.3 秒，如果后续的动画时间比较长，应该相应削减字幕的 wait
- 每个动画动作都要明确地设定 run_time 参数，并相应维护动画计时器 animation_timer
- 先给出详细的策划，经我审核后再进行动画代码的生成
```

## 关键参数配置
在`template.py`中可调整：
```python
# 视频质量设置
quality = "l"  # 可选 l(480p), m(720p), h(1080p), k(4K)
preview = ""  # 改为 -p 可自动预览

# 语音合成设置
voice_name = "longlaotie"  # 推荐发音人：longlaotie/loongbella
self.time_per_char = 0.3  # 每个字符的默认持续时间
```

## 依赖安装
确保已安装所有依赖
```bash
pip install -r requirements.txt
```

## FFmpeg 安装

本项目需要 FFmpeg 来处理音频和视频。请按照以下步骤安装：

### Windows 安装
1. 下载 FFmpeg：访问 [FFmpeg官网](https://ffmpeg.org/download.html) 或 [FFmpeg Windows 构建](https://www.gyan.dev/ffmpeg/builds/)
2. 下载 "FFmpeg Git Full Build" 压缩包并解压
3. 将解压后的 bin 文件夹路径添加到系统环境变量 PATH 中
4. 重启命令提示符或 PowerShell，输入 `ffmpeg -version` 验证安装

### macOS 安装
使用 Homebrew 安装：

### Ubuntu 安装
使用 apt 包管理器安装：
```
sudo apt update
sudo apt install ffmpeg
```

## 项目结构

```
manim_template/
├── scenes/            # 您的场景文件
├── examples/          # 示例场景
├── assets/            # 图像、音频等资源文件
├── utils/             # 实用工具函数
├── requirements.txt   # 项目依赖
└── README.md          # 项目说明
```

## 贡献指南

欢迎提交问题和拉取请求！

## 许可证

MIT 