from manim import *
import json
import os
import shutil
import argparse
import numpy as np
import matplotlib.cm as cm
import subprocess
from generate_speech import generate_speech

# 定义复函数
def complex_function1(z):
    return z**2/2

def complex_function2(z):
    return z**3/4 - z**2/2 + z

def complex_function3(z):
    x = z.real
    y = z.imag
    return (x+y) + (x**2+y**2)/2*1j


# 定义复函数对应的 latex 文本公式
latex_formula1 = "f(z) = z^2/2"
latex_formula2 = "f(z) = z^3/4 - z^2/2 + z"
latex_formula3 = "f(z) = (x+y) + \mathbf{i}(x^2+y^2)/2"
# 定义复函数自变量的范围
z_scale = 1.0


# 使用数值方法计算函数值的微分（注意不是导数）
def numerical_derivative(z, function, num_segments=360):
    """使用数值微分计算复数函数在点z处的导数
    返回一个列表，包含不同方向上的导数值
    """
    epsilon = 1e-5

    # 生成dz的角度
    dz_angles = np.linspace(0, 2 * np.pi, num_segments, endpoint=False)
    
    # 计算所有方向的dz
    dzs = epsilon * (np.cos(dz_angles) + 1j * np.sin(dz_angles))
    
    # 计算所有方向的df，归一化到epsilon
    dfs = function(z + dzs) - function(z)
    dfs = dfs / epsilon

    return dz_angles, dfs


# 获取 viridis 颜色映射
def get_viridis_color(t):
    """获取 viridis 颜色映射中对应 t 的颜色
    
    参数:
        t: 0到1之间的值
        
    返回:
        RGB颜色值
    """
    rgba = cm.viridis(t)
    return rgb_to_color(rgba[:3])


