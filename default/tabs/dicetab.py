import tkinter as tk
import MetaNexusv1.default.engine.datatypes as dt


class DiceTab(tk.Canvas):
    NAME = 'Die Roller'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, highlightthickness=0, borderwidth=0,
                         *args, **kwargs)
        self._mother = mother
        self._chat = mother.the_chat
        self._user_name = mother.the_user.player_data.name

        self._colors = mother.the_user.player_data.ui_colors
        self.configure(bg=self._colors['BG #3'])

        self.nameplate = tk.Label(
            self, text="Die Roller",
            font=('courier', 18, 'bold'),
            highlightthickness=0, borderwidth=0,
            bg=self._colors['BG #3'], fg=self._colors['Dim #1'])
        self.nameplate.place(x=15, y=15)

        self.backdrop_image_path = 'default/tabs/img/dicetab/background.png'
        self.backdrop_image = tk.PhotoImage(file=self.backdrop_image_path)
        self.backdrop = self.create_image(
            7, 47, anchor=tk.NW,
            image=self.backdrop_image)

        self.dice_types = dt.dice_types
        self.selected_key = 'd4'
        self.selected_multiplier = 1
        self.selected_bonus = 0
        self.chat_string = ''

        self.prepare_dice_images()
        self.selected_image = self.create_image(
            0, 0, anchor='nw',
            image=self.dice_types[self.selected_key]['Image'])
        self.move_selector()

        self.roll_image_path = 'default/tabs/img/dicetab/rollme.png'
        self.roll_image = tk.PhotoImage(file=self.roll_image_path)
        self.roll_button = tk.Button(
            self, image=self.roll_image,
            highlightthickness=0, borderwidth=0,
            command=self.roll_button_clicked)
        self.roll_button.place(x=230, y=220, width=96, height=45)

        self.roll_request_label = tk.Label(
            self, text="/roll 1d4",
            font=('courier', 14, 'bold'),
            highlightthickness=0, borderwidth=0,
            bg=self._colors['BG #3'], fg=self._colors['Bright #1'])
        self.roll_request_label.place(x=20, y=290)

        self.bind("<Button-1>", self.surface_clicked)

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
                self.selected_key = dice_type
                self.move_selector()
                self.get_chat_string()
                print(dice_type+' clicked.\n')

    def get_chat_string(self):
        t = str(self.selected_multiplier)
        t += str(self.selected_key)
        if self.selected_bonus > 0:
            t += '+'+str(self.selected_bonus)
        self.chat_string = t
        self.roll_request_label.configure(text='/roll '+self.chat_string)

    def move_selector(self):
        selected_dice_info = self.dice_types[self.selected_key]
        x_pos, y_pos = selected_dice_info['Placement']
        self.coords(self.selected_image, x_pos, y_pos)
        self.itemconfig(self.selected_image, image=selected_dice_info['Image'])

    def roll_button_clicked(self):
        f = int(self.selected_key.strip('d'))
        m = self.selected_multiplier
        b = self.selected_bonus
        roll = dt.DieRoll(rolled_by=self._user_name, faces=f, multiplier=m, bonus=b)
        self._chat.cc_roll(die_roll=roll)
        self.selected_multiplier = 1
        self.selected_bonus = 0
        self.get_chat_string()

# root = tk.Tk()
# root.configure(width=900, height=530, bg='black')
# test = DiceTab(root)
# root.mainloop()
