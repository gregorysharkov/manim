import manim as mn


class MaskedModeling(mn.Scene):
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
        # Create the original sentence
        words = ["The", "quick", "brown", "cat", "jumped", "over", "the", "lazy", "dog."]
        word_objects = []

        for word in words:
            word_obj = mn.Text(word.upper(), font_size=32, color=mn.WHITE)
            word_objects.append(word_obj)

        # Arrange words in a sentence with proper alignment
        sentence = (
            mn.VGroup(*word_objects)
            .arrange(mn.RIGHT, buff=0.3)
            .move_to(mn.ORIGIN)
        )

        # Show the original sentence
        self.play(mn.Write(sentence))
        self.wait(1)

        # Create new sentence with <MASK> instead of "cat"
        masked_words = ["The", "quick", "brown", "<MASK>", "jumped", "over", "the", "lazy", "dog."]
        masked_word_objects = []

        for i, word in enumerate(masked_words):
            if word == "<MASK>":
                word_obj = mn.Text(word.upper(), font_size=32, color=mn.RED)
            else:
                word_obj = mn.Text(word.upper(), font_size=32, color=mn.WHITE)
            masked_word_objects.append(word_obj)

        # Arrange the new sentence with proper spacing
        masked_sentence = (
            mn.VGroup(*masked_word_objects)
            .arrange(mn.RIGHT, buff=0.3)
            .move_to(mn.ORIGIN)
        )

        # Transform to the masked sentence
        self.play(mn.Transform(sentence, masked_sentence))
        self.wait(1)

        # Get the mask token for arrow targeting
        mask_token = masked_word_objects[3]  # "<MASK>" is at index 3

        # Create arched arrows from surrounding words to the mask
        # Words that will point to the mask: quick, jumped, over, lazy, dog
        arrow_indices = [1, 4, 5, 7, 8]  # quick, jumped, over, lazy, dog

        arrows = mn.VGroup()
        for i in arrow_indices:
            source_word = masked_word_objects[i]

            # Get the top middle points of source and target
            start_point = source_word.get_bottom() if i < 3 else source_word.get_top()
            end_point = mask_token.get_bottom() if i < 3 else mask_token.get_top()

            # Create arched arrow
            arrow = mn.CurvedArrow(
                start_point=start_point,
                end_point=end_point,
                color=mn.YELLOW,
                stroke_width=3,
                angle=mn.TAU / 4,  # Creates a nice arch
            )
            arrows.add(arrow)

        # Show arrows pointing to the mask
        self.play(mn.Create(arrows))
        self.wait(1)

        # Add a title to explain what's happening
        title = mn.Text("Predicting masked word from context", font_size=36, color=mn.BLUE)
        title.to_edge(mn.UP)
        self.play(mn.Write(title))
        self.wait(1)

        # Create final sentence with CAT prediction
        final_words = ["The", "quick", "brown", "CAT", "jumped", "over", "the", "lazy", "dog."]
        final_word_objects = []

        for i, word in enumerate(final_words):
            if word == "CAT":
                word_obj = mn.Text(word.upper(), font_size=32, color=mn.GREEN)
            else:
                word_obj = mn.Text(word.upper(), font_size=32, color=mn.WHITE)
            final_word_objects.append(word_obj)

        # Arrange the final sentence
        final_sentence = (
            mn.VGroup(*final_word_objects)
            .arrange(mn.RIGHT, buff=0.3)
            .move_to(mn.ORIGIN)
        )

        # Transform to the final sentence and fade out arrows
        self.play(mn.Transform(sentence, final_sentence), mn.FadeOut(arrows))
        self.wait(1)

        # Final highlight of the predicted word
        predicted_word = final_word_objects[3]  # "CAT" is at index 3
        highlight = mn.SurroundingRectangle(predicted_word, color=mn.GREEN, buff=0.1)
        self.play(mn.Create(highlight))
        self.wait(2)

        # Fade out everything
        self.play(mn.FadeOut(mn.VGroup(sentence, title, highlight)))
        self.wait(1)


if __name__ == "__main__":
    scene = MaskedModeling()
    scene.render()
