import manim as mn
import numpy as np


def create_elbow_arrow(start, end, angle=mn.TAU / 4):
    midpoint = (start + end) / 2
    control_point = midpoint + np.array([np.cos(angle), np.sin(angle), 0]) * 0.5

    path = mn.CubicBezier(start, start, control_point, end)

    # Create the arrow tip
    tip = (
        mn.ArrowTriangleTip()
        .scale(0.2)  # Increased scale for better visibility
        .set_color(mn.WHITE)  # Set color to make it more visible
    )

    # Create the arrow
    arrow = mn.VGroup(
        path,
        tip.move_to(
            path.get_end(), aligned_edge=path.get_end() - path.get_last_point()
        ),
    )

    return arrow
