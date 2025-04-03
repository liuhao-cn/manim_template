import json
import os
import subprocess
import argparse
import numpy as np
import shutil
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
        self.manim_output_dir = 'media'      # manim 默认输出文件夹
        self.animation_timer = 0.0            # 动画计时器
        self.subtitle_id = 0                  # 字幕序号
        self.time_per_char = 0.28             # 单字符语音时间
        
        # 确保缓存目录存在
        os.makedirs(self.manim_output_dir, exist_ok=True)
        self.subtitle_file = os.path.join(self.manim_output_dir, f"subtitles_{self.__class__.__name__}.jsonl")
        
        # 初始化字幕文件
        if os.path.exists(self.subtitle_file):
            with open(self.subtitle_file, 'w', encoding='utf-8') as f:
                f.write('')  # 写入空字符串，即清空文件
            print(f"已清空字幕文件: {self.subtitle_file}")
        else:
            os.makedirs(os.path.dirname(self.subtitle_file), exist_ok=True)
            
        # 初始化字幕对象
        self.subtitle = Text("")

    def update_subtitle(self, text_subtitle, text_voice=None, wait=0.0, fontsize=28):
        """更新字幕并同步写入字幕文件，包括时间。注意需要内置动画计时器支持"""
        # 如果有旧字幕，先移除
        if hasattr(self, 'subtitle') and self.subtitle is not None:
            self.remove(self.subtitle)
        
        # 如果没有提供语音文本，使用字幕文本
        if text_voice is None:
            text_voice = text_subtitle
            
        # 创建新字幕
        new_subtitle = MathTex(text_subtitle, font_size=fontsize)
        new_subtitle.to_edge(DOWN)
        self.add(new_subtitle)
        self.subtitle = new_subtitle

        # 将字幕记录到 jsonl 文件，包括编号、开始时间、文本内容
        self.subtitle_id += 1
        subtitle_json = {
            "id": self.subtitle_id,
            "text": text_voice.strip(),
            "start_time": self.animation_timer
        }
        with open(self.subtitle_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(subtitle_json, ensure_ascii=False) + '\n')

        # 默认情况下根据字符数目自动决定等待时间
        if wait == 0:
            wait = len(text_voice) * self.time_per_char
            
        # 等待语音播放并更新动画计时器
        self.wait(wait); self.animation_timer += float(wait)
    
    def construct(self):
        # 开场：介绍单连通区域和拓扑变换
        self.update_subtitle(r"\text{下面我们演示单连通区域的拓扑变换}", 
                             "下面我们演示单连通区域的拓扑变换")
        
        # 介绍单连通概念
        self.update_subtitle(r"\text{单连通区域是指其中任意闭合曲线都可以连续收缩为一点的区域}", 
                           "单连通区域是指其中任意闭合曲线都可以连续收缩为一点的区域")
        
        # 介绍拓扑等价概念
        self.update_subtitle(r"\text{而拓扑等价是指两个图形可以通过连续变形相互转化，但不能撕裂或粘合}", 
                           "而拓扑等价是指两个图形可以通过连续变形相互转化，但不能撕裂或粘合")

        # 介绍本演示的主要内容
        self.update_subtitle(r"\text{根据拓扑学原理，所有单连通区域都拓扑等价于圆形}", 
                           "根据拓扑学原理，所有单连通区域都拓扑等价于圆形")

        # 介绍接下来的演示内容
        self.update_subtitle(r"\text{接下来我们将展示几种单连通区域是如何连续变形为圆形的}", 
                           "接下来我们将展示几种单连通区域是如何连续变形为圆形的")
        
        # 1. 方形变换
        square = Square(side_length=2, color=BLUE)
        self.update_subtitle(r"\text{首先是方形区域}", "首先是方形区域")
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
        self.update_subtitle(r"\text{接下来是五角星形区域}", "接下来是五角星形区域")
        star = Star(n=5, outer_radius=1, color=GREEN)
        # 确保五角星朝向一致
        star.rotate(-PI/2)  # 调整初始方向
        self.play(Create(star), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        self.update_subtitle(r"\text{连续变形过程}", "先变形为五边形")
        
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
        self.update_subtitle(r"\text{继续变形为圆形}", "再从五边形变为圆形")
        
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
        self.update_subtitle(r"\text{阿基米德螺线区域}", "现在是一个阿基米德螺线区域")
        
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
        ).set_stroke(width=30)
        
        self.play(Create(spiral_region), run_time=2)
        self.animation_timer += 2  # 更新计时器
        
        self.wait(1)
        self.animation_timer += 1  # 更新计时器
        
        # 逐步减小k值来展开螺线（更精细的步骤）
        self.update_subtitle(r"\text{首先要把螺线打开}", 
                             "这个区域不能直接撑开成圆形，但是可以先把螺线打开，然后再变形", wait=1)
        
        # 为了提高效率，这里可以合并一些帧
        step_count = 200
        for k in np.linspace(1.0, 0.0, step_count):
            new_spiral = ParametricFunction(
                lambda t: spiral_func(t, k),
                t_range=[0, 6*PI],
                color=PURPLE
            ).set_stroke(width=30)
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
        
        # 创建矩形边缘（只有边框，无填充）
        rectangle_edge = Rectangle(
            width=bar_length,
            height=0.22,
            color=PURPLE,
            stroke_width=5,  # 使用细边缘
            fill_opacity=0    # 无填充
        ).move_to(center)
        
        # 先保留展开的螺线，并添加矩形边缘
        self.update_subtitle(r"\text{提取边缘}", "打开为条形后，再提取边缘")
        self.play(FadeIn(rectangle_edge), run_time=1.5)
        self.animation_timer += 1.5  # 更新计时器
        
        self.wait(0.5)
        self.animation_timer += 0.5  # 更新计时器
        
        # 将螺线淡出，保留边缘
        self.play(FadeOut(spiral_region), run_time=1)
        self.animation_timer += 1  # 更新计时器
        
        # 将矩形边缘变形为圆形边缘
        self.update_subtitle(r"\text{撑开为圆形}", "然后按边缘撑开就可以变形为圆形")
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
                           "演示完成，谢谢观看!", wait=4)

