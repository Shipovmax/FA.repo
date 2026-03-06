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


    def draw(self):
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

        print("\nПоле 40x40 (Треугольник):")
        for row in canvas:
            print("".join(row))


filled_triangle = Triangle(20, 5, 5, 30, 35, 30)
filled_triangle.draw()
