from manim import *
from manim.utils.color.X11 import VIOLET

class BeatFrequency(Scene):
    COLORS = {
        "wave1": VIOLET,
        "wave2": YELLOW,
        "interference": BLUE,
        "constructive": GREEN,
        "destructive": RED,
        "axes": WHITE
    }

    def construct(self):
        # Parameters for the sine waves
        self.freq1 = 10  # Frequency of the first wave (Hz)
        self.freq2 = 12  # Frequency of the second wave (Hz)
        self.amplitude = 1
        self.time_range = np.linspace(0, 2, 1000)  # Time range for the waves (2 seconds)

        # Create axes
        self.axes_wave1 = self.create_axes(UP)
        self.axes_wave2 = self.create_axes(DOWN)
        self.axes_bottom = self.create_axes(DOWN)

        # Define sine wave functions
        self.wave1 = self.define_wave(self.freq1)
        self.wave2 = self.define_wave(self.freq2)

        self.interference = lambda t: self.wave1(t) + self.wave2(t)

        # Create wave graphs
        self.wave1_graph = self.axes_wave1.plot(lambda t: self.wave1(t), color=self.COLORS["wave1"], x_range=[0, 2])
        self.wave2_graph = self.axes_wave2.plot(lambda t: self.wave2(t), color=self.COLORS["wave2"], x_range=[0, 2])

        # Add labels
        self.wave1_label = self.create_label(f"{self.freq1} Hz", self.axes_wave1, self.COLORS["wave1"])
        self.wave2_label = self.create_label(f"{self.freq2} Hz", self.axes_wave2, self.COLORS["wave2"])
        self.interference_label = self.create_label("Interference", self.axes_bottom, self.COLORS["interference"])
        
        self.constructive_label = self.create_label("Constructive", self.axes_wave1, self.COLORS["constructive"])
        self.destructive_label = self.create_label("Destructive", self.axes_wave1, self.COLORS["destructive"], RIGHT*2.5)


        # Animate individual waves
        self.play(Create(self.axes_wave1), Create(self.axes_wave2))
        self.play(Create(self.wave1_graph), Write(self.wave1_label))
        self.play(Create(self.wave2_graph), Write(self.wave2_label))
        self.wait(1)

        # Transition wave2_graph into axes_wave1
        self.play(FadeOut(self.axes_wave2, self.wave1_label, self.wave2_label),
                  Transform(self.wave2_graph, self.axes_wave1.plot(lambda t: self.wave2(t), color=self.COLORS["wave2"], x_range=[0, 2])))
        self.wait(1)

        self.play(Create(self.axes_bottom), Write(self.interference_label))
        self.play(Write(self.constructive_label), Write(self.destructive_label))


        # Create dynamic waves and interference
        dynamic_wave1 = VGroup()
        dynamic_wave2 = VGroup()
        dynamic_interference = VGroup()
        for t in np.linspace(0, 2, 200):
            segment_wave1 = self.axes_wave1.plot(lambda x: self.wave1(x), x_range=[t, t + 0.01], color=self.get_color(self.wave1, self.wave2, t))
            segment_wave2 = self.axes_wave1.plot(lambda x: self.wave2(x), x_range=[t, t + 0.01], color=self.get_color(self.wave1, self.wave2, t))
            segment_interference = self.axes_bottom.plot(lambda x: self.interference(x), x_range=[t, t + 0.01], color=self.COLORS["interference"])
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

    def create_axes(self, position):
        return Axes(
            x_range=[0, 2, 0.2],
            y_range=[-2.5, 2.5, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"color": self.COLORS["axes"]},
        ).to_edge(position, buff=0.3)

    def define_wave(self, frequency):
        return lambda t: self.amplitude * np.sin(2 * PI * frequency * t)

    def create_label(self, text, axes, color, position=0):
        return Text(text, font_size=24, color=color).move_to(axes.get_corner(UL) + RIGHT * 1.5 + position)

    def get_color(self, wave1, wave2, t):
        if np.abs(wave1(t) + wave2(t)) > 0.5 * (np.abs(wave1(t)) + np.abs(wave2(t))):
            return self.COLORS["constructive"]
        else:
            return self.COLORS["destructive"]
