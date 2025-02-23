import manim as mn
import numpy as np


class AdjacencyMatrix(mn.Scene):
    def construct(self):
        # Create a simple undirected graph
        graph = mn.Graph(
            vertices=["0", "1", "2"],
            edges=[("0", "1"), ("1", "2")],
            labels=True,
            layout={"0": mn.LEFT * 2, "1": mn.ORIGIN, "2": mn.RIGHT * 2},
            vertex_config={"fill_color": mn.GREEN, "stroke_color": mn.BLACK},
        ).scale(0.8)

        # Create adjacency matrix (3x3 grid)
        matrix = [
            ["0" for _ in range(3)] for _ in range(3)
        ]  # Use strings instead of integers
        adjacency_matrix = (
            mn.Table(
                matrix,
                row_labels=[mn.Text(str(i)) for i in range(3)],
                col_labels=[mn.Text(str(j)) for j in range(3)],
                include_outer_lines=True,
            )
            .scale(0.6)
            .to_edge(mn.RIGHT)
        )

        # Create labels
        graph_label = mn.Text("Graph (G)").next_to(graph, mn.UP, buff=0.5)
        matrix_label = mn.Text("Adjacency Matrix (A)").next_to(
            adjacency_matrix, mn.UP, buff=0.5
        )

        # Group graph and table
        graph_group = mn.VGroup(graph, graph_label)
        table_group = mn.VGroup(adjacency_matrix, matrix_label)

        # Arrange graph and table side by side
        combined_group = mn.VGroup(graph_group, table_group).arrange(mn.RIGHT, buff=3)
        combined_group.move_to(mn.ORIGIN)

        # Style the table
        adjacency_matrix.get_entries().set_color(mn.WHITE)
        for i in range(3):
            self.highlight_cell(adjacency_matrix, i + 2, 1, mn.GREY)
            self.highlight_cell(adjacency_matrix, 1, i + 2, mn.GREY)

        # Animation sequence
        self.play(mn.Create(graph), mn.Write(graph_label), run_time=3)
        self.wait(3)
        self.play(mn.Create(adjacency_matrix), mn.Write(matrix_label), run_time=4)
        self.wait(2)

        # Animate transfer of node labels to matrix
        text_elements = []
        for i, vertex in enumerate(graph.vertices):
            horizon_cell_copy = graph.vertices[vertex].copy()
            target_row_horizon = adjacency_matrix.get_rows()[i + 1]
            target_cell_horizon = target_row_horizon[0]
            new_text_horizon = mn.Text(str(i), color=mn.GREEN_C).scale(0.6)
            text_elements.append(new_text_horizon)

            vertical_cell_copy = graph.vertices[vertex].copy()
            target_cell_vertical = adjacency_matrix.get_rows()[0][i + 1]
            new_text_vertical = mn.Text(str(i), color=mn.GREEN_B).scale(0.6)
            text_elements.append(new_text_vertical)

            # Animate the transfer
            self.play(
                horizon_cell_copy.animate.set_color(mn.GREEN_C),
                mn.ReplacementTransform(
                    horizon_cell_copy, new_text_horizon.move_to(target_cell_horizon)
                ),
                mn.FadeOut(target_cell_horizon),
                run_time=2,
            )

            self.play(
                vertical_cell_copy.animate.set_color(mn.GREEN_B),
                mn.ReplacementTransform(
                    vertical_cell_copy, new_text_vertical.move_to(target_cell_vertical)
                ),
                mn.FadeOut(target_cell_vertical),
                run_time=2,
            )

            # Replace the old cell with the new one in the table
            # table.get_entries()[4 * i + 1] = new_text_horizon

            self.wait(0.5)

        # Process edges and update matrix
        edges = [("0", "1"), ("1", "2")]  # Use strings instead of integers
        for u, v in edges:
            # Highlight the edge in the graph
            edge = graph.edges[(u, v)]
            self.play(edge.animate.set_color(mn.YELLOW), run_time=1)

            # Create copies of the edge for animation
            edge_copy1 = edge.copy().set_color(mn.YELLOW)
            edge_copy2 = edge.copy().set_color(mn.YELLOW)

            # Update the adjacency matrix
            row = int(u) + 1  # Convert string to int, then offset for row labels
            col = int(v) + 1  # Convert string to int, then offset for column labels
            cell_uv = adjacency_matrix.get_entries()[row * 4 + col - 1]
            cell_vu = adjacency_matrix.get_entries()[col * 4 + row - 1]

            new_text_uv = mn.Text("1", color=mn.YELLOW).scale(0.6)
            new_text_vu = mn.Text("1", color=mn.YELLOW).scale(0.6)

            # Animate the edge copies moving and transforming into cells
            self.play(
                mn.ReplacementTransform(edge_copy1, new_text_uv.move_to(cell_uv)),
                mn.ReplacementTransform(edge_copy2, new_text_vu.move_to(cell_vu)),
                mn.FadeOut(cell_uv),
                mn.FadeOut(cell_vu),
                run_time=1.5,
            )

            # Replace the old cells with the new ones in the table
            adjacency_matrix.get_entries()[row * 4 + col - 1] = new_text_uv
            adjacency_matrix.get_entries()[col * 4 + row - 1] = new_text_vu

            self.wait(2)

        # Calculate the vertical shift needed to align the tops of the labels
        vertical_shift = matrix_label.get_top()[1] - graph_label.get_top()[1]

        # Animate the graph group moving up
        self.play(graph_group.animate.shift(mn.UP * vertical_shift), run_time=2)
        self.wait(1)

        # make node features appear next to nodes
        FEATURE_DIMENSION = 5
        node_features = np.random.randint(
            0, 100, size=(len(graph.vertices), FEATURE_DIMENSION)
        )
        feature_tables = []  # Create a list to store the feature tables
        for i, vertex in enumerate(graph.vertices):
            feature_list = [[feature] for feature in node_features[i]]
            vertex_features = mn.DecimalTable(
                feature_list,
                include_outer_lines=True,
                element_to_mobject_config={
                    "num_decimal_places": 0
                },  # Display as integers
            ).scale(0.5)
            vertex_features.next_to(graph.vertices[vertex], mn.DOWN, buff=0.5)
            feature_tables.append(vertex_features)
            self.play(
                mn.Create(vertex_features),
                run_time=1,
            )

        every_element = mn.Group(*self.mobjects)
        self.play(
            every_element.animate.shift(
                mn.UP * (mn.config.frame_height / 2 - every_element.get_top()[1] - 0.5)
            ),
            run_time=2,
        )
        self.wait(2)

        # transform the feature tables into the matrix
        feature_table = mn.DecimalTable(
            node_features.tolist(),
            include_outer_lines=True,
        ).scale(0.4)

        # Add a label to the new feature table
        feature_table_label = (
            mn.Text("Node Features").next_to(graph, mn.DOWN, buff=0.5).scale(0.6)
        )

        # Position the new feature table
        feature_table.next_to(feature_table_label, mn.DOWN, buff=1)
        self.feature_matrix = feature_table

        # Animate the transformation
        self.play(
            *[mn.FadeOut(ft) for ft in feature_tables],  # Fade out old feature tables
            mn.FadeIn(feature_table),  # Fade in new feature table
            run_time=2,
        )

        # Add a label to the new feature table
        feature_table_label = mn.Text("Node Features (X)").next_to(
            feature_table, mn.UP, buff=0.5
        )
        self.play(mn.Write(feature_table_label), run_time=1)

        self.wait(2)

        new_matrix = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        new_adjacency_matrix = mn.DecimalTable(
            new_matrix,
            include_outer_lines=True,
            element_to_mobject_config={"num_decimal_places": 0},
        )
        scale_factor = feature_table.height / new_adjacency_matrix.height

        # Hide the graph and its label
        # Move the feature table and its label to the top left
        self.play(
            mn.VGroup(feature_table, feature_table_label).animate.shift(
                mn.UP
                * (mn.config.frame_height / 2 - feature_table_label.get_top()[1] - 0.5)
            ),
            mn.FadeOut(graph),
            mn.FadeOut(graph_label),
            run_time=2,
        )
        new_adjacency_matrix.scale(scale_factor)
        new_adjacency_matrix.next_to(matrix_label, mn.DOWN, buff=0.5)
        self.adjacency_matrix = new_adjacency_matrix
        self.play(
            mn.FadeOut(adjacency_matrix),
            *[mn.FadeOut(text_label) for text_label in text_elements],
            mn.FadeIn(new_adjacency_matrix),
            run_time=2,
        )

        self.wait(2)

        self.show_matrix_multiplication_equation()
        equation = mn.MathTex(
            "A",
            "X",
            "=",
            r"\begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1N} \\ a_{21} & a_{22} & \cdots & a_{2N} \\ \vdots & \vdots & \ddots & \vdots \\ a_{N1} & a_{N2} & \cdots & a_{NN} \end{bmatrix}",
            r"\begin{bmatrix} x_{11} & x_{12} & \cdots & x_{1D} \\ x_{21} & x_{22} & \cdots & x_{2D} \\ \vdots & \vdots & \ddots & \vdots \\ x_{N1} & x_{N2} & \cdots & x_{ND} \end{bmatrix}",
            "=",
            r"\begin{bmatrix} y_{11} & y_{12} & \cdots & y_{1D} \\ y_{21} & y_{22} & \cdots & y_{2D} \\ \vdots & \vdots & \ddots & \vdots \\ y_{N1} & y_{N2} & \cdots & y_{ND} \end{bmatrix}",
        ).scale(0.7)

        # Position the equation
        equation.scale(0.8).move_to(mn.ORIGIN)
        equation.move_to(mn.DOWN * 1.5)

        # Animate the equation
        self.play(mn.Write(equation), run_time=3)

        # Add labels
        adj_label = (
            mn.Text("Adjacency Matrix", color=mn.BLUE)
            .scale(0.5)
            .next_to(equation[3], mn.UP, buff=0.2)
        )
        feat_label = (
            mn.Text("Feature Matrix", color=mn.GREEN)
            .scale(0.5)
            .next_to(equation[4], mn.UP, buff=0.2)
        )
        result_label = (
            mn.Text("Aggregated features (H)", color=mn.RED)
            .scale(0.5)
            .next_to(equation[6], mn.UP, buff=0.2)
        )

        self.play(
            mn.Write(adj_label),
            mn.Write(feat_label),
            mn.Write(result_label),
            run_time=2,
        )

        matrix_multiplication_equation = mn.VGroup(
            equation, adj_label, feat_label, result_label
        )
        self.wait(5)
        self.play(mn.FadeOut(matrix_multiplication_equation))
        self.remove(matrix_multiplication_equation)

        self.show_identity_matrix()
        self.show_matrix_transfer()
        self.show_degree_matrix()
        self.show_feature_aggregation_equation()

    def show_matrix_multiplication_equation(self):
        # Create the equation
        pass

    def show_identity_matrix(self):
        # Create a 3x3 Identity matrix
        identity_matrix = mn.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).scale(0.8)
        identity_matrix_label = mn.Text("Identity Matrix")
        identity_matrix_label.next_to(identity_matrix, mn.UP, buff=0.75)

        # Position the matrix in the center of the screen
        i_matrix_group = (
            mn.VGroup(identity_matrix, identity_matrix_label)
            .move_to(mn.ORIGIN)
            .scale(0.75)
            .move_to(mn.DOWN * 1.5)
        )

        # Animate the appearance of the Identity matrix
        self.play(mn.Write(i_matrix_group), run_time=2)
        self.imatrix_group = i_matrix_group

        # Wait for a moment to let the audience see the matrix
        self.wait(2)

    def show_matrix_transfer(self):
        # Highlight diagonal elements in both matrices
        # Highlight diagonal elements in both matrices
        for i in range(3):
            self.play(
                self.adjacency_matrix.get_entries()[i * 3 + i].animate.set_color(
                    mn.YELLOW
                ),
                self.imatrix_group[0]
                .get_entries()[i * 3 + i]
                .animate.set_color(mn.YELLOW),
                run_time=0.5,
            )

        self.wait(1)

        # Transfer diagonal elements
        for i in range(3):
            matrix_element = self.imatrix_group[0].get_entries()[i * 3 + i]
            matrix_value = int(matrix_element.tex_string)

            old_entry = self.adjacency_matrix.get_entries()[i * 3 + i]
            new_value = int(old_entry.get_value()) + matrix_value

            new_element = old_entry.copy()
            new_element.become(mn.MathTex(str(new_value), color=mn.YELLOW))
            new_element.match_height(old_entry)
            new_element.move_to(old_entry)
            self.adjacency_matrix.get_entries()[i * 3 + i] = new_element

            self.play(
                mn.ReplacementTransform(matrix_element, new_element),
            )

        self.play(mn.FadeOut(self.imatrix_group), run_time=1)
        self.wait(2)

    def show_degree_matrix(self):
        # Calculate the degree of each node
        degrees = [
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 2],
        ]

        normalized_degrees = [
            [r"\frac{1}{\sqrt{2}}", "0", "0"],
            ["0", r"\frac{1}{\sqrt{3}}", "0"],
            ["0", "0", r"\frac{1}{\sqrt{2}}"],
        ]

        # Create a Manim matrix object
        degree_matrix_mobject = mn.Matrix(degrees).scale(0.8)
        degree_matrix_label = mn.Text("Degree Matrix (D)")
        degree_matrix_label.next_to(degree_matrix_mobject, mn.UP, buff=0.75)

        normalized_degree_matrix_mobject = mn.Matrix(
            normalized_degrees,
            v_buff=1.3,
            h_buff=1.3,
            element_alignment_corner=mn.ORIGIN,
        ).scale(0.8)
        normalized_degree_matrix_label = normalized_degree_matrix_label = mn.MathTex(
            r"\text{Normalized Degree Matrix } (D^{-\frac{1}{2}})"
        )
        normalized_degree_matrix_label.next_to(
            normalized_degree_matrix_mobject, mn.UP, buff=0.5
        )

        # Position the matrix
        d_matrix_group = (
            mn.VGroup(degree_matrix_mobject, degree_matrix_label)
            .move_to(mn.ORIGIN)
            .scale(0.75)
            .move_to(mn.DOWN * 1.5)
        )

        self.play(mn.Write(d_matrix_group), run_time=2)
        self.wait(5)

        nd_matrix_group = (
            mn.VGroup(normalized_degree_matrix_mobject, normalized_degree_matrix_label)
            .next_to(d_matrix_group, mn.RIGHT, buff=2)
            .scale(0.6)
        )

        combined_matrices = mn.VGroup(d_matrix_group.copy(), nd_matrix_group)
        combined_matrices.arrange(mn.RIGHT, buff=1.5).move_to(mn.ORIGIN).move_to(
            mn.DOWN * 1.5
        )
        # combined_matrices.move_to(mn.ORIGIN).move_to(mn.DOWN * 1.5)

        new_d_matrix_position = combined_matrices[0].get_center()
        self.play(
            d_matrix_group.animate.move_to(new_d_matrix_position),
            mn.Write(nd_matrix_group),
            run_time=3,
        )

        self.wait(2)

        self.play(
            mn.FadeOut(d_matrix_group),
            nd_matrix_group.animate.next_to(self.feature_matrix, mn.DOWN, buff=1),
            run_time=1,
        )
        self.degree_matrix_group = nd_matrix_group

    def show_feature_aggregation_equation(self):
        equation = mn.MathTex(r"H = D^{-\frac{1}{2}} \cdot A \cdot D^{-\frac{1}{2}}")
        equation_label = mn.Text("Aggregated Features (H) Equation").scale(0.7)
        equation_label.next_to(equation, mn.UP, buff=0.5)
        equation_group = mn.VGroup(equation, equation_label)
        equation_group.next_to(self.adjacency_matrix, mn.DOWN, buff=1)
        self.play(mn.Write(equation_group), run_time=3)

    def highlight_cell(self, table, row, col, color):
        cell = table.get_cell((row, col))
        highlight = mn.BackgroundRectangle(cell, fill_color=color, fill_opacity=0.2)
        table.add_to_back(highlight)
