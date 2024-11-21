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


def calculate_scale_ratio(groups, camera, horizontal_buff=1, margin=0.9):
    """
    Calculate the scale ratio for multiple groups arranged horizontally.

    Args:
    groups (list): List of VGroup objects to be scaled and arranged.
    camera: The camera object of the scene.
    horizontal_buff (float): Buffer space between groups.
    margin (float): Margin factor for the camera frame (0.9 means 90% of the frame will be used).

    Returns:
    tuple: (scale_factor, arranged_group)
    """
    combined_group = mn.Group(*groups)
    combined_group.arrange(mn.RIGHT, buff=horizontal_buff)

    width_scale = (camera.frame_width * margin) / combined_group.width
    height_scale = (camera.frame_height * margin) / combined_group.height
    scale_factor = min(width_scale, height_scale)

    return scale_factor, combined_group


class RandomForestScene(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.BLUE_E

        # Create two sets of settings for two different trees
        decision_settings1 = {
            "Condition 1": mn.LIGHT_GRAY,
        }
        output_settings1 = {
            "Output 1": mn.RED,
            "Output 2": mn.GREEN,
        }

        decision_settings2 = {
            "Condition 2": mn.YELLOW_E,
        }
        output_settings2 = {
            "Output 3": mn.BLUE,
            "Output 4": mn.PURPLE,
        }

        # Create two forests
        forest1 = MiniTree(decision_settings1, output_settings1)
        forest2 = MiniTree(decision_settings2, output_settings2)

        # Calculate scale factor and get the arranged group
        scale_factor, arranged_group = calculate_scale_ratio(
            [forest1, forest2], self.camera
        )

        # Apply scaling to the arranged group
        arranged_group.scale(scale_factor)

        # Center the arranged group in the scene
        arranged_group.move_to(self.camera.frame_center)

        # Animate the appearance of both forests in parallel
        self.play(
            mn.AnimationGroup(mn.FadeIn(forest1), mn.FadeIn(forest2), lag_ratio=0.2)
        )
        self.wait(2)

        # Example animations to demonstrate the trees working in parallel
        self.play(
            forest1.decision_blocks[0].animate.set_fill(mn.YELLOW),
            forest2.decision_blocks[0].animate.set_fill(mn.GREEN),
        )
        self.wait(1)
        self.play(
            forest1.output_blocks[0].animate.scale(1.2),
            forest2.output_blocks[1].animate.scale(1.2),
        )
        self.wait(2)


if __name__ == "__main__":
    scene = RandomForestScene()
    scene.render()
