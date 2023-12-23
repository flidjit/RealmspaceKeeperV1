import tkinter as tk
from tkinter import ttk
from default.datatypes import DieRoll


class DieRow(tk.Frame):
    def __init__(self, master=None, dice_type='', face_number=20, aoa_window=None):
        super().__init__(master=master, bg='black',
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


class DiceTab(tk.Frame):
    NAME = 'Dice'
    DICE_TYPES = [100, 20, 12, 10, 8, 6, 4]

    def __init__(self, notebook, aoa_window=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)
        self.aoa_window = aoa_window
        self.die_type = {}
        placement_mult = 0
        for i in self.DICE_TYPES:
            key = 'd' + str(i)
            self.die_type[key] = DieRow(self, key, i, aoa_window)
            self.die_type[key].place(y=60 * placement_mult + 60)
            placement_mult += 1
