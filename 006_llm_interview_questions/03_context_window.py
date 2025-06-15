import manim as mn


class ContextWindow(mn.Scene):
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
        # Chat history

        chat_history_1 = mn.Text("03/01: Then the Client asked for daily standups.").scale(0.7)
        chat_history_2 = mn.Text("02/01: Then the Client asked for weekly standups.").scale(0.7)
        chat_history_3 = mn.Text("01/01: The Client asked for daily standups.").scale(0.7)

        chat_title = mn.Text("Chat History").scale(0.7).to_edge(mn.UP + mn.LEFT)
        chat_history = mn.VGroup(
            chat_history_1,
            chat_history_2,
            chat_history_3,
        ).arrange(mn.DOWN, buff=0.5, aligned_edge=mn.LEFT)
        chat_history.next_to(chat_title, mn.DOWN, buff=0.5, aligned_edge=mn.LEFT)

        self.play(mn.Write(chat_title))
        self.play(mn.Write(chat_history))
        self.wait(1)

        # Question
        question = mn.Text("Question: What is the current frequency of progress updates?").scale(0.7)
        question.next_to(chat_history, mn.DOWN, buff=1)
        question.align_to(chat_title, mn.LEFT)
        self.play(mn.Write(question))
        self.wait(1)

        # LLM Answer
        answer_title = mn.Text("Answer: ").scale(0.7)
        answer_text = mn.Text("Daily").scale(0.7)
        answer_group = mn.VGroup(answer_title, answer_text).arrange(mn.RIGHT, buff=0.4, aligned_edge=mn.UP)
        answer_group.next_to(question, mn.DOWN, buff=0.5, aligned_edge=mn.LEFT)

        # Context window 1
        context_window = mn.SurroundingRectangle(chat_history_3, color=mn.YELLOW, buff=0.2)
        self.play(mn.Create(context_window))
        self.play(mn.Write(answer_group))
        self.wait(2)

        # Context window 2
        self.play(context_window.animate.become(mn.SurroundingRectangle(chat_history[1:], color=mn.YELLOW, buff=0.2)))
        new_answer_text = mn.Text("Weekly").scale(0.7)
        new_answer_group = mn.VGroup(answer_title, new_answer_text).arrange(mn.RIGHT, buff=0.4, aligned_edge=mn.UP)
        new_answer_group.next_to(question, mn.DOWN, buff=0.5, aligned_edge=mn.LEFT)
        self.play(mn.Transform(answer_group, new_answer_group))
        self.wait(2)

        # Context window 3
        self.play(context_window.animate.become(mn.SurroundingRectangle(chat_history, color=mn.YELLOW, buff=0.2)))
        new_answer_text_2 = mn.Text("Daily").scale(0.7)
        new_answer_group_2 = mn.VGroup(answer_title, new_answer_text_2).arrange(mn.RIGHT, buff=0.4, aligned_edge=mn.UP)
        new_answer_group_2.next_to(question, mn.DOWN, buff=0.5, aligned_edge=mn.LEFT)
        self.play(mn.Transform(new_answer_group, new_answer_group_2))
        self.wait(2)


if __name__ == "__main__":
    scene = ContextWindow()
    scene.render()
