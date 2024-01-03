import tkinter as tk
from tkinter import ttk


class PinMapEditorTab(tk.Frame):
    NAME = 'World Map'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)

        self._mother = mother
        self._view = mother.the_view
        self._user = mother.the_user
        self._tabs = mother.the_tabs
        self._chat = mother.the_chat

        self._colors = self._user.player_data.ui_colors
        self.configure(bg=self._colors['BG #3'])

        self.buttons_w = {}
        self.labels_w = {}
        self.listbox_w = None
        self.build_me()

        self.title_lbl = tk.Label(
            self, bg='black', fg='white',
            text='Pin Map Editor', font=('courier', 20, 'bold'))
        self.title_lbl.place(x=10, y=10)

        self.pin_label = tk.Label(self, text=' Pins: ')
        self.pin_label.place(x=10, y=30)
        self.pin_list = tk.Listbox(self)
        self.pin_list.place(x=10, y=60)

    def build_me(self):
        print('hi')

    def build_buttons(self):
        d_buttons = [
            ['Add Pin Button', 'Bright #2', 'BG #2',
             'Add', None,
             220, 40, 50, 25],
            ['Remove Pin Button', 'Bright #2', 'BG #2',
             'Remove', None,
             220, 40, 50, 25],
            ['Link Pin Button', 'Bright #2', 'BG #2',
             'Link', None,
             220, 40, 50, 25],
            ['Un-Link Pin Button', 'Bright #2', 'BG #2',
             'Un-Link', None,
             220, 40, 50, 25]]
