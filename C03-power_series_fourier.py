import json
import os
import subprocess
import numpy as np
import argparse
from manim import *

config.tex_template.add_to_preamble(r"""
\usepackage{ctex}
\usepackage{amsmath}
\usepackage{amssymb}
""")

# 幂函数向傅里叶级数展开动画类
class PowerFunctionFourierSeries(Scene): 
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
            self.add(new_subtitle)  # 2D 模式下用这个
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
    
    # 创建坐标系
    def create_axes(self, x_range=[-5, 5], y_range=[-5, 5]):
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"color": BLUE},
            x_length=10,
            y_length=6
        )
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        return VGroup(axes, x_label, y_label)
    
    # 计算傅里叶系数
    def calculate_fourier_coefficients(self, n, power):
        """计算 x^power 在 [-π, π] 上的傅里叶系数"""
        if power % 2 == 0:  # 偶函数
            a0 = 2 / (power + 1) if power > 0 else 2
            a = [0] * (n + 1)
            b = [0] * (n + 1)
            
            for k in range(1, n + 1):
                if k % 2 == 0:  # 偶数项
                    a[k] = 0
                else:  # 奇数项
                    a[k] = 4 * (-1)**((k-1)/2) / (k**2 - power**2) if k != power else 0
                b[k] = 0  # 偶函数的 b_k 都为 0
                
            return a0, a, b
        else:  # 奇函数
            a0 = 0
            a = [0] * (n + 1)
            b = [0] * (n + 1)
            
            for k in range(1, n + 1):
                a[k] = 0  # 奇函数的 a_k 都为 0
                if k % 2 == 0:  # 偶数项
                    b[k] = 0
                else:  # 奇数项
                    b[k] = 4 * (-1)**((k-1)/2) * k / (k**2 - power**2) if k != power else 0
                    
            return a0, a, b
    
    # 创建傅里叶级数函数
    def fourier_series(self, x, a0, a, b, n):
        """计算傅里叶级数在 x 处的值，使用前 n 项"""
        result = a0 / 2
        for k in range(1, n + 1):
            result += a[k] * np.cos(k * x) + b[k] * np.sin(k * x)
        return result
    
    # 构建动画的主体
    def construct(self):
        
        self.update_subtitle(r"\text{今天我们介绍幂函数向傅里叶级数的展开}", "今天我们介绍幂函数向傅里叶级数的展开")
        
        
        # 介绍幂函数
        power_func_def = MathTex(r"f(x) = x^n, \quad n \in \mathbb{N}")
        self.play(Write(power_func_def), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(r"\text{一般的幂函数}", "幂函数的一般形式是 f(x) = x 的 n 次方，其中 n 是自然数")
        
        # 介绍傅里叶级数
        fourier_def = MathTex(
            r"f(x) = \frac{a_0}{2} + \sum_{k=1}^{\infty} \left[ a_k \cos(kx) + b_k \sin(kx) \right]"
        )
        self.play(ReplacementTransform(power_func_def, fourier_def), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(
            r"\text{傅里叶级数的一般形式}", 
            "傅里叶级数的一般形式是 f(x) 等于 a_0 除以 2 加上 a_k 乘以余弦 kx 加 b_k 乘以正弦 kx 的无穷求和"
        )
        
        # 介绍傅里叶系数
        fourier_coef = MathTex(
            r"a_0 &= \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) dx \\",
            r"a_k &= \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos(kx) dx \\",
            r"b_k &= \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin(kx) dx"
        )
        self.play(ReplacementTransform(fourier_def, fourier_coef), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(
            r"\text{傅里叶级数的计算}", 
            "傅里叶系数 a_0、a_k 和 b_k 分别通过特定的积分公式计算"
        )
        
        self.play(FadeOut(fourier_coef), run_time=1)
        self.animation_timer += 1
        
        # 场景2：幂函数图像
        self.update_subtitle(r"\text{幂函数图像}", "接下来我们来看几个典型幂函数的图像")
        
        # 创建坐标系
        axes = self.create_axes(x_range=[-3, 3], y_range=[-5, 5])
        self.play(Create(axes), run_time=2)
        self.animation_timer += 2
        
        # 创建幂函数图像
        power_funcs = []
        power_labels = []
        colors = [BLUE, GREEN, RED]
        
        for i, n in enumerate([1, 2, 3]):
            func = axes[0].plot(lambda x: x**n, x_range=[-3, 3], color=colors[i])
            label = MathTex(f"f(x) = x^{n}", color=colors[i])
            label.next_to(func, UP)
            power_funcs.append(func)
            power_labels.append(label)
        
        # 显示 x^1
        self.play(Create(power_funcs[0]), Write(power_labels[0]), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(r"f(x) = x", "一次幂函数 f(x) = x 是一条直线")
        
        # 显示 x^2
        self.play(FadeOut(power_funcs[0]), FadeOut(power_labels[0]), run_time=1)
        self.animation_timer += 1
        self.play(Create(power_funcs[1]), Write(power_labels[1]), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(r"f(x) = x^2", "二次幂函数 f(x) = x 的平方是一条抛物线")
        
        # 显示 x^3
        self.play(FadeOut(power_funcs[1]), FadeOut(power_labels[1]), run_time=1)
        self.animation_timer += 1
        self.play(Create(power_funcs[2]), Write(power_labels[2]), run_time=2)
        self.animation_timer += 2   
        
        self.update_subtitle(r"f(x) = x^3", "三次幂函数 f(x) = x 的立方是一条三次曲线")
        
        # 讨论基偶性
        self.update_subtitle(r"\text{幂函数的基偶性}", "幂函数的基偶性取决于指数 n 的基偶性")
        
        # even_odd = MathTex(
        #     r"\text{当 } n \text{ 为偶数时}, f(-x) = f(x) \text{ (偶函数)} \\",
        #     r"\text{当 } n \text{ 为奇数时}, f(-x) = -f(x) \text{ (奇函数)}"
        # )
        # even_odd.to_edge(RIGHT)
        
        # self.play(Write(even_odd), run_time=2)
        # self.animation_timer += 2
        
        self.update_subtitle(
            r"\text{当 } n \text{ 为偶数时}, f(-x) = f(x) \text{ (偶函数)}; \text{当 } n \text{ 为奇数时}, f(-x) = -f(x) \text{ (奇函数)}", 
            "当 n 为偶数时，幂函数是偶函数；当 n 为基数时，幂函数是基函数。这对傅里叶展开有重要影响"
        )
        
        self.play(FadeOut(axes), FadeOut(VGroup(*power_funcs)), FadeOut(VGroup(*power_labels)), run_time=1)
        self.animation_timer += 1
        
        # 场景3：傅里叶级数基本形式
        self.update_subtitle(r"\text{傅里叶级数展开的特点}", "傅里叶级数展开有一些重要特点")
        
        fourier_properties = MathTex(
            r"1. \text{ 周期性：傅里叶级数适合展开周期函数} \\",
            r"2. \text{ 收敛性：在合适条件下，级数收敛于原函数} \\",
            r"3. \text{ 正交性：三角函数系构成正交基}"
        )
        
        self.play(Write(fourier_properties), run_time=3)
        self.animation_timer += 3
        
        self.update_subtitle(
            r"\text{1. 周期性 2. 收敛性 3. 正交性}", 
            "傅里叶级数的三个重要特点是：周期性、收敛性和正交性"
        )
        
        # 幂函数在区间上的周期延拓
        self.update_subtitle(
            r"\text{幂函数在} [-\pi, \pi] \text{上的周期延拓}", 
            "为了用傅里叶级数展开幂函数，我们需要将其在区间负派到派上进行周期延拓"
        )
        
        self.play(FadeOut(fourier_properties), run_time=1)
        self.animation_timer += 1
        
        # 创建新坐标系
        axes_periodic = self.create_axes(x_range=[-4*np.pi, 4*np.pi], y_range=[-1, 5])
        self.play(Create(axes_periodic), run_time=2)
        self.animation_timer += 2
        
        # 创建 x^2 在 [-π, π] 上的周期延拓
        def periodic_x_squared(x):
            x = x % (2 * np.pi)
            if x > np.pi:
                x = x - 2 * np.pi
            return x**2
        
        periodic_func = axes_periodic[0].plot(periodic_x_squared, x_range=[-4*np.pi, 4*np.pi], color=BLUE)
        periodic_label = MathTex(r"f(x) = x^2 \text{ 的 } 2\pi \text{ 周期延拓}", color=BLUE)
        periodic_label.next_to(periodic_func, UP)
        
        self.play(Create(periodic_func), Write(periodic_label), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(
            r"f(x) = x^2 \text{ 的 } 2\pi \text{ 周期延拓}", 
            "这是 x 平方函数在区间负派到派上的二派周期延拓"
        )
        
        self.play(FadeOut(axes_periodic), FadeOut(periodic_func), FadeOut(periodic_label), run_time=1)
        self.animation_timer += 1
        
        # 场景4：推导过程
        self.update_subtitle(r"\text{以} f(x) = x^2 \text{为例进行傅里叶展开}", "下面我们以 x 的平方为例，推导其傅里叶级数展开")
        
        # 展示 x^2 的傅里叶系数计算
        fourier_calc = MathTex(
            r"f(x) &= x^2 \text{ 在 } [-\pi, \pi] \text{ 上} \\",
            r"a_0 &= \frac{1}{\pi} \int_{-\pi}^{\pi} x^2 dx = \frac{2\pi^2}{3} \\",
            r"a_k &= \frac{1}{\pi} \int_{-\pi}^{\pi} x^2 \cos(kx) dx = \frac{4}{k^2}(-1)^k \\",
            r"b_k &= \frac{1}{\pi} \int_{-\pi}^{\pi} x^2 \sin(kx) dx = 0 \text{ (因为 } x^2 \text{ 是偶函数)}"
        )
        
        self.play(Write(fourier_calc), run_time=4)
        self.animation_timer += 4
        
        self.update_subtitle(
            r"f(x) = x^2 \text{ 的傅里叶系数计算}", 
            "通过计算积分，我们得到 x 平方的傅里叶系数：a_0 等于二派平方除以三，a_k 等于四乘以负一的 k 次方除以 k 平方，b_k 全为零"
        )
        
        # 展示 x^2 的傅里叶级数
        fourier_series_x2 = MathTex(
            r"x^2 = \frac{\pi^2}{3} + 4\sum_{k=1}^{\infty} \frac{(-1)^k}{k^2} \cos(kx)"
        )
        
        self.play(ReplacementTransform(fourier_calc, fourier_series_x2), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(
            r"\text{最终的傅里叶级数}", 
            "最终，x 平方的傅里叶级数为：派平方除以三加上四乘以负一的 k 次方除以 k 的平方乘以余弦 k x 的无穷求和"
        )
        
        self.play(FadeOut(fourier_series_x2), run_time=1)
        self.animation_timer += 1
        
        # 场景5：可视化逼近效果
        self.update_subtitle(r"\text{傅里叶级数逼近效果可视化}", "接下来我们通过动画展示傅里叶级数如何逐步逼近原函数")
        
        # 创建坐标系
        axes_approx = self.create_axes(x_range=[-np.pi, np.pi], y_range=[0, 10])
        self.play(Create(axes_approx), run_time=2)
        self.animation_timer += 2
        
        # 创建原函数 x^2
        original_func = axes_approx[0].plot(lambda x: x**2, x_range=[-np.pi, np.pi], color=BLUE)
        original_label = MathTex(r"f(x) = x^2", color=BLUE)
        original_label.next_to(original_func, UP)
        
        self.play(Create(original_func), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(r"f(x) = x^2", "这是原函数 x 的平方")
        
        # 创建傅里叶级数逼近函数
        approx_funcs = []
        approx_labels = []
        
        # 计算 x^2 的傅里叶系数
        a0 = 2 * np.pi**2 / 3
        
        def fourier_x2(x, n):
            result = a0 / 2
            for k in range(1, n + 1):
                result += 4 * (-1)**k * np.cos(k * x) / (k**2)
            return result
        
        n_list = [1, 2, 3, 4, 8, 12, 20]
        for n in n_list:
            func = axes_approx[0].plot(lambda x: fourier_x2(x, n), x_range=[-np.pi, np.pi], color=RED)
            n_str = str(n)
            label = MathTex(r"S_{" + n_str + r"}(x) \text{ (n = " + n_str + r")}", color=RED)
            label.next_to(func, LEFT, buff=-1.5)
            approx_funcs.append(func)
            approx_labels.append(label)
        
        # 逐步展示不同阶数的逼近效果
        for i, (func, label) in enumerate(zip(approx_funcs, approx_labels)):
            if i > 0:
                self.play(
                    ReplacementTransform(approx_funcs[i-1], func),
                    ReplacementTransform(approx_labels[i-1], label),
                    run_time=2
                )
            else:
                self.play(Create(func), Write(label), run_time=2)
            
            self.animation_timer += 2
            
            n_value = n_list[i] + 1
            n_str = str(n_value)
            self.update_subtitle(
                r"\text{使用前 } " + n_str + r" \text{ 项的傅里叶级数逼近}", 
                f"前 {n_value} 项"
            )
        
        self.wait(1); self.animation_timer += 1

        # 展示误差随项数增加而减小
        self.update_subtitle(
            r"\text{随着项数增加，逼近误差减小}", 
            "随着傅里叶级数项数的增加，逼近误差逐渐减小，级数收敛于原函数"
        )
        
        error_text = MathTex(
            r"\lim_{n \to \infty} S_n(x) = f(x)"
        )
        error_text.to_edge(UP)
        
        self.play(Write(error_text), run_time=2)
        self.animation_timer += 2
        
        self.play(
            FadeOut(axes_approx), 
            FadeOut(original_func), 
            FadeOut(original_label),
            FadeOut(approx_funcs[-1]), 
            FadeOut(approx_labels[-1]),
            FadeOut(error_text),
            run_time=1
        )
        self.animation_timer += 1
        
        # 场景6：总结与应用
        self.update_subtitle(r"\text{总结与应用}", "最后我们来总结幂函数傅里叶展开的意义和应用")
        
        summary = MathTex(
            r"1. \text{ 幂函数可以展开为三角函数的级数} \\",
            r"2. \text{ 展开形式取决于幂函数的基偶性} \\",
            r"3. \text{ 收敛速度取决于函数的光滑性}"
        )
        
        self.play(Write(summary), run_time=3)
        self.animation_timer += 3
        
        self.update_subtitle(
            r"\text{幂函数傅里叶展开的特点}", 
            "幂函数傅里叶展开的特点：可以展开为三角函数级数，展开形式取决于基偶性，收敛速度取决于光滑性"
        )
        
        applications = MathTex(
            r"1. \text{ 信号处理：将复杂信号分解为简单波形} \\",
            r"2. \text{ 微分方程：求解边值问题} \\",
            r"3. \text{ 数值计算：快速傅里叶变换 (FFT)}"
        )
        
        self.play(ReplacementTransform(summary, applications), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(
            r"\text{应用领域}", 
            "傅里叶级数在信号处理、微分方程求解和数值计算等领域有广泛应用"
        )
        
        # 结束语
        conclusion = Text("幂函数的傅里叶级数展开揭示了函数空间的美妙结构", font_size=36)
        
        self.play(ReplacementTransform(applications, conclusion), run_time=2)
        self.animation_timer += 2
        
        self.update_subtitle(
            r"\text{幂函数的傅里叶级数展开揭示了函数空间的美妙结构}", 
            "幂函数的傅里叶级数展开揭示了函数空间的美妙结构，是数学分析中的重要内容"
        )
        
        self.play(FadeOut(conclusion), run_time=2)
        self.animation_timer += 2




# 主函数
if __name__ == "__main__":
    # 从命令行输入质量参数
    parser = argparse.ArgumentParser(description="运行模板动画")
    parser.add_argument("--quality", "-q", type=str, choices=["l", "m", "h", "k"], default="l",
                        help="动画质量：l(低), m(中), h(高), k(4K)")
    args = parser.parse_args()

    # 定义 manim 命令行参数
    quality = args.quality  # 从命令行参数获取质量设置
    voice_name = "longlaotie"  # 可选的有 longlaotie, longbella 等

    buff = PowerFunctionFourierSeries() # 创建一个虚的对象用于获取字幕文件路径
    class_name = buff.__class__.__name__
    script_filename = os.path.splitext(os.path.basename(__file__))

    quality_to_str = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60",
        "k": "2160p60"
    }; quality_str = quality_to_str.get(quality)

    # 构建并执行 manim 命令，-q 指定渲染质量，-p 指定预览，__file__ 指定当前文件，PowerFunctionFourierSeries 指定类名
    # 计算并输出渲染时间
    import time
    start_time = time.time()
    cmd = f"manim -q{quality} {__file__} {class_name}"
    result = subprocess.run(cmd, shell=True)
    render_time = time.time() - start_time
    print(f"渲染完成！总耗时：{render_time:.2f}秒")

    result = subprocess.run(cmd, shell=True)

    from generate_speech import generate_speech
    # 根据 manim 的输出结构确定文件路径
    # 视频文件路径：media/videos/ai_code/质量标识/类名.mp4
    # 字幕文件路径：media/subtitles.jsonl
    video_file = f"media/videos/{script_filename[0]}/{quality_str}/{class_name}.mp4"
    
    # 调用语音生成函数，使用阿里云的龙老铁音色，因其断句一般较好
    generate_speech(buff.subtitle_file)
    
    print(f"动画已通过命令行渲染完成，带配音的文件为：{video_file.replace('.mp4', '_WithAudio.mp4')}")
