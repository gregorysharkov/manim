import manim as mn
import numpy as np


class AdjacencyMatrix(mn.Scene):
    debug: bool = False  # Set debug to False to disable debugging features
    
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
        self.create_initial_graph()
        self.create_adjacency_matrix()
        self.transfer_node_labels()
        self.process_edges()
        self.align_graph_and_matrix()
        self.show_node_features()
        self.transform_to_feature_matrix()
        self.prepare_for_matrix_operations()
        self.show_matrix_multiplication()
        self.show_identity_matrix()
        self.show_matrix_transfer()
        self.show_degree_matrix()
        self.show_feature_aggregation_equation()
        self.show_weights_matrix()

    def create_initial_graph(self):
        # Create a simple undirected graph
        self.graph = mn.Graph(
            vertices=["0", "1", "2"],
            edges=[("0", "1"), ("1", "2")],
            labels=True,
            layout={"0": mn.LEFT * 2, "1": mn.ORIGIN, "2": mn.RIGHT * 2},
            vertex_config={"fill_color": mn.GREEN, "stroke_color": mn.BLACK},
        ).scale(0.8)
        
        self.graph_label = mn.MathTex("Graph (G)").next_to(self.graph, mn.UP, buff=0.5)
        self.graph_group = mn.VGroup(self.graph, self.graph_label)
        
        self.play(mn.Create(self.graph), mn.Write(self.graph_label), run_time=3)
        self.wait(3)

    def create_adjacency_matrix(self):
        # Create adjacency matrix (3x3 grid)
        matrix = [
            ["0" for _ in range(3)] for _ in range(3)
        ]  # Use strings instead of integers
        self.adjacency_matrix = (
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
        self.adjacency_matrix_label = mn.MathTex("Adjacency Matrix (A)").next_to(
            self.adjacency_matrix, mn.UP, buff=0.5
        )

        # Group graph and table
        self.adjacency_matrix_group = mn.VGroup(
            self.adjacency_matrix, self.adjacency_matrix_label
        )

        # Arrange graph and table side by side
        combined_group = mn.VGroup(
            self.graph_group, self.adjacency_matrix_group
        ).arrange(mn.RIGHT, buff=3)
        combined_group.move_to(mn.ORIGIN)

        # Style the table
        self.adjacency_matrix.get_entries().set_color(mn.WHITE)
        for i in range(3):
            self.highlight_cell(self.adjacency_matrix, i + 2, 1, mn.GREY)
            self.highlight_cell(self.adjacency_matrix, 1, i + 2, mn.GREY)

        # Animation sequence
        self.play(mn.Create(self.adjacency_matrix), mn.Write(self.adjacency_matrix_label), run_time=4)
        self.wait(2)

    def transfer_node_labels(self):
        self.text_elements = []
        for i, vertex in enumerate(self.graph.vertices):
            horizon_cell_copy = self.graph.vertices[vertex].copy()
            target_row_horizon = self.adjacency_matrix.get_rows()[i + 1]
            target_cell_horizon = target_row_horizon[0]
            new_text_horizon = mn.Text(str(i), color=mn.GREEN_C).scale(0.6)
            self.text_elements.append(new_text_horizon)
            # self.adjacency_matrix.get_entries()[4 * i + 1 + i] = new_text_horizon

            vertical_cell_copy = self.graph.vertices[vertex].copy()
            target_cell_vertical = self.adjacency_matrix.get_rows()[0][i + 1]
            new_text_vertical = mn.Text(str(i), color=mn.GREEN_B).scale(0.6)
            self.text_elements.append(new_text_vertical)
            # self.adjacency_matrix.get_entries()[i + 1] = new_text_vertical
            # Animate the transfer
            # Replace the old cell with the new one in the table
            self.adjacency_matrix.get_entries()[4 * i + 1 + i] = new_text_vertical
            self.adjacency_matrix.get_entries()[i + 1] = new_text_horizon

            self.play(
                horizon_cell_copy.animate.set_color(mn.GREEN_C),
                vertical_cell_copy.animate.set_color(mn.GREEN_B),
                mn.ReplacementTransform(
                    horizon_cell_copy, new_text_horizon.move_to(target_cell_horizon)
                ),
                mn.ReplacementTransform(
                    vertical_cell_copy, new_text_vertical.move_to(target_cell_vertical)
                ),
                mn.FadeOut(target_cell_horizon),
                mn.FadeOut(target_cell_vertical),
                run_time=3,
            )

            self.wait(0.5)

    def process_edges(self):
        edges = [("0", "1"), ("1", "2")]  # Use strings instead of integers
        
        # Initialize additional_text_elements if not already created
        if not hasattr(self, 'additional_text_elements'):
            self.additional_text_elements = []
            
        for u, v in edges:
            # Highlight the edge in the graph
            edge = self.graph.edges[(u, v)]
            self.play(edge.animate.set_color(mn.YELLOW), run_time=1)

            # Create copies of the edge for animation
            edge_copy1 = edge.copy().set_color(mn.YELLOW)
            edge_copy2 = edge.copy().set_color(mn.YELLOW)

            # Update the adjacency matrix
            row = int(u) + 1  # Convert string to int, then offset for row labels
            col = int(v) + 1  # Convert string to int, then offset for column labels
            cell_uv = self.adjacency_matrix.get_entries()[row * 4 + col - 1]
            cell_vu = self.adjacency_matrix.get_entries()[col * 4 + row - 1]

            new_text_uv = mn.Text("1", color=mn.YELLOW).scale(0.6)
            new_text_vu = mn.Text("1", color=mn.YELLOW).scale(0.6)
            
            # Track these new text elements for later cleanup
            self.additional_text_elements.extend([new_text_uv, new_text_vu])

            # Animate the edge copies moving and transforming into cells
            self.play(
                mn.ReplacementTransform(edge_copy1, new_text_uv.move_to(cell_uv)),
                mn.ReplacementTransform(edge_copy2, new_text_vu.move_to(cell_vu)),
                mn.FadeOut(cell_uv),
                mn.FadeOut(cell_vu),
                run_time=1.5,
            )

            # Replace the old cells with the new ones in the table
            self.adjacency_matrix.get_entries()[row * 4 + col - 1] = new_text_uv
            self.adjacency_matrix.get_entries()[col * 4 + row - 1] = new_text_vu

            self.wait(2)

    def align_graph_and_matrix(self):
        vertical_shift = self.adjacency_matrix_label.get_top()[1] - self.graph_label.get_top()[1]
        self.play(self.graph_group.animate.shift(mn.UP * vertical_shift), run_time=2)
        self.wait(1)

    def show_node_features(self):
        FEATURE_DIMENSION = 5
        np.random.seed(0)  # Set the seed for reproducibility for the example purposes
        node_features = np.random.randint(
            0, 100, size=(len(self.graph.vertices), FEATURE_DIMENSION)
        )
        self.feature_tables = []  # Create a list to store the feature tables
        for i, vertex in enumerate(self.graph.vertices):
            feature_list = [[feature] for feature in node_features[i]]
            vertex_features = mn.DecimalTable(
                feature_list,
                include_outer_lines=True,
                element_to_mobject_config={
                    "num_decimal_places": 0
                },  # Display as integers
            ).scale(0.5)
            vertex_features.next_to(self.graph.vertices[vertex], mn.DOWN, buff=0.5)
            self.feature_tables.append(vertex_features)
            self.play(
                mn.Create(vertex_features),
                run_time=1,
            )

        every_element = mn.Group(*self.mobjects)
        top_edge = self.camera.frame_height / 3
        group_top = every_element[2].get_top()
        shift_amount = top_edge - group_top - 0.5

        self.play(
            every_element.animate.shift(mn.UP * shift_amount),
            run_time=2,
        )
        self.wait(2)

        # transform the feature tables into the matrix
        self.feature_matrix = mn.Matrix(
            node_features.tolist(),
        ).scale(0.4)

        # Create and position the feature matrix label
        feature_matrix_label = mn.MathTex("Node Features (X)").next_to(
            self.feature_matrix, mn.UP, buff=0.5
        )

        # Group the feature matrix and its label
        self.feature_matrix_group = mn.VGroup(self.feature_matrix, feature_matrix_label).next_to(self.graph_group, mn.DOWN, buff=.5)

        # Animate the transformation
        self.play(
            *[mn.FadeOut(ft) for ft in self.feature_tables],  # Fade out old feature tables
            mn.FadeIn(self.feature_matrix),  # Fade in new feature table
            mn.Write(feature_matrix_label),  # Write the label
            run_time=2,
        )

        self.wait(2)

    def transform_to_feature_matrix(self):
        new_matrix = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        new_adjacency_matrix = mn.Matrix(new_matrix)
        scale_factor = self.feature_matrix.height / new_adjacency_matrix.height

        # Calculate a more moderate shift for the feature matrix
        target_shift = mn.UP * (mn.config.frame_height / 6)

        # Take a "snapshot" of all current objects in the scene before removing anything
        # This will help us identify new artifacts that appear later
        current_objects = [obj for obj in self.mobjects]

        # Move feature matrix up and fade out graph
        self.play(
            self.feature_matrix_group.animate.shift(target_shift),
            mn.FadeOut(self.graph),
            mn.FadeOut(self.graph_label),
            run_time=2,
        )
        
        # Scale and position the new adjacency matrix
        new_adjacency_matrix.scale(scale_factor)
        
        # Update the adjacency matrix label position
        self.adjacency_matrix_label.next_to(new_adjacency_matrix, mn.UP, buff=0.5)
        
        # Store the old adjacency matrix group before replacing it
        old_adjacency_matrix_group = self.adjacency_matrix_group
        
        # Create the new matrix 
        self.adjacency_matrix = new_adjacency_matrix
        self.adjacency_matrix_group = mn.VGroup(
            new_adjacency_matrix, self.adjacency_matrix_label
        ).next_to(self.feature_matrix_group, mn.RIGHT, buff=2)
        
        # First, animate the fadeout of the old matrix
        self.play(
            mn.FadeOut(old_adjacency_matrix_group),
            run_time=1.5
        )
        
        # Now after fading out, actually remove the old matrix from the scene
        self.remove(old_adjacency_matrix_group)
        
        # Remove all individual elements that might cause artifacts
        if hasattr(self, 'text_elements') and self.text_elements:
            for text in self.text_elements:
                self.remove(text)
            self.text_elements.clear()
        
        if hasattr(self, 'additional_text_elements') and self.additional_text_elements:
            for text in self.additional_text_elements:
                self.remove(text)
            self.additional_text_elements.clear()
        
        # Remove any zero or one text objects that might be artifacts
        # This is a more targeted approach to remove specific artifacts
        for mobject in self.mobjects.copy():
            if mobject not in current_objects:
                continue  # Skip objects that were added after we started
                
            if isinstance(mobject, mn.Text) or isinstance(mobject, mn.MathTex):
                # Don't remove the new matrix or its elements
                if mobject in new_adjacency_matrix.get_family() or mobject in [self.adjacency_matrix_label, self.feature_matrix_group[1]]:
                    continue
                
                # Only target potential artifacts - specifically those with values "0" or "1"
                if (hasattr(mobject, 'tex_string') and mobject.tex_string in ["0", "1"]) or \
                   (hasattr(mobject, 'text') and mobject.text in ["0", "1"]):
                    # Remove the mobject
                    self.remove(mobject)
                # Also remove any objects positioned outside the normal matrix region
                elif mobject.get_center()[0] > self.adjacency_matrix_group.get_right()[0] - 1:
                    self.remove(mobject)
        
        # Now add the new matrix to the scene
        self.add(self.adjacency_matrix_group)
        
        # Fade in the new matrix
        self.play(
            mn.FadeIn(new_adjacency_matrix),
            run_time=2,
        )

        self.wait(2)

    def prepare_for_matrix_operations(self):
        self.show_matrix_multiplication()

    def show_matrix_multiplication(self):
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
            new_value = int(old_entry.tex_string) + matrix_value

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
        degree_matrix_label = mn.MathTex("Degree Matrix (D)")
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

        combined_group = mn.VGroup(
            self.degree_matrix_group,
            self.adjacency_matrix_group,
            self.feature_matrix_group,
        )
        self.play(
            combined_group[1].animate.scale(2),
            combined_group[2].animate.scale(2),
            combined_group.animate.arrange(mn.RIGHT, buff=1, aligned_edge=mn.UP)
            .scale(0.8)
            .to_edge(mn.UP, buff=0.5),
        )

    def show_feature_aggregation_equation(self):
        equation = mn.MathTex(
            r"H = D^{-\frac{1}{2}} \cdot A \cdot D^{-\frac{1}{2}}\cdot X"
        )
        equation_label = mn.MathTex("Aggregated Features (H) Equation").scale(0.7)
        equation_label.next_to(equation, mn.UP, buff=0.5)
        equation_group = mn.VGroup(equation, equation_label)
        equation_group.next_to(self.adjacency_matrix, mn.DOWN, buff=2)
        self.play(mn.Write(equation_group), run_time=3)
        self.equation_group = equation_group

    def show_weights_matrix(self):
        weights = [
            [0.3, 0.5],
            [0.7, 0.2],
            [0.2, 0.1],
        ]

        weights_matrix = mn.Matrix(weights).scale(0.8)
        weights_matrix_label = mn.MathTex("Weights Matrix (W)")
        weights_matrix_label.next_to(weights_matrix, mn.UP, buff=0.75)

        weights_matrix_group = (
            mn.VGroup(weights_matrix, weights_matrix_label).next_to(
                mn.ORIGIN,
            )
            # .scale(0.75)
            .shift(mn.DOWN * 2)
        )

        combined_group = mn.VGroup(
            self.equation_group,
            weights_matrix_group,
        )
        self.play(
            combined_group.animate.arrange(mn.RIGHT, buff=1.5, aligned_edge=mn.ORIGIN)
            .scale(0.8)
            .shift(mn.DOWN),
            run_time=1,
        )

        # Add dot W to the equation
        new_equation = mn.MathTex(
            r"H = D^{-\frac{1}{2}} \cdot A \cdot D^{-\frac{1}{2}}\cdot X \cdot W"
        )
        new_equation.move_to(self.equation_group[0])

        self.play(
            mn.TransformMatchingTex(self.equation_group[0], new_equation), run_time=2
        )

        # Update the equation_group with the new equation
        self.equation_group[0] = new_equation

        self.wait(2)

    def highlight_cell(self, table, row, col, color):
        cell = table.get_cell((row, col))
        highlight = mn.BackgroundRectangle(cell, fill_color=color, fill_opacity=0.2)
        table.add_to_back(highlight)

    def show_matrix_multiplication_equation(self):
        # Create the equation
        pass
