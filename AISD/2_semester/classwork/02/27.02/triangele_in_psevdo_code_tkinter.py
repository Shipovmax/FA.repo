import tkinter as tk


class Triangle:
    def __init__(
        self, vertex_a_x, vertex_a_y, vertex_b_x, vertex_b_y, vertex_c_x, vertex_c_y
    ):
        self.vertex_a_x = vertex_a_x
        self.vertex_a_y = vertex_a_y
        self.vertex_b_x = vertex_b_x
        self.vertex_b_y = vertex_b_y
        self.vertex_c_x = vertex_c_x
        self.vertex_c_y = vertex_c_y

    def _draw_outline(self, canvas, start_x, start_y, end_x, end_y):
        current_x = start_x
        current_y = start_y
        distance_x = abs(end_x - start_x)
        distance_y = abs(end_y - start_y)

        step_x = 1 if start_x < end_x else -1
        step_y = 1 if start_y < end_y else -1

        accumulated_error = distance_x - distance_y

        while True:
            if 0 <= current_y < 40 and 0 <= current_x < 40:
                canvas[current_y][current_x] = "*"

            if current_x == end_x and current_y == end_y:
                break

            double_error = accumulated_error * 2

            if double_error > -distance_y:
                accumulated_error -= distance_y
                current_x += step_x

            if double_error < distance_x:
                accumulated_error += distance_x
                current_y += step_y

    def get_grid(self):
        canvas = [["." for _ in range(40)] for _ in range(40)]
        self._draw_outline(
            canvas, self.vertex_a_x, self.vertex_a_y, self.vertex_b_x, self.vertex_b_y
        )
        self._draw_outline(
            canvas, self.vertex_b_x, self.vertex_b_y, self.vertex_c_x, self.vertex_c_y
        )
        self._draw_outline(
            canvas, self.vertex_c_x, self.vertex_c_y, self.vertex_a_x, self.vertex_a_y
        )
        return canvas

    def _fill_area(self, canvas):
        min_x = max(0, min(self.vertex_a_x, self.vertex_b_x, self.vertex_c_x))
        max_x = min(39, max(self.vertex_a_x, self.vertex_b_x, self.vertex_c_x))
        min_y = max(0, min(self.vertex_a_y, self.vertex_b_y, self.vertex_c_y))
        max_y = min(39, max(self.vertex_a_y, self.vertex_b_y, self.vertex_c_y))

        for current_y in range(min_y, max_y + 1):
            for current_x in range(min_x, max_x + 1):
                cross_product_ab = (self.vertex_b_x - self.vertex_a_x) * (
                    current_y - self.vertex_a_y
                ) - (self.vertex_b_y - self.vertex_a_y) * (current_x - self.vertex_a_x)
                cross_product_bc = (self.vertex_c_x - self.vertex_b_x) * (
                    current_y - self.vertex_b_y
                ) - (self.vertex_c_y - self.vertex_b_y) * (current_x - self.vertex_b_x)
                cross_product_ca = (self.vertex_a_x - self.vertex_c_x) * (
                    current_y - self.vertex_c_y
                ) - (self.vertex_a_y - self.vertex_c_y) * (current_x - self.vertex_c_x)

                is_inside = (
                    cross_product_ab >= 0
                    and cross_product_bc >= 0
                    and cross_product_ca >= 0
                ) or (
                    cross_product_ab <= 0
                    and cross_product_bc <= 0
                    and cross_product_ca <= 0
                )

                if is_inside:
                    canvas[current_y][current_x] = "*"


def render_gui():
    root = tk.Tk()
    root.title("Алгоритм Брезенхема")
    root.configure(bg="#000000")

    cell_size = 15
    grid_size = 40
    canvas_size = grid_size * cell_size

    tk_canvas = tk.Canvas(
        root, width=canvas_size, height=canvas_size, bg="#1e1e1e", highlightthickness=0
    )
    tk_canvas.pack(padx=20, pady=20)

    triangle = Triangle(20, 5, 5, 30, 35, 30)
    grid = triangle.get_grid()

    for y in range(grid_size):
        for x in range(grid_size):
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            if grid[y][x] == "*":
                tk_canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#2ccdd2", outline="#000000"
                )
            else:
                tk_canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#1e1e1e", outline="#000000"
                )

    root.mainloop()


if __name__ == "__main__":
    render_gui()
