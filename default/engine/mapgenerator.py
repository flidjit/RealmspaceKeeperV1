

import tkinter as tk
import random
from queue import PriorityQueue
from tkinter import simpledialog


class MapSettingsDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Number of Land Masses:").grid(row=0, column=0)
        tk.Label(master, text="Move Failure Probability:").grid(row=1, column=0)
        tk.Label(master, text="Minimum Land Mass Size:").grid(row=2, column=0)
        tk.Label(master, text="Maximum Land Mass Size:").grid(row=3, column=0)

        self.num_land_masses = tk.Entry(master)
        self.move_failure_probability = tk.Entry(master)
        self.min_land_mass_size = tk.Entry(master)
        self.max_land_mass_size = tk.Entry(master)

        self.num_land_masses.grid(row=0, column=1)
        self.move_failure_probability.grid(row=1, column=1)
        self.min_land_mass_size.grid(row=2, column=1)
        self.max_land_mass_size.grid(row=3, column=1)

        return self.num_land_masses  # Initial focus

    def apply(self):
        self.result = (
            int(self.num_land_masses.get()),
            float(self.move_failure_probability.get()),
            int(self.min_land_mass_size.get()),
            int(self.max_land_mass_size.get()))


class WorldMapGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("World Map Generator")
        self.geometry("1600x900")

        self.settings = self.get_user_settings()

        self.canvas = tk.Canvas(self, width=1600, height=900, bg="navy")  # Dark blue background
        self.canvas.pack()

        self.generate_world_map()

    def get_user_settings(self):
        dialog = MapSettingsDialog(self)
        return dialog.result

    def generate_world_map(self):
        num_land_masses, move_failure_probability, min_land_mass_size, max_land_mass_size = self.settings

        for _ in range(num_land_masses):
            land_mass_size = random.randint(min_land_mass_size, max_land_mass_size)
            start_x, start_y = random.randint(0, 1599), random.randint(0, 899)
            self.generate_land_mass(start_x, start_y, land_mass_size, move_failure_probability)

    def generate_land_mass(self, start_x, start_y, land_mass_size, move_failure_probability):
        land_color = "green"  # Green color

        def is_valid_move(x, y):
            # Wrap around if the coordinates go beyond the screen edges
            return 0 <= x < 1600 and 0 <= y < 900 and random.random() < move_failure_probability

        priority_queue = PriorityQueue()
        priority_queue.put((0, start_x, start_y))

        visited = set()

        while not priority_queue.empty() and len(visited) < land_mass_size:
            _, current_x, current_y = priority_queue.get()

            if (current_x, current_y) in visited:
                continue

            visited.add((current_x, current_y))

            # Draw a green dot on the canvas
            self.canvas.create_rectangle(current_x, current_y, current_x + 1, current_y + 1, fill=land_color, outline="")

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)

            for dx, dy in directions:
                new_x, new_y = (current_x + dx) % 1600, (current_y + dy) % 900
                if is_valid_move(new_x, new_y):
                    priority_queue.put((random.random(), new_x, new_y))


if __name__ == "__main__":
    app = WorldMapGenerator()
    app.mainloop()