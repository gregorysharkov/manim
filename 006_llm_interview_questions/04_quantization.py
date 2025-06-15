import manim as mn
import numpy as np
import math

np.random.seed(42)


class WeightQuantizationScene(mn.Scene):
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
        # Create the weight values with different precisions
        w_64 = np.float64(math.pi)
        w_32 = np.float32(math.pi)
        w_16 = np.float16(math.pi)

        # Create the initial weight display
        w_64_text = mn.MathTex(f"W64_{{11}} = {w_64:.32f}", color=mn.WHITE).scale(0.8).to_edge(mn.UP)
        rounded_32_text = mn.MathTex(f"W32_{{q11}} = {w_32:.32f}", color=mn.WHITE).scale(0.8).next_to(w_64_text, mn.DOWN, buff=0.5)
        clear_32_text = mn.MathTex(f"W32_{{q11}} = {w_32:.16f}", color=mn.WHITE).scale(0.8).next_to(w_64_text, mn.DOWN, buff=0.5)
        rounded_16_text = mn.MathTex(f"W16_{{q11}} = {w_16:.16f}", color=mn.WHITE).scale(0.8).next_to(clear_32_text, mn.DOWN, buff=0.5)
        clear_16_text = mn.MathTex(f"W16_{{q11}} = {w_16:.8f}", color=mn.WHITE).scale(0.8).next_to(clear_32_text, mn.DOWN, buff=0.5)


        texts = mn.VGroup(w_64_text, rounded_32_text, clear_32_text, rounded_16_text, clear_16_text).arrange(mn.DOWN, buff=0.5, aligned_edge=mn.LEFT)

        self.play(
            mn.Write(w_64_text),
        )
        self.wait(1)
        self.play(
            mn.Write(rounded_32_text),
        )
        self.wait(1)
        self.play(
            mn.Transform(rounded_32_text, clear_32_text),
        )
        self.wait(1)
        self.play(
            mn.Write(rounded_16_text),
        )
        self.wait(1)
        self.play(
            mn.Transform(rounded_16_text, clear_16_text),
        )
        self.wait(1)

if __name__ == "__main__":
    scene = WeightQuantizationScene()
    scene.render()
