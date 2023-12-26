import tkinter as tk
from tkinter import ttk
import os
from default.altvp import AltViewport
from default.datatypes import GameMode
from userbot import UserBot
from default.aoamarquee import AOAMarquee
from default.macros import marquee_macro


class StartupAltVP(AltViewport):
    def __init__(self, master=None, mother=None):
        super().__init__(master, backdrop_image_path="rec/img/bg1.png")
        self.mother = mother
        self.colors = self.mother.the_user.player_data.ui_colors

        rps_list = tk.StringVar()  # ??
        self.rps_combobox = ttk.Combobox(
            self, font=('Courier', 15),
            textvariable=rps_list, state="readonly")
        self.rps = []
        self.scan_for_rps()
        self.rps_combobox['values'] = self.rps
        self.rps_combobox.place(
            x=480, y=250, width=300)

        self.pc_button = tk.Button(
            self, bg=self.colors['BG #4'],
            fg=self.colors['Bright #1'],
            font=('Courier', 25),
            text='PC Mode',
            command=self.pc_mode_selected)
        self.pc_button.place(x=480, y=285, width=300, height=50)
        self.gm_button = tk.Button(
            self, bg=self.colors['BG #3'],
            fg=self.colors['Bright #3'],
            font=('Courier', 25),
            text='GM Mode',
            command=self.gm_mode_selected)
        self.gm_button.place(x=480, y=340, width=300, height=50)

        self.load_list = []
        self.load_listbox = None
        self.ok_btn = None

        self.usr_name = None
        self.usr_email = None
        self.usr_male = None
        self.usr_female = None
        self.gender_var = tk.IntVar()

        self.rps_combobox.current(0)
        self.rps_combobox.update()

        self.new_player_check()

    def pc_mode_selected(self):
        self.mother.the_user.player_data.game_mode = GameMode.PLAYER_
        self.finish_up()

    def gm_mode_selected(self):
        self.mother.the_user.player_data.game_mode = GameMode.GM_
        self.finish_up()

    def finish_up(self):
        self.mother.the_user.player_data.current_rps_key = self.rps_combobox.get()
        if self.usr_name:
            self.mother.the_user.player_data.name = self.usr_name.get()
            self.mother.the_user.player_data.email = self.usr_email.get()
            self.mother.the_user.player_data.is_male = self.gender_var.get()
        self.mother.the_user.save_player_data()
        self.mother.the_tabs.change_tab_modes()
        self.destroy()

    def new_player_check(self):
        try:
            self.mother.the_user.load_player_data()
            print("Returning player: " + self.mother.the_user.player_data.name)
        except FileNotFoundError:
            self.mother.the_user = UserBot()
            self.mother.the_user.save_player_data()

        if self.mother.the_user.player_data.name == "New Player":
            print('New player detected!')
            self.usr_name = tk.Entry(
                self, bg=self.colors['BG #3'],
                fg=self.colors['Normal #2'])
            self.usr_name.place(x=500, y=150, width=250)
            self.usr_email = tk.Entry(
                self, bg=self.colors['BG #2'],
                fg=self.colors['Bright #1'])
            self.usr_email.place(x=500, y=175, width=250)
            self.usr_male = ttk.Radiobutton(
                self, text="Male", variable=self.gender_var, value=True)
            self.usr_male.place(x=500, y=200)
            self.usr_female = ttk.Radiobutton(
                self, text="Female", variable=self.gender_var, value=False)
            self.usr_female.place(x=600, y=200)

    def scan_for_rps(self):
        try:
            all_items = os.listdir('RPS')
            directories = [item for item in all_items if os.path.isdir(os.path.join('RPS', item))]
            self.rps.extend(directories)

            # Check if the combobox has any values before setting the current index
            if self.rps:
                self.rps_combobox['values'] = self.rps
                self.rps_combobox.current(0)
        except FileNotFoundError:
            print("RPS directory not found.")
        except Exception as e:
            print(f"Error scanning for RPS directories: {e}")


