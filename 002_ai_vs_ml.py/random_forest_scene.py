import manim as mn
from blocks import InputBlock, OutputBlock, DecisionBlock, create_elbow_arrow


class MiniTree(mn.VGroup):
    def __init__(self, decision_settings: dict, output_settings: dict, **kwargs):
        """
        Args:
            decision_blocks (dict): A dictionary mapping decision block names to their respective colors.
            output_blocks (dict): A dictionary mapping output block names to their respective colors.
        """
        super().__init__(**kwargs)
        self.input_block = InputBlock("Input")
        self.decision_blocks = [
            DecisionBlock(decision_text=name, fill_color=color)
            for name, color in decision_settings.items()
        ]
        self.output_blocks = [
            OutputBlock(input_text=name, fill_color=color)
            for name, color in output_settings.items()
        ]

        self.add(self.input_block, *self.decision_blocks, *self.output_blocks)

        # Arrange elements
        self._arrange_elements()

    def _arrange_elements(self):
        # Position input block at the top
        self.input_block.to_edge(mn.UP, buff=1)
        self.decision_blocks[0].next_to(self.input_block, mn.DOWN, buff=1)

        # Position output blocks
        self.output_blocks[0].next_to(self.decision_blocks[0], mn.DOWN + mn.LEFT, buff=1)
        self.output_blocks[1].next_to(self.decision_blocks[0], mn.DOWN + mn.RIGHT, buff=1)

        # Create arrows
        self.arrows = []
        self._create_arrows()

    def _create_arrows(self):
        # Arrow from input to each decision block
        arrows = [
            create_elbow_arrow(self.input_block.get_bottom(), self.decision_blocks[0].get_top()),
            create_elbow_arrow(self.decision_blocks[0].get_left(), self.output_blocks[0].get_top()),
            create_elbow_arrow(self.decision_blocks[0].get_right(), self.output_blocks[1].get_top()),
        ]
        self.add(*arrows)


def calculate_scale_ratio(group, camera):
    """Calculate the scale ratio for the group without rearranging elements."""
    current_width = group.width
    current_height = group.height

    width_scale = (
        (camera.frame_width * 0.9) / current_width
        if current_width > camera.frame_width * 0.9
        else 1
    )
    height_scale = (
        (camera.frame_height * 0.9) / current_height
        if current_height > camera.frame_height * 0.9
        else 1
    )

    return min(width_scale, height_scale)


class RandomForestScene(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.BLUE_E

        decision_settings = {
            "Condition 1": mn.LIGHT_GRAY,
        }
        output_settings = {
            "Output 1": mn.RED,
            "Output 2": mn.GREEN,
        }

        forest = MiniTree(decision_settings, output_settings)
        scale_factor = calculate_scale_ratio(forest, self.camera)
        forest.scale(scale_factor)

        # Center the forest in the scene
        forest.move_to(self.camera.frame_center)

        self.play(mn.FadeIn(forest))
        self.wait(2)


if __name__ == "__main__":
    scene = RandomForestScene()
    scene.render()
