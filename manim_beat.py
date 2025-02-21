from manim import *
from manim.opengl import *

from manim.utils.color.AS2700 import X14_MANDARIN
from manim.utils.color.X11 import BEIGE, VIOLET
from manim.utils.color import color_to_rgb, rgb_to_color
from manim.utils.color.XKCD import BLUEGREEN

import colorsys


class BeatFrequency(Scene):
    COLORS = {
        "wave1": GREEN_C,
        "wave2": BLUEGREEN,
        "wave3": VIOLET,
        "interference": BLUE,
        "constructive": GREEN,
        "destructive": RED,
        "axes": WHITE
    }
    X_MAX = 2
    X_MIN = 0
    AMPLITUDE = 1
    BASE_FREQ = 30

    def create_axes(self, position, height=3, labels=False, y_max=2.5, step=0.5):
        y_tick = 0.5
        y_numbers = np.arange(-y_max, y_max + y_tick, y_tick)

        # mod = 2 if len(y_numbers) < 20 else 5
        # r = 1 if mod == 2 else 0 

        # step = 0.5 if len(y_numbers) < 20 else 5
        
        # filtered_y_numbers = [
        #     num for i, num in enumerate(y_numbers) if i % mod == r or num == 0
        # ]
        axes = Axes(
            x_range=[self.X_MIN, self.X_MAX*1.05, 0.2],
            y_range=[-y_max, y_max, step],
            x_length=11,
            y_length=height,
            y_axis_config={
                "include_numbers": labels,
                # "numbers_to_include": filtered_y_numbers,
                "font_size": 20
            },
            axis_config={"color": self.COLORS["axes"]},
        )
        if isinstance(position, np.ndarray):
            axes.to_edge(position, buff=0.3)
        elif position == "center":
            axes.move_to(ORIGIN)
        else:
            raise ValueError("Check position value")

        return axes

    def define_wave(self, amplitude, frequency):
        return lambda t: amplitude * np.sin(2 * PI * frequency * t)

    def interference(self, freqs, t):
        return np.sum([self.define_wave(self.AMPLITUDE, freq)(t) for freq in freqs], axis=0)

    def construct(self):
        # step size for wave
        step_size = 0.005

        ## 2 waves beat interference

        # Create axes
        axes_wave1 = self.create_axes(UP)
        axes_wave2 = self.create_axes(DOWN)
        axes_bottom = self.create_axes(DOWN, labels=True)

        # Define sine wave functions
        wave1 = self.define_wave(self.AMPLITUDE, self.BASE_FREQ)
        wave2 = self.define_wave(self.AMPLITUDE, self.BASE_FREQ + 2)

        # Create wave graphs
        wave1_graph = axes_wave1.plot(
            lambda t: wave1(t),
            color=self.COLORS["wave1"],
            x_range=[0, self.X_MAX, step_size],
        )
        wave2_graph = axes_wave2.plot(
            lambda t:
            wave2(t),
            color=self.COLORS["wave2"],
            x_range=[0, self.X_MAX, step_size]
        )

        # Add labels
        wave1_label = self.create_label(
            "240 Hz",
            axes_wave1,
            self.COLORS["wave1"]
        )
        wave2_label = self.create_label(
            "242 Hz",
            axes_wave2,
            self.COLORS["wave2"]
        )
        interference_label = self.create_label(
            "2 Wave Interference",
            axes_bottom,
            self.COLORS["interference"],
            shift_h=RIGHT*1 + UP*0.2,
        )
        

        def get_legend_rectangle(height=0.33, width=2.5, num_strips=50, eps=0.00):
            # Define the number of strips (more strips = smoother gradient)
            strip_width = (width / num_strips) + eps
    
            # Define the start and end colors
            left_color = self.COLORS["constructive"]
            right_color = self.COLORS["destructive"]
            strips = VGroup()

            for i in range(num_strips):
                # Calculate alpha (goes from 0 to 1)
                alpha = i / (num_strips - 1)
                interp_color = self.interpolate_hsl(
                    left_color,
                    right_color,
                    alpha
                )
                # Create a thin rectangle (strip) with the interpolated color
                strip = Rectangle(
                    width=strip_width,
                    height=height,
                    fill_color=interp_color,
                    fill_opacity=1,
                    stroke_width=0
                )
                # Position each strip next to the previous one
                # Starting from the left edge (-total_width/2)
                strip.move_to(np.array([
                    -width/2 + strip_width/2 + i * strip_width,
                    0,
                    0
                ]))
                strips.add(strip)


            constructive_label = Text(
                "Constructive",
                font_size=20,
                color=self.COLORS["constructive"]
            ).move_to(strips.get_corner(UL) + UP * 0.3)

            destructive_label = Text(
                "Destructive",
                font_size=20,
                color=self.COLORS["destructive"]
            ).move_to(strips.get_corner(UR) + UP * 0.3)

            strips.add(constructive_label)
            strips.add(destructive_label)
            return strips

        legend_rect = get_legend_rectangle()
        legend_rect.move_to(axes_wave1.get_top() + UP * 0.2 + LEFT * 2.5)

        # Animate individual waves
        self.play(Create(axes_wave1), Create(axes_wave2))
        self.play(Create(wave1_graph), Write(wave1_label))
        self.play(Create(wave2_graph), Write(wave2_label))
        self.wait(1)

        # Transition wave2_graph into axes_wave1
        self.play(
            FadeOut(axes_wave2, wave1_label, wave2_label),
            Transform(
                wave2_graph,
                axes_wave1.plot(
                    lambda t: wave2(t),
                    color=self.COLORS["wave2"],
                    x_range=[0, self.X_MAX, step_size]
                )
            )
        )
        self.wait(1)

        self.play(
            Create(axes_bottom),
            Write(interference_label),
            Create(legend_rect),
        )

        # Create dynamic waves and interference
        dynamic_wave1 = VGroup()
        dynamic_wave2 = VGroup()
        dynamic_interference = VGroup()
        for t in np.linspace(0, self.X_MAX, 200):
            segment_wave1 = axes_wave1.plot(
                lambda x: wave1(x),
                x_range=[t, t + 0.01, 0.001],
                color=self.get_color([wave1, wave2], t)
            )
            segment_wave2 = axes_wave1.plot(
                lambda x: wave2(x),
                x_range=[t, t + 0.01, 0.001],
                color=self.get_color([wave1, wave2], t)
            )
            segment_interference = axes_bottom.plot(
                lambda x: self.interference(
                    [self.BASE_FREQ + i for i in range(0, 4, 2)], x
                ),
                x_range=[t, t + 0.01, 0.001],
                color=self.COLORS["interference"]
            )
            dynamic_wave1.add(segment_wave1)
            dynamic_wave2.add(segment_wave2)
            dynamic_interference.add(segment_interference)

        infer_dot, wave1_dot, wave2_dot = (
            Dot(color=self.COLORS[i], radius=0.075)
            for i in ("interference", "wave1", "wave2")
        )
        self.add(infer_dot, wave1_dot, wave2_dot)

        # Animate dynamic waves and interference
        for segment1, segment2, segment_interf in zip(dynamic_wave1, dynamic_wave2, dynamic_interference):
            self.play(
                Create(segment1),
                Create(segment2),
                Create(segment_interf),
                MoveAlongPath(infer_dot, segment_interf),
                MoveAlongPath(wave1_dot, segment1),
                MoveAlongPath(wave2_dot, segment2),
                run_time=0.02,
                rate_func=linear
            )
        self.wait(2)

        def add_vertical_line(audio_name, axes=axes_bottom):
            vertical_line = Line(
                axes.c2p(self.X_MIN+0.03, axes.y_range[0]),
                axes.c2p(self.X_MIN+0.03, axes.y_range[1]),
                color=WHITE,
            )
            self.play(Create(vertical_line))

            # 1 second per tick
            speed = (axes.c2p(1.05, 0) - axes.c2p(0, 0))
            
            def update_line(mob, dt):
                mob.shift(RIGHT * speed * dt)
                current_center = axes.p2c(mob.get_center())
                if current_center[0] > self.X_MAX:
                    mob.move_to(np.array([
                        axes.c2p(self.X_MIN, 0)[0],
                        mob.get_center()[1],
                        mob.get_center()[2],
                    ]))

            vertical_line.add_updater(update_line)
            self.add_sound(audio_name)

            self.wait(4)

            vertical_line.remove_updater(update_line)
            self.play(FadeOut(vertical_line))

        add_vertical_line("waves2beat.wav")

        # Clear previous scene
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )

        ## Begin 3 wave animation

        axes_wave1_original = self.create_axes(UP)
        axes_wave1 = self.create_axes(UP, height=2)
        axes_wave2 = self.create_axes(ORIGIN, height=2)
        axes_wave3 = self.create_axes(DOWN, height=2)
        axes_bottom = self.create_axes(DOWN, labels=True, y_max=3.5)

        # Define sine wave functions
        wave1 = self.define_wave(self.AMPLITUDE, self.BASE_FREQ)
        wave2 = self.define_wave(self.AMPLITUDE, self.BASE_FREQ + 2)
        wave3 = self.define_wave(self.AMPLITUDE, self.BASE_FREQ + 4)

        # Create wave graphs
        wave1_graph = axes_wave1.plot(
            lambda t: wave1(t),
            color=self.COLORS["wave1"],
            x_range=[0, self.X_MAX, step_size]
        )
        wave2_graph = axes_wave2.plot(
            lambda t: wave2(t),
            color=self.COLORS["wave2"],
            x_range=[0, self.X_MAX, step_size]
        )
        wave3_graph = axes_wave3.plot(
            lambda t: wave3(t),
            color=self.COLORS["wave3"],
            x_range=[0, self.X_MAX, step_size]
        )

        # Add labels
        wave1_label = self.create_label(
            "240 Hz",
            axes_wave1,
            self.COLORS["wave1"],
            corner=UL
        )
        wave2_label = self.create_label(
            "242 Hz",
            axes_wave2,
            self.COLORS["wave2"],
            corner=UL
        )
        wave3_label = self.create_label(
            "244 Hz",
            axes_wave3,
            self.COLORS["wave3"],
            corner=UL
        )
        interference_label = self.create_label(
            "3 Wave Interference",
            axes_bottom,
            self.COLORS["interference"],
            shift_h=RIGHT*1,
            shift_v=UP*0.5,
        )

        # Animate individual waves
        self.play(Create(axes_wave1), Create(axes_wave2), Create(axes_wave3))
        self.play(Create(wave1_graph), Write(wave1_label))
        self.play(Create(wave2_graph), Write(wave2_label))
        self.play(Create(wave3_graph), Write(wave3_label))
        self.wait(1)

        # Transition wave2_graph & wave3_graph into axes_wave1
        self.play(
            FadeOut(axes_wave2, axes_wave3, wave1_label, wave2_label, wave3_label),
            Transform(
                wave2_graph,
                axes_wave1.plot(
                    lambda t: wave2(t),
                    color=self.COLORS["wave2"],
                    x_range=[0, self.X_MAX, step_size]
                )
            ),
            Transform(
                wave3_graph,
                axes_wave1.plot(
                    lambda t: wave3(t),
                    color=self.COLORS["wave3"],
                    x_range=[0, self.X_MAX, step_size]
                )
            ),
        )

        self.wait(1)

        legend_rect = get_legend_rectangle()
        legend_rect.move_to(axes_wave1.get_top() + UP * 0.2 + LEFT * 2.5)

        self.play(
            Create(axes_bottom),
            Write(interference_label),
            Transform(axes_wave1, axes_wave1_original),
            Transform(
                wave1_graph,
                axes_wave1_original.plot(
                    lambda t: wave1(t),
                    color=self.COLORS["wave1"],
                    x_range=[0, self.X_MAX, step_size]
                )
            ),
            Transform(
                wave2_graph,
                axes_wave1_original.plot(
                    lambda t: wave2(t),
                    color=self.COLORS["wave2"],
                    x_range=[0, self.X_MAX, step_size]
                )
            ),
            Transform(
                wave3_graph,
                axes_wave1_original.plot(
                    lambda t: wave3(t),
                    color=self.COLORS["wave3"],
                    x_range=[0, self.X_MAX, step_size]
                )
            ),
            Create(legend_rect),
        )

        # Create dynamic waves and interference
        dynamic_wave1 = VGroup()
        dynamic_wave2 = VGroup()
        dynamic_wave3 = VGroup()
        dynamic_interference = VGroup()
        for t in np.linspace(0, self.X_MAX, 200):
            segment_wave1 = axes_wave1.plot(
                lambda x: wave1(x),
                x_range=[t, t + 0.01, 0.001],
                color=self.get_color([wave1, wave2, wave3], t)
            )
            segment_wave2 = axes_wave1.plot(
                lambda x: wave2(x),
                x_range=[t, t + 0.01, 0.001],
                color=self.get_color([wave1, wave2, wave3], t)
            )
            segment_wave3 = axes_wave1.plot(
                lambda x: wave3(x),
                x_range=[t, t + 0.01, 0.001],
                color=self.get_color([wave1, wave2, wave3], t)
            )
            dynamic_wave1.add(segment_wave1)
            dynamic_wave2.add(segment_wave2)
            dynamic_wave3.add(segment_wave3)
            segment_interference = axes_bottom.plot(
                lambda x: self.interference(
                    [self.BASE_FREQ + i for i in range(0, 3*2, 2)], x
                ),
                x_range=[t, t + 0.01, 0.001],
                color=self.COLORS["interference"]
            )
            dynamic_interference.add(segment_interference)

        infer_dot, wave1_dot, wave2_dot, wave3_dot = (
            Dot(color=self.COLORS[i], radius=0.075)
            for i in ("interference", "wave1", "wave2", "wave3")
        )
        self.add(infer_dot, wave1_dot, wave2_dot)

        # Animate dynamic waves and interference
        for segment1, segment2, segment3, segment_interf in zip(dynamic_wave1, dynamic_wave2, dynamic_wave3, dynamic_interference):
            self.play(
                Create(segment1),
                Create(segment2),
                Create(segment3),
                Create(segment_interf),
                MoveAlongPath(infer_dot, segment_interf),
                MoveAlongPath(wave1_dot, segment1),
                MoveAlongPath(wave2_dot, segment2),
                MoveAlongPath(wave3_dot, segment3),
                run_time=0.02,
                rate_func=linear
            )
        self.wait(2)

        add_vertical_line("waves3beat.wav")

        
        ## 5 Wave interference

        # Clear previous scene
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # self.interactive_embed()

        axes_5 = self.create_axes(
            "center", 
            height=5, 
            labels=True, 
            y_max=6,
            step=1,
        )

        # Create wave graphs
        axes_5_graph = axes_5.plot(
            lambda t: self.interference(
                [self.BASE_FREQ + i for i in range(0, 5*2, 2)], t
            ),
            color=self.COLORS["interference"],
            x_range=[0, self.X_MAX, step_size]
        )

        dot_5 = Dot(color=self.COLORS["interference"], radius=0.075)

        dot_5.add_updater(
            lambda t: t.move_to(axes_5_graph.get_end()) # type: ignore
        )

        axes_5_label = self.create_label(
            "5 Waves - Interference",
            axes_5,
            self.COLORS["interference"],
            shift_h=RIGHT*0.9,
            shift_v=UP*0.3
        )

        # Animate individual waves
        self.play(Create(axes_5), Write(axes_5_label))

        self.add(dot_5)
        self.play(
            Create(axes_5_graph),
            run_time=1,
            rate_func=linear
        )

        add_vertical_line("waves5beat.wav", axes=axes_5)

        self.wait(1)


        ## 20 Wave interference

        axes_20 = self.create_axes(
            "center",
            height=5,
            labels=True,
            y_max=25,
            step=5,
        )

        self.play(
            FadeOut(axes_5, axes_5_graph, axes_5_label, dot_5),
            FadeIn(axes_20)
        )

        # Create wave graphs
        axes_20_graph = axes_20.plot(
            lambda t: self.interference(
                [self.BASE_FREQ + i for i in range(0, 20*2, 2)], t
            ),
            color=self.COLORS["interference"],
            x_range=[0, self.X_MAX, step_size/10.]
        )

        dot_20 = Dot(color=self.COLORS["interference"], radius=0.075)

        dot_20.add_updater(
            lambda t: t.move_to(axes_20_graph.get_end()) # type: ignore
        )

        axes_20_label = self.create_label(
            "20 Waves - Interference",
            axes_20,
            self.COLORS["interference"],
            shift_h=RIGHT*0.9,
            shift_v=UP*0.3
        )

        self.play(
            Write(axes_20_label),
        )

        self.add(dot_20)
        self.play(
            Create(axes_20_graph),
            run_time=1,
            rate_func=linear
        )

        add_vertical_line("waves20beat.wav", axes=axes_20)

        self.wait(1)

        axes_50 = self.create_axes(
            "center",
            height=5,
            labels=True,
            y_max=50,
            step=10,
        )

        self.play(
            FadeOut(axes_20_graph, axes_20_label, dot_20, axes_20),
            FadeIn(axes_50)
        )

        # Create wave graphs
        axes_50_graph = axes_50.plot(
            lambda t: self.interference(
                [self.BASE_FREQ + i for i in range(0, 50*2, 2)], t
            ),
            color=self.COLORS["interference"],
            x_range=[0, self.X_MAX, step_size/20.]
        )

        dot_50 = Dot(color=self.COLORS["interference"], radius=0.075)

        dot_50.add_updater(
            lambda t: t.move_to(axes_50_graph.get_end()) # type: ignore
        )

        axes_50_label = self.create_label(
            "50 Waves - Interference",
            axes_50,
            self.COLORS["interference"],
            shift_h=RIGHT*0.9,
            shift_v=UP*0.3
        )

        # Animate individual waves
        self.play(
            Write(axes_50_label),
        )

        self.add(dot_50)
        self.play(
            Create(axes_50_graph),
            run_time=1,
            rate_func=linear
        )

        add_vertical_line("waves50beat.wav", axes=axes_50)

        self.wait(1)


        axes_101 = self.create_axes(
            "center", 
            height=5, 
            labels=True, 
            y_max=90,
            step=20,
        )

        self.play(
            FadeOut(axes_50, axes_50_graph, axes_50_label, dot_50),
            FadeIn(axes_101)
        )

        # Create wave graphs
        axes_101_graph = axes_101.plot(
            lambda t: self.interference(
                [self.BASE_FREQ + i for i in range(0, 101*2, 2)], t
            ),
            color=self.COLORS["interference"],
            x_range=[0, self.X_MAX, step_size/100.]
        )

        dot_101 = Dot(color=self.COLORS["interference"], radius=0.075)

        dot_101.add_updater(
            lambda t: t.move_to(axes_101_graph.get_end()) # type: ignore
        )

        axes_101_label = self.create_label(
            "101 Waves - Interference",
            axes_101,
            self.COLORS["interference"],
            shift_h=RIGHT*0.9,
            shift_v=UP*0.3
        )

        # Animate individual waves
        self.play(
            Write(axes_101_label)
        )

        self.add(dot_101)
        self.play(
            Create(axes_101_graph),
            run_time=1,
            rate_func=linear
        )

        add_vertical_line("waves101beat.wav", axes=axes_101)

        self.wait(3)

    def create_label(
        self,
        text,
        axes,
        color,
        shift_h=np.array(0),
        shift_v=np.array(0),
        corner=UL
    ):
        return Text(
            text,
            font_size=24,
            color=color
        ).move_to(
            axes.get_corner(corner) + \
            (RIGHT * 1.5 + shift_h) + \
            (DOWN * 0.1 + shift_v)
        )

    def interpolate_hsl(self, color1, color2, alpha):
        # Convert the colors to RGB tuples in [0, 1]
        rgb1 = color_to_rgb(color1)
        rgb2 = color_to_rgb(color2)

        # Convert RGB to HLS (note: colorsys uses HLS)
        h1, l1, s1 = colorsys.rgb_to_hls(*rgb1)
        h2, l2, s2 = colorsys.rgb_to_hls(*rgb2)

        # Interpolate each component
        h = h1 + (h2 - h1) * alpha
        l = l1 + (l2 - l1) * alpha
        s = s1 + (s2 - s1) * alpha

        # Convert back to RGB and then to a Manim color
        rgb_interp = colorsys.hls_to_rgb(h, l, s)
        return rgb_to_color(rgb_interp)

    def get_color(self, waves, t):
        total = sum(wave(t) for wave in waves)
        total_abs = sum(np.abs(wave(t)) for wave in waves)
        if total_abs == 0:
            return self.COLORS["constructive"]  # or some default color
        # interference_factor is 0 for perfect cancellation and 1 for full constructive interference
        interference_factor = np.abs(total) / total_abs
        # interpolate_color interpolates between destructive (RED) and constructive (GREEN)
        return self.interpolate_hsl(
            self.COLORS["destructive"],
            self.COLORS["constructive"],
            interference_factor
        )
