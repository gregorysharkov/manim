import manim as mn
import numpy as np


class DecisionBlock(mn.VGroup):
    def __init__(self, decision_text: str, **kwargs):
        super().__init__(**kwargs)
        decision_box = mn.Square(
            side_length=2,
            fill_color=mn.LIGHT_GREY,
            fill_opacity=1,
            stroke_color=mn.BLACK,
        ).rotate(mn.PI / 4)
        text_block = mn.Text(decision_text, color=mn.BLACK)

        max_size = decision_box.width / np.sqrt(2) * 0.9

        # Scale the text to fit
        scaling_factor = min(max_size / text_block.width, max_size / text_block.height)
        text_block.scale(scaling_factor)

        self.add(decision_box, text_block)
