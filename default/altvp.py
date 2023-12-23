import tkinter as tk
from tkinter import filedialog
from default.datatypes import OverworldMapData


class AltViewport(tk.Canvas):
    def __init__(self, master=None, backdrop_image_path=None):
        super().__init__(
            master, width=800, height=400,
            highlightthickness=0, borderwidth=0, bg='black')
        self.backdrop_image_path = backdrop_image_path
        self.backdrop_image = None
        self.backdrop = None
        self.place(x=15, y=55, width=800, height=400)
        self.draw_backdrop()

    def draw_backdrop(self):
        if self.backdrop_image_path:
            self.backdrop_image = tk.PhotoImage(file=self.backdrop_image_path)
            self.backdrop = self.create_image(
                0, 0, anchor=tk.NW, image=self.backdrop_image)


class ClickAndDragViewport(AltViewport):
    def __init__(self, master=None, backdrop_image_path=None):
        super().__init__(master, backdrop_image_path)
        self.start_x = None
        self.start_y = None
        self.image_offset = [0, 0]
        self.image_item = None
        self.image = None
        self.bind("<ButtonPress-3>", self.on_button_press)
        self.bind("<B3-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-3>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        self.move(self.image_item, delta_x, delta_y)
        self.start_x = event.x
        self.start_y = event.y

    def on_button_release(self, event):
        pass  # You can add additional actions here if needed

    def show_image(self, image_path):
        try:
            new_image = tk.PhotoImage(file=image_path)
            self.image_item = self.create_image(
                self.image_offset[0], self.image_offset[1],
                anchor=tk.NW, image=new_image)
            self.image = new_image
            self.itemconfig(self.image_item, image=self.image)
        except Exception as e:
            print(f"Error loading image: {e}")

