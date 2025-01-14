from manim import *

class AutocorrelationDemo(Scene):
    def construct(self):
        # Time range
        time_range = np.linspace(-5, 5, 500)

        # Pulse parameters
        omega_c = 2 * PI  # Carrier frequency
        envelope = lambda t: np.exp(-t**2)  # Gaussian envelope A(t)
        pulse = lambda t: envelope(t) * np.cos(omega_c * t)  # E(t) = A(t) * cos(ω_c * t)

        # Autocorrelation function
        def autocorrelation(tau):
            return np.trapz(pulse(time_range) * pulse(time_range - tau), time_range)

        # Axes for pulse plot (scaled down vertically)
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2, 2, 0.5],
            x_length=10,
            y_length=3,  # Reduced height
            axis_config={"color": BLUE},
        ).to_edge(UP, buff=0.2)  # Minimal spacing from the top edge

        # Pulse and delayed pulse graphs
        pulse_graph = axes.plot(pulse, color=YELLOW, x_range=[-5, 5])
        delayed_graph = axes.plot(lambda t: pulse(t - 0), color=GREEN, x_range=[-5, 5])
        delayed_graph.set_opacity(0)

        # Axes for autocorrelation plot (scaled down vertically)
        autocorr_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 1.5, 0.5],
            x_length=10,
            y_length=2,  # Reduced height
            axis_config={"color": BLUE},
        ).next_to(axes, DOWN, buff=0.3)  # Reduced spacing between plots

        autocorr_graph = autocorr_axes.plot(
            lambda tau: autocorrelation(tau),
            x_range=[-5, 5],
            color=RED,
        )
        autocorr_graph.set_opacity(0)

        # Labels for graphs
        pulse_label = axes.get_graph_label(pulse_graph, label="Pulse", x_val=-4, direction=UP)
        delayed_label = axes.get_graph_label(delayed_graph, label="Delayed Pulse", x_val=4, direction=UP)
        autocorr_label = autocorr_axes.get_graph_label(autocorr_graph, label="Autocorrelation", x_val=4, direction=UP)

        # Add components to the scene
        self.play(Create(axes),
                  Create(autocorr_axes),
                  Create(autocorr_graph),
        )
        self.play(
                  Write(pulse_label),
                  Create(delayed_graph),
                  Write(delayed_label),
                  Write(autocorr_label)
        )
        self.play(Create(pulse_graph))

        # Animate delay τ and update the delayed pulse
        delayed_graph.set_opacity(1)
        autocorr_graph.set_opacity(1)
        for tau in np.linspace(-5, 7, 100):
            delayed_graph.become(axes.plot(lambda t: pulse(t - tau), color=GREEN, x_range=[max(-5, tau-2.5), min(5, tau+2.5)]))
            autocorr_graph.become(autocorr_axes.plot(lambda t: autocorrelation(t), color=RED, x_range=[-5, min(5, tau)]))
            self.wait(0.1)

        self.wait(1)
