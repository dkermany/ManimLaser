from manim import *

from manim.typing import Image
from manim.utils.color.X11 import BEIGE, VIOLET
from manim.utils.color.XKCD import BLUEGREEN


class Comparison(Scene):
    COLORS = {
        "wave1": BEIGE,
        "wave2": BLUEGREEN,
        "wave3": VIOLET,
        "interference": BLUE,
        "constructive": GREEN,
        "destructive": RED,
        "axes": WHITE
    }

    def define_wave(self, amplitude, frequency):
        return lambda t: amplitude * np.sin(2 * PI * frequency * t)

    def construct(self):
        # Create the body of the laser pointer using a rounded rectangle.
        laser_pointer = RoundedRectangle(width=0.75, height=0.25, corner_radius=0.05, fill_color=GRAY, fill_opacity=1)
        
        
        # Move the entire pointer to the left side.
        laser_pointer.move_to(LEFT * 4)
        
        # Create the laser beam as a thick red line.
        laser_beam = Line(
            start=laser_pointer.get_right(),
            end=laser_pointer.get_right() + RIGHT * 7.7,
            color=RED
        )
        laser_beam.set_stroke(width=8)
        glow = laser_beam.copy().set_stroke(width=20, opacity=0.3)
        laser_group = VGroup(laser_beam, glow)

        sec_text = Tex(r"1 second laser pulse")
        sec_dist_text = Tex(r"$\approx$ 0.77 earth-moon distance")
        sec_text.move_to((UP * 3) + (LEFT * 1))
        sec_dist_text.move_to((UP * 2.5) + (LEFT * 0.1))
        
        self.play(
            FadeIn(laser_pointer),
            Write(sec_text),
        )
        self.play(
            Create(laser_group, run_time=1, lag_ratio=0),
            rate_func=linear,
        )
        self.play(
            laser_pointer.animate.shift(LEFT*4).set_run_time(1),
            rate_func=linear,
        )
        laser_pointer.remove()
        
        self.wait(1)

        self.play(laser_group.animate.shift(DOWN * 1))

        brace = Brace(laser_beam, direction=DOWN) # type: ignore
        distance_label = brace.get_text("299,792,458 meters")

        moon = ImageMobject("media/images/manim_comparison/moon.jpg")
        earth = ImageMobject("media/images/manim_comparison/earth.jpg")

        earth.scale(0.8)
        moon.scale(0.2)
        self.remove(earth)
        self.remove(moon)
        self.mobjects.insert(0, earth)
        self.mobjects.insert(0, moon)

        moon.move_to(laser_group.get_right() + (UP * 1.5) + (RIGHT * 3))
        earth.move_to(laser_group.get_left() + (UP * 1.5) + (LEFT * 3))
        
        self.play(
            FadeIn(earth),
            FadeIn(moon),
            GrowFromCenter(brace),
            Write(sec_dist_text, run_time=1),
        )
        self.play(Write(distance_label))
        self.wait(2)

        self.play(
            FadeOut(
                earth,
                moon,
                sec_dist_text,
                sec_text
            )
        )

        millisec_text = Tex(r"1 millisecond laser pulse")
        millisec_dist_text = Tex(r"$\approx$ Houston-San Antonio distance")
        millisec_text.move_to((UP * 3) + (LEFT * 1))
        millisec_dist_text.move_to((UP * 2.5) + (LEFT * 0.1))

        # Create the laser beam as a thick red line.
        milli_laser_beam = Line(
            start=laser_beam.get_left(),
            end=laser_beam.get_left() + RIGHT * 7.7/1000,
            color=RED
        )
        milli_laser_beam.set_stroke(width=8)
        milli_glow = milli_laser_beam.copy().set_stroke(width=20, opacity=0.3)
        milli_laser_group = VGroup(milli_laser_beam, milli_glow)

        target_point = laser_beam.point_from_proportion(0.001)
        arrow = Arrow(start=target_point + DOWN, end=target_point, buff=0.1)
        arrow_text = Tex(r"299,792 meters").next_to(arrow.get_start(), DOWN, buff=0.2)
        
        distance_label_divided = Tex(r"299,792,458 meters / 1000").move_to(distance_label.get_left())
        distance_label_converted = Tex(r"$\approx$299,792 meters").next_to(arrow.get_start(), DOWN, buff=0.2)
        
        self.play(Write(millisec_text))
        self.play(Transform(distance_label, distance_label_divided))
        self.play(Transform(brace, arrow), distance_label_divided.animate.next_to(arrow.get_start(), DOWN, buff=0.2))
        self.play(Transform(distance_label_divided, distance_label_converted))

        self.play(GrowArrow(arrow), Transform(distance_label, arrow_text))
        self.play(Transform(laser_group, milli_laser_group), run_time=1)

        self.wait(1)

        self.play(Transform(milli_laser_group, laser_group), Transform(arrow, brace))

        self.wait(2)
        
