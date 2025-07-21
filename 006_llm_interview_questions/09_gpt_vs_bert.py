import manim as mn


class GPTvsBERT(mn.Scene):
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
        # Create split screen titles
        gpt_title = mn.Text("Autoregressive (GPT)", font_size=36, color=mn.YELLOW)
        bert_title = mn.Text("Masked (BERT)", font_size=36, color=mn.YELLOW)

        gpt_title.to_edge(mn.UP).shift(mn.UP * 0.25)
        bert_title.move_to(mn.ORIGIN).shift(mn.DOWN * 0.5)

        # Create horizontal dividing line
        divider = mn.Line(start=mn.LEFT * 6, end=mn.RIGHT * 6, stroke_width=2, color=mn.WHITE)

        # Show titles and divider
        self.play(mn.Write(gpt_title), mn.Write(bert_title), mn.Create(divider))
        self.wait(1)

        # GPT Side - Autoregressive generation
        gpt_words = ["The", "cat", "sat", "on", "the", "mat."]
        gpt_word_objects = []

        # Create word objects for GPT side
        for word in gpt_words:
            word_obj = mn.Text(word.upper(), font_size=28, color=mn.WHITE)
            gpt_word_objects.append(word_obj)

        # Position GPT words on the top half
        gpt_sentence = mn.VGroup(*gpt_word_objects).arrange(mn.RIGHT, buff=0.2).move_to(mn.UP * 1.5)

        # Show GPT words appearing one by one
        for i, word_obj in enumerate(gpt_word_objects):
            self.play(mn.Write(word_obj), run_time=0.5)

            # Add leftward arrows after each word (except the first)
            if i > 0:
                arrows = mn.VGroup()
                for j in range(i):
                    source_word = gpt_word_objects[j]
                    target_word = gpt_word_objects[i]

                    arrow = mn.CurvedArrow(
                        start_point=source_word.get_bottom(),
                        end_point=target_word.get_bottom(),
                        color=mn.GREEN,
                        stroke_width=2,
                        angle=mn.TAU / 6,
                    )
                    arrows.add(arrow)

                self.play(mn.Create(arrows), run_time=0.3)
                self.wait(0.2)
                self.play(mn.FadeOut(arrows), run_time=0.2)

            self.wait(0.3)

        # BERT Side - Masked modeling
        bert_words = ["The", "young", "<MASK>", "loves", "to", "play", "with", "a", "ball."]
        bert_word_objects = []

        # Create word objects for BERT side
        for i, word in enumerate(bert_words):
            if word == "<MASK>":
                word_obj = mn.Text(word.upper(), font_size=28, color=mn.RED)
            else:
                word_obj = mn.Text(word.upper(), font_size=28, color=mn.WHITE)
            bert_word_objects.append(word_obj)

        # Position BERT words on the bottom half
        bert_sentence = mn.VGroup(*bert_word_objects).arrange(mn.RIGHT, buff=0.2).move_to(mn.DOWN * 1.5)

        # Show BERT sentence all at once
        self.play(mn.Write(bert_sentence))
        self.wait(1)

        # Get the mask token for arrow targeting
        mask_token = bert_word_objects[2]  # "<MASK>" is at index 2

        # Create bidirectional arrows from all other words to the mask
        bert_arrows = mn.VGroup()
        for i, word_obj in enumerate(bert_word_objects):
            if i != 2:  # Skip the mask token itself
                start_point = word_obj.get_bottom() if i < 2 else word_obj.get_top()
                end_point = mask_token.get_bottom() if i < 2 else mask_token.get_top()

                arrow = mn.CurvedArrow(
                    start_point=start_point,
                    end_point=end_point,
                    color=mn.BLUE,
                    stroke_width=2,
                    angle=mn.TAU / 8 if abs(i - 2) > 2 else mn.TAU / 10,
                )
                bert_arrows.add(arrow)

        # Show arrows pointing to the mask
        self.play(mn.Create(bert_arrows))
        self.wait(1)

        # Replace mask with predicted word
        predicted_word = mn.Text("CAT", font_size=28, color=mn.GREEN)
        predicted_word.move_to(mask_token.get_center())

        # Transform mask to prediction and fade out arrows
        self.play(mn.Transform(mask_token, predicted_word), mn.FadeOut(bert_arrows))
        self.wait(1)

        # Add explanatory text
        gpt_explanation = mn.Text(
            "Sequential prediction\n(left-to-right context)", font_size=20, color=mn.LIGHT_GREY
        ).move_to(mn.UP * 2.5)

        bert_explanation = mn.Text(
            "Bidirectional context\n(surrounding words)", font_size=20, color=mn.LIGHT_GREY
        ).move_to(mn.DOWN * 2.5)

        self.play(mn.Write(gpt_explanation), mn.Write(bert_explanation))
        self.wait(2)

        # Fade out everything
        self.play(
            mn.FadeOut(
                mn.VGroup(
                    gpt_title, bert_title, divider, gpt_sentence, bert_sentence, gpt_explanation, bert_explanation
                )
            )
        )
        self.wait(1)


if __name__ == "__main__":
    scene = GPTvsBERT()
    scene.render()
