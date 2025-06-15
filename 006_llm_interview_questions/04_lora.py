import manim as mn
import numpy as np

np.random.seed(42)


class NeuralNetworkScene(mn.Scene):
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
            # Create the neural network layers
            layer1 = mn.Circle(radius=0.3, color=mn.WHITE, fill_color=mn.WHITE, fill_opacity=1)
            layer2 = mn.VGroup(
                *[mn.Circle(radius=0.3, color=mn.WHITE, fill_color=mn.WHITE, fill_opacity=1) for _ in range(3)]
            ).arrange(mn.DOWN, buff=0.75)
            layer3 = mn.VGroup(
                *[mn.Circle(radius=0.3, color=mn.WHITE, fill_color=mn.WHITE, fill_opacity=1) for _ in range(2)]
            ).arrange(mn.DOWN, buff=0.75)

            # Position layers relative to each other
            layer2.next_to(layer1, mn.RIGHT, buff=1.5)
            layer3.next_to(layer2, mn.RIGHT, buff=1.5)

            # Create connections between layers
            connections = mn.VGroup()
            for node1 in [layer1]:
                for node2 in layer2:
                    line = mn.Line(node1.get_center(), node2.get_center(), color=mn.GREEN)
                    connections.add(line)

            for node1 in layer2:
                for node2 in layer3:
                    line = mn.Line(node1.get_center(), node2.get_center(), color=mn.GREEN)
                    connections.add(line)

            network = mn.VGroup(connections, layer1, layer2, layer3)
            # Center the network horizontally
            network.move_to(mn.ORIGIN + mn.UP)

            # Create the equation
            equation = mn.MathTex("Y = f(X \\cdot W + \\beta)", color=mn.WHITE).next_to(network, mn.DOWN, buff=2)

            # Color W in green
            equation[0][6].set_color(mn.GREEN)

            # Animate the scene
            self.play(mn.Create(layer1))
            self.play(mn.Create(layer2))
            self.play(mn.Create(layer3))
            self.play(mn.Create(connections))
            self.play(mn.Write(equation))
            self.wait(1)

            # Create additional layers for the transition
            layer4 = (
                mn.VGroup(*[mn.Circle(radius=0.3, color=mn.WHITE, fill_color=mn.WHITE, fill_opacity=1) for _ in range(2)])
                .arrange(mn.DOWN, buff=0.75)
                .next_to(layer3, mn.RIGHT, buff=1.5)
            )
            layer5 = (
                mn.VGroup(*[mn.Circle(radius=0.3, color=mn.WHITE, fill_color=mn.WHITE, fill_opacity=1) for _ in range(2)])
                .arrange(mn.DOWN, buff=0.75)
                .next_to(layer4, mn.RIGHT, buff=1.5)
            )

            # Create yellow connections for new layers
            new_connections = mn.VGroup()
            for node1 in layer3:
                for node2 in layer4:
                    line = mn.Line(node1.get_center(), node2.get_center(), color=mn.YELLOW)
                    new_connections.add(line)

            for node1 in layer4:
                for node2 in layer5:
                    line = mn.Line(node1.get_center(), node2.get_center(), color=mn.YELLOW)
                    new_connections.add(line)

            new_network = mn.VGroup(new_connections, layer4, layer5)
            updated_network = mn.VGroup(network, new_network)
            # Center the updated network horizontally
            updated_network.move_to(mn.ORIGIN + mn.UP)

            # Create new equation
            new_equation = mn.MathTex("Y = f(X \\cdot (W + R) + \\beta)", color=mn.WHITE).next_to(
                updated_network, mn.DOWN, buff=2
            )
            new_equation[0][7].set_color(mn.GREEN)  # W in green
            new_equation[0][9].set_color(mn.YELLOW)  # R in yellow

            # Animate the transition
            self.play(
                mn.Transform(network, updated_network),
                mn.Transform(equation, new_equation),
            )
            self.wait(2)


if __name__ == "__main__":
    scene = NeuralNetworkScene()
    scene.render()
