import manim as mn


class AttentionVisual(mn.Scene):
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
        # Create Text objects for the sentence
        sentence = mn.VGroup(
            mn.Text("The"), mn.Text("cat"), mn.Text("chased"), mn.Text("the"), mn.Text("mouse")
        ).arrange(mn.RIGHT, buff=0.4, aligned_edge=mn.DOWN)

        # Position the sentence in the middle of the screen
        sentence.move_to(mn.ORIGIN)

        # Show the sentence
        self.play(mn.Write(sentence))
        self.wait(1)

        # Words to be highlighted
        cat = sentence[1]
        chased = sentence[2]
        mouse = sentence[4]

        # Highlight "cat"
        self.play(cat.animate.set_color(mn.YELLOW))
        box_cat = mn.SurroundingRectangle(cat, color=mn.YELLOW, buff=0.1)
        self.play(mn.Create(box_cat))
        self.wait(0.5)

        # Highlight "chased" and draw arrow from "cat"
        self.play(chased.animate.set_color(mn.YELLOW))
        box_chased = mn.SurroundingRectangle(chased, color=mn.YELLOW, buff=0.1)
        self.play(mn.Create(box_chased))

        arrow_cat_to_chased = mn.CurvedArrow(box_cat.get_top(), box_chased.get_top(), radius=-2, color=mn.RED)
        self.play(mn.Create(arrow_cat_to_chased))
        self.wait(0.5)

        # Highlight "mouse" and draw arrow from "chased"
        self.play(mouse.animate.set_color(mn.YELLOW))
        box_mouse = mn.SurroundingRectangle(mouse, color=mn.YELLOW, buff=0.1)
        self.play(mn.Create(box_mouse))

        arrow_chased_to_mouse = mn.CurvedArrow(box_chased.get_top(), box_mouse.get_top(), radius=-2, color=mn.RED)
        self.play(mn.Create(arrow_chased_to_mouse))

        self.wait(2)