# 复函数可视化演示
class ComplexFunctionVisualization(Scene):
    def __init__(self):
        super().__init__()
        # 初始化总时间计数器
        self.animation_timer = 0.0
        self.subtitle_id = 0
        self.time_per_char = 0.28      # 单字符语音时间
        self.default_output_dir = 'media'

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
        self.subtitle = Text("", font_size=28)
    
    def update_subtitle(self, text_subtitle, text_voice=None, wait=0.0, fontsize=24):
        """更新字幕并同步写入字幕文件，包括时间。注意需要内置动画计时器支持"""
        # 如果有旧字幕，先移除
        if hasattr(self, 'subtitle') and self.subtitle is not None:
            self.remove(self.subtitle)
        
        # 如果没有提供语音文本，使用字幕文本
        if text_voice is None:
            text_voice = text_subtitle
            
        if text_subtitle:
            # 创建新字幕
            new_subtitle = Text(text_subtitle, font_size=fontsize)
            new_subtitle.to_edge(DOWN)

            # 将字幕添加到场景中
            # self.add_fixed_in_frame_mobjects(new_subtitle) # 3D 模式下
            self.add(new_subtitle) # 2D 模式下
            self.subtitle = new_subtitle

            # 将字幕记录到 jsonl 文件，包括编号、开始时间、文本内容
            self.subtitle_id += 1
            subtitle_json = {
                "id":           self.subtitle_id, 
                "text":         text_voice.strip(),  # 移除空白
                "start_time":   self.animation_timer
                }
        
            # 写入字幕数据
            with open(self.subtitle_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(subtitle_json, ensure_ascii=False) + '\n')

        # 默认情况下根据字符数目自动决定等待时间
        if wait == 0:
            wait = len(text_voice) * self.time_per_char
            
        # 等待语音播放并更新动画计时器
        self.wait(wait); self.animation_timer += float(wait)
    
    def demonstrate_path(self, complex_plane, function, path_type_text, path_name, path_creator):
        """演示特定路径上的函数变化
        
        参数:
            complex_plane: 复平面对象
            function: 复函数
            path_type_text: 路径类型文本对象
            path_name: 路径名称
            path_creator: 创建路径的函数
        """
        # path_type_text = Text(path_name).to_corner(UR).set_color(WHITE)

        self.update_subtitle(f"现在是{path_name}", f"现在是{path_name}", wait=2)

        
        # 创建路径
        z_path, start_point = path_creator()
        
        # 创建表示 z 和 f(z) 的点
        z_dot = Dot(complex_plane.n2p(start_point), color=RED)
        f_dot = Dot(complex_plane.n2p(function(start_point)), color=YELLOW)
        
        # # 添加标签
        # z_label = MathTex("z").next_to(z_dot, DOWN).set_color(RED)
        # f_label = MathTex("f(z)").next_to(f_dot, DOWN).set_color(YELLOW)
        
        # 创建路径跟踪
        z_path_trace = TracedPath(z_dot.get_center, stroke_width=3, stroke_color=RED)
        f_path_trace = TracedPath(f_dot.get_center, stroke_width=3, stroke_color=YELLOW)
        
        # 添加点和路径跟踪
        # self.update_subtitle("红色点表示变量 z，黄色点表示函数值 f(z)", wait=0.5)
        self.play(
            Create(z_dot), Create(f_dot),
            # Write(z_label), Write(f_label),
            Create(z_path_trace), Create(f_path_trace),
            run_time=2.0
        )
        self.animation_timer += 2.0
        
        # 创建动画
        def update_f_dot(mob):
            # 获取 z 的复数值
            z_pos = complex_plane.p2n(z_dot.get_center())
            # 计算 f(z) 的值
            f_z = function(z_pos)
            # 更新 f(z) 点的位置
            mob.move_to(complex_plane.n2p(f_z))
            # 更新 f(z) 标签的位置
            # f_label.next_to(mob, DOWN)
        
        # 设置 f_dot 的更新函数
        f_dot.add_updater(update_f_dot)
        
        # 沿路径移动 z 点
        # self.update_subtitle(f"观察当 z 沿{path_name}移动时，f(z) 的轨迹", wait=0.5)
        self.play(
            MoveAlongPath(z_dot, z_path),
            # UpdateFromFunc(z_label, lambda m: m.next_to(z_dot, DOWN)),
            run_time=10.0
        )
        self.animation_timer += 10.0
        
        # 移除更新器
        f_dot.clear_updaters()
        
        # 暂停一下
        # self.update_subtitle(f"注意 f(z) 的轨迹形状，这反映了函数 {latex_formula} 的特性", wait=1.0)
        
        # 清除点和路径
        self.play(
            FadeOut(z_dot), FadeOut(f_dot),
            # FadeOut(z_label), FadeOut(f_label),
            FadeOut(z_path_trace), FadeOut(f_path_trace), 
            FadeOut(path_type_text),
            run_time=1.5
        )
        self.animation_timer += 1.5


    def demo_path_combined(self, complex_plane, path_type, function):
        # label_obj = None
        # 1. 矩形路径演示
        self.demonstrate_path(
            complex_plane, function, 
            path_type, "矩形路径", 
            self.create_rectangle_path,
        )
        
        # 2. 圆形路径演示
        self.demonstrate_path(
            complex_plane, function, 
            path_type, "圆形路径", 
            self.create_circle_path,
        )
        
        # 3. 径向路径演示
        self.demonstrate_path(
            complex_plane, function, 
            path_type, "径向路径", 
            self.create_radial_path,
        )
        
        # 4. 阿基米德螺线路径演示
        self.demonstrate_path(
            complex_plane, function, 
            path_type, "阿基米德螺线", 
            self.create_archimedes_spiral_path,
        )


    def demonstrate_derivative(self, complex_plane, function):
        """展示复函数在不同点的导数特性
        
        参数:
            complex_plane: 复平面对象
            function: 复函数
        """
        # 选择几个关键点展示导数
        test_points = [
            complex(1, 0),
            complex(2, 0),
            complex(0, 1),
            complex(-1, 0),
            complex(-2, 0),
            complex(0, -1),
            complex(0, -2),
            complex(1, 1),
            complex(2, 2),
            complex(1, -1),
            complex(2, -2),
        ]

        for i, z_point in enumerate(test_points):
            # 在复平面上标记当前点
            z_dot = Dot(complex_plane.n2p(z_point), color=RED)
            # z_label = MathTex("z").next_to(z_dot, DOWN).set_color(RED)
            
            # 计算函数值
            f_z = function(z_point)
            f_dot = Dot(complex_plane.n2p(f_z), color=YELLOW)
            # f_label = MathTex("f(z)").next_to(f_dot, DOWN).set_color(YELLOW)
            
            # 添加点和标签
            self.play(
                Create(z_dot), 
                # Write(z_label),
                Create(f_dot), 
                # Write(f_label),
                run_time=1.0
            )
            self.animation_timer += 1.0
            
            # 计算导数
            num_segments = 720  # 减少段数以提高性能
            dz_angles, dfs = numerical_derivative(z_point, function, num_segments)
            
            # 创建 dz 圆环和 df 圆环
            dz_radius = 0.5
            
            # 创建彩色环的新方法
            dz_segments = VGroup()
            df_segments = VGroup()
            
            # 为每个方向创建一个线段
            for j in range(num_segments):
                # 计算当前段的角度
                angle = dz_angles[j]
                
                # 计算颜色（基于角度的归一化值）
                t = angle / (2 * np.pi)
                color = get_viridis_color(t)
                
                # 计算 dz 线段的起点和终点
                start_point = complex_plane.n2p(z_point)
                end_point = start_point + np.array([
                    dz_radius * np.cos(angle),
                    dz_radius * np.sin(angle),
                    0
                ])
                start_point = (start_point + 3*end_point)/4
                
                # 创建 dz 线段
                dz_line = Line(
                    start=start_point,
                    end=end_point,
                    stroke_width=3,
                    color=color
                )
                dz_segments.add(dz_line)
                
                # 获取对应角度的导数值
                df_value = dfs[j]
                
                # 将复数导数值转换为向量
                df_vector = np.array([df_value.real, df_value.imag, 0])
                
                # 缩放导数向量，使其与 dz_radius 成比例
                df_vector = df_vector * dz_radius if abs(df_value) > 0 else np.zeros(3)
                
                # 计算 df 线段的起点和终点
                start_point = complex_plane.n2p(f_z)
                end_point = start_point + df_vector
                start_point = (start_point + 3*end_point)/4
                
                # 创建 df 线段，使用与 dz 相同的颜色
                df_line = Line(
                    start=start_point,
                    end=end_point,
                    stroke_width=3,
                    color=color  # 使用与 dz 相同的颜色
                )
                df_segments.add(df_line)
            
            # 显示 dz 线段组
            self.play(
                Create(dz_segments),
                run_time=2
            )
            self.animation_timer += 2
            self.wait(2)  # 额外等待时间
            self.animation_timer += 2
            
            # 显示 df 线段组
            self.play(
                Create(df_segments),
                run_time=2
            )
            self.animation_timer += 2
            self.wait(2)  # 额外等待时间
            self.animation_timer += 2
            
            # 清除当前点的可视化
            self.play(
                FadeOut(z_dot), 
                FadeOut(f_dot), 
                FadeOut(dz_segments), 
                FadeOut(df_segments),
                run_time=0.2
            )
            self.animation_timer += 0.2

    def create_rectangle_path(self):
        """创建矩形路径
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 矩形的四个顶点（复平面坐标）
        rect_points = [
            complex(-1, -1)*z_scale,  # 左下
            complex(1, -1)*z_scale,   # 右下
            complex(1, 1)*z_scale,    # 右上
            complex(-1, 1)*z_scale,   # 左上
            complex(-1, -1)*z_scale   # 回到起点
        ]
        
        # 创建矩形路径
        vertices = [np.array([p.real, p.imag, 0]) for p in rect_points]
        rectangle = VMobject()
        rectangle.set_points_as_corners(vertices)
        
        return rectangle, rect_points[0]
    
    def create_circle_path(self):
        """创建圆形路径
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 圆的参数
        radius = 1*z_scale
        center = complex(0, 0)
        start_point = center + radius
        
        # 创建圆形路径
        circle = Circle(radius=radius)
        
        return circle, start_point
    
    def create_radial_path(self):
        """创建径向路径（从原点向外辐射的直线）
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 径向路径参数
        num_rays = 8  # 径向线的数量
        ray_length = z_scale  # 径向线的长度
        
        # 创建径向路径（多条从原点出发的直线）
        radial_path = VMobject()
        
        # 为每条径向线创建点集
        all_points = []
        for i in range(num_rays):
            angle = i * 2 * PI / num_rays
            # 从原点到目标点
            start_point = np.array([0, 0, 0])
            end_point = np.array([ray_length * np.cos(angle), ray_length * np.sin(angle), 0])
            
            # 添加去程路径点
            all_points.append(start_point)
            all_points.append(end_point)
            
            # 如果不是最后一条径向线，添加回程路径点
            if i < num_rays - 1:
                all_points.append(start_point)
        
        # 设置路径点
        radial_path.set_points_as_corners(all_points)
        
        # 起始点为原点
        start_point = complex(0, 0)
        
        return radial_path, start_point
    
    def create_archimedes_spiral_path(self):
        """创建阿基米德螺线路径
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 螺线参数
        a = 0.15*z_scale  # 螺线系数
        max_theta = 4 * PI  # 最大角度
        
        # 参数方程: r = a * theta
        def spiral_func(t):
            theta = t * max_theta
            r = a * theta
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            return np.array([x, y, 0])
        
        # 创建螺线路径 - 修复 scaling 参数问题
        spiral = ParametricFunction(
            spiral_func,
            t_range=[0, 1, 0.01],  # 使用三元组格式 [t_min, t_max, t_step]
        )
        
        # 起始点 (t=0)
        start_point = complex(0, 0)
        
        return spiral, start_point
        
    
    def construct(self):
        
        # 创建复平面
        complex_plane = ComplexPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            }
        ).scale(1.0)
        
        # 添加坐标轴标签
        complex_plane.add_coordinates()
        
        # 函数公式文本
        function_formula = MathTex(latex_formula1).to_corner(UL).set_color(WHITE)
        
        # 路径类型文本（初始为空，后续会更新）
        path_type = Text("").to_corner(UR).set_color(WHITE)
        
        # 添加字幕介绍
        self.update_subtitle("欢迎来到复函数可视化演示", "欢迎来到复函数可视化演示", wait=3.0)
        self.update_subtitle(f"我们将在复平面上探索复变函数及其导数的行为", f"我们将在复平面上探索复变函数及其导数的行为", wait=5.0)
        
        # 添加复平面和函数公式
        self.update_subtitle("首先让我们创建复平面", "首先让我们创建复平面", wait=1)
        self.play(Create(complex_plane), run_time=2.0)
        self.animation_timer += 2.0
        
        self.update_subtitle("这是我们要研究的复函数", "这是我们要研究的复函数", wait=1)
        self.play(Write(function_formula), run_time=1.5)
        self.animation_timer += 1.5
        
        self.update_subtitle("第一个问题是：当自变量沿复平面上的特定路径移动时，函数值会怎样移动？", "第一个问题是：当自变量沿复平面上的特定路径移动时，函数值会怎样移动？", wait=7.5)
        self.update_subtitle("接下来自变量和函数值将分别沿着红色、黄色路径移动，请注意观察。", "接下来自变量和函数值将分别沿着红色、黄色路径移动，请注意观察。", wait=7.5)
        
        self.demo_path_combined(complex_plane, path_type, complex_function1)
        
        # 5. 展示导数可视化
        self.update_subtitle("现在我们继续探索复函数的导数特性", "现在我们继续探索复函数的导数特性", wait=4.0)

        self.update_subtitle(f"接下来大家将依次看到两个彩色环，它们分别表示自变量和函数值的微小变化", f"接下来大家将依次看到两个彩色环，它们分别表示自变量和函数值的微小变化", wait=8)

        self.update_subtitle("当然，为了能看清，两个环会被放大同样的倍数。", "当然，为了能看清，两个环会被放大同样的倍数。", wait=5)

        self.update_subtitle("环在不同角度具有不同颜色，相同颜色的 df 和 dz 是一对", "环在不同角度具有不同颜色，相同颜色的 df 和 dz 是一对", wait=7)

        self.update_subtitle("如果复变函数可导，df 和 dz 的比值就是常数", "如果复变函数可导，df 和 dz 的比值就是常数", wait=6)

        self.update_subtitle("那么 df 环应该也是圆的，而且颜色和 dz 圆环只差一个固定的角度", "那么 df 环应该也是圆的，而且颜色和 dz 圆环只差一个固定的角度", wait=1)

        self.demonstrate_derivative(complex_plane, complex_function1)

        self.play(FadeOut(function_formula), run_time=0.5)
        self.animation_timer += 0.5

        self.update_subtitle("现在让我们换一个函数，请大家随着演示心算，看看函数值和导数对不对", "现在让我们换一个函数，请大家随着演示心算，看看函数值和导数对不对", wait=5)

        function_formula = MathTex(latex_formula2).to_corner(UL).set_color(WHITE)
        self.play(Write(function_formula), run_time=1.5)
        self.animation_timer += 1.5

        self.update_subtitle("首先是路径展示", "首先是路径展示", wait=2)  
        self.demo_path_combined(complex_plane, path_type, complex_function2)

        self.update_subtitle("然后是导数可视化", "然后是导数可视化", wait=2)
        self.demonstrate_derivative(complex_plane, complex_function2)

        self.play(FadeOut(function_formula), run_time=0.5)
        self.animation_timer += 0.5
        
        self.update_subtitle("现在让我们换一个不可导函数，请大家注意观察它和可导函数的不同", "现在让我们换一个不可导函数，请大家注意观察它和可导函数的不同", wait=5)
        
        function_formula = MathTex(latex_formula3).to_corner(UL).set_color(WHITE)
        self.play(Write(function_formula), run_time=1.5)
        self.animation_timer += 1.5

        self.update_subtitle("首先是路径展示", "首先是路径展示", wait=2)  
        self.demo_path_combined(complex_plane, path_type, complex_function3)

        self.update_subtitle("然后是导数可视化，这个时候请注意 df 就不一定是圆环了", "然后是导数可视化，这个时候请注意 df 就不一定是圆环了", wait=2)
        self.demonstrate_derivative(complex_plane, complex_function3)
    
        self.update_subtitle("演示结束，感谢观看！", "演示结束，感谢观看！", wait=3.0)
    


# 主函数更新
if __name__ == "__main__":
    # 从命令行输入质量参数
    parser = argparse.ArgumentParser(description="运行复函数可视化动画")
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
    buff = ComplexFunctionVisualization()
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