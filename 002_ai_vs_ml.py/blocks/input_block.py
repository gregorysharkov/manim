import manim as mn


class InputBlock(mn.VGroup):
    def __init__(self, input_text: str, fill_color=mn.LIGHT_GREY, **kwargs):
        super().__init__(**kwargs)
        input_box = mn.RoundedRectangle(
            width=4,
            height=2,
            corner_radius=0.5,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_color=mn.BLACK,
        )
        input_block = mn.Text(input_text, color=mn.BLACK)
        self.add(input_box, input_block)


class OutputBlock(InputBlock):
    def __init__(self, input_text, fill_color=mn.LIGHT_GREY, **kwargs):
        super().__init__(input_text, fill_color=fill_color, **kwargs)
