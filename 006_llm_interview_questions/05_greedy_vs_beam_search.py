import manim as mn
import numpy as np


class GreedyVsBeamSearch(mn.Scene):
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

    def create_token_bubble(self, text, color=mn.WHITE):
        """Create a glowing token bubble with text inside."""
        bubble = mn.Circle(radius=0.5, color=color, fill_opacity=0.4, stroke_width=2)
        text_mob = mn.Text(text, font_size=24, color=color)
        text_mob.move_to(bubble.get_center())
        return mn.VGroup(bubble, text_mob)

    def create_path(self, start, end, color=mn.WHITE):
        """Create a glowing path between two points."""
        path = mn.Line(start=start, end=end, color=color, stroke_width=2)
        return path

    def construct(self):
        # Create labels
        greedy_label = mn.Text("Greedy", font_size=48).to_edge(mn.UP).shift(mn.LEFT * 4)
        beam_label = mn.Text("Beam Search", font_size=48).to_edge(mn.UP).shift(mn.RIGHT * 4)

        self.play(mn.Write(greedy_label), mn.Write(beam_label))
        self.wait()

        # Greedy side setup
        greedy_tokens = []
        greedy_paths = []

        # Create initial token
        the_token = self.create_token_bubble("The", mn.WHITE)
        the_token.next_to(greedy_label, mn.DOWN, buff=0.5)
        greedy_tokens.append(the_token)

        self.play(mn.FadeIn(the_token))
        self.wait()

        # Add "cat" token
        cat_token = self.create_token_bubble("cat", mn.WHITE)
        cat_token.next_to(the_token, mn.DOWN, buff=0.5)
        greedy_tokens.append(cat_token)

        # Create path from "The" to "cat"
        path1 = self.create_path(the_token.get_bottom(), cat_token.get_top(), mn.WHITE)
        greedy_paths.append(path1)

        self.play(mn.Create(path1), mn.FadeIn(cat_token))
        self.wait()

        # Add "slept" token
        slept_token = self.create_token_bubble("slept", mn.WHITE)
        slept_token.next_to(cat_token, mn.DOWN, buff=0.5)
        greedy_tokens.append(slept_token)

        # Create path from "cat" to "slept"
        path2 = self.create_path(cat_token.get_bottom(), slept_token.get_top(), mn.WHITE)
        greedy_paths.append(path2)

        self.play(mn.Create(path2), mn.FadeIn(slept_token))
        self.wait()

        # Beam Search side setup
        beam_tokens = []
        beam_paths = []

        # Create initial token
        beam_the_token = self.create_token_bubble("The", mn.WHITE)
        beam_the_token.next_to(beam_label, mn.DOWN, buff=0.5)
        beam_tokens.append(beam_the_token)

        self.play(mn.FadeIn(beam_the_token))
        self.wait()

        # Add "cat" and "dog" tokens
        beam_cat_token = self.create_token_bubble("cat", mn.BLUE)
        beam_cat_token.next_to(beam_the_token, mn.DOWN, buff=0.5).shift(mn.LEFT * 1)
        beam_dog_token = self.create_token_bubble("dog", mn.GREEN)
        beam_dog_token.next_to(beam_the_token, mn.DOWN, buff=0.5).shift(mn.RIGHT * 1)
        beam_tokens.extend([beam_cat_token, beam_dog_token])

        # Create paths from "The" to both tokens
        beam_path1 = self.create_path(beam_the_token.get_bottom(), beam_cat_token.get_top(), mn.BLUE)
        beam_path2 = self.create_path(beam_the_token.get_bottom(), beam_dog_token.get_top(), mn.GREEN)
        beam_paths.extend([beam_path1, beam_path2])

        self.play(mn.Create(beam_path1), mn.Create(beam_path2), mn.FadeIn(beam_cat_token), mn.FadeIn(beam_dog_token))
        self.wait()

        # Add second level tokens for beam search
        beam_slept_token = self.create_token_bubble("slept", mn.BLUE)
        beam_slept_token.next_to(beam_cat_token, mn.DOWN, buff=0.5)
        beam_napped_token = self.create_token_bubble("napped", mn.BLUE)
        beam_napped_token.next_to(beam_cat_token, mn.DOWN, buff=0.5).shift(mn.LEFT * 1)
        beam_chased_token = self.create_token_bubble("chased", mn.BLUE)
        beam_chased_token.next_to(beam_cat_token, mn.DOWN, buff=0.5).shift(mn.RIGHT * 1)

        beam_ran_token = self.create_token_bubble("ran", mn.GREEN)
        beam_ran_token.next_to(beam_dog_token, mn.DOWN, buff=0.5)
        beam_played_token = self.create_token_bubble("played", mn.GREEN)
        beam_played_token.next_to(beam_dog_token, mn.DOWN, buff=0.5).shift(mn.RIGHT * 1)

        beam_tokens.extend([beam_slept_token, beam_napped_token, beam_chased_token, beam_ran_token, beam_played_token])

        # Create paths for second level
        beam_paths.extend(
            [
                self.create_path(beam_cat_token.get_bottom(), beam_slept_token.get_top(), mn.BLUE),
                self.create_path(beam_cat_token.get_bottom(), beam_napped_token.get_top(), mn.BLUE),
                self.create_path(beam_cat_token.get_bottom(), beam_chased_token.get_top(), mn.BLUE),
                self.create_path(beam_dog_token.get_bottom(), beam_ran_token.get_top(), mn.GREEN),
                self.create_path(beam_dog_token.get_bottom(), beam_played_token.get_top(), mn.GREEN),
            ]
        )

        self.play(*[mn.Create(path) for path in beam_paths[2:]], *[mn.FadeIn(token) for token in beam_tokens[3:]])
        self.wait()

        # Fade out less probable paths
        paths_to_fade = beam_paths[3:]  # Keep only the first two paths
        tokens_to_fade = beam_tokens[4:]  # Keep only the first three tokens

        self.play(
            *[mn.FadeOut(path, opacity=0.3) for path in paths_to_fade],
            *[mn.FadeOut(token, opacity=0.3) for token in tokens_to_fade],
        )
        self.wait()

        # Add final comparison text
        comparison_text = mn.Text("Beam Search: More Coherent, Natural Outputs", font_size=36).to_edge(mn.DOWN)

        self.play(mn.Write(comparison_text))
        self.wait(2)


if __name__ == "__main__":
    scene = GreedyVsBeamSearch()
    scene.render()
