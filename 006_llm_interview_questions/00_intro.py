import manim as mn

# Configure for vertical 9:16 format
mn.config.pixel_width = 1080
mn.config.pixel_height = 1920
mn.config.frame_width = 9
mn.config.frame_height = 16


class LLMInterviewIntro(mn.Scene):
    def setup(self):
        self.camera.background_color = mn.DARK_BLUE

        # Create the grid background like other scenes
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
        # Question text - positioned first to determine alignment
        question_text = mn.Text(
            "Question:\nHow do top-k and top-p sampling\ndiffer in text generation?",
            font_size=40,  # Reduced from 48
            color=mn.YELLOW,
            line_spacing=1.3,
        )
        question_text.move_to([0, -4, 0])

        # Main title - aligned with question text
        main_title = mn.Text(
            "50 LLM Interview\nQuestions", font_size=40, color=mn.YELLOW, line_spacing=1.2
        )  # Reduced from 48
        main_title.align_to(question_text, mn.LEFT)
        main_title.move_to([main_title.get_x(), 4, 0])

        # Part number - aligned with question text
        part_text = mn.Text("Part 12", font_size=40, color=mn.YELLOW)  # Reduced from 48
        part_text.align_to(question_text, mn.LEFT)
        part_text.move_to([part_text.get_x(), 0, 0])

        # Animate the intro elements
        self.play(mn.Write(main_title), run_time=1.5)
        self.wait(0.5)

        self.play(mn.FadeIn(part_text), run_time=1)
        self.wait(0.5)

        self.play(mn.Write(question_text), run_time=2)
        self.wait(2)

        # Fade out all elements
        self.play(mn.FadeOut(main_title), mn.FadeOut(part_text), mn.FadeOut(question_text), run_time=1)
        self.wait(0.5)


if __name__ == "__main__":
    scene = LLMInterviewIntro()
    scene.render()
