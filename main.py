import tkinter as tk
from tkinter import ttk, messagebox
import math
import random


class EulerCirclesDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Круги Эйлера - Визуализатор")
        self.root.geometry("900x700")

        self.numbers_A = set()
        self.numbers_B = set()

        self.colors = {
            'A_only': '#FF9999',
            'B_only': '#9999FF',
            'intersection': '#FF99FF',
            'outside': '#E0E0E0'
        }

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        ttk.Label(control_frame, text="Множество A (числа через пробел):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_A = ttk.Entry(control_frame, width=30)
        self.entry_A.grid(row=1, column=0, pady=5)
        self.entry_A.insert(0, "1 2 3 4 5")

        ttk.Label(control_frame, text="Множество B (числа через пробел):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_B = ttk.Entry(control_frame, width=30)
        self.entry_B.grid(row=3, column=0, pady=5)
        self.entry_B.insert(0, "4 5 6 7 8")

        ttk.Button(control_frame, text="Обновить диаграмму", command=self.update_diagram).grid(row=4, column=0, pady=10)

        ttk.Button(control_frame, text="Случайные числа", command=self.random_numbers).grid(row=5, column=0, pady=5)

        info_frame = ttk.LabelFrame(control_frame, text="Информация", padding="10")
        info_frame.grid(row=6, column=0, pady=10, sticky=(tk.W, tk.E))

        self.info_text = tk.Text(info_frame, width=30, height=14, font=("Arial", 10))  # Увеличил высоту
        self.info_text.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=scrollbar.set)

        canvas_frame = ttk.LabelFrame(main_frame, text="Диаграмма Эйлера-Венна", padding="10")
        canvas_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        self.canvas = tk.Canvas(canvas_frame, width=500, height=500, bg='white', highlightthickness=1,
                                highlightbackground='gray')
        self.canvas.grid(row=0, column=0)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        legend_frame = ttk.Frame(canvas_frame)
        legend_frame.grid(row=1, column=0, pady=10)

        self.create_legend(legend_frame)

        self.update_diagram()

    def create_legend(self, parent):
        frame_a = ttk.Frame(parent)
        frame_a.pack(side=tk.LEFT, padx=20)

        canvas_a = tk.Canvas(frame_a, width=20, height=20, bg=self.colors['A_only'],
                             highlightthickness=1, highlightbackground='black')
        canvas_a.pack(side=tk.LEFT, padx=2)

        ttk.Label(frame_a, text="Круг A", font=("Arial", 10, "bold")).pack(side=tk.LEFT)

        frame_b = ttk.Frame(parent)
        frame_b.pack(side=tk.LEFT, padx=20)

        canvas_b = tk.Canvas(frame_b, width=20, height=20, bg=self.colors['B_only'],
                             highlightthickness=1, highlightbackground='black')
        canvas_b.pack(side=tk.LEFT, padx=2)

        ttk.Label(frame_b, text="Круг B", font=("Arial", 10, "bold")).pack(side=tk.LEFT)

    def parse_numbers(self, text):
        try:
            numbers = set()
            for num in text.split():
                if num.strip():
                    numbers.add(int(num.strip()))
            return numbers
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целые числа через пробел")
            return None

    def update_diagram(self):
        numbers_A = self.parse_numbers(self.entry_A.get())
        numbers_B = self.parse_numbers(self.entry_B.get())

        if numbers_A is None or numbers_B is None:
            return

        self.numbers_A = numbers_A
        self.numbers_B = numbers_B

        self.canvas.delete("all")

        self.draw_circles()

        self.update_info()

    def draw_circles(self):
        width = 500
        height = 500

        self.center1_x = width * 0.35
        self.center1_y = height * 0.5
        self.center2_x = width * 0.65
        self.center2_y = height * 0.5
        self.radius = 150

        self.canvas.create_rectangle(0, 0, width, height, fill=self.colors['outside'], outline='')
        self.draw_intersection()

        self.draw_circle_part(self.center1_x, self.center1_y, self.radius,
                              self.center2_x, self.center2_y, is_left=True)
        self.draw_circle_part(self.center2_x, self.center2_y, self.radius,
                              self.center1_x, self.center1_y, is_left=False)

        self.canvas.create_oval(self.center1_x - self.radius, self.center1_y - self.radius,
                                self.center1_x + self.radius, self.center1_y + self.radius,
                                outline='black', width=2, fill='')

        self.canvas.create_oval(self.center2_x - self.radius, self.center2_y - self.radius,
                                self.center2_x + self.radius, self.center2_y + self.radius,
                                outline='black', width=2, fill='')

        self.canvas.create_text(self.center1_x - 70, self.center1_y - 100, text="A", font=("Arial", 24, "bold"))
        self.canvas.create_text(self.center2_x + 70, self.center2_y - 100, text="B", font=("Arial", 24, "bold"))

        self.place_numbers()

    def draw_intersection(self):
        x1, y1 = self.center1_x, self.center1_y
        x2, y2 = self.center2_x, self.center2_y
        r = self.radius

        dx = x2 - x1
        dy = y2 - y1
        d = math.sqrt(dx * dx + dy * dy)

        if d < 2 * r and d > 0:
            a = (r * r - r * r + d * d) / (2 * d)
            h = math.sqrt(abs(r * r - a * a))

            x0 = x1 + a * dx / d
            y0 = y1 + a * dy / d

            rx = -dy * (h / d)
            ry = dx * (h / d)

            x3 = x0 + rx
            y3 = y0 + ry
            x4 = x0 - rx
            y4 = y0 - ry

            points = []

            start_angle1 = math.degrees(math.atan2(y3 - y1, x3 - x1))
            end_angle1 = math.degrees(math.atan2(y4 - y1, x4 - x1))

            start_angle2 = math.degrees(math.atan2(y4 - y2, x4 - x2))
            end_angle2 = math.degrees(math.atan2(y3 - y2, x3 - x2))

            self.canvas.create_polygon(self.arc_points(x1, y1, r, start_angle1, end_angle1) +
                                       self.arc_points(x2, y2, r, start_angle2, end_angle2),
                                       fill=self.colors['intersection'], outline='', smooth=True)

    def arc_points(self, cx, cy, r, start, end, num_points=50):
        points = []
        start_rad = math.radians(start)
        end_rad = math.radians(end)

        if end_rad < start_rad:
            end_rad += 2 * math.pi

        for i in range(num_points + 1):
            angle = start_rad + (end_rad - start_rad) * i / num_points
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.extend([x, y])

        return points

    def draw_circle_part(self, cx, cy, r, other_cx, other_cy, is_left):
        points = []

        for i in range(360):
            angle = math.radians(i)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)

            dist_to_other = math.sqrt((x - other_cx) ** 2 + (y - other_cy) ** 2)
            if dist_to_other > r - 0.1:
                points.extend([x, y])

        if points:
            self.canvas.create_polygon(points, fill=self.colors['A_only' if is_left else 'B_only'],
                                       outline='', smooth=True)

    def place_numbers(self):
        only_A = self.numbers_A - self.numbers_B
        only_B = self.numbers_B - self.numbers_A
        intersection = self.numbers_A & self.numbers_B

        only_A_str = ", ".join(map(str, sorted(only_A))) if only_A else "нет"
        only_B_str = ", ".join(map(str, sorted(only_B))) if only_B else "нет"
        intersection_str = ", ".join(map(str, sorted(intersection))) if intersection else "нет"

        self.canvas.create_text(self.center1_x - 50, self.center1_y, text=only_A_str,
                                font=("Arial", 10), width=80, justify='center')

        self.canvas.create_text(self.center2_x + 50, self.center2_y, text=only_B_str,
                                font=("Arial", 10), width=80, justify='center')

        self.canvas.create_text((self.center1_x + self.center2_x) / 2, self.center1_y - 30,
                                text=intersection_str, font=("Arial", 10),
                                width=80, justify='center')

    def update_info(self):
        self.info_text.delete(1.0, tk.END)

        only_A = self.numbers_A - self.numbers_B
        only_B = self.numbers_B - self.numbers_A
        intersection = self.numbers_A & self.numbers_B
        union = self.numbers_A | self.numbers_B

        info = [
            "СТАТИСТИКА:",
            "=" * 25,
            f"|A| = {len(self.numbers_A)}",
            f"|B| = {len(self.numbers_B)}",
            f"|A∩B| = {len(intersection)}",
            f"|A∪B| = {len(union)}",
            "",
            "Только A:",
            f"  кол-во: {len(only_A)}",
            f"  числа: {sorted(only_A) if only_A else 'нет'}",
            "",
            "Только B:",
            f"  кол-во: {len(only_B)}",
            f"  числа: {sorted(only_B) if only_B else 'нет'}",
            "",
            "Пересечение A∩B:",
            f"  кол-во: {len(intersection)}",
            f"  числа: {sorted(intersection) if intersection else 'нет'}",
            "",
            "Объединение A∪B:",
            f"  кол-во: {len(union)}",
            f"  числа: {sorted(union) if union else 'нет'}"
        ]

        self.info_text.insert(1.0, "\n".join(info))

    def random_numbers(self):
        a_numbers = set(random.sample(range(1, 21), random.randint(3, 7)))

        b_numbers = set(random.sample(range(1, 21), random.randint(3, 7)))

        self.entry_A.delete(0, tk.END)
        self.entry_A.insert(0, " ".join(map(str, sorted(a_numbers))))

        self.entry_B.delete(0, tk.END)
        self.entry_B.insert(0, " ".join(map(str, sorted(b_numbers))))

        self.update_diagram()

    def on_canvas_click(self, event):
        x, y = event.x, event.y

        in_A = math.sqrt((x - self.center1_x) ** 2 + (y - self.center1_y) ** 2) <= self.radius
        in_B = math.sqrt((x - self.center2_x) ** 2 + (y - self.center2_y) ** 2) <= self.radius

        if in_A and in_B:
            area = "Пересечение A∩B"
            numbers = self.numbers_A & self.numbers_B
        elif in_A:
            area = "Только A"
            numbers = self.numbers_A - self.numbers_B
        elif in_B:
            area = "Только B"
            numbers = self.numbers_B - self.numbers_A
        else:
            area = "Вне множеств"
            numbers = set()

        if numbers:
            messagebox.showinfo("Информация об области",
                                f"Область: {area}\n"
                                f"Количество элементов: {len(numbers)}\n"
                                f"Элементы: {sorted(numbers)}")
        else:
            messagebox.showinfo("Информация об области",
                                f"Область: {area}\n"
                                f"В этой области нет элементов")


def main():
    root = tk.Tk()
    app = EulerCirclesDrawer(root)
    root.mainloop()


if __name__ == "__main__":
    main()