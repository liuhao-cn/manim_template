from manim import *
from manim import Surface
import numpy as np
import argparse
import os
import json
import argparse
import shutil

# manim default output dir
default_output_dir = "./media/"

class RiemannSphere(ThreeDScene):
    def __init__(self):
        super().__init__()
        
        # 初始化总时间计数器
        self.animation_timer = 0.0
        self.subtitle_id = 0

        # 确保缓存目录存在
        os.makedirs(default_output_dir, exist_ok=True)
        self.subtitle_file = os.path.join(default_output_dir, f"subtitles_{self.__class__.__name__}.jsonl")

        # 如果字幕文件存在，则清空文件，否则创建文件
        if os.path.exists(self.subtitle_file):
            with open(self.subtitle_file, 'w', encoding='utf-8') as f:
                f.write('')  # 写入空字符串，即清空文件
            print(f"已清空字幕文件: {self.subtitle_file}")
        else:
            os.makedirs(os.path.dirname(self.subtitle_file), exist_ok=True)

    def update_subtitle(self, text, wait=0.0, fontsize=24):
        """更新字幕并同步写入字幕文件，包括时间。注意需要内置动画计时器支持"""
        # 移除旧字幕
        if hasattr(self, 'subtitle') and self.subtitle is not None:
            self.remove(self.subtitle)
        
        if text:
            # 创建新字幕
            new_subtitle = Text(text, font_size=fontsize)
            new_subtitle.to_edge(DOWN)
            self.add_fixed_in_frame_mobjects(new_subtitle)
            self.subtitle = new_subtitle

            # 将字幕记录到文件，包括编号、开始时间、文本内容
            self.subtitle_id += 1
            subtitle_json = {
                "id":           self.subtitle_id, 
                "text":         text.strip(),  # 移除空白
                "start_time":   self.animation_timer
                }
        
            # 写入字幕数据
            with open(self.subtitle_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(subtitle_json, ensure_ascii=False) + '\n')
            
        self.wait(wait); self.animation_timer += float(wait)
    
    def format_complex_number(self, r, angle_index):
        """格式化复数文本，确保使用两位整数表示分子"""
        # 确保angle_index是两位整数
        num_str = f"{angle_index:02d}"
        den_str = f"{16}"  # 硬编码分母为16
        
        return f"z = {r}e^{{\\frac{{{num_str}}}{{{den_str}}}\\pi \\mathbf{{i}}}}"
    
    def construct(self):
        # 设置常量和初始化
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 添加极坐标转笛卡尔坐标的方法
        self.setup_scene()
        
        # 第一阶段：复平面
        self.phase1_2D_complex_plane()
        
        # 第二阶段：过渡到3D
        self.phase2_transition_to_3d()
        
        # 第三阶段：黎曼球面
        self.phase3_riemann_sphere()
        
        # 第四阶段：点的移动与投影变化
        self.phase4_point_movement()
        
        # 第五阶段：无穷远点映射
        self.phase5_infinity_point()
        
        # 结束
        self.ending()
    
    def polar_to_cartesian(self, r, theta):
        """将极坐标转换为笛卡尔坐标"""
        # 当 r<0 时返回值乘以 -1
        point = np.array([r * np.cos(theta), r * np.sin(theta), 0])
        return point
    
    def setup_scene(self):
        """设置基本场景和常量"""
        # 常量定义
        self.SPHERE_RADIUS = 1  # 硬编码球体半径
        self.INITIAL_Z_POINT = [1, 0, 0]  # 从实轴上的点开始
        
        # 创建字幕模板
        self.subtitle_template = Text("", font_size=28)
        self.subtitle = self.subtitle_template.copy()
        self.add_fixed_in_frame_mobjects(self.subtitle.to_edge(DOWN))
        
        # 创建复数值显示模板 - 增大字体大小
        self.complex_value = MathTex("", font_size=48)
        self.complex_value.to_corner(UR).shift(LEFT*0.5)
        
        # 设置相机初始角度（平面视图）
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        
    def phase1_2D_complex_plane(self):
        """第一阶段：2D复平面及点的运动"""
        # 创建坐标轴
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],  # 缩短虚轴长度
            x_length=10,
            y_length=6,  # 缩短虚轴长度
            axis_config={"include_tip": True}
        )
        
        # 轴标签
        x_label = Tex("$\\mathrm{Re}(z)$").next_to(axes.x_axis, RIGHT)
        y_label = Tex("$\\mathrm{Im}(z)$").next_to(axes.y_axis, UP)
        
        # 保存标签引用以便后续阶段使用
        self.x_label = x_label
        self.y_label = y_label
        
        # 1. 展示实轴
        
        self.play(Create(axes.x_axis), Create(x_label), run_time=1)
        self.animation_timer += 1
        self.update_subtitle("复平面上有实轴和虚轴，实轴代表复数的实部", wait=4)
        
        # 2. 展示虚轴
        self.play(Create(axes.y_axis), Create(y_label), run_time=1)
        self.animation_timer += 1
        self.update_subtitle("虚轴代表复数的虚部", wait=3)
        
        # 3. 展示原点
        self.update_subtitle("原点则表示复数 0", wait=2)
        origin = Dot([0, 0, 0], color=WHITE)
        origin_label = Tex("$0$", color=WHITE).next_to(origin, DOWN+LEFT, buff=0.1)
        self.play(Create(origin), Write(origin_label), run_time=2)
        self.animation_timer += 2
        
        # 4. 展示复平面上的点
        z_dot = Dot(self.INITIAL_Z_POINT, color=YELLOW)
        
        # 将复数值添加到场景 - 增大字体
        complex_num = MathTex("z = 1 + 0i", font_size=48).to_corner(UR).shift(LEFT*0.5)
        self.add_fixed_in_frame_mobjects(complex_num)
        
        self.update_subtitle("复平面上的点对应于不同的复数", wait=1)
        self.play(Create(z_dot), run_time=2)
        self.animation_timer += 2
        
        # 创建完整的复平面 - 增强网格线
        complex_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],  # 缩短虚轴范围
            background_line_style={
                "stroke_color": BLUE,  # 加深颜色
                "stroke_width": 1.5,   # 加粗线条
                "stroke_opacity": 0.8  # 增加不透明度
            }
        ).set_opacity(0.7)  # 增加整体不透明度
        
        self.play(Create(complex_plane), run_time=2)
        self.animation_timer += 2
        self.update_subtitle("这就是复平面，每一点对应一个复数", wait=3)
        
        # 5. 按直角坐标系运动 - 修改为正方形路径
        positions = [
            [1, 0, 0],    # 初始位置
            [2, 0, 0],    # 右
            [2, 2, 0],    # 右上角
            [0, 2, 0],    # 左上角
            [0, 0, 0],    # 左下角
            [2, 0, 0],    # 右下角
            [1, 0, 0]     # 回到初始位置
        ]
        
        self.update_subtitle("让我们观察点在复平面上的运动", wait=3)
        # 角点位置索引
        corner_indices = [1, 2, 3, 4, 5]
        
        for i, pos in enumerate(positions):
            if pos != positions[0]:  # 不是第一个位置才播放动画
                # 更新复数值显示
                new_complex = MathTex(f"z = {pos[0]} + {pos[1]}i", font_size=48).to_corner(UR).shift(LEFT*0.5)
                
                # 如果是角点，添加强调动画
                if i in corner_indices:
                    self.play(
                        z_dot.animate.move_to(pos),
                        FadeTransform(complex_num, new_complex),
                        run_time=1.5
                    )
                    self.animation_timer += 1.5
                    
                    # 在角点处添加强调动画
                    self.play(
                        z_dot.animate.scale(1.5),  # 放大
                        run_time=0.3
                    ); self.animation_timer += 0.3

                    self.play(
                        z_dot.animate.scale(1/1.5),  # 恢复原大小
                        run_time=0.3
                    ); self.animation_timer += 0.3
                    self.wait(0.5); self.animation_timer += 0.5
                else:
                    self.play(
                        z_dot.animate.move_to(pos),
                        FadeTransform(complex_num, new_complex),
                        run_time=1.5
                    ); self.animation_timer += 1.5
                complex_num = new_complex
        
        self.update_subtitle("接下来我们使用极坐标表示复数", wait=3)
        # 6. 按极坐标系运动（半径不变，角度变化）
        radius = 2
        
        # 创建表示半径的线
        radius_line = Line([0, 0, 0], [radius, 0, 0], color=RED)
        theta_arc = Arc(radius=0.5, angle=0, color=GREEN)
        theta_label = MathTex("\\theta", color=GREEN).move_to([0.7*0.5, 0.2, 0])
        
        self.play(
            z_dot.animate.move_to([radius, 0, 0]),
            FadeOut(complex_num),
            Create(radius_line),
            Create(theta_arc),
            Write(theta_label),
            run_time=2
        ); self.animation_timer += 2
        
        # 创建极坐标表示的复数值
        initial_complex = self.format_complex_number(radius, 0)
        polar_complex = MathTex(initial_complex, font_size=48).to_corner(UR).shift(LEFT*0.5)
        self.add_fixed_in_frame_mobjects(polar_complex)
        
        self.update_subtitle("极坐标表示复数更适合描述旋转和缩放", wait=3)
        
        # 定义四个特殊角度（0°, 90°, 180°, 270°）
        special_angles = [0, PI/2, PI, 3*PI/2, 2*PI]
        special_indices = [0, 8, 16, 24]  # 对应的索引
        
        # 创建更新函数，用于连续更新点的位置、半径线、角度弧和标签
        def update_point(mob, alpha, start_angle, end_angle):
            # 计算当前角度
            angle = start_angle + alpha * (end_angle - start_angle)
            
            # 计算新位置
            new_pos = [radius * np.cos(angle), radius * np.sin(angle), 0]
            mob.move_to(new_pos)
            
            # 更新半径线
            radius_line.put_start_and_end_on([0, 0, 0], new_pos)
            
            # 更新角度弧
            theta_arc.become(Arc(radius=0.5, angle=angle, color=GREEN))
            
            # 更新角度标签位置
            theta_label.move_to([0.7*0.5*np.cos(angle/2), 0.7*0.5*np.sin(angle/2), 0])
            
            # 计算当前索引（0-32之间的值）
            current_index = int(32 * angle / (2*PI))
            
            # 更新复数值显示 - 始终使用分数形式，确保两位整数
            new_complex = self.format_complex_number(radius, current_index)
            new_tex = MathTex(new_complex, font_size=48).to_corner(UR).shift(LEFT*0.5)
            polar_complex.become(new_tex)
        
        # 分四段播放动画，每段到达一个特殊角度后暂停并强调
        for i in range(4):
            start_angle = special_angles[i]
            end_angle = special_angles[i+1]
            
            # 播放连续动画
            self.play(
                UpdateFromAlphaFunc(
                    z_dot,
                    lambda m, a: update_point(m, a, start_angle, end_angle)
                ),
                run_time=2.0,  # 每段动画时间
                rate_func=linear  # 线性变化，使速度均匀
            )
            self.animation_timer += 2.0
            
            # 添加强调动画
            self.play(
                z_dot.animate.scale(1.5),  # 放大
                run_time=0.3
            ); self.animation_timer += 0.3
            self.play(
                z_dot.animate.scale(1/1.5),  # 恢复原大小
                run_time=0.3
            ); self.animation_timer += 0.3
            self.wait(0.2); self.animation_timer += 0.2
        
        # 保存复数值显示的引用
        self.complex_num = polar_complex
        
        self.update_subtitle("这就是复数在极坐标下的表示和运动", wait=4)
        
        # 清理临时对象，保留重要元素
        self.play(
            FadeOut(theta_arc),
            FadeOut(theta_label),
            FadeOut(radius_line),
            run_time=0.3
        )
        self.animation_timer += 0.3

        # 保存引用以在后续阶段使用  
        self.complex_plane = complex_plane
        self.z_dot = z_dot
        self.axes_2d = axes
    
    def phase2_transition_to_3d(self):
        """第二阶段：从复平面过渡到3D空间"""
        # 在过渡到3D之前，移除右上角的复数文本，避免遗留
        self.play(FadeOut(self.complex_num), run_time=0.3)
        self.animation_timer += 0.3
        
        self.update_subtitle("现在我们将从复平面过渡到三维空间以引入黎曼球面。", wait=4)
        
        # 硬编码坐标轴配置
        axes_config = {
            'axes_3d': {
                'x_range': [-5, 5, 1],
                'y_range': [-5, 5, 1],
                'z_range': [ 0, 4, 1],
                'x_length': 10,
                'y_length': 10,
                'z_length': 4
            }
        }
        
        # 在转换到3D之前，先扩展2D平面的y轴到足够长度
        # 直接使用phase1中保存的标签引用
        x_label = self.x_label
        y_label = self.y_label
        
        # 保存当前的 2D 坐标轴
        old_x_axis = self.axes_2d.x_axis
        old_y_axis = self.axes_2d.y_axis
        
        # 创建新的y轴，范围更大
        new_y_axis = NumberLine(
            x_range=axes_config['axes_3d']['y_range'],
            length=axes_config['axes_3d']['y_length'],
            include_tip=True,
            rotation=90 * DEGREES  # 直接在创建时设置旋转角度
        )
        
        # 将新y轴放置在正确位置
        new_y_axis.move_to(old_y_axis.get_center())
        
        # 更新y轴标签位置 - 直接使用保存的引用
        new_y_label_pos = new_y_axis.get_end() + UP * 0.3
        self.play(
            FadeOut(old_y_axis),
            Create(new_y_axis),
            y_label.animate.move_to(new_y_label_pos),
            run_time=0.3
        )
        self.animation_timer += 0.3
        
        # 更新复平面的y轴范围 - 创建新的复平面而不是修改现有的
        new_complex_plane = NumberPlane(
            x_range=axes_config['axes_3d']['x_range'],
            y_range=axes_config['axes_3d']['y_range'],
            background_line_style={
                'stroke_color': BLUE,
                'stroke_width': 1.5,
                'stroke_opacity': 0.8
            }
        ).set_opacity(0.7)
        
        # 替换旧的复平面
        self.play(
            FadeOut(self.complex_plane), 
            FadeIn(new_complex_plane),
            run_time=0.3
        )
        self.animation_timer += 0.3
        self.complex_plane = new_complex_plane
        
        # 计算从(1,-1,1)望向原点的相机角度
        target_phi = 50 * DEGREES
        target_theta = 315 * DEGREES
        
        # 创建3D坐标轴
        axes_3d = ThreeDAxes(
            x_range=axes_config['axes_3d']['x_range'],
            y_range=axes_config['axes_3d']['y_range'],
            z_range=axes_config['axes_3d']['z_range'],
            x_length=axes_config['axes_3d']['x_length'],
            y_length=axes_config['axes_3d']['y_length'],
            z_length=axes_config['axes_3d']['z_length']
        )
        
        # 创建3D标签
        x_label_3d = Tex("$\\mathrm{Re}(z)$").next_to(axes_3d.x_axis.get_end(), RIGHT)
        y_label_3d = Tex("$\\mathrm{Im}(z)$").next_to(axes_3d.y_axis.get_end(), UP)
        
        # 将2D点转换为3D点
        z_dot_3d = Dot3D(
            self.z_dot.get_center(),
            color=YELLOW,
            radius=0.08
        )
        
        # 直接旋转相机到最终3D视角
        # 选择最短路径旋转
        target_theta_options = [target_theta, target_theta - 360*DEGREES]
        final_theta = min(target_theta_options, key=lambda x: abs(x))
        self.move_camera(
            phi=target_phi,
            theta=final_theta,  # 使用绝对值较小的角度实现最短路径旋转
            zoom=1.0,
            run_time=4
        )
        self.animation_timer += 4
        
        # 在相机移动后，转换2D元素到3D元素
        # 保留原有的xy标签,不创建新的3D标签
        self.play(
            FadeTransform(old_x_axis, axes_3d.x_axis),
            FadeTransform(new_y_axis, axes_3d.y_axis), 
            FadeIn(axes_3d.z_axis),
            # 将2D平面上的点(self.z_dot)平滑过渡到3D空间中的点(z_dot_3d)
            FadeTransform(self.z_dot, z_dot_3d),
            run_time=3
        )
        self.animation_timer += 3

        # # 将标签添加到固定帧,这样它们就不会随相机旋转而消失，但目前暂时不需要
        # self.add_fixed_in_frame_mobjects(x_label, y_label)
        # self.add_fixed_in_frame_mobjects(x_label_3d, y_label_3d, z_label_3d)
        
        # 保存3D标签引用以便后续使用
        self.x_label_3d = x_label_3d
        self.y_label_3d = y_label_3d
        self.wait(0.3); self.animation_timer += 0.3
        
        # 解释3D视角
        self.update_subtitle("在三维空间中，复平面位于水平面上", wait=3)
        
        # 更新场景引用
        self.complex_plane = new_complex_plane
        self.z_dot = z_dot_3d
        self.axes_3d = axes_3d
    
    def phase3_riemann_sphere(self):
        """第三阶段：黎曼球面展示"""
        # 清除之前可能存在的球体
        for obj in self.mobjects[:]:
            if isinstance(obj, Sphere) or isinstance(obj, Surface):
                self.remove(obj)
        
        # 硬编码网格配置
        grid_config = {
            'longitude_count': 120,
            'latitude_count': 60,
            'stroke_width': 1,
            'color': BLUE_D,
            'opacity': 0.6
        }
        
        # 创建经线
        longitudes = VGroup()
        for phi in np.linspace(0, 2*PI, grid_config['longitude_count'], endpoint=False):
            longitude = ParametricFunction(
                lambda t: np.array([
                    self.SPHERE_RADIUS * np.sin(t) * np.cos(phi),
                    self.SPHERE_RADIUS * np.sin(t) * np.sin(phi),
                    self.SPHERE_RADIUS * np.cos(t) + self.SPHERE_RADIUS
                ]),
                t_range=[0, PI],
                stroke_width=grid_config['stroke_width'],
                stroke_color=grid_config['color'],
                stroke_opacity=grid_config['opacity']
            )
            longitudes.add(longitude)
        
        # 创建纬线
        latitudes = VGroup()
        for theta in np.linspace(0, PI, grid_config['latitude_count'], endpoint=True):
            if theta == 0 or theta == PI:  # 跳过极点
                continue
            latitude = ParametricFunction(
                lambda t: np.array([
                    self.SPHERE_RADIUS * np.sin(theta) * np.cos(t),
                    self.SPHERE_RADIUS * np.sin(theta) * np.sin(t),
                    self.SPHERE_RADIUS * np.cos(theta) + self.SPHERE_RADIUS
                ]),
                t_range=[0, 2*PI],
                stroke_width=grid_config['stroke_width'],
                stroke_color=grid_config['color'],
                stroke_opacity=grid_config['opacity']
            )
            latitudes.add(latitude)
        
        # 组合所有网格线
        sphere_grid = VGroup(longitudes, latitudes)
        
        self.update_subtitle("这是黎曼球面，它将复平面映射到球面上", wait=1)
        self.play(Create(sphere_grid), run_time=2)
        self.animation_timer += 2
        
        # 硬编码视觉配置
        visual_config = {
            'north_pole_color': BLUE,
            'dot_radius': 0.08,
            'arrow_length': 2,
            'arrow_buff': 0.1
        }
        
        # 硬编码文本配置
        text_config = {
            'label_font_size': 24,
            'complex_value': {
                'font_size': 48
            }
        }
        
        # 添加北极点
        north_pole_pos = np.array([0, 0, 2*self.SPHERE_RADIUS])
        north_pole = Dot3D(
            north_pole_pos,
            color=visual_config['north_pole_color'],
            radius=visual_config['dot_radius']
        )
        
        # 北极点标签和箭头
        north_pole_label = Text(
            "北极点",
            font_size=text_config['label_font_size']
        ).to_corner(UR).shift(DOWN)
        
        # 先显示北极点，然后等待一帧使摄像机更新
        self.play(Create(north_pole), run_time=2)
        self.animation_timer += 2
        # # 将北极点移到前面，使其始终显示在球面网格之上
        # # bring_to_front 在3D场景中可能不生效，使用以下方法确保北极点可见
        # self.remove(north_pole)  # 先移除北极点
        # self.add(north_pole)     # 再添加回来，确保它在渲染顺序中位于最后
        # 另一种方法是调整z_index
        north_pole.set_z_index(10)  # 设置较高的z_index值
        self.wait(0.3); self.animation_timer += 0.3
        
        # 获取北极点在屏幕上的2D投影坐标
        north_pole_screen_pos = self.camera.project_point(north_pole_pos)
        north_pole_screen_point = np.array([north_pole_screen_pos[0], north_pole_screen_pos[1], 0])
        
        # 计算从标签到北极点投影的方向向量
        # 首先获取方向向量
        label_to_pole = north_pole_screen_point - north_pole_label.get_left()
        # 归一化方向向量
        label_to_pole = label_to_pole / np.linalg.norm(label_to_pole)
        # 计算箭头终点位置 - 长度加倍
        arrow_end = north_pole_label.get_left() + label_to_pole * (visual_config['arrow_length'] * 2)
        
        north_pole_arrow = Arrow(
            north_pole_label.get_left(), 
            arrow_end,
            buff=visual_config['arrow_buff'],
            color=visual_config['north_pole_color']
        )
        
        self.add_fixed_in_frame_mobjects(north_pole_label, north_pole_arrow)
        self.update_subtitle("黎曼球面的北极点对应复平面上的无穷远点", wait=6)
        
        def get_projection_point(z_point):
            """
            立体投影函数：将复平面上的点投影到黎曼球面上
            
            参数:
                z_point: 复平面上点的坐标，形式为 [x, y, 0]
                
            返回:
                黎曼球面上对应的投影点坐标 [x', y', z']
            """
            # 获取复平面上点的坐标
            x, y = z_point[0], z_point[1]
            z = 0  # 复平面上的点z坐标为0
            
            # 北极点坐标
            north_x, north_y, north_z = 0, 0, 2*self.SPHERE_RADIUS
            
            # 注意：输入的点是复平面上的点，z坐标为0，不可能接近北极点(0,0,2R)
            # 这个条件实际上永远不会满足，因为z总是0而north_z是2*self.SPHERE_RADIUS
            # 保留此检查只是为了代码的健壮性
            if abs(x) < 1e-10 and abs(y) < 1e-10 and abs(z - north_z) < 1e-10:
                return np.array([0, 0, 2*self.SPHERE_RADIUS - 0.01])
            
            # 如果点非常远，直接返回北极点
            if x*x + y*y > 1000:
                return np.array([0, 0, 2*self.SPHERE_RADIUS - 0.01])
            
            # 计算从北极点到复平面点的方向向量
            direction = np.array([x - north_x, y - north_y, z - north_z])
            
            # 归一化方向向量
            direction_length = np.sqrt(np.sum(direction**2))
            if direction_length < 1e-10:
                unit_direction = np.array([0, 0, -1])  # 默认向下
            else:
                unit_direction = direction / direction_length
            
            # 球心坐标
            center_x, center_y, center_z = 0, 0, self.SPHERE_RADIUS

            # 代入射线方程到球面方程，得到关于t的二次方程: at^2 + bt + c = 0
            a = np.sum(unit_direction**2)  # 应该等于1
            b = 2 * np.sum(unit_direction * np.array([north_x - center_x, north_y - center_y, north_z - center_z]))
            c = np.sum((np.array([north_x, north_y, north_z]) - np.array([center_x, center_y, center_z]))**2) - self.SPHERE_RADIUS**2
            
            # 计算判别式
            discriminant = b*b - 4*a*c
            
            # 如果没有交点（不应该发生），返回北极点
            if discriminant < 0:
                return np.array([north_x, north_y, north_z])
            
            # 计算t的两个解
            t1 = (-b + np.sqrt(discriminant)) / (2*a)
            t2 = (-b - np.sqrt(discriminant)) / (2*a)
            
            # 选择较小的正t值（第一个交点）
            if t1 > 0 and (t2 <= 0 or t1 < t2):
                t = t1
            else:
                t = t2
            
            # 计算交点坐标
            intersection = np.array([north_x, north_y, north_z]) + t * unit_direction
            
            return intersection
        
        # 创建从北极点到复平面点的连接线
        z_point = self.z_dot.get_center()
        projection_point = get_projection_point(z_point)
        projection_dot = Dot3D(projection_point, color=RED, radius=0.08)
        
        # 连接线：北极点到复平面点
        north_to_z_line = Line3D(
            north_pole_pos,
            z_point,
            color=YELLOW,
            stroke_width=3
        )
        
        self.update_subtitle("从北极点向复平面上的点连一条直线", wait=4)
        self.play(Create(north_to_z_line), run_time=2)
        self.animation_timer += 2
        
        # 投影点及标签 - 确保在网格线之前显示
        self.update_subtitle("直线与球面相交的点，就是复数在黎曼球面上的投影", wait=4)
        projection_dot.set_z_index(10)  # 设置较高的z_index值
        self.play(Create(projection_dot), run_time=2)
        self.animation_timer += 2
        
        # 在计算投影点后，修正投影点箭头
        # 添加投影标签和箭头
        proj_label = Text("投影点", font_size=24).to_corner(UL).shift(DOWN)
        
        # 获取投影点在屏幕上的2D位置
        projection_screen_pos = self.camera.project_point(projection_point)
        projection_screen_point = np.array([projection_screen_pos[0], projection_screen_pos[1], 0])
        
        # 计算从标签到投影点的方向向量
        label_to_proj = projection_screen_point - proj_label.get_right()
        label_to_proj = label_to_proj / np.linalg.norm(label_to_proj)
        proj_arrow_end = proj_label.get_right() + label_to_proj * 4  # 增加到原来的4倍
        
        proj_arrow = Arrow(
            proj_label.get_right(),
            proj_arrow_end,
            buff=0.1,
            color=RED
        )
        
        self.add_fixed_in_frame_mobjects(proj_label, proj_arrow)
        
        self.wait(1); self.animation_timer += 1

        # 移除箭头和标签
        self.play(
            FadeOut(north_pole_arrow),
            FadeOut(proj_arrow),
            FadeOut(north_pole_label),
            FadeOut(proj_label),
            run_time=0.5
        )
        self.animation_timer += 0.5
        
        # 创建复数值显示，供后续阶段使用
        initial_complex = self.format_complex_number(2, 0)
        self.complex_num = MathTex(initial_complex, font_size=48).to_corner(UR).shift(LEFT*0.5)
        self.add_fixed_in_frame_mobjects(self.complex_num)
        
        # 保存引用以在后续阶段使用 - 删除sphere引用，只保留sphere_grid
        self.sphere_grid = sphere_grid
        self.north_pole = north_pole
        self.projection_dot = projection_dot
        self.north_to_z_line = north_to_z_line
        self.get_projection_point = get_projection_point
    
    def phase4_point_movement(self):
        """第四阶段：点的移动与投影变化"""
        # 移除前一阶段的复数文本，避免文本重叠
        if hasattr(self, 'complex_num'):
            self.play(FadeOut(self.complex_num), run_time=0.3)
            self.animation_timer += 0.3
            
        self.update_subtitle("现在我们改变复数的辐角，观察投影点的变化", wait=4)
        
        # 硬编码文本配置
        text_config = {
            'label_font_size': 24,
            'complex_value': {
                'font_size': 48
            }
        }
        
        # 创建复平面上的起始点
        start_angle = 0
        start_r = 2
        z_point = self.polar_to_cartesian(start_r, start_angle)
        z_dot = Dot3D(np.array([z_point[0], z_point[1], 0]), color=RED)
        self.z_dot = z_dot  # 保存引用供phase5使用
        
        # 获取投影点位置
        projection_pos = self.get_projection_point(z_point)
        projection_dot = Dot3D(projection_pos, color=RED)
        self.projection_dot = projection_dot  # 保存引用供phase5使用
        
        # 北极点位置
        north_pole_pos = np.array([0, 0, 2*self.SPHERE_RADIUS])
        
        # 创建连接线
        north_to_z_line = Line3D(
            north_pole_pos,
            np.array([z_point[0], z_point[1], 0]),
            color=YELLOW
        )
        
        # 添加点和线
        self.play(
            FadeIn(z_dot),
            FadeIn(projection_dot),
            Create(north_to_z_line),
            run_time=0.3    
        )
        self.animation_timer += 0.3
        # 创建初始复数值显示，使用极坐标格式
        initial_complex = self.format_complex_number(start_r, 0)
        complex_text = MathTex(initial_complex, font_size=48).to_corner(UR)
        
        # 移除旧的complex_num并添加新的
        self.remove(self.complex_num)
        self.add_fixed_in_frame_mobjects(complex_text)
        self.complex_num = complex_text
        
        # 在开始新的动画前，明确移除原有连接线
        self.play(FadeOut(north_to_z_line), run_time=0.3)
        self.animation_timer += 0.3
        
        # 减少帧数 - 只取8个关键角度点（每45度一个）
        angles = [i * PI/8 for i in range(1, 17)]  # 从PI/4到2PI，每PI/4一个点
        
        # 对每个角度执行一次更新
        for i, angle in enumerate(angles):
            # 计算新位置
            r = start_r
            z_new = self.polar_to_cartesian(r, angle)
            projection_new = self.get_projection_point(z_new)
            
            # 创建新连接线
            new_line = Line3D(
                north_pole_pos,
                np.array([z_new[0], z_new[1], 0]),
                color=YELLOW
            )
            
            # 计算当前索引（0-32之间的值）
            current_index = round(32 * angle / (2*PI))
            
            # 更新复数值显示，使用极坐标格式
            new_complex = self.format_complex_number(r, current_index)
            new_tex = MathTex(new_complex, font_size=48).to_corner(UR)
            
            # 播放动画
            self.play(
                z_dot.animate.move_to(np.array([z_new[0], z_new[1], 0])),
                projection_dot.animate.move_to(projection_new),
                Transform(self.complex_num, new_tex),
                Create(new_line),
                run_time=1.0  # 减少每段动画的时间
            )
            self.animation_timer += 1.0
            
            # 在下一帧之前移除当前连接线
            self.play(FadeOut(new_line), run_time=0.2)
            self.animation_timer += 0.2
    
    def phase5_infinity_point(self):
        """第五阶段：无穷远点映射"""
        # 移除复数文本，彻底解决重叠问题
        self.play(FadeOut(self.complex_num), run_time=0.3)
        self.animation_timer += 0.3
        
        self.update_subtitle("现在我们观察当复数沿实轴移动时，投影点的变化", wait=6)

        # 北极点位置
        north_pole_pos = np.array([0, 0, 2*self.SPHERE_RADIUS])
        
        # 添加字幕说明移动方向和效果
        self.update_subtitle("接下来复数将沿着实轴从负无穷移动到正无穷", wait=1)

        # 定义r值序列
        # 从大到小的正数值和从小到大的负数值，用于模拟复数从负无穷到正无穷的移动
        r_negative = [-20, -10, -7, -5, -4, -3.5, -3, -2.5, -2, -1.7, -1.4, -1.1, -0.8, -0.5, -0.2]
        r_positive = [0.2, 0.5, 0.8, 1.1, 1.4, 1.7, 2, 2.5, 3, 3.5, 4, 5, 7, 10, 20]
        r_values = r_negative + r_positive
        
        # 先让z_dot隐身,
        self.play(FadeOut(self.z_dot), run_time=0.3)
        self.animation_timer += 0.3
        self.play(FadeOut(self.projection_dot), run_time=0.3)
        self.animation_timer += 0.3
        
        # 计算r_values起始点的位置
        initial_r = r_values[0]  # 获取r_values的第一个值
        z_point = self.polar_to_cartesian(initial_r, 0)
        projection_pos = self.get_projection_point(z_point)
        # 移动z_dot和projection_dot到新位置
        self.z_dot.move_to(np.array([z_point[0], z_point[1], 0]))
        self.projection_dot.move_to(projection_pos)
        
        # 让投影点重新显形
        self.play(FadeIn(self.projection_dot), run_time=0.3)
        self.animation_timer += 0.3
        self.play(FadeIn(self.z_dot), run_time=0.3)
        self.animation_timer += 0.3

        # 创建轨迹对象 - 使用TracedPath跟踪投影点的移动
        # 注意：我们需要先创建一个新的投影点，因为TracedPath会跟踪这个点的移动
        tracing_dot = Dot3D(north_pole_pos, color=RED, radius=0.08)
        tracing_dot.set_z_index(10)  # 确保点在轨迹上方
        
        # 创建TracedPath对象，它会自动跟踪点的移动并生成轨迹
        trajectory = TracedPath(tracing_dot.get_center, stroke_width=2, stroke_color=RED)
        
        # 将轨迹和跟踪点添加到场景
        self.add(trajectory, tracing_dot)
        
        # 遍历r值序列，使点沿着轨迹移动
        for i, r in enumerate(r_values):
            # 计算复平面上的新位置
            z_new = self.polar_to_cartesian(r, 0)
            
            # 计算投影点位置
            projection_new = self.get_projection_point(z_new)
            
            # 创建从北极点到复平面点的连接线
            new_line = Line3D(
                north_pole_pos,
                np.array([z_new[0], z_new[1], 0]),
                color=YELLOW
            )
            
            # 播放动画：移动复平面上的点、更新投影点位置、创建连接线
            # 注意：同时移动self.projection_dot和tracing_dot，后者会自动生成轨迹
            self.play(
                self.z_dot.animate.move_to(np.array([z_new[0], z_new[1], 0])),
                self.projection_dot.animate.move_to(projection_new),
                tracing_dot.animate.move_to(projection_new),  # 这个点的移动会被TracedPath跟踪
                Create(new_line),
                run_time=1.0
            )
            self.animation_timer += 1.0
            
            # 在下一帧之前移除当前连接线
            self.play(FadeOut(new_line), run_time=0.2)
            self.animation_timer += 0.2
        
        self.update_subtitle("当复数沿着实轴从负无穷移动到正无穷，投影点会画出一个大圆", wait=6)
        
        self.update_subtitle("大圆经过北极点，意味着黎曼球面北极点对应的是复平面上的无穷远点", wait=7)
        
        self.update_subtitle("复平面上的直线对应于黎曼球面上的圆，它们全都经过北极点，但未必都是大圆", wait=7)

    def ending(self):
        """动画结束阶段"""
        # 总结动画内容
        self.update_subtitle("今天我们学习了如何将复平面映射到黎曼球面", wait=7)
        self.update_subtitle("请大家进一步思考：什么样的直线一定对应于大圆？", wait=7)
        self.update_subtitle("谢谢观看！", wait=3)


