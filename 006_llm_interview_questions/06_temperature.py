import manim as mn
import numpy as np

TOKENS = [
    "blue",
    "azure",
    "vast",
    "boundless",
    "infinite",
]

TOKEN_LOGITS = [3.0, 2.8, 1.5, 1.3, 1.0]


class Temperature(mn.Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        title = mn.Text("The sky is", font_size=48)
        output_word = mn.Text("", font_size=48)  # Placeholder for now
        self.sentence = mn.VGroup(title, output_word).arrange(mn.RIGHT, buff=0.2).to_edge(mn.UP)
        self.temperature = 0.0
        self.token_logits_dict = self._update_logits(
            self.temperature, {token: logit for token, logit in zip(TOKENS, TOKEN_LOGITS)}
        )
        self.bars = self.render_bar_chart(self.temperature, self.token_logits_dict)

        # Temperature slider
        self.slider_group = mn.Group()
        self.slider_label = mn.Text("Temperature:", font_size=24)
        self.slider_value = mn.DecimalNumber(
            self.temperature,
            num_decimal_places=2,
            font_size=24,
        )
        self.slider_readout = (
            mn.Group(self.slider_label, self.slider_value).arrange(mn.RIGHT).next_to(self.slider_group, mn.UP)
        )

        self.slider = mn.NumberLine(
            x_range=[0, 5.01, 1],
            length=8,
            color=mn.LIGHT_GREY,
            label_direction=mn.DOWN,
            include_numbers=True,
            font_size=24,
        )
        self.slider_dot = mn.Dot(color=mn.YELLOW).move_to(self.slider.number_to_point(self.temperature))
        self.slider_group = mn.Group(self.slider, self.slider_readout, self.slider_dot).next_to(
            self.sentence, mn.DOWN, buff=0.5
        )

    def setup(self):
        self.camera.background_color = mn.DARK_BLUE

        # Create the grid
        grid = mn.VGroup()
        for i in range(-10, 11):
            h_line = mn.Line(
                start=mn.LEFT * 10 + mn.UP * i,
                end=mn.RIGHT * 10 + mn.UP * i,
                stroke_width=0.5,
                color=mn.LIGHT_GREY,
            ).set_opacity(0.5)
            v_line = mn.Line(
                start=mn.LEFT * i + mn.UP * 10,
                end=mn.LEFT * i + mn.DOWN * 10,
                stroke_width=0.5,
                color=mn.LIGHT_GREY,
            ).set_opacity(0.5)
            grid.add(h_line, v_line)
        self.add(grid)

    def construct(self):
        # Temperature value
        self.temperature = 0.3

        # --- Animation ---
        self.play(mn.Write(self.sentence), mn.FadeIn(self.slider_group))
        self.wait(1)

        self.bars.next_to(self.slider_group, mn.DOWN, buff=0.5)
        self.play(mn.FadeIn(self.bars))
        self.wait(1)

        for temp in np.arange(0.0, 5.01, 0.6):
            self.animate_slider_change(temp)

        self.animate_slider_change(0.7)
        self.wait(1)
        self.animate_word_selection()
        self.wait(1)

        new_word = mn.Text("azure", font_size=48).next_to(self.sentence[0], mn.RIGHT, buff=0.2)
        self.play(mn.Transform(self.bars[1][0], new_word))
        self.wait(1)
        self.play(mn.FadeOut(self.highlight_rect))
        self.wait(1)

    def animate_slider_change(self, new_temp: float):
        new_bars = self.render_bar_chart(new_temp, self.token_logits_dict)
        new_bars.next_to(self.slider_group, mn.DOWN, buff=0.5)
        old_bars = self.bars
        self.play(
            self.slider_value.animate.set_value(new_temp),
            self.slider_dot.animate.move_to(self.slider.number_to_point(new_temp)),
            mn.ReplacementTransform(old_bars, new_bars),
        )
        self.bars = new_bars

    def render_bar_chart(self, temp: float, token_logits: dict[str, float]) -> mn.VGroup:
        logits = self._update_logits(temp, token_logits)

        # Sort tokens by logit value, descending
        sorted_logits = sorted(logits.items(), key=lambda item: item[1], reverse=True)

        bars = mn.VGroup()
        for token, logit in sorted_logits:
            bar = mn.Rectangle(width=logit, height=0.5, fill_color=mn.BLUE, fill_opacity=0.5, stroke_width=0)
            label = mn.Text(token, font_size=24).next_to(bar, mn.RIGHT, buff=0.2)
            bar_group = mn.VGroup(label, bar)  # Use Group for easier handling
            bars.add(bar_group)

        bars.arrange(mn.DOWN, aligned_edge=mn.LEFT, buff=0.3)
        return bars

    def _update_logits(self, temp: float, token_logits: dict[str, float]) -> dict[str, float]:
        """update the logits for a given temperature"""
        mean_logit = np.mean(list(token_logits.values()))
        interpolation_factor = temp / 5.0
        return {token: logit + (mean_logit - logit) * interpolation_factor for token, logit in token_logits.items()}

    def animate_word_selection(self):
        self.highlight_rect = None
        np.random.seed(42)
        # To sample from a range without replacement, you can use
        # np.random.permutation to get all items in a random order.
        iteration_indices = [0, *np.random.permutation(len(self.bars)), 1]
        for i in iteration_indices:
            target_bar = self.bars[i]
            new_highlight_rect = mn.SurroundingRectangle(target_bar, color=mn.YELLOW, buff=0.1)

            if self.highlight_rect is None:
                self.play(mn.Create(new_highlight_rect))
            else:
                self.play(mn.ReplacementTransform(self.highlight_rect, new_highlight_rect))

            self.highlight_rect = new_highlight_rect
            self.wait(0.2)


if __name__ == "__main__":
    scene = Temperature()
    scene.render()
