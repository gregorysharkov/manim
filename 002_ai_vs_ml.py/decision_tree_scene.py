import manim as mn

from blocks import InputBlock, OutputBlock, DecisionBlock, create_elbow_arrow


class DecisionTree(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.BLUE_E

        # Create elements
        new_input_block = InputBlock("New Fruit", fill_color=mn.YELLOW)
        input_block = InputBlock("Fruit")
        decision_block1 = DecisionBlock("Is it soft?", mn.LIGHT_GREY)
        decision_block2 = DecisionBlock("Is it sweet?", mn.LIGHT_GREY)
        decision_block3 = DecisionBlock("Is it sour?", mn.LIGHT_GREY)

        output_block1 = OutputBlock("Ripe", fill_color=mn.RED)
        output_block2 = OutputBlock("Perfect", fill_color=mn.GREEN)
        output_block3 = OutputBlock("Unripe", fill_color=mn.ORANGE)

        # Scale down elements if they're too large
        all_elements = mn.VGroup(
            new_input_block,
            input_block,
            decision_block1,
            decision_block2,
            decision_block3,
            output_block1,
            output_block2,
            output_block3,
        )
        all_elements.arrange(mn.DOWN, buff=0.5)

        if all_elements.height > self.camera.frame_height * 0.9:
            scale_factor = (self.camera.frame_height * 0.9) / all_elements.height
            all_elements.scale(scale_factor)

        # Position elements
        input_block.to_edge(mn.UP, buff=1)
        new_input_block.next_to(input_block, mn.LEFT, buff=2.2)
        decision_block1.next_to(input_block, mn.DOWN, buff=0.5)
        decision_block2.next_to(decision_block1, mn.DOWN + mn.LEFT, buff=1)
        decision_block3.next_to(decision_block1, mn.DOWN + mn.RIGHT, buff=1)

        # Position output blocks
        output_block1.next_to(decision_block2, mn.DOWN + mn.LEFT, buff=0.5)
        output_block3.next_to(decision_block3, mn.DOWN + mn.RIGHT, buff=0.5)

        # Calculate the vertical position for output_block2
        output_y = min(output_block1.get_y(), output_block3.get_y())

        # Position output_block2
        output_block2.next_to(decision_block1, mn.DOWN, buff=0.5)
        output_block2.set_y(output_y)

        # Create arrows
        arrows = [
            create_elbow_arrow(input_block.get_bottom(), decision_block1.get_top()),
            create_elbow_arrow(
                decision_block1.get_left(),
                decision_block2.get_top(),  # angle=mn.TAU / 4
            ),
            create_elbow_arrow(
                decision_block1.get_right(),
                decision_block3.get_top(),  # angle=-mn.TAU / 4
            ),
            create_elbow_arrow(
                decision_block2.get_left(),
                output_block1.get_top(),  # angle=mn.TAU / 4
            ),
            create_elbow_arrow(
                decision_block2.get_right(),
                output_block2.get_top(),  # angle=-mn.TAU / 4
            ),
            create_elbow_arrow(
                decision_block3.get_left(),
                output_block2.get_top(),  # angle=mn.TAU / 4
            ),
            create_elbow_arrow(
                decision_block3.get_right(),
                output_block3.get_top(),  # angle=-mn.TAU / 4
            ),
        ]

        # Animate
        self.play(mn.Write(input_block))
        self.play(mn.Create(arrows[0]), mn.Write(decision_block1))
        self.play(
            mn.Create(arrows[1]),
            mn.Create(arrows[2]),
            mn.Write(decision_block2),
            mn.Write(decision_block3),
        )
        self.play(
            *[mn.Create(arrow) for arrow in arrows[3:]],  # Create remaining arrows
            mn.Write(output_block1),
            mn.Write(output_block2),
            mn.Write(output_block3),
        )
        self.wait(2)

        self.play(mn.Write(new_input_block))
        self.wait(1)
        self.play(new_input_block.animate.move_to(input_block))
        self.wait(1)
        self.play(arrows[0].animate.set_color(mn.ORANGE))
        self.wait(0.5)
        self.play(
            decision_block1[0].animate.set_fill(mn.ORANGE),
            decision_block1[1].animate.set_color(mn.BLACK),
        )
        self.wait(0.5)
        self.play(arrows[2].animate.set_color(mn.ORANGE))
        self.play(
            decision_block3[0].animate.set_fill(mn.ORANGE),
            decision_block3[1].animate.set_color(mn.BLACK),
        )
        self.wait(0.5)
        self.play(arrows[6].animate.set_color(mn.ORANGE))
        self.wait(1)
        self.play(output_block3.animate.scale(1.5))
        self.wait(2)


if __name__ == "__main__":
    scene = DecisionTree()
    scene.render()