# 主函数
if __name__ == "__main__":
    # 从命令行输入质量参数
    parser = argparse.ArgumentParser(description="运行单连通区域变换动画")
    parser.add_argument("--quality", "-q", type=str, choices=["l", "m", "h", "k"], default="l",
                        help="动画质量：l(低), m(中), h(高), k(4K)")
    parser.add_argument("--preview", "-p", action="store_true",
                        help="是否自动预览")
    parser.add_argument("--force", "-f", action="store_true",
                        help="是否强制重新渲染")
    parser.add_argument("--keep-cache", "-k", action="store_true",
                        help="是否保留缓存文件不清除")
    args = parser.parse_args()

    # 创建一个临时对象用于获取字幕文件路径
    buff = TopologyTransformation()
    class_name = buff.__class__.__name__
    script_filename = os.path.splitext(os.path.basename(__file__))

    # 将质量参数转换为 manim 的输出质量
    quality = args.quality
    voice_name = "longlaotie"  # 使用龙老铁音色
    quality_to_str = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60",
        "k": "2160p60"
    }
    quality_str = quality_to_str.get(quality)

    # 构建并执行命令
    preview_flag = "-p" if args.preview else ""
    force_flag = "-f" if args.force else ""
    cmd = f"manim -q{quality} {preview_flag} {force_flag} {__file__} {class_name}"
    print(f"执行命令: {cmd}")
    print("正在渲染动画，请耐心等待...")
    
    # 计时
    import time
    start_time = time.time()
    result = subprocess.run(cmd, shell=True)
    render_time = time.time() - start_time
    print(f"渲染完成！总耗时：{render_time:.2f}秒")

    # 视频文件路径
    video_file = f"media/videos/{script_filename[0]}/{quality_str}/{class_name}.mp4"
    
    # 在字幕文件第一行插入视频文件和音色信息
    with open(buff.subtitle_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(json.dumps({"video_file": video_file, "voice_name": voice_name}, ensure_ascii=False) + '\n' + content)
    
    # 调用语音生成函数
    generate_speech(buff.subtitle_file)
    
    print(f"动画已通过命令行渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}")
    
    # 清理缓存文件（仅当未指定保留缓存时）
    if not args.keep_cache:
        partial_dir = f"media/videos/{script_filename[0]}/{quality_str}/partial_movie_files"
        if os.path.exists(partial_dir):
            shutil.rmtree(partial_dir)
            print(f"已清除部分电影文件缓存: {partial_dir}")
        print("缓存清理完成！")
    else:
        print("根据设置保留了缓存文件") 