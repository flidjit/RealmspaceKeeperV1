import tkinter as tk
from tkinter import ttk


class DynoTab(ttk.Notebook):
    def __init__(self, master=None, mother=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.mother = mother
        self.tabs_dict = {}
        self.icon_path_dict = {}
        self.icon_image_dict = {}

    def disable_me(self):
        self.state(["disabled"])
        for tab in self.tabs_dict:
            try:
                self.get_tab(tab).state(["disabled"])
            except Exception:
                print(Exception)
            try:
                self.get_tab(tab).disable_me()
            except Exception:
                print(Exception)

    def enable_me(self):
        self.state(["!disabled"])
        for tab in self.tabs_dict:
            try:
                self.get_tab(tab).state(["!disabled"])
            except Exception:
                print(Exception)
            try:
                self.get_tab(tab).enable_me()
            except Exception:
                print(Exception)

    def add_custom_tab(self, tab_class,
                       icon_path='default/tabs/img/icons/t_minimap.png',
                       *args, **kwargs):
        tab = tab_class(self, self.mother, *args, **kwargs)
        self.icon_path_dict[tab.NAME] = icon_path
        self.icon_image_dict[tab.NAME] = tk.PhotoImage(
            file=self.icon_path_dict[tab.NAME])
        self.add(tab, text=tab.NAME,
                 image=self.icon_image_dict[tab.NAME])
        self.tabs_dict[tab.NAME] = tab
        return tab

    def get_tab(self, tab_key):
        return self.tabs_dict.get(tab_key)

    def remove_tab(self, tab_key):
        tab = self.tabs_dict.pop(tab_key, None)
        if tab:
            self.forget(tab)

