from manim import *
from manim.utils.color.X11 import VIOLET

class BeatFrequency(Scene):
    COLORS = {
        "wave1": VIOLET,
        "wave2": YELLOW,
        "wave3": ORANGE,
        "interference": BLUE,
        "constructive": GREEN,
        "destructive": RED,
        "axes": WHITE
    }

    def construct(self):
        # Parameters for the sine waves
        freq1 = 10  # Frequency of the first wave (Hz)
        freq2 = 12  # Frequency of the second wave (Hz)
        amplitude = 1
        time_range = np.linspace(0, 2, 1000)  # Time range for the waves (2 seconds)

        # Create axes
        axes_wave1 = self.create_axes(UP)
        axes_wave2 = self.create_axes(DOWN)
        axes_bottom = self.create_axes(DOWN)

        # Define sine wave functions
        wave1 = self.define_wave(amplitude, freq1)
        wave2 = self.define_wave(amplitude, freq2)

        interference = lambda t: wave1(t) + wave2(t)

        # Create wave graphs
        wave1_graph = axes_wave1.plot(lambda t: wave1(t), color=self.COLORS["wave1"], x_range=[0, 1.9])
        wave2_graph = axes_wave2.plot(lambda t: wave2(t), color=self.COLORS["wave2"], x_range=[0, 1.9])

        # Add labels
        wave1_label = self.create_label(f"{freq1} Hz", axes_wave1, self.COLORS["wave1"])
        wave2_label = self.create_label(f"{freq2} Hz", axes_wave2, self.COLORS["wave2"])
        interference_label = self.create_label("Interference", axes_bottom, self.COLORS["interference"])
        
        constructive_label = self.create_label("Constructive", axes_wave1, self.COLORS["constructive"])
        destructive_label = self.create_label("Destructive", axes_wave1, self.COLORS["destructive"], RIGHT*2.5)


        # Animate individual waves
        self.play(Create(axes_wave1), Create(axes_wave2))
        self.play(Create(wave1_graph), Write(wave1_label))
        self.play(Create(wave2_graph), Write(wave2_label))
        self.wait(1)

        # Transition wave2_graph into axes_wave1
        self.play(FadeOut(axes_wave2, wave1_label, wave2_label),
                  Transform(wave2_graph, axes_wave1.plot(lambda t: wave2(t), color=self.COLORS["wave2"], x_range=[0, 1.9])))
        self.wait(1)

        self.play(Create(axes_bottom), Write(interference_label))
        self.play(Write(constructive_label), Write(destructive_label))

        # Create dynamic waves and interference
        dynamic_wave1 = VGroup()
        dynamic_wave2 = VGroup()
        dynamic_interference = VGroup()
        for t in np.linspace(0, 1.9, 200):
            segment_wave1 = axes_wave1.plot(lambda x: wave1(x), x_range=[t, t + 0.01], color=self.get_color([wave1, wave2], t))
            segment_wave2 = axes_wave1.plot(lambda x: wave2(x), x_range=[t, t + 0.01], color=self.get_color([wave1, wave2], t))
            segment_interference = axes_bottom.plot(lambda x: interference(x), x_range=[t, t + 0.01], color=self.COLORS["interference"])
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

        # Define sine wave functions
        wave1 = self.define_wave(amplitude, freq1)
        wave2 = self.define_wave(amplitude, freq2)
        wave3 = self.define_wave(amplitude, freq2 + 2)

        interference3 = lambda t: wave1(t) + wave2(t) + wave3(t)

        # Create wave graphs
        wave1_graph = axes_wave1.plot(lambda t: wave1(t), color=self.COLORS["wave1"], x_range=[0, 1.9])
        wave2_graph = axes_wave2.plot(lambda t: wave2(t), color=self.COLORS["wave2"], x_range=[0, 1.9])
        wave3_graph = axes_wave3.plot(lambda t: wave3(t), color=self.COLORS["wave3"], x_range=[0, 1.9])

        # Add labels
        wave1_label = self.create_label(f"{freq1} Hz", axes_wave1, self.COLORS["wave1"], corner=UL)
        wave2_label = self.create_label(f"{freq2} Hz", axes_wave2, self.COLORS["wave2"], corner=UL)
        wave3_label = self.create_label(f"{freq2 + 2} Hz", axes_wave3, self.COLORS["wave3"], corner=UL)

        # Animate individual waves
        self.play(Create(axes_wave1), Create(axes_wave2), Create(axes_wave3))
        self.play(Create(wave1_graph), Write(wave1_label))
        self.play(Create(wave2_graph), Write(wave2_label))
        self.play(Create(wave3_graph), Write(wave3_label))
        self.wait(1)

        # Transition wave2_graph & wave3_graph into axes_wave1
        self.play(FadeOut(axes_wave2, axes_wave3, wave1_label, wave2_label, wave3_label),
                  Transform(wave2_graph, axes_wave1.plot(lambda t: wave2(t), color=self.COLORS["wave2"], x_range=[0, 1.9])),
                  Transform(wave3_graph, axes_wave1.plot(lambda t: wave3(t), color=self.COLORS["wave3"], x_range=[0, 1.9])),)

        self.wait(1)



        self.play(
            Create(axes_bottom),
            Write(interference_label),
            Transform(axes_wave1, axes_wave1_original),
            Transform(wave1_graph, axes_wave1_original.plot(lambda t: wave1(t), color=self.COLORS["wave1"], x_range=[0, 1.9])),
            Transform(wave2_graph, axes_wave1_original.plot(lambda t: wave2(t), color=self.COLORS["wave2"], x_range=[0, 1.9])),
            Transform(wave3_graph, axes_wave1_original.plot(lambda t: wave3(t), color=self.COLORS["wave3"], x_range=[0, 1.9])),
        )

        self.play(Write(constructive_label), Write(destructive_label))

        # Create dynamic waves and interference
        dynamic_wave1 = VGroup()
        dynamic_wave2 = VGroup()
        dynamic_wave3 = VGroup()
        dynamic_interference = VGroup()
        for t in np.linspace(0, 1.9, 200):
            segment_wave1 = axes_wave1.plot(lambda x: wave1(x), x_range=[t, t + 0.01], color=self.get_color([wave1, wave2, wave3], t))
            segment_wave2 = axes_wave1.plot(lambda x: wave2(x), x_range=[t, t + 0.01], color=self.get_color([wave1, wave2, wave3], t))
            segment_wave3 = axes_wave1.plot(lambda x: wave3(x), x_range=[t, t + 0.01], color=self.get_color([wave1, wave2, wave3], t))
            dynamic_wave1.add(segment_wave1)
            dynamic_wave2.add(segment_wave2)
            dynamic_wave3.add(segment_wave3)
            segment_interference = axes_bottom.plot(lambda x: interference3(x), x_range=[t, t + 0.01], color=self.COLORS["interference"])
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

    def create_axes(self, position, height=3):
        axes = Axes(
            x_range=[0, 2, 0.2],
            y_range=[-2.5, 2.5, 0.5],
            x_length=10,
            y_length=height,
            axis_config={"color": self.COLORS["axes"]},
        )
        if position == "center":
            axes.move_to(ORIGIN)
        else:
            axes.to_edge(position, buff=0.3)
        return axes

    def define_wave(self, amplitude, frequency):
        return lambda t: amplitude * np.sin(2 * PI * frequency * t)

    def create_label(self, text, axes, color, shift_h=0, corner=UL):
        return Text(
            text,
            font_size=24,
            color=color
        ).move_to(axes.get_corner(corner) + (RIGHT * 1.5 + shift_h) + (DOWN * 0.15))

    def get_color(self, waves, t, threshold=0.5):
        total = sum(wave(t) for wave in waves)
        total_abs = sum(np.abs(wave(t)) for wave in waves)

        if np.abs(total) > threshold * total_abs:
            return self.COLORS["constructive"]
        else:
            return self.COLORS["destructive"]

