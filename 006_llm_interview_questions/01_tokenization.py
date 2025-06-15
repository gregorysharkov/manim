import manim as mn


class Tokenization(mn.Scene):
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
        # Set seed for reproducibility
        mn.np.random.seed(0)

        # 1. word artificial should be in the center of the screen
        parts_data = {"art": mn.RED, "ific": mn.GREEN, "ial": mn.BLUE}

        text_mobjects = [mn.Text(text, font_size=48) for text in parts_data.keys()]
        original_word = mn.VGroup(*text_mobjects).arrange(mn.RIGHT, buff=0.1)
        original_word.move_to(mn.ORIGIN)

        self.play(mn.Write(original_word))
        self.wait()

        # 2. Then parts of the word change color
        animations = []
        for part, color in zip(original_word, parts_data.values()):
            animations.append(part.animate.set_color(color))
        self.play(mn.Succession(*animations, lag_ratio=0.5))
        self.wait()

        # 3. these parts get copied below with some spacing in between
        copied_parts = original_word.copy()

        target_position = copied_parts.copy().arrange(mn.RIGHT, buff=0.5).next_to(original_word, mn.DOWN, buff=1.5)

        self.play(mn.Transform(copied_parts, target_position))
        self.wait()

        # 4. Transform copied parts into matrices
        matrices = mn.VGroup()
        for part in copied_parts:
            matrix_data = mn.np.random.randint(-9, 10, size=(3, 1))
            matrix = mn.IntegerMatrix(matrix_data).scale(0.8)
            matrix.set_color(part.get_color())
            matrix.move_to(part)
            matrices.add(matrix)

        self.play(mn.Transform(copied_parts, matrices))
        self.wait()

        # Recenter the final group, which is now taller.
        final_group = mn.VGroup(original_word, copied_parts)
        self.play(final_group.animate.move_to(mn.ORIGIN))

        self.wait(2)
