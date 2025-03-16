import json
import os
import subprocess
import numpy as np
from manim import *

# 根据实际需求可以采用 Scene 或 ThreeDScene 类
class Template(ThreeDScene): 
    # 初始化代码
    def __init__(self):
        super().__init__()
        # 初始化输出文件夹、总时间计数器、字幕编号、字幕字体大小、单字符语音时间
        self.default_output_dir = 'media'
        self.animation_timer = 0.0
        self.subtitle_id = 0
        self.time_per_char = 0.28

        # 确保缓存目录存在
        os.makedirs(self.default_output_dir, exist_ok=True)
        self.subtitle_file = os.path.join(self.default_output_dir, f"subtitles_{self.__class__.__name__}.jsonl")

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
    def update_subtitle(self, text_subtitle, text_voice, wait=0.0, fontsize=24):
        """更新字幕并同步写入字幕文件，包括时间。注意需要内置动画计时器支持"""
        # 如果有旧字幕，先移除
        if hasattr(self, 'subtitle') and self.subtitle is not None:
            self.remove(self.subtitle)
        
        # 如果文本不为空，则创建新字幕
        if text_subtitle:
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
            wait = len(text) * self.time_per_char
        else:
            wait = wait
            
        # 等待语音播放并更新动画计时器
        self.wait(wait); self.animation_timer += float(wait)
    
    # 构建动画的主体
    def construct(self):
        # ------------------------------
        # 在这里插入动画代码。
        # ------------------------------
        print("在这里插入动画代码。")

        




# 主函数
if __name__ == "__main__":
    # 定义 manim 命令行参数
    quality = "l"  # 可选的有 l, m, h, k
    preview = ""   # 不自动预览，若需要预览可设为 "-p"
    voice_name = "longlaotie"  # 可选的有 longlaotie, longbella 等

    buff = Template() # 创建一个虚的对象用于获取字幕文件路径

    print(f"字幕文件路径：{buff.subtitle_file}")
    
    quality_to_str = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60",
        "k": "2160p60"
    }; quality_str = quality_to_str.get(quality)

    # 构建并执行 manim 命令，-q 指定渲染质量，-p 指定预览，__file__ 指定当前文件，Template 指定类名
    cmd = f"manim -q{quality} {preview} {__file__} Template"
    result = subprocess.run(cmd, shell=True)

    from generate_speech import generate_speech
    # 根据 manim 的输出结构确定文件路径
    # 视频文件路径：media/videos/template/质量标识/类名.mp4
    # 字幕文件在类初始化时会自动设定。
    video_file = f"media/videos/template/{quality_str}/Template.mp4"
    
    # 调用语音生成函数，使用阿里云的龙老铁音色，因其断句一般较好
    generate_speech(video_file, buff.subtitle_file, voice_name)
    
    print(f"动画已通过命令行渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}")