import json
import os
import subprocess
import argparse
from generate_speech import generate_speech
from manim import *

config.tex_template.add_to_preamble(r"""
\usepackage{ctex}
\usepackage{amsmath}
\usepackage{amssymb}
""")

# 根据实际需求可以采用 Scene 或 ThreeDScene 类
class Template(ThreeDScene): 
    # 初始化代码
    def __init__(self):
        super().__init__()
        self.manim_output_dir = 'media' # manim 默认输出文件夹，不要修改
        self.animation_timer = 0.0      # 动画计时器
        self.subtitle_id = 0            # 字幕序号
        self.time_per_char = 0.28       # 单字符语音时间

        # 确保缓存目录存在
        os.makedirs(self.manim_output_dir, exist_ok=True)
        
        # 设定字幕文件
        self.subtitle_file = os.path.join(self.manim_output_dir, f"subtitles_{self.__class__.__name__}.jsonl")

        # 如果字幕文件存在，则清空文件，否则创建文件
        if os.path.exists(self.subtitle_file):
            with open(self.subtitle_file, 'w', encoding='utf-8') as f:
                f.write('')  # 写入空字符串，即清空文件
            print(f"已清空字幕文件: {self.subtitle_file}")
        else:
            os.makedirs(os.path.dirname(self.subtitle_file), exist_ok=True)
        
        # 初始化字幕对象
        self.subtitle = Text("") 
    
    # 用于构建字幕并自动计时的函数
    def update_subtitle(self, text_subtitle, text_voice, wait=0.0, fontsize=28):
        """更新字幕并同步写入字幕文件，包括时间。注意需要内置动画计时器支持"""
        # 如果有旧字幕，先移除
        if hasattr(self, 'subtitle') and self.subtitle is not None:
            self.remove(self.subtitle)
        
        new_subtitle = MathTex(text_subtitle, font_size=fontsize)
        new_subtitle.to_edge(DOWN)

        # 将字幕添加到场景中
        self.add_fixed_in_frame_mobjects(new_subtitle) # 3D 模式下用这个
        # self.add(new_subtitle) # 2D 模式下用这个
        self.subtitle = new_subtitle

        # 将字幕记录到 jsonl 文件，包括编号、开始时间、文本内容
        self.subtitle_id += 1
        subtitle_json = {
            "id":           self.subtitle_id, 
            "text":         text_voice.strip(),  # 移除空白
            "start_time":   self.animation_timer
            }
        with open(self.subtitle_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(subtitle_json, ensure_ascii=False) + '\n')

        # 默认情况下根据字符数目自动决定等待时间
        if wait==0:
            wait = len(text_voice) * self.time_per_char
        else:
            wait = wait
            
        # 等待语音播放并更新动画计时器
        self.wait(wait); self.animation_timer += float(wait)
    
    # 构建动画的主体
    def construct(self):
        # ------------------------------
        # 在这里插入动画代码。
        # ------------------------------
        self.update_subtitle(r"y=x^2", "Hello, World!")


# 主函数
if __name__ == "__main__":
    # 从命令行输入质量参数，例如 -ql 表示低质量
    parser = argparse.ArgumentParser(description="动画模板")
    parser.add_argument("--quality", "-q", type=str, choices=["l", "m", "h", "k"], default="l",
                        help="动画质量：l(低), m(中), h(高), k(4K)")
    args = parser.parse_args()

    buff = Template() # 创建一个虚的对象用于获取字幕文件路径
    class_name = buff.__class__.__name__
    script_filename = os.path.splitext(os.path.basename(__file__))

    # 定义 manim 命令行参数
    quality = args.quality  # 从命令行参数获取质量设置
    voice_name = "longlaotie"  # 可选的有 longlaotie, longbella 等

    # 将质量参数转换为 manim 的输出质量
    quality_to_str = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60",
        "k": "2160p60"
    }; quality_str = quality_to_str.get(quality)

    # 构建并执行 manim 命令，-q 指定渲染质量，-p 指定预览，__file__ 指定当前文件，class_name 指定类名
    cmd = f"manim -q{quality} {__file__} {class_name}"
    result = subprocess.run(cmd, shell=True)

    # 根据 manim 的输出结构确定文件路径
    # 视频文件路径：media/videos/类名/质量标识/类名.mp4
    # 字幕文件在类初始化时会自动设定。
    video_file = f"media/videos/{script_filename[0]}/{quality_str}/{class_name}.mp4"

    # 在字幕文件第一行插入视频文件和音色信息
    with open(buff.subtitle_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(json.dumps({"video_file": video_file, "voice_name": voice_name}, ensure_ascii=False) + '\n' + content)
    
    # 调用语音生成函数，使用阿里云的龙老铁音色，因其断句一般较好
    generate_speech(buff.subtitle_file)
    
    print(f"动画已通过命令行渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}")