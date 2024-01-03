import tkinter as tk

from MetaNexusv1.default.engine.tools import DatTool


class AltViewport(tk.Canvas):
    def __init__(self, master=None, backdrop_image_path=None):
        super().__init__(
            master, width=800, height=400,
            highlightthickness=0, borderwidth=0, bg='black')
        self.backdrop_image_path = backdrop_image_path
        self.backdrop_image = None
        self.backdrop = None
        self.responding = True
        self.place(x=15, y=55, width=800, height=400)
        self.draw_backdrop()

    def draw_backdrop(self):
        if self.backdrop_image_path:
            self.backdrop_image = tk.PhotoImage(
                file=self.backdrop_image_path)
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
        self.bind("<ButtonPress-3>", self.on_right_click)
        self.bind("<B3-Motion>", self.on_right_click_and_drag)
        self.bind("<ButtonRelease-3>", self.on_right_click_release)

    def on_right_click(self, event):
        if self.responding:
            self.start_x = event.x
            self.start_y = event.y

    def on_right_click_and_drag(self, event):
        if self.responding:
            delta_x = event.x - self.start_x
            self.image_offset[0] += delta_x
            delta_y = event.y - self.start_y
            self.image_offset[1] += delta_y
            self.move(self.image_item, delta_x, delta_y)
            self.start_x = event.x
            self.start_y = event.y

    def on_right_click_release(self, event):
        if self.responding:
            pass  # You can add additional actions here if needed

    def show_image(self, image_data):
        try:
            img_ = DatTool.data_to_tk(image_data)
            self.image_item = self.create_image(
                self.image_offset[0], self.image_offset[1],
                anchor=tk.NW, image=img_)
            self.image = img_
            self.itemconfig(self.image_item, image=self.image)
        except Exception as e:
            print(f"Error loading image: {e}")

