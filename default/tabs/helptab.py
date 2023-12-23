import tkinter as tk
from tkinter import ttk
from default.macros import help_data


class HelpTab(tk.Frame):
    NAME = 'Help'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother
        self.colors = self.mother.the_user.player_data.ui_colors
        self.configure(bg=self.colors['BG #2'])

        self.nameplate = tk.Label(
            self, text="Help",
            font=('courier', 18, 'bold'),
            highlightthickness=0, borderwidth=0,
            bg=self.colors['BG #4'], fg=self.colors['FG #1'])
        self.nameplate.place(x=15, y=15)

        self.help_treeview = ttk.Treeview(self)
        self.treeview_scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.help_treeview.yview)

        self.help_treeview.config(yscrollcommand=self.treeview_scrollbar.set)
        self.help_treeview.tag_configure(
            "item_tag", background=self.colors['BG #1'],
            foreground=self.colors['FG #4'])
        self.help_treeview.place(x=10, y=50, width=410, height=155)
        self.treeview_scrollbar.place(x=410, y=50, height=155)

        current_node = ""
        for topic in help_data.keys():
            if topic.startswith(" - "):
                self.help_treeview.insert(
                    current_node, "end", text=topic.lstrip(" - "),
                    values=(help_data[topic],), tags="item_tag")
            else:
                current_node = self.help_treeview.insert(
                    "", "end", text=topic,
                    values=(help_data[topic],), tags="item_tag")

        self.help_treeview.bind("<ButtonRelease-1>", self.display_selection)

        self.content = tk.Text(
            self, highlightthickness=0, borderwidth=0,
            bg=self.colors['BG #2'], fg=self.colors['FG #1'],
            wrap=tk.WORD, state=tk.DISABLED)
        self.content.place(x=10, y=220, width=420, height=350)

    def display_selection(self, event):
        selected_item = self.help_treeview.selection()
        if selected_item:
            # noinspection PyTypeChecker
            help_content = self.help_treeview.item(selected_item, "values")[0]
            self.content.config(state=tk.NORMAL)
            self.content.delete(1.0, tk.END)
            self.content.insert(tk.END, help_content)
            self.content.config(state=tk.DISABLED)