import tkinter as tk
from tkinter import ttk
from default.datatypes import DieRoll


class DieRow(tk.Frame):
    def __init__(self, master=None, dice_type='', face_number=20, aoa_window=None):
        super().__init__(master=master, bg='blue',
                         width=420, height=60)
        self.face_number = face_number
        self.number_var = tk.StringVar()
        self.number = ttk.Spinbox(
            self, from_=0, to=100, textvariable=self.number_var,
            font=("Arial", 18, "bold"))
        self.number.place(x=20, width=40)
        self.dice_type = dice_type
        self.die_image = tk.Label(self, bg='grey', text=dice_type)
        self.die_image.place(x=100, height=40, width=40)
        self.bonus_var = tk.StringVar()
        self.bonus = ttk.Spinbox(
            self, from_=0, to=100, textvariable=self.bonus_var,
            font=("Arial", 18, "bold"))
        self.bonus.place(x=180, width=40)
        self.roll_button = tk.Button(self, text='Roll', command=self.roll_dice)
        self.roll_button.place(x=250, height=40)
        self.aoa_window = aoa_window

    def roll_dice(self):
        number_of_dice = int(self.number_var.get())
        bonus = int(self.bonus_var.get())
        roll_string = f"{number_of_dice}d{self.face_number}+{bonus}"
        die_roll = DieRoll(rolled_by='Player', roll_string=roll_string,
                           faces=self.face_number, number=number_of_dice, bonus=bonus)
        die_roll.get_roll_string()
        result_text = die_roll.roll_string+'\n'
        self.aoa_window.the_chat.log.insert(tk.END, result_text, 'chat_macro_tag')


dice_types = {
    'd20': {
        'Faces': 20, 'Placement': [344, 36], 'Selected': False,
        'Image Path': 'default/tabs/img/dicetab/d20.png',
        'Image': None},
    'd12': {
        'Faces': 12, 'Placement': [281, 36], 'Selected': False,
        'Image Path': 'default/tabs/img/dicetab/d12.png',
        'Image': None},
    'd10': {
        'Faces': 10, 'Placement': [218, 36], 'Selected': False,
        'Image Path': 'default/tabs/img/dicetab/d10.png',
        'Image': None},
    'd8': {
        'Faces': 8, 'Placement': [155, 36], 'Selected': False,
        'Image Path': 'default/tabs/img/dicetab/d8.png',
        'Image': None},
    'd6': {
        'Faces': 6, 'Placement': [92, 36], 'Selected': False,
        'Image Path': 'default/tabs/img/dicetab/d6.png',
        'Image': None},
    'd4': {
        'Faces': 4, 'Placement': [29, 36], 'Selected': False,
        'Image Path': 'default/tabs/img/dicetab/d4.png',
        'Image': None}}


class DiceTab(tk.Frame):
    NAME = 'Die Roller'

    def __init__(self, notebook, aoa_window=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)
        self.aoa_window = aoa_window
        self.colors = aoa_window.the_user.player_data.ui_colors
        self.configure(bg=self.colors['BG #3'])

        self.nameplate = tk.Label(
            self, text="Die Roller",
            font=('courier', 18, 'bold'),
            highlightthickness=0, borderwidth=0,
            bg=self.colors['BG #3'], fg=self.colors['Dim #1'])
        self.nameplate.place(x=15, y=15)

        self.surface = tk.Canvas(
            self, bg=self.colors['BG #4'],
            highlightthickness=0, borderwidth=0)
        self.surface.place(x=0, y=50, width=434, height=700)
        self.backdrop_image_path = 'default/tabs/img/dicetab/background.png'
        self.backdrop_image = tk.PhotoImage(file=self.backdrop_image_path)
        self.backdrop = self.surface.create_image(
            7, 7, anchor=tk.NW,
            image=self.backdrop_image)

        self.dice_types = dice_types
        self.selected_type = 'd4'
        self.selected_multiplier = 1
        self.selected_bonus = 0
        self.chat_string = ''

        self.prepare_dice_images()
        self.selected_image = self.surface.create_image(
            0, 0, anchor='nw',
            image=self.dice_types[self.selected_type]['Image'])
        self.move_selector()

        self.roll_image_path = 'default/tabs/img/dicetab/rollme.png'
        self.roll_image = tk.PhotoImage(file=self.roll_image_path)
        self.roll_button = tk.Button(
            self.surface, image=self.roll_image,
            highlightthickness=0, borderwidth=0,
            command=self.roll_button_clicked)
        self.roll_button.place(x=230, y=180, width=96, height=45)

        self.roll_request_label = tk.Label(
            self.surface, text="/roll",
            font=('courier', 14, 'bold'),
            highlightthickness=0, borderwidth=0,
            bg=self.colors['BG #3'], fg=self.colors['Bright #1'])
        self.roll_request_label.place(x=20, y=250)

        self.surface.bind("<Button-1>", self.surface_clicked)

    def prepare_dice_images(self):
        for dice_type in self.dice_types:
            image_path = self.dice_types[dice_type]['Image Path']
            x, y = self.dice_types[dice_type]['Placement']
            image = tk.PhotoImage(file=image_path)
            self.dice_types[dice_type]['Image'] = image

    def surface_clicked(self, event):
        x, y = event.x, event.y
        for dice_type in self.dice_types:
            x_pos, y_pos = self.dice_types[dice_type]['Placement']
            if x_pos <= x <= x_pos + 63 and y_pos <= y <= y_pos + 89:
                self.selected_type = dice_type
                self.move_selector()
                self.get_chat_string()
                print(dice_type+' clicked.\n')

    def get_chat_string(self):
        t = '/roll '
        t += str(self.selected_multiplier)
        t += str(self.selected_type)
        if self.selected_bonus > 0:
            t += '+'+str(self.selected_bonus)
        self.chat_string = t
        self.roll_request_label.configure(text=self.chat_string)

    def move_selector(self):
        selected_dice_info = self.dice_types[self.selected_type]
        x_pos, y_pos = selected_dice_info['Placement']
        self.surface.coords(self.selected_image, x_pos, y_pos)
        self.surface.itemconfig(self.selected_image, image=selected_dice_info['Image'])

    def roll_button_clicked(self):
        self.selected_bonus = 0
        self.selected_multiplier = 1
        print("Roll button clicked")


