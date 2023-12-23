import random
import tkinter as tk
from tkinter import font


class AOAMarquee(tk.Frame):
    def __init__(self, master=None,
                 mq_font=("Times New Roman", 15, 'bold'),
                 mq_color='Yellow', text=' Text to scroll',
                 mq_bg='black', friction=30,
                 **kwargs):
        super().__init__(master, **kwargs)
        self.configure(highlightthickness=0, borderwidth=0)
        self.pack()
        self.canvas = tk.Canvas(
            self, bg=mq_bg, highlightthickness=0, borderwidth=0,
            height=30, width=655)
        self.canvas.place(x=0, y=0)
        self.mq_font = mq_font
        self.mq_color = mq_color
        self.categories = {
            'Tooltip': [],
            'News': [],
            'Campaign': [],
            'Recent Events': [],
            'Player Announcements': [],
            'GM  Announcements': []}
        # replace messages with categories.
        self.messages = [' 111 ', '222', '333']
        self.friction = friction
        self.text = text
        self.text_item = None
        self.text_width = 1
        self.place(x=16, y=466, height=30, width=655)
        self.init_marquee()

    def init_marquee(self):
        self.text_item = self.canvas.create_text(
            0, 15, text=self.text, fill=self.mq_color,
            anchor="w", font=self.mq_font)
        self.text_width = self.canvas.bbox(self.text_item, "all")[2]
        self.scroll_text()

    def scroll_text(self):
        self.canvas.move(self.text_item, -1, 0)
        x_pos = self.canvas.coords(self.text_item)[0]
        if x_pos + self.text_width <= 0:
            self.canvas.move(
                self.text_item,
                self.text_width+self.winfo_width(), 0)
            self.prepare_message()
        else:
            self.after(self.friction, self.scroll_text)

    def get_text_width(self):
        bbox = self.canvas.bbox(self.text_item)
        width = bbox[2] - bbox[0]
        return width

    def prepare_message(self):
        selection = random.randint(0, len(self.messages)-1)
        self.canvas.itemconfig(self.text_item, text=self.messages[selection])
        self.text_width = self.get_text_width()
        self.scroll_text()

    def receive_messages(self, add_message=None, new_set=None):
        if new_set:
            self.messages = new_set
        if add_message:
            self.messages.append(add_message)