if __name__ == "__main__":
    # 解析命令行参数
    # 命令行参数配置
    parser = argparse.ArgumentParser(description="运行黎曼球面动画")
    parser.add_argument("--quality", "-q", type=str, choices=["l", "m", "h", "k"], default="l",
                        help="动画质量：l(低), m(中), h(高), k(4K)")
    parser.add_argument("--preview", "-p", action="store_true",
                        help="是否自动预览")
    parser.add_argument("--force", "-f", action="store_true",
                        help="是否强制重新渲染")
    parser.add_argument("--keep-cache", "-k", action="store_true",
                        help="是否保留缓存文件不清除")
    args = parser.parse_args()

    # 构建manim命令
    quality_flag = f"-q{args.quality}"
    preview_flag = "-p" if args.preview else ""
    force_flag = "-f" if args.force else ""

    # 构建并执行命令
    cmd = f"manim {quality_flag} {preview_flag} {force_flag} {__file__} RiemannSphere"
    print(f"执行命令: {cmd}")
    print("正在渲染动画，请耐心等待...")
    os.system(cmd)
    
    # 输出文件路径
    quality_map = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
    output_dir = f"{default_output_dir}/videos/demo/{quality_map[args.quality]}"
    output_file = f"{output_dir}/RiemannSphere.mp4"
    print(f"渲染完成！")
    print(f"输出文件: {output_file}")
    
    # 清理缓存文件（仅当未指定保留缓存时）
    if not args.keep_cache:
        partial_dir = f"{output_dir}/partial_movie_files"
        if os.path.exists(partial_dir):
            shutil.rmtree(partial_dir)
            print(f"已清除部分电影文件缓存: {partial_dir}")
        print("缓存清理完成！")
    else:
        print("根据设置保留了缓存文件")