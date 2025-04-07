import json
import os
import subprocess
import argparse
import numpy as np
from generate_speech import generate_speech
from manim import *

config.tex_template.add_to_preamble(r"""
\usepackage{ctex}
\usepackage{amsmath}
\usepackage{amssymb}
""")

scaler = 2

# 参数方程的定义
def param_a(k):
    """参数方程 a(k) 的实现"""
    term1 = 3 * k / (2 * 10**4)
    term2 = np.sin(np.pi/2 * (k/10**4)**7) * np.cos(41*k*np.pi/10**4)**6
    term3 = 0.25 * np.cos(41*k*np.pi/10**4)**16 * np.cos(k*np.pi/(2*10**4))**12 * np.sin(6*k*np.pi/10**4)
    return scaler * (term1 + term2 + term3)

def param_b(k):
    """参数方程 b(k) 的实现"""
    term1 = 0.5 * np.cos(3*k*np.pi/10**5)**10 * np.cos(9*k*np.pi/10**5)**10 * np.cos(18*k*np.pi/10**5)**10
    term2 = np.cos(np.pi/2 * (k/10**4)**7) * (1 + 1.5 * np.cos(k*np.pi/(2*10**4))**6 * np.cos(3*k*np.pi/(2*10**4))**6) * np.cos(41*k*np.pi/10**4)**6
    return scaler * (term1 - term2 + 0.5)

class LineArtAnimation(Scene):
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
        # self.add_fixed_in_frame_mobjects(new_subtitle) # 3D 模式下用这个
        self.add(new_subtitle) # 2D 模式下用这个
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
        # 设置坐标系
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-1, 1, 0.5],
            axis_config={"color": BLUE},
            x_length=12,
            y_length=6
        )
        
        # 介绍参数方程
        self.update_subtitle(
            r"\text{参数方程是用一个变量 } k \text{ 同时表示 } x \text{ 和 } y \text{ 的方程}",
            "参数方程是用一个变量 k 同时表示 x 和 y 的方程"
        )
        
        # 显示公式
        eq_a = MathTex(
            r"a(k) = \frac{3k}{2 \cdot 10^4} + \sin \left( \frac{\pi}{2} \left( \frac{k}{10^4} \right)^7 \right) \cos^6 \left( \frac{41k\pi}{10^4} \right) + \frac{1}{4} \cos^{16} \left( \frac{41k\pi}{10^4} \right) \cos^{12} \left( \frac{k\pi}{2 \cdot 10^4} \right) \sin \left( \frac{6k\pi}{10^4} \right)",
            font_size=24
        ).shift(UP * 2.5)
        
        self.play(Write(eq_a), run_time=3)
        self.animation_timer += 3
        
        eq_b = MathTex(
            r"b(k) = \frac{1}{2} \cos^{10} \left( \frac{3k\pi}{10^5} \right) \cos^{10} \left( \frac{9k\pi}{10^5} \right) \cos^{10} \left( \frac{18k\pi}{10^5} \right) - \cos \left( \frac{\pi}{2} \left( \frac{k}{10^4} \right)^7 \right) \left( 1 + \frac{3}{2} \cos^6 \left( \frac{k\pi}{2 \cdot 10^4} \right) \cos^6 \left( \frac{3k\pi}{2 \cdot 10^4} \right) \right) \cos^6 \left( \frac{41k\pi}{10^4} \right)",
            font_size=24
        ).shift(UP * 1.5)
        
        self.play(Write(eq_b), run_time=3)
        self.animation_timer += 3
        
        k_range = MathTex(r"-10^4 \leq k \leq 10^4", font_size=28).shift(UP * 0.5)
        self.play(Write(k_range), run_time=1)
        self.animation_timer += 1
        
        # 简化说明参数方程
        self.update_subtitle(
            r"\text{这组复杂的参数方程将绘制一只小鸟}",
            "这组复杂的参数方程将绘制一只小鸟"
        )
        
        # 准备开始绘制
        self.update_subtitle(
            r"\text{现在让我们观察曲线如何随着参数 } k \text{ 的变化被绘出}",
            "现在让我们观察曲线如何随着参数 k 的变化被绘出"
        )
        
        # 隐藏方程
        self.play(
            FadeOut(eq_a),
            FadeOut(eq_b),
            FadeOut(k_range),
            run_time=1
        )
        self.animation_timer += 1
        
        self.play(Create(axes), run_time=2)

        # 生成参数点并创建曲线
        k_values = np.linspace(-10000, 10000, 10000)
        points = []
        for k in k_values:
            a = param_a(k)
            b = param_b(k)
            points.append([a, b, 0])
        
        # 创建渐变色曲线
        parametric_curve = VMobject()
        parametric_curve.set_points_smoothly(points)
        parametric_curve.set_stroke(width=2.5)
        parametric_curve.set_color_by_gradient([BLUE, GREEN, YELLOW, RED])
        
        # 添加点跟踪器
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(points[0][0], points[0][1]))
        
        # 绘制曲线动画
        self.update_subtitle(
            r"\text{随着参数 }k\text{ 从 }-10^4\text{ 到 }10^4\text{ 变化，曲线逐渐成形}",
            "随着参数 k 从负一万到一万变化，曲线逐渐成形", 
            wait=2
        )
        
        self.add(dot)
        
        # 使用UpdateFromAlphaFunc绘制曲线
        def update_curve(mob, alpha):
            n = int(alpha * len(points))
            if n > 0:
                mob.set_points_smoothly(points[:n])
                # 更新点的位置
                dot.move_to(axes.c2p(points[n-1][0], points[n-1][1]))
                
        self.play(
            UpdateFromAlphaFunc(parametric_curve, update_curve),
            run_time=10
        )
        self.animation_timer += 15
        
        # 移除跟踪点
        self.play(FadeOut(dot), run_time=0.5)
        self.animation_timer += 0.5
        
        # 完整展示曲线
        self.update_subtitle(
            r"\text{这就是我们的参数曲线，犹如一只小鸟}",
            "这就是我们的参数曲线，犹如一只小鸟"
        )
        
        # 放大观察细节
        self.update_subtitle(
            r"\text{让我们放大观察曲线的细节部分}",
            "让我们放大观察曲线的细节部分", 
            wait=2
        )
        
        # 选择放大的区域
        self.play(
            axes.animate.scale(3).move_to(ORIGIN - 1),
            parametric_curve.animate.scale(3).move_to(ORIGIN - 1),
            run_time=3
        )
        self.animation_timer += 3
        
        # 总结
        self.update_subtitle(
            r"\text{简单的数学公式可以创造出令人惊叹的视觉艺术}",
            "简单的数学公式可以创造出令人惊叹的视觉艺术"
        )
        
        # 结束画面
        self.play(
            FadeOut(parametric_curve),
            FadeOut(axes),
            run_time=2
        )
        self.animation_timer += 2

        self.update_subtitle(
            r"\text{感谢观看}",
            "感谢观看", 
            wait=3
        )


# 主函数
if __name__ == "__main__":
    # 从命令行输入质量参数，例如 -ql 表示低质量
    parser = argparse.ArgumentParser(description="参数方程线条画动画")
    parser.add_argument("--quality", "-q", type=str, choices=["l", "m", "h", "k"], default="l",
                        help="动画质量：l(低), m(中), h(高), k(4K)")
    args = parser.parse_args()

    buff = LineArtAnimation() # 创建一个虚的对象用于获取字幕文件路径
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
    # generate_speech(buff.subtitle_file)
    
    print(f"动画已通过命令行渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}") 