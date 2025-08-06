import manim as mn

# Configure for vertical 9:16 format
mn.config.pixel_width = 1080
mn.config.pixel_height = 1920
mn.config.frame_width = 9
mn.config.frame_height = 16


class EmbeddingVisualization(mn.Scene):
    def setup(self):
        self.camera.background_color = mn.DARK_BLUE

    def create_axes(self):
        """Create clear X and Y axes with labels for vertical format"""
        axes = mn.VGroup()

        # X axis (shorter for vertical format)
        x_axis = mn.Arrow(
            [-3.5, 0, 0], [3.5, 0, 0], color=mn.WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.07
        )
        x_label = mn.Text("Semantic Dimension 1", font_size=20, color=mn.WHITE).next_to(
            x_axis.get_end(), mn.DOWN, buff=0.2
        )

        # Y axis (can be taller in vertical format)
        y_axis = mn.Arrow([0, -4, 0], [0, 4, 0], color=mn.WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.05)
        y_label = mn.Text("Semantic Dimension 2", font_size=20, color=mn.WHITE).next_to(
            y_axis.get_end(), mn.RIGHT, buff=0.2
        )

        axes.add(x_axis, y_axis, x_label, y_label)
        return axes

    def construct(self):
        # Step 1: Add "Dense Vectors" title at top
        title = mn.Text("Dense Vectors", font_size=40, color=mn.YELLOW)
        title.move_to([0, 6.5, 0])  # Position higher for vertical format
        self.play(mn.Write(title), run_time=0.8)
        self.wait(0.2)

        # Step 2: Create and show axes (0-1 seconds)
        axes = self.create_axes()
        axes.shift(mn.UP * 1)  # Move axes up to make room
        self.play(mn.Create(axes), run_time=1)
        self.wait(0.5)

        # Step 3: Show word points (1-3 seconds)
        words = ["dog", "cat", "car"]
        word_colors = [mn.GREEN, mn.BLUE, mn.RED]
        # Adjusted positions for narrower vertical format
        word_positions = [
            [-1.5, 1.5, 0],  # dog
            [-0.8, 0.5, 0],  # cat (close to dog)
            [2.2, 1, 0],  # car (far from animals)
        ]

        word_points = mn.VGroup()
        word_labels = mn.VGroup()

        for i, (word, color, pos) in enumerate(zip(words, word_colors, word_positions)):
            # Create point
            point = mn.Dot(pos, radius=0.15, color=color)
            point.set_sheen(0.8, mn.UP)

            # Create label
            label = mn.Text(word, font_size=32, color=color)
            label.next_to(point, mn.UP, buff=0.3)

            word_points.add(point)
            word_labels.add(label)

            # Animate appearance
            self.play(mn.FadeIn(point), mn.Write(label), run_time=0.6)
            self.wait(0.1)

        self.wait(0.5)

        # Step 4: Show semantic relationship (3-5 seconds)
        # Highlight similarity between dog and cat
        dog_pos = word_positions[0]
        cat_pos = word_positions[1]

        similarity_line = mn.Line(dog_pos, cat_pos, color=mn.YELLOW, stroke_width=3)
        similarity_line.set_opacity(0.7)

        # Show connection with pulsing effect
        self.play(mn.Create(similarity_line), run_time=0.8)
        self.play(similarity_line.animate.set_opacity(0.3), run_time=0.5)
        self.play(similarity_line.animate.set_opacity(0.7), run_time=0.5)

        # Add distance labels
        close_label = mn.Text("Similar", font_size=22, color=mn.YELLOW)
        close_label.move_to([(dog_pos[0] + cat_pos[0]) / 2, (dog_pos[1] + cat_pos[1]) / 2 - 0.6, 0])

        self.play(mn.Write(close_label), run_time=0.5)
        self.wait(0.7)

        # Clean up similarity visualization
        self.play(mn.FadeOut(similarity_line), mn.FadeOut(close_label), run_time=0.5)
        self.wait(0.3)

        # Step 5: Introduce "pet" (5-7 seconds)
        pet_pos = [3, 3, 0]  # Start position (adjusted for vertical)
        pet_point = mn.Dot(pet_pos, radius=0.15, color=mn.PURPLE)
        pet_label = mn.Text("pet", font_size=32, color=mn.PURPLE)
        pet_label.next_to(pet_point, mn.UP, buff=0.3)

        # Pet appears from the side
        self.play(mn.FadeIn(pet_point, shift=mn.LEFT), mn.Write(pet_label), run_time=1)
        self.wait(0.5)

        # Step 6: Show influence and fine-tuning (7-11 seconds)
        # Move pet to influence position (adjusted for vertical)
        new_pet_pos = [-1, 2.5, 0]
        self.play(
            pet_point.animate.move_to(new_pet_pos),
            pet_label.animate.next_to([new_pet_pos[0], new_pet_pos[1] + 0.3, 0], mn.UP, buff=0),
            run_time=1.5,
        )

        # Show influence lines to dog and cat
        influence_to_dog = mn.Line(new_pet_pos, dog_pos, color=mn.PURPLE, stroke_width=2)
        influence_to_cat = mn.Line(new_pet_pos, cat_pos, color=mn.PURPLE, stroke_width=2)
        influence_to_dog.set_opacity(0.6)
        influence_to_cat.set_opacity(0.6)

        self.play(mn.Create(influence_to_dog), mn.Create(influence_to_cat), run_time=1)
        self.wait(0.5)

        # Step 7: Fine-tuning - move dog and cat closer (11-13 seconds)
        new_dog_pos = [-1.3, 1.8, 0]  # Adjusted for vertical format
        new_cat_pos = [-0.9, 0.8, 0]  # Adjusted for vertical format

        # Animate the movement
        self.play(
            word_points[0].animate.move_to(new_dog_pos),  # dog
            word_points[1].animate.move_to(new_cat_pos),  # cat
            word_labels[0].animate.next_to([new_dog_pos[0], new_dog_pos[1] + 0.3, 0], mn.UP, buff=0),
            word_labels[1].animate.next_to([new_cat_pos[0], new_cat_pos[1] + 0.3, 0], mn.UP, buff=0),
            mn.FadeOut(influence_to_dog),
            mn.FadeOut(influence_to_cat),
            run_time=2,
        )

        # Step 8: Show final result (13-15 seconds)
        final_similarity = mn.Line(new_dog_pos, new_cat_pos, color=mn.GREEN_A, stroke_width=2)
        final_similarity.set_opacity(0.8)

        self.play(mn.Create(final_similarity), run_time=0.5)

        # Final message
        final_label = mn.Text("Semantic relationships\nlearned from context", font_size=26, color=mn.WHITE)
        final_label.move_to([0, -4, 0])  # Position at bottom for vertical format

        self.play(mn.Write(final_label), run_time=1)
        self.wait(1)

        # Clean ending
        self.play(mn.FadeOut(final_similarity), run_time=0.5)
        self.wait(1)


if __name__ == "__main__":
    scene = EmbeddingVisualization()
    scene.render()
