from manim import *
import numpy as np

def sinc(x):
    return np.sin(x) / x

def I(x):
    # lam = 500
    # d = 1e3
    # (np.sin(theta) * d) / lam
    return sinc(x) ** 2

class Sinc(Scene):
    def construct(self):
        axes = Axes(x_range=[-18,18,3], 
                    y_range=[0,2.5,1],
                    x_length=15,
                    y_length=6,
                    axis_config={"include_tip": False, "numbers_to_exclude": [0]})

        axes.add_coordinates()
        axis_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.plot(sinc, x_range=[0.001, 15, 0.01], color=YELLOW)
        graph2 = axes.plot(sinc, x_range=[-0.001, -15, -0.01], color=YELLOW)

        self.play(DrawBorderThenFill(axes), Write(axis_labels), run_time=2)
        self.play(Create(graph), Create(graph2))

class Diffraction(Scene):
    def construct(self):
        axes = Axes(x_range=[-15,15,3], 
                    y_range=[-0.2,1.2,1],
                    x_length=10,
                    y_length=6,
                    axis_config={"include_tip": False, "numbers_to_exclude": [0]})

        axes.add_coordinates()
        axis_labels = axes.get_axis_labels(x_label=Tex(R"$d \cdot \sin(\theta) / \lambda$"), y_label=Tex("I"))
        
        graph = axes.plot(I, x_range=[-0.01, -15, -0.01], color=YELLOW)
        graph2 = axes.plot(I, x_range=[0.01, 15, 0.01], color=YELLOW)

        # Create the equation in math mode
        equation = MathTex(
            R"I(\theta) = I_0 \cdot \text{sinc}^2\left(\frac{d \pi}{\lambda} \sin(\theta)\right)",
        )

        # Position equation on the screen
        equation.scale(0.75)
        equation.to_edge(UL, buff=0.5)

        self.play(DrawBorderThenFill(axes), Write(axis_labels), Write(equation), run_time=1)
        self.play(Create(graph), Create(graph2), run_time=1)

        
if __name__ == "__main__":
    print("hello")
    for i in range(0, 1000):
        print(I(i/1000))