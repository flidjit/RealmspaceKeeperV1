import tkinter as tk
from tkinter import ttk
import MetaNexusv1.default.engine.datatypes as dt
import MetaNexusv1.default.text.macros as macro


class TextBot(tk.Frame):
    """ TextBot Portfolio:
    -    Holds in-game console widgets.
    -    Handles user commands typed into the console. """

    def __init__(self, mother=None):
        super().__init__(mother.root,
                         highlightthickness=0, borderwidth=0)
        self._mother = mother
        self._p_dat = mother.the_user.player_data
        self._colors = self._p_dat.ui_colors
        self.configure(bg=self._colors['BG #3'])

        self.log = None
        self.usr_input = None
        self.scrollbar = None

        self.p_comm = []
        self.commands = {
            'say': lambda: self.cc_says(),
            'roll': lambda: self.cc_roll()}

        self.tags = [['player_tag', 'Dim #1'],
                     ['character_tag', 'Normal #2'],
                     ['chat_macro_tag', 'Normal #3'],
                     ['narrator_tag', 'Dim #4'],
                     ['error_tag', 'Warning'],
                     ['die_roll_tag', 'Normal #4']]
        self.build_me()

    def build_me(self):
        self.log = tk.Text(
            self, bg=self._colors['BG #2'], fg='white',
            font=('Consolas', 12), highlightthickness=0,
            borderwidth=0, wrap=tk.WORD)
        self.log.place(x=0, y=0, width=790, height=242)

        self.usr_input = tk.Entry(
            self, bg=self._colors['BG #1'], fg=self._colors['Bright #4'],
            insertbackground=self._colors['Bright #2'],
            insertwidth=5, borderwidth=0,
            highlightcolor=self._colors['Highlight #2'],
            highlightbackground=self._colors['Highlight #1'])
        self.usr_input.place(x=10, y=248, height=20, width=760)
        self.usr_input.bind(
            '<Return>', lambda event: self.parse_input())

        self.scrollbar = ttk.Scrollbar( self, command=self.log.yview)
        self.scrollbar.place(x=780, y=0, height=275, width=20)
        self.log.config(yscrollcommand=self.scrollbar.set)

        self.place(x=15, y=508, width=800, height=275)
        self.log.insert(tk.END, macro.welcome_macro, 'player_tag')
        self.log.yview(tk.END)
        for t in self.tags:
            self.log.tag_configure(
                t[0], foreground=self._colors[t[1]])

    def parse_input(self):
        words = self.usr_input.get()
        if words.startswith('/'):
            words = words.split(maxsplit=1)
            self.p_comm = [words[0] if words else "",
                           words[1] if len(words) > 1 else ""]
            self.execute_command_and_get_text()
        else:
            output = [
                self._p_dat.name + ': ' + words + '\n', 'player_tag']
        self.log.insert(tk.END, self.p_comm[0], self.p_comm[1])
        self.log.yview(tk.END)
        self.usr_input.delete(0, tk.END)

    def execute_command_and_get_text(self):
        if self.p_comm[0]:
            character_name = self._p_dat.current_character_key
            command = self.p_comm[0].strip('/')
            if command in self.commands:
                message = self.commands[command]()
                return [message, 'chat_macro_tag']
            elif command in macro.emote_macro:
                message = character_name + macro.emote_macro[command]
                return [message, 'chat_macro_tag']
            else:
                return ['Invalid command: ' + command, 'error_tag']

    def cc_says(self):
        character_name = self._p_dat.current_character_key
        chat_string = character_name + 'says, ' + self.p_comm[1] + '\n'
        return [chat_string, 'character_tag']

    def cc_roll(self, die_roll=None):
        if not die_roll:
            die_roll = dt.DieRoll(
                rolled_by=self._p_dat.name, faces=20, multiplier=2, bonus=1,
                rolls=None, total=0, roll_me=True)
        chat_string = die_roll.roll_string+'\n'
        return [chat_string, 'character_tag']

    def system_message(self, text=' No system message...'):
        self.log.insert(tk.END, text, 'narrator_tag')
        self.log.yview(tk.END)
