from manim import *

class TestDot(Scene):
    def construct(self):
        dot = Dot(point=ORIGIN, color=YELLOW, radius=0.5)
        self.add(dot)
        self.wait(2)
