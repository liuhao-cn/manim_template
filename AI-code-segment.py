# # 设置相机角度
        # self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # # 介绍黎曼面概念
        # self.update_subtitle("黎曼面是理解复变函数多值性的重要工具", fontsize=28)
        
        # # 创建复平面
        # complex_plane = NumberPlane(
        #     x_range=[-3, 3, 1],
        #     y_range=[-3, 3, 1],
        #     background_line_style={"stroke_opacity": 0.6}
        # )
        # complex_plane_label = Text("复平面", font_size=24).next_to(complex_plane, UP)
        # self.add_fixed_in_frame_mobjects(complex_plane_label)
        
        # self.play(Create(complex_plane), Write(complex_plane_label), run_time=2)
        # self.animation_timer += 2
        
        # # 解释多值函数问题
        # self.update_subtitle("以平方根函数f(z)=√z为例，它在复平面上是多值的")
        
        # # 创建一个点和它的平方根值
        # z_point = Dot(complex_plane.coords_to_point(2, 0), color=YELLOW)
        # z_label = MathTex("z", color=YELLOW).next_to(z_point, RIGHT, buff=0.1)
        # self.add_fixed_in_frame_mobjects(z_label)
        
        # # 平方根的两个值
        # sqrt_z_point1 = Dot(complex_plane.coords_to_point(np.sqrt(2), 0), color=RED)
        # sqrt_z_point2 = Dot(complex_plane.coords_to_point(-np.sqrt(2), 0), color=BLUE)
        # sqrt_z_label1 = MathTex("\\sqrt{z}", color=RED).next_to(sqrt_z_point1, UP, buff=0.1)
        # sqrt_z_label2 = MathTex("-\\sqrt{z}", color=BLUE).next_to(sqrt_z_point2, UP, buff=0.1)
        # self.add_fixed_in_frame_mobjects(sqrt_z_label1, sqrt_z_label2)
        
        # self.play(
        #     FadeIn(z_point, z_label),
        #     run_time=1
        # )
        # self.animation_timer += 1
        
        # self.play(
        #     FadeIn(sqrt_z_point1, sqrt_z_label1, sqrt_z_point2, sqrt_z_label2),
        #     run_time=2
        # )
        # self.animation_timer += 2
        
        # # 解释分支切割
        # self.update_subtitle("传统方法使用分支切割来处理多值性，但这导致函数不连续")
        
        # branch_cut = DashedLine(
        #     complex_plane.coords_to_point(0, 0),
        #     complex_plane.coords_to_point(-3, 0),
        #     color=RED
        # )
        # branch_cut_label = Text("分支切割", font_size=20, color=RED).next_to(branch_cut, DOWN)
        # self.add_fixed_in_frame_mobjects(branch_cut_label)
        
        # self.play(
        #     Create(branch_cut),
        #     Write(branch_cut_label),
        #     run_time=2
        # )
        # self.animation_timer += 2
        
        # # 清除场景，准备展示黎曼面
        # self.play(
        #     *[FadeOut(mob) for mob in self.mobjects if mob != self.subtitle],
        #     run_time=1
        # )
        # self.animation_timer += 1
        
        # # 介绍黎曼面
        # self.update_subtitle("黎曼面通过将多个复平面层叠在一起，解决了多值问题")
        
        # # 创建两个复平面表示黎曼面的两个片
        # sheet1 = NumberPlane(
        #     x_range=[-3, 3, 1],
        #     y_range=[-3, 3, 1],
        #     background_line_style={"stroke_opacity": 0.4}
        # ).set_color(RED_A)
        
        # sheet2 = NumberPlane(
        #     x_range=[-3, 3, 1],
        #     y_range=[-3, 3, 1],
        #     background_line_style={"stroke_opacity": 0.4}
        # ).set_color(BLUE_A)
        
        # # 初始位置重叠
        # sheet1.move_to(ORIGIN)
        # sheet2.move_to(ORIGIN)
        
        # sheet1_label = Text("第一片", font_size=24, color=RED).next_to(sheet1, UP+RIGHT)
        # sheet2_label = Text("第二片", font_size=24, color=BLUE).next_to(sheet2, DOWN+LEFT)
        # self.add_fixed_in_frame_mobjects(sheet1_label, sheet2_label)
        
        # self.play(
        #     Create(sheet1),
        #     Create(sheet2),
        #     Write(sheet1_label),
        #     Write(sheet2_label),
        #     run_time=2
        # )
        # self.animation_timer += 2
        
        # # 分离两个片以便观察
        # self.update_subtitle("我们可以将两个片分开来观察它们的连接方式")
        
        # self.play(
        #     sheet1.animate.shift(UP),
        #     sheet2.animate.shift(DOWN),
        #     run_time=2
        # )
        # self.animation_timer += 2
        
        # # 展示黎曼面的连接方式
        # self.update_subtitle("在黎曼面上，两个片沿着分支切割线连接")
        
        # # 创建连接线
        # connection_lines = VGroup()
        # for x in np.linspace(-3, 0, 10):
        #     line = Line(
        #         sheet1.coords_to_point(x, 0, 0),
        #         sheet2.coords_to_point(x, 0, 0),
        #         color=YELLOW
        #     )
        #     connection_lines.add(line)
        
        # self.play(
        #     LaggedStart(*[Create(line) for line in connection_lines]),
        #     run_time=3
        # )
        # self.animation_timer += 3
        
        # # 展示绕原点的路径
        # self.update_subtitle("当我们绕原点一周时，会从一个片转移到另一个片")
        
        # # 在第一个片上创建路径
        # path1 = ParametricFunction(
        #     lambda t: sheet1.coords_to_point(
        #         2 * np.cos(t), 2 * np.sin(t), 0
        #     ),
        #     t_range=[0, PI],
        #     color=YELLOW
        # )
        
        # # 在第二个片上创建路径
        # path2 = ParametricFunction(
        #     lambda t: sheet2.coords_to_point(
        #         2 * np.cos(t), 2 * np.sin(t), 0
        #     ),
        #     t_range=[PI, 2*PI],
        #     color=YELLOW
        # )
        
        # # 创建移动点
        # moving_dot = Dot(path1.point_from_proportion(0), color=GREEN)
        
        # # 先显示完整路径
        # self.play(
        #     Create(path1),
        #     Create(path2),
        #     run_time=2
        # )
        # self.animation_timer += 2
        
        # # 然后演示点的移动
        # self.update_subtitle("这就是黎曼面如何使多值函数变为单值函数的方式")
        
        # self.play(
        #     MoveAlongPath(moving_dot, path1),
        #     run_time=3
        # )
        # self.animation_timer += 3
        
        # # 点从第一片跳到第二片
        # self.play(
        #     moving_dot.animate.move_to(path2.point_from_proportion(0)),
        #     run_time=0.5
        # )
        # self.animation_timer += 0.5
        
        # self.play(
        #     MoveAlongPath(moving_dot, path2),
        #     run_time=3
        # )
        # self.animation_timer += 3
        
        # # 展示完整的黎曼面结构
        # self.update_subtitle("完整的黎曼面是一个连通的曲面，解决了多值函数的问题")
        
        # # 清除当前场景
        # self.play(
        #     *[FadeOut(mob) for mob in self.mobjects if mob != self.subtitle],
        #     run_time=1
        # )
        # self.animation_timer += 1
        
        # # 创建一个更复杂的黎曼面模型（螺旋形状）
        # def riemann_surface(u, v):
        #     r = 3 + v
        #     x = r * np.cos(u)
        #     y = r * np.sin(u)
        #     z = u / (2 * PI)
        #     return np.array([x, y, z])
        
        # riemann = Surface(
        #     lambda u, v: riemann_surface(u, v),
        #     u_range=[0, 4 * PI],
        #     v_range=[-1, 1],
        #     resolution=(30, 10),
        #     checkerboard_colors=[RED_D, RED_E]
        # )
        
        # self.play(
        #     Create(riemann),
        #     run_time=3
        # )
        # self.animation_timer += 3
        
        # # 旋转以展示完整结构
        # self.update_subtitle("从不同角度观察，我们可以更好地理解黎曼面的拓扑结构")
        
        # self.begin_ambient_camera_rotation(rate=0.2)
        # self.wait(5)
        # self.animation_timer += 5
        # self.stop_ambient_camera_rotation()
        
        # # 总结
        # self.update_subtitle("黎曼面是理解复变函数的强大工具，它使多值函数变为单值函数")
        # self.wait(2)
        # self.animation_timer += 2
        
        # self.update_subtitle("这一概念由伯恩哈德·黎曼在19世纪提出，至今仍是复分析的基础")
        # self.wait(2)
        # self.animation_timer += 2
        
        # # 结束动画
        # self.update_subtitle("谢谢观看！")
        # self.wait(2)
        # self.animation_timer += 2