import manim as mn

BOX_HEIGHT = 1.2
BOX_WIDTH = 4.0
ARROW_WIDTH = 4.0
STROKE_BUFF = 0.05

class SeqToSeq(mn.Scene):
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
        # Create the main components

        # 1. Input sequence box
        input_text = mn.Text("I don't know", font_size=32, color=mn.WHITE)
        input_label = mn.Text("Input (EN)", font_size=20, color=mn.LIGHT_GREY)
        input_box = mn.RoundedRectangle(
            width=BOX_WIDTH,
            height=BOX_HEIGHT,
            corner_radius=0.1,
            stroke_color=mn.BLUE,
            stroke_width=2,
            fill_color=mn.DARK_BLUE,
            fill_opacity=0.8,
        )
        input_group = mn.VGroup(input_box, input_text)

        # 2. Encoder box
        encoder_text = mn.Text("Encoder", font_size=28, color=mn.WHITE)
        encoder_box = mn.RoundedRectangle(
            width=BOX_WIDTH,
            height=BOX_HEIGHT,
            corner_radius=0.1,
            stroke_color=mn.GREEN,
            stroke_width=2,
            fill_color=mn.GREEN_E,
            fill_opacity=0.8,
        )
        encoder_group = mn.VGroup(encoder_box, encoder_text)

        # 3. Intermediary state box (vector of float values)
        vector_values = mn.VGroup(
            mn.Text("0.23,", font_size=18, color=mn.WHITE),
            mn.Text("-0.45,", font_size=18, color=mn.WHITE),
            mn.Text("0.78,", font_size=18, color=mn.WHITE),
            mn.Text("0.12,", font_size=18, color=mn.WHITE),
            mn.Text("...", font_size=18, color=mn.WHITE),
        ).arrange(mn.RIGHT, buff=0.1)

        intermediary_label = mn.Text("Hidden State", font_size=20, color=mn.LIGHT_GREY)
        intermediary_box = mn.RoundedRectangle(
            width=BOX_WIDTH,
            height=BOX_HEIGHT,
            corner_radius=0.1,
            stroke_color=mn.YELLOW,
            stroke_width=2,
            fill_color=mn.DARK_BLUE,
            fill_opacity=0.8,
        )
        intermediary_group = mn.VGroup(
            intermediary_box, vector_values
        )

        # 4. Decoder box
        decoder_text = mn.Text("Decoder", font_size=28, color=mn.WHITE)
        decoder_box = mn.RoundedRectangle(
            width=BOX_WIDTH,
            height=BOX_HEIGHT,
            corner_radius=0.1,
            stroke_color=mn.RED,
            stroke_width=2,
            fill_color=mn.RED_E,
            fill_opacity=0.8,
        )
        decoder_group = mn.VGroup(decoder_box, decoder_text)

        # 5. Output sequence box
        output_text = mn.Text("Je ne sais pas", font_size=32, color=mn.WHITE)
        output_label = mn.Text("Output (FR)", font_size=20, color=mn.LIGHT_GREY)
        output_box = mn.RoundedRectangle(
            width=BOX_WIDTH,
            height=BOX_HEIGHT,
            corner_radius=0.1,
            stroke_color=mn.PURPLE,
            stroke_width=2,
            fill_color=mn.DARK_BLUE,
            fill_opacity=0.8,
        )
        output_group = mn.VGroup(output_box, output_text)

        # Position all elements vertically
        input_group.move_to(mn.UP * 3)
        input_label.next_to(input_group, mn.LEFT, buff=0.5)
        encoder_group.move_to(mn.UP * 1.5)
        intermediary_group.move_to(mn.ORIGIN)
        intermediary_label.next_to(intermediary_group, mn.LEFT, buff=0.5)
        decoder_group.move_to(mn.DOWN * 1.5)
        output_group.move_to(mn.DOWN * 3)
        output_label.next_to(output_group, mn.LEFT, buff=0.5)
        # Animation steps

        # Step 0: Input sequence, encoder and decoder appear (leaving space for other elements)
        self.play(mn.FadeIn(input_group), mn.FadeIn(encoder_group), mn.FadeIn(decoder_group), mn.Write(input_label), run_time=1.5)
        self.wait(0.5)

        # Step 1: Input text goes into encoder
        # Create an arrow from input to encoder
        arrow_input_to_encoder = mn.Arrow(
            start=input_group.get_bottom(), end=encoder_group.get_top(), color=mn.WHITE, stroke_width=ARROW_WIDTH, buff=STROKE_BUFF
        )

        self.play(mn.GrowArrow(arrow_input_to_encoder), input_text.animate.set_color(mn.BLUE), run_time=1.0)
        self.wait(0.5)

        # Step 2: The intermediary state appears
        arrow_encoder_to_intermediary = mn.Arrow(
            start=encoder_group.get_bottom(), end=intermediary_group.get_top(), color=mn.WHITE, stroke_width=ARROW_WIDTH, buff=STROKE_BUFF
        )

        self.play(mn.GrowArrow(arrow_encoder_to_intermediary), mn.FadeIn(intermediary_group), mn.Write(intermediary_label), run_time=1.5)
        self.wait(0.5)

        # Step 3: The intermediary state goes into decoder
        arrow_intermediary_to_decoder = mn.Arrow(
            start=intermediary_group.get_bottom(), end=decoder_group.get_top(), color=mn.WHITE, stroke_width=ARROW_WIDTH, buff=STROKE_BUFF
        )

        self.play(mn.GrowArrow(arrow_intermediary_to_decoder), vector_values.animate.set_color(mn.YELLOW), run_time=1.0)
        self.wait(0.5)

        # Step 4: The output sequence appears
        arrow_decoder_to_output = mn.Arrow(
            start=decoder_group.get_bottom(), end=output_group.get_top(), color=mn.WHITE, stroke_width=ARROW_WIDTH, buff=STROKE_BUFF
        )

        self.play(mn.GrowArrow(arrow_decoder_to_output), mn.FadeIn(output_group), mn.Write(output_label), run_time=1.5)
        self.wait(0.5)

        # Final highlight of the complete flow
        self.play(output_text.animate.set_color(mn.PURPLE), run_time=1.0)
        self.wait(2)


if __name__ == "__main__":
    scene = SeqToSeq()
    scene.render()