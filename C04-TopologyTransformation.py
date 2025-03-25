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

class TopologyTransformation(Scene):
    def __init__(self):
        super().__init__()
        self.manim_output_dir = 'media'
        self.animation_timer = 0.0
        self.subtitle_id = 0
        self.time_per_char = 0.28
        self.subtitle_file = os.path.join(self.manim_output_dir, "subtitles_TopologyTransformation.jsonl")
        
        # 初始化字幕文件
        if os.path.exists(self.subtitle_file):
            with open(self.subtitle_file, 'w', encoding='utf-8') as f:
                f.write('')
        else:
            os.makedirs(os.path.dirname(self.subtitle_file), exist_ok=True)

    def update_subtitle(self, text_subtitle, text_voice, wait=0.0, fontsize=28):
        """更新字幕并同步写入字幕文件"""
        if hasattr(self, 'subtitle'):
            self.remove(self.subtitle)
        
        new_subtitle = MathTex(text_subtitle, font_size=fontsize)
        new_subtitle.to_edge(DOWN)
        self.add(new_subtitle)
        self.subtitle = new_subtitle

        # 写入字幕文件
        self.subtitle_id += 1
        subtitle_json = {
            "id": self.subtitle_id,
            "text": text_voice.strip(),
            "start_time": self.animation_timer
        }
        with open(self.subtitle_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(subtitle_json, ensure_ascii=False) + '\n')

        wait = len(text_voice) * self.time_per_char if wait == 0 else wait
        self.wait(wait)
        self.animation_timer += float(wait)

    def construct(self):
        # 开场：介绍单连通区域和拓扑变换
        self.update_subtitle(r"\text{单连通区域拓扑变换}", "欢迎观看单连通区域拓扑变换演示")
        
        # 介绍单连通概念
        self.update_subtitle(r"\text{单连通区域：任意闭合曲线可收缩为一点}", 
                           "单连通区域是指其中任意闭合曲线都可以连续收缩为一点的区域")
        
        # 介绍拓扑等价概念
        self.update_subtitle(r"\text{拓扑等价：可通过连续变形相互转化，但不能撕裂或粘合}", 
                           "拓扑等价是指两个图形可以通过连续变形相互转化，不允许撕裂或粘合")

        # 介绍本演示的主要内容
        self.update_subtitle(r"\text{单连通区域定理：所有单连通区域拓扑等价于圆}", 
                           "根据拓扑学原理，所有单连通区域都拓扑等价于圆形")

        # 介绍接下来的演示内容
        self.update_subtitle(r"\text{下面将展示几种典型单连通区域变形为圆的过程}", 
                           "接下来我们将展示几种典型单连通区域连续变形为圆形的过程")
        
        # 1. 方形变换
        square = Square(side_length=2, color=BLUE)
        self.update_subtitle(r"\text{方形单连通区域}", "首先展示方形区域")
        self.play(Create(square), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        circle = Circle(radius=1, color=RED)
        self.update_subtitle(r"\text{连续变形过程}", "现在变形为圆形")
        
        # 使用ReplacementTransform并固定形状方向，避免扭转
        # 创建中间形状帮助过渡
        rounded_square = RoundedRectangle(
            width=2, height=2,
            corner_radius=0.5,
            color=BLUE
        )
        
        self.play(ReplacementTransform(square, rounded_square), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        self.play(ReplacementTransform(rounded_square, circle), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        self.wait(1)
        self.animation_timer += 1  # 更新计时器

        self.play(FadeOut(circle), run_time=0.1)
        self.animation_timer += 0.1  # 更新计时器

        # 2. 五角星变换
        self.update_subtitle(r"\text{五角星单连通区域}", "接下来是五角星形")
        star = Star(n=5, outer_radius=1, color=GREEN)
        # 确保五角星朝向一致
        star.rotate(-PI/2)  # 调整初始方向
        self.play(Create(star), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        self.update_subtitle(r"\text{连续变形过程}", "正在变形为五边形")
        
        # 创建正五边形作为过渡形状（不添加到场景中）
        pentagon = RegularPolygon(n=5, color=GREEN)
        pentagon.scale(1)      # 调整大小
        pentagon.rotate(-PI/2)  # 保持方向一致
        
        # 从五角星变形为五边形
        self.play(Transform(star, pentagon), run_time=3)
        self.animation_timer += 3  # 更新计时器
        
        self.wait(1)
        self.animation_timer += 1  # 更新计时器
        
        # 从五边形变形为圆形
        self.update_subtitle(r"\text{继续变形为圆形}", "从五边形变形为圆形")
        
        # 创建圆形作为变换目标（不添加到场景中）
        target_circle = Circle(radius=1, color=RED)
        
        # 确保明确的变化过程
        self.play(star.animate.become(target_circle), run_time=3)  # 使用animate.become而不是Transform
        self.animation_timer += 3  # 更新计时器
        
        self.wait(1)
        self.animation_timer += 1  # 更新计时器
        
        # 保存引用以便后续使用
        circle = star

        self.play(FadeOut(circle), run_time=0.1)
        self.animation_timer += 0.1  # 更新计时器

        # 3. 阿基米德螺线区域变换 - 直接开始
        self.update_subtitle(r"\text{阿基米德螺线区域}", "现在展示阿基米德螺线区域")
        
        # 创建螺线区域（带宽度的闭合区域）
        def spiral_func(t, k=1.0):
            return np.array([
                t/4 * np.cos(k*t),
                t/4 * np.sin(k*t),
                0
            ])
            
        spiral_region = ParametricFunction(
            lambda t: spiral_func(t),
            t_range=[0, 6*PI],
            color=PURPLE
        ).set_stroke(width=15)
        
        self.play(Create(spiral_region), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        self.wait(1)
        self.animation_timer += 1  # 更新计时器
        
        # 逐步减小k值来展开螺线（更精细的步骤）
        self.update_subtitle(r"\text{逐步展开螺线}", "正在逐步展开螺线")
        
        # 为了提高效率，这里可以合并一些帧
        step_count = 200
        for k in np.linspace(1.0, 0.0, step_count):
            new_spiral = ParametricFunction(
                lambda t: spiral_func(t, k),
                t_range=[0, 6*PI],
                color=PURPLE
            ).set_stroke(width=15)
            self.play(Transform(spiral_region, new_spiral), run_time=0.05)
            self.animation_timer += 0.05  # 更新计时器
        
        # 获取展开后螺线的实际长度和位置信息
        points = np.array(spiral_region.points)
        x_min = np.min(points[:, 0])
        x_max = np.max(points[:, 0])
        bar_length = x_max - x_min  # 实际条形长度
        
        # 计算矩形中心点位置
        center_x = (x_max + x_min) / 2
        center_y = np.median(points[:, 1])
        center = np.array([center_x, center_y, 0])
        
        # 边缘高度
        edge_height = 0.3
        
        # 创建矩形边缘（只有边框，无填充）
        rectangle_edge = Rectangle(
            width=bar_length,
            height=edge_height-0.1,
            color=PURPLE,
            stroke_width=5,  # 使用细边缘
            fill_opacity=0    # 无填充
        ).move_to(center)
        
        # 先保留展开的螺线，并添加矩形边缘
        self.update_subtitle(r"\text{计算条形边缘}", "计算展开后的条形边缘")
        self.play(FadeIn(rectangle_edge), run_time=1.5)
        self.animation_timer += 1.5  # 更新计时器
        
        self.wait(0.5)
        self.animation_timer += 0.5  # 更新计时器
        
        # 将螺线淡出，保留边缘
        self.play(FadeOut(spiral_region), run_time=1)
        self.animation_timer += 1  # 更新计时器
        
        # 将矩形边缘变形为圆形边缘
        self.update_subtitle(r"\text{边缘变形为圆形}", "然后将条形边缘变形为圆形")
        circle_edge = Circle(
            radius=bar_length/2,  # 直径等于条形长度
            color=PURPLE,
            stroke_width=5,    # 保持细边缘
            fill_opacity=0     # 无填充
        ).move_to(center)  # 圆心在条形中心
        
        self.play(Transform(rectangle_edge, circle_edge), run_time=4)
        self.animation_timer += 4  # 更新计时器
        
        self.wait(1)
        self.animation_timer += 1  # 更新计时器
        
        # 可选：调整为标准圆形颜色
        final_circle = Circle(
            radius=bar_length/2,
            color=RED,
            stroke_width=5,
            fill_opacity=0
        ).move_to(center)
        
        self.play(rectangle_edge.animate.become(final_circle), run_time=1)
        self.animation_timer += 1  # 更新计时器
        
        # 最终总结
        self.update_subtitle(r"\text{所有单连通区域都拓扑等价于圆}", 
                           "演示完成，谢谢观看")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="单连通区域变换动画")
    parser.add_argument("--quality", "-q", type=str, choices=["l", "m", "h", "k"], default="l",
                       help="动画质量：l(低), m(中), h(高), k(4K)")
    args = parser.parse_args()

    buff = TopologyTransformation()
    class_name = buff.__class__.__name__
    script_filename = os.path.splitext(os.path.basename(__file__))[0]

    # 质量参数转换
    quality_to_str = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60",
        "k": "2160p60"
    }
    quality_str = quality_to_str.get(args.quality)

    # 执行manim渲染
    cmd = f"manim -q{args.quality} {__file__} {class_name}"
    subprocess.run(cmd, shell=True)

    # 处理视频和字幕文件
    video_file = f"media/videos/{script_filename}/{quality_str}/{class_name}.mp4"
    with open(buff.subtitle_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(json.dumps({"video_file": video_file, "voice_name": "longlaotie"}, ensure_ascii=False) + '\n' + content)
    
    # 生成语音
    generate_speech(buff.subtitle_file)
    
    print(f"动画渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}") 