import manim as mn
from blocks import InputBlock, OutputBlock, DecisionBlock, create_elbow_arrow


class MiniTree(mn.VGroup):
    def __init__(
        self, decision_settings: dict, output_settings: dict, caption: str, **kwargs
    ):
        """
        Args:
            decision_blocks (dict): A dictionary mapping decision block names to their respective colors.
            output_blocks (dict): A dictionary mapping output block names to their respective colors.
            caption (str): The caption for the mini tree.
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
        self.caption_block = mn.Text(caption, font_size=48)
        self.add(
            self.input_block,
            *self.decision_blocks,
            *self.output_blocks,
            self.caption_block,
        )
        # Arrange elements
        self._arrange_elements()

    def _arrange_elements(self):
        # Position input block at the top
        self.input_block.to_edge(mn.UP, buff=1)
        self.decision_blocks[0].next_to(self.input_block, mn.DOWN, buff=1)

        # Position output blocks
        self.output_blocks[0].next_to(
            self.decision_blocks[0], mn.DOWN + mn.LEFT, buff=1
        )
        self.output_blocks[1].next_to(
            self.decision_blocks[0], mn.DOWN + mn.RIGHT, buff=1
        )

        # Position caption block
        self.caption_block.next_to(
            mn.VGroup(self.output_blocks[0], self.output_blocks[1]),
            mn.DOWN,
            buff=0.5,
        )

        # Create arrows
        self.arrows = []
        self._create_arrows()

    def _create_arrows(self):
        # Arrow from input to each decision block
        arrows = [
            create_elbow_arrow(
                self.input_block.get_bottom(), self.decision_blocks[0].get_top()
            ),
            create_elbow_arrow(
                self.decision_blocks[0].get_left(), self.output_blocks[0].get_top()
            ),
            create_elbow_arrow(
                self.decision_blocks[0].get_right(), self.output_blocks[1].get_top()
            ),
        ]
        self.arrows = arrows
        self.add(*self.arrows)


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
            "Is it soft?": mn.LIGHT_GRAY,
        }
        output_settings1 = {
            "Ripe": mn.RED,
            "Perfect": mn.GREEN,
        }

        decision_settings2 = {
            "Is it sweet?": mn.LIGHT_GRAY,
        }
        output_settings2 = {
            "Perfect": mn.GREEN,
            "Unripe": mn.ORANGE,
        }

        decision_settings3 = {
            "Is it ripe": mn.LIGHT_GRAY,
        }
        output_settings3 = {
            "Ripe": mn.RED,
            "Unripe": mn.ORANGE,
        }
        forest1 = MiniTree(
            decision_settings1, output_settings1, "Tree 1: Softness Check"
        )
        forest2 = MiniTree(
            decision_settings2, output_settings2, "Tree 2: Sweetness Check"
        )
        forest3 = MiniTree(decision_settings3, output_settings3, "Tree 3: Ripe check")

        scale_factor, arranged_group = calculate_scale_ratio(
            [forest1, forest2, forest3], self.camera
        )

        arranged_group.scale(scale_factor)
        arranged_group.move_to(self.camera.frame_center)

        self.play(
            mn.AnimationGroup(
                mn.FadeIn(forest1),
                mn.FadeIn(forest2),
                mn.FadeIn(forest3),
                lag_ratio=0.2,
            )
        )

        self.wait(1)
        new_input = InputBlock("New Input", fill_color=mn.ORANGE)
        new_input.move_to(forest2.get_top() + mn.UP * 1.5)
        new_input.scale(scale_factor * 1.25)

        self.play(mn.FadeIn(new_input))

        self.wait(1)

        output_1 = self._animate_tree(new_input, forest1)
        output_2 = self._animate_tree(new_input, forest2)
        output_3 = self._animate_tree(new_input, forest3)

        final_output = OutputBlock("Final output")
        final_output.next_to(forest2, mn.DOWN, buff=.5)
        final_output.scale(scale_factor=new_input.height / final_output.height)
        self.play(mn.FadeIn(final_output))

        self.play(
            output_1.copy().animate.move_to(final_output).scale(scale_factor=output_1.height / final_output.height),
            output_2.copy().animate.move_to(final_output).scale(scale_factor=output_2.height / final_output.height),
            output_3.copy().animate.move_to(final_output).scale(scale_factor=output_3.height / final_output.height),
        )

    def _animate_tree(self, new_input: InputBlock, tree: MiniTree) -> OutputBlock:
        new_input_copy = new_input.copy()
        target_scale = tree.input_block.height / new_input_copy.height
        self.play(new_input_copy.animate.move_to(tree.input_block).scale(target_scale))

        input_to_decision_arrow = tree.arrows[0]
        self.play(input_to_decision_arrow.animate.set_color(mn.ORANGE))

        is_soft_block = tree.decision_blocks[0]
        self.play(
            is_soft_block[0].animate.set_fill(mn.ORANGE),
            is_soft_block[1].animate.set_color(mn.BLACK),
        )

        decision_to_perfect_arrow = tree.arrows[2]  # Assuming it's the third arrow
        self.play(decision_to_perfect_arrow.animate.set_color(mn.ORANGE))

        perfect_block = tree.output_blocks[1]
        self.play(perfect_block.animate.scale(1.3))

        self.wait(1)
        return perfect_block


if __name__ == "__main__":
    scene = RandomForestScene()
    scene.render()
