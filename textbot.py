import tkinter as tk
from tkinter import ttk
from default.macros import emote_macro


command_dict = {
    'say': lambda chat_section: chat_section.says()
}


class TextBot:
    """ TextBot Portfolio:
    -    Holds in-game console widgets.
    -    Handles user commands typed into the console. """

    def __init__(self, mother=None):
        self.mother = mother
        self.colors = mother.the_user.player_data.ui_colors
        self.frame = tk.Frame(
            self.mother.mother_frame,
            bg='black', highlightthickness=0, borderwidth=0)
        self.log = tk.Text(
            self.frame,
            bg=self.colors['BG #2'],
            fg='white',
            highlightthickness=0, borderwidth=0, wrap=tk.WORD)
        self.log.place(x=0, y=0, width=790, height=142)
        self.usr_input = tk.Entry(
            self.frame,
            bg=self.colors['BG #1'],
            fg='white',
            highlightthickness=0, borderwidth=0)
        self.usr_input.place(x=0, y=145, width=790, height=20)
        self.usr_input.bind(
            '<Return>', lambda event: self.evaluate_usr_input())
        self.scrollbar = ttk.Scrollbar(
            self.frame, command=self.log.yview)
        self.scrollbar.place(x=780, y=0, height=165, width=20)
        self.log.config(yscrollcommand=self.scrollbar.set)

        self.commands = command_dict
        tags = [['player_tag', 'Chat #1'],
                ['character_tag', 'Chat #2'],
                ['chat_macro_tag', 'Chat #3'],
                ['narrator_tag', 'Chat #4'],
                ['invalid_command_tag', 'Chat #5'],
                ['die_roll_tag', 'Chat #6']]
        for t in tags:
            self.log.tag_configure(
                t[0], foreground=self.colors[t[1]])

        self.frame.place(x=15, y=508, width=800, height=165)

    def evaluate_usr_input(self):
        user_input = self.usr_input.get()
        words = user_input.split()
        player_name = self.mother.the_user.player_data.name
        character_name = self.mother.the_user.player_data.current_character_key

        if words and words[0].startswith('/'):
            command = words[0][1:]
            if command in self.commands:
                self.commands[command](self)
            elif command in emote_macro:
                # If the command is in chat_macro, append the macro text to the message
                message = f"{character_name}{emote_macro[command]}"
                self.log.insert(tk.END, f"{message}\n", 'chat_macro_tag')
            else:
                self.log.insert(tk.END, f"Invalid command: {command}\n", 'invalid_command_tag')
        else:
            self.log.insert(tk.END, f"{player_name}: {user_input}\n", 'player_tag')

        # Scroll to the end
        self.log.yview(tk.END)

        self.usr_input.delete(0, tk.END)

    def says(self):
        character_name = self.mother.the_user.player_data.current_character_key
        user_input = self.usr_input.get()

        words = user_input.split(maxsplit=1)
        command = words[0] if words else ""
        message = words[1] if len(words) > 1 else ""

        self.log.insert(tk.END, f"{character_name} says: {message}\n",
                        'character_tag')
        self.log.yview(tk.END)

    def system_message(self, text=' No system message...'):
        self.log.insert(tk.END, text, 'narrator_tag')
        self.log.yview(tk.END)
