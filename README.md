# Manim 动画模板项目（含自动语音合成）

这是一个基于[Manim](https://www.manim.community/)的动画生成模板项目，用于创建高质量的数学和物理可视化动画。项目中已经包含一些创建好的动画脚本。


## 技术背景

Manim是一个由3Blue1Brown（Grant Sanderson）开发的Python库，用于创建精美的数学解释视频。本项目提供了一个简单的模板，帮助您快速开始使用Manim创建自己的动画。

本项目主要是建立了一个可以较好处理字幕和配音、便于使用的模板。


## 安装指南

### 克隆代码仓库：

```bash
git clone https://github.com/liuhao-cn/manim_template.git
cd manim_template
```

### 一键安装（文件尾部介绍了可选的手动安装方法）

确定已经进入代码仓库后：
```bash
chmod +x install_manim.sh
./install_manim.sh
```


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
voice_name = "longlaotie"  # 推荐发音人：longlaotie/loongbella
self.time_per_char = 0.28  # 朗读字幕时每个字符的默认占用时间
```

## 运行方式
```bash
python3 ai_code.py -ql  # -ql、-qm、-qh、-qk = 480、720、1080、2160 画质
```
默认情况下会自动完成配音，如果配音字幕不同步，应该优先检查是否每个 run_time 后面都有对应的时间累加代码。如果只需要微调或者只需要修改音色，也可以手动打开 media 目录下对应的字幕文件编辑字幕时间，并在第一行调整音色，然后运行以下命令单独配音：
```bash
python3 generate_speech.py path/to/your/subtitle/file
```
部分可选音色代码和对应的阿里云官方介绍包括：

| 音色代码      | 描述|
|-|-|
| longwan       | 龙婉声音温柔甜美，富有亲和力，给人温暖陪伴感。|
| longcheng     | 龙橙声音温柔清澈，富有亲和力，是邻家的温暖大哥哥。|
| longhua       | 龙华声音活泼可爱，有趣生动，是孩子们的好朋友。|
| longxiaochun  | 龙小淳的嗓音如丝般柔滑，温暖中流淌着亲切与抚慰，恰似春风吹过心田。|
| longxiaoxia   | 龙小夏以温润磁性的声线，宛如夏日细雨，悄然滋润听者心灵，营造恬静氛围。|
| longjing      | 龙婧的嗓音庄重而凛然，精准传达严肃主题，赋予话语以权威与力量。|
| longyue       | 龙悦以抑扬顿挫、韵味十足的评书腔调，生动讲述故事，引领听众步入传奇世界！|
| longxiaobai   | 龙小白以轻松亲和的声调，演绎闲适日常，其嗓音如邻家女孩般亲切自然。|
| longshu       | 龙书以专业、沉稳的播报风格，传递新闻资讯，其嗓音富含权威与信赖感。|
| longyuan      | 龙媛以细腻入微、情感丰富的嗓音，将小说人物与情节娓娓道来，引人入胜。|
| longshuo      | 龙硕嗓音充满活力与阳光，如暖阳照耀，增添无限正能量，使人精神焕发。|
| longlaotie    | 龙老铁以纯正东北腔，豪爽直率，幽默风趣，为讲述增添浓郁地方特色与生活气息。|
| loongbella    | Bella2.0 以精准干练的播报风格，传递全球资讯，其专业女声犹如新闻现场的引导者。|
| loongstella   | Stella2.0以其飒爽利落的嗓音，演绎独立女性风采，展现坚韧与力量之美。|
| longjielidou  | 龙杰力豆以和煦如春阳的童声娓娓道来，透出了欣欣向荣的生命力，温暖每一个倾听的耳朵。|

可参考阿里云语音合成体验页面寻找更多音色，或使用序列猴子等 tts 引擎。


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



## 附录：手动安装方法

如果希望自行控制整个安装流程，请按以下提示进行：

1. 安装系统级应用：

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

sudo apt install -y build-essential python3-dev python3-pip python3-venv git

sudo apt install -y ffmpeg libavdevice-dev sox

sudo apt install -y libcairo2-dev libpango1.0-dev \
    libgl1-mesa-dev libxi-dev libxrandr-dev \
    libgles2-mesa-dev libosmesa6-dev

sudo apt install -y fonts-dejavu fonts-freefont-ttf fonts-noto-cjk

sudo apt-mark hold texlive-context

sudo apt install -y --ignore-missing texlive-base texlive-latex-recommended \
    texlive-latex-extra texlive-fonts-recommended \
    texlive-lang-chinese texlive-lang-cyrillic cm-super \
    texlive-xetex

# 如果 latex 安装有问题，可以尝试这个：
# sudo apt install -y texlive texlive-xetex texlive-lang-chinese 

sudo apt autoremove -y && sudo apt clean
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

5. API密钥设置

本项目的语音部分使用阿里云语音合成服务，请按以下方式设置API密钥或修改 tts_engine_aliyun 改用你偏好的API：
```bash
echo "export ALIYUNAPI='your_api_key_here'" >> ~/.bashrc
source ~/.bashrc
source manim/bin/activate
```