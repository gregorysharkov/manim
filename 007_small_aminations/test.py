from manim import *


class MyPythonCode(Scene):
    def construct(self):
        code_string = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Call the function
result = factorial(5)
print(f"The factorial of 5 is: {result}")
"""
        # Create a Code mobject
        rendered_code = Code(
            code_string=code_string,
            language="python",
            font_size=24,
            tab_width=4,
            line_numbers_from=1,
            add_line_numbers=True,
            background="window",  # or "rectangle"
            formatter_style="manni",  # or "default", "monokai", etc.
        )

        self.play(Create(rendered_code))
        self.wait(2)

        # You can also highlight specific lines later
        self.play(Indicate(rendered_code.get_line_by_number(3)))  # Highlight the 'if' line
        self.wait(1)
        self.play(Circumscribe(rendered_code.get_line_by_number(6)))  # Highlight the 'return' line
        self.wait(1)
