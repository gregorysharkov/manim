import manim as mn
import numpy as np


class PolitePieChart(mn.Scene):
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

        title = mn.Text("Politeness Distribution", color=mn.BLACK).to_edge(mn.UP)

        polite_percentage = 0.67
        not_polite_percentage = 0.33

        polite_angle = polite_percentage * 2 * np.pi
        not_polite_angle = not_polite_percentage * 2 * np.pi

        outer_radius = 2.5

        polite_sector = mn.AnnularSector(
            inner_radius=0,
            outer_radius=outer_radius,
            angle=polite_angle,
            start_angle=0,
            color=mn.GREEN,
            fill_opacity=0.8,
            stroke_color=mn.WHITE,
            stroke_width=4,
        )

        not_polite_sector = mn.AnnularSector(
            inner_radius=0,
            outer_radius=outer_radius,
            angle=not_polite_angle,
            start_angle=polite_angle,
            color=mn.GRAY,
            fill_opacity=0.8,
            stroke_color=mn.WHITE,
            stroke_width=4,
        )

        pie_chart = mn.VGroup(polite_sector, not_polite_sector)

        polite_label_angle = polite_angle / 2
        polite_label_pos = np.array(
            [
                outer_radius * 0.6 * np.cos(polite_label_angle),
                outer_radius * 0.6 * np.sin(polite_label_angle),
                0,
            ]
        )

        not_polite_label_angle = polite_angle + not_polite_angle / 2
        not_polite_label_pos = np.array(
            [
                outer_radius * 0.6 * np.cos(not_polite_label_angle),
                outer_radius * 0.6 * np.sin(not_polite_label_angle),
                0,
            ]
        )

        polite_label_text = f"Polite\n({polite_percentage:.0%})"
        polite_label = mn.Text(polite_label_text, font_size=36, color=mn.BLACK, weight=mn.BOLD).move_to(
            polite_label_pos
        )

        not_polite_label_text = f"Not Polite\n({not_polite_percentage:.0%})"
        not_polite_label = mn.Text(not_polite_label_text, font_size=36, color=mn.BLACK, weight=mn.BOLD).move_to(
            not_polite_label_pos
        )

        self.play(mn.Write(title))
        self.play(mn.Create(polite_sector), mn.Create(not_polite_sector))
        self.play(mn.Write(polite_label), mn.Write(not_polite_label))
        self.wait(2)


if __name__ == "__main__":
    scene = PolitePieChart()
    scene.render()
