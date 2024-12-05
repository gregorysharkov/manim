from typing import Union
import logging
import random
import manim as mn
from blocks import InputBlock, OutputBlock

random.seed(0)

logger = logging.getLogger(__name__)

class NeuronLayer(mn.VGroup):

    def __init__(
        self, neuron_number: int, layer_color: Union[mn.color, list[mn.color]], **kwargs,
    ):
        super().__init__(**kwargs)
        self.layer_number = neuron_number
        self.layer_color = layer_color

        if isinstance(layer_color, list):
            colors = [layer_color[i % len(layer_color)] for i in range(neuron_number)]
        else:
            colors = [layer_color] * neuron_number

        self.neurons = mn.VGroup(
            *[mn.Dot(color=color, radius=1) for color in colors]
        )
        self.neurons.arrange(mn.RIGHT, buff=1)

        self.add(self.neurons)


class NeuronNetworkScene(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.BLUE_E
        input_block = InputBlock("Input")
        layer_1 = NeuronLayer(10, mn.WHITE)
        layer_2 = NeuronLayer(8, mn.WHITE)
        layer_3 = NeuronLayer(8, mn.WHITE)
        final_layer = NeuronLayer(3, layer_color=[mn.RED, mn.ORANGE, mn.GREEN])
        output_block = OutputBlock("Output")

        neural_network = mn.VGroup(
            input_block,
            layer_1,
            layer_2,
            layer_3,
            final_layer,
            output_block,
        )
        neural_network.arrange(mn.DOWN, buff=2)

        scale_factor = get_scale(self.camera, neural_network)
        neural_network.scale(scale_factor)

        input_block.to_edge(mn.UP, buff=0.5)

        layer_1.next_to(input_block, mn.DOWN, buff=2 * scale_factor)
        layer_2.next_to(layer_1, mn.DOWN, buff=2 * scale_factor)
        layer_3.next_to(layer_2, mn.DOWN, buff=2 * scale_factor)

        # Randomly select active neurons in the second layer
        num_active = min(5, len(layer_2.neurons))  # Select up to 5 active neurons
        active_neurons = random.sample(list(layer_2.neurons), num_active)

        # Randomly select active neurons in the third layer
        num_active_3 = min(5, len(layer_3.neurons))
        active_neurons_3 = random.sample(list(layer_3.neurons), num_active_3)

        # final layer
        active_neurons_final = final_layer.neurons[-1]

        connections_1_2, dots_1_2 = create_layer_connections(layer_1, layer_2, active_neurons=active_neurons)
        connections_2_3, dots_2_3 = create_layer_connections(layer_2, layer_3)
        connections_3_4, dots_3_4 = create_layer_connections(layer_3, final_layer)
        all_connections = mn.VGroup(connections_1_2, connections_2_3, connections_3_4)

        self.play(mn.Write(input_block))
        self.wait(.5)
        self.play(
            mn.Create(layer_1),
            mn.Create(layer_2),
            mn.Create(layer_3),
            mn.Create(final_layer),
        )
        self.wait(.5)
        self.play(mn.Create(all_connections))
        self.wait(.5)
        self.play(mn.Write(output_block))

        layer_inputs = [
            round(random.uniform(0, 1), 2) for _ in range(layer_1.layer_number)
        ]

        # first to second layer
        self.draw_layer_values(layer_1, inputs=layer_inputs)
        self.animate_signal_flow(connections_1_2, dots_1_2)
        self.highlight_active_neurons(active_neurons)
        self.draw_layer_values(layer_2, active_neurons=active_neurons)

        # second to third layer
        self.animate_signal_flow(connections_2_3, dots_2_3)
        self.highlight_active_neurons(active_neurons_3)
        self.draw_layer_values(layer_3, active_neurons=active_neurons_3)

        # third to final layer
        self.animate_signal_flow(connections_3_4, dots_3_4)
        self.highlight_active_neurons(active_neurons_final)
        self.draw_layer_values(final_layer, active_neurons=active_neurons_final)

        last_neuron = final_layer.neurons[-1]
        new_text = mn.Text("Perfect", color=mn.BLACK, font_size=18)
        new_text.move_to(output_block[1].get_center())

        self.play(
            last_neuron.animate.scale(1.5),
            output_block[0].animate.set_fill(mn.GREEN, opacity=0.8),
            mn.Transform(output_block[1], new_text),
            run_time=1,
        )
        self.wait(2)

    def draw_layer_values(self, layer, inputs=None, active_neurons=None):
        input_labels = mn.VGroup()
        neuron_animations = []

        for i, neuron in enumerate(layer.neurons):
            if inputs is not None:
                input_value = inputs[i]
            elif active_neurons is not None:
                input_value = (
                    round(random.uniform(0.5, 1), 2) if neuron in active_neurons else 0.09
                )
            else:
                raise ValueError("Either inputs or active_neurons must be provided")

            label = mn.Text(str(input_value), font_size=18, color=mn.BLACK)
            label.move_to(neuron.get_center(), aligned_edge=mn.ORIGIN)
            input_labels.add(label)

            neuron_animations.append(neuron.animate.set_opacity(input_value))
            neuron_animations.append(neuron.animate.set_fill(opacity=input_value))

        self.play(mn.Write(input_labels))
        self.wait(0.25)
        self.play(*neuron_animations, run_time=.5)
        self.wait(0.25)

    def animate_signal_flow(self, connections, dots):
        animations = []
        for connection, dot in zip(connections, dots):
            animations.append(
                mn.MoveAlongPath(dot, path=connection, rate_func=mn.linear)
            )
        self.play(*animations, run_time=1)

    def highlight_active_neurons(self, active_neurons):
        highlight_animations = [neuron.animate.set_color(mn.GREEN) for neuron in active_neurons]
        self.play(*highlight_animations)


def create_layer_connections(layer1, layer2, active_neurons = None):
    connections = mn.VGroup()
    dots = mn.VGroup()
    if active_neurons:
        target_neurons = active_neurons
    else:
        target_neurons = layer2.neurons

    for neuron1 in layer1.neurons:
        for neuron2 in target_neurons:
            line = mn.Line(
                neuron1.get_center(),
                neuron2.get_center(),
                stroke_width=0.5,
                color=mn.LIGHT_GRAY,
            )
            line.set_opacity(0.75)
            connections.add(line)

            dot = mn.Dot(color=mn.GREEN, radius=0.05)
            dot.move_to(neuron1.get_center())
            dots.add(dot)

    return connections, dots


def get_scale(camera, group):
    width_scale_factor = (camera.frame_width * 0.8) / group.width
    height_scale_factor = (camera.frame_height * 0.8) / group.height
    scale_factor = min(width_scale_factor, height_scale_factor)
    return min(scale_factor, 1)


if __name__ == "__main__":
    scene = NeuronNetworkScene()
    scene.render()
