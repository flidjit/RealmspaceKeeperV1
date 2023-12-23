import tkinter as tk
import importlib

from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr

from default.aoamarquee import AOAMarquee
from viewbot import ViewBot
from textbot import TextBot
from userbot import UserBot
from tabbot import TabBot
from default.tools import get_basic_style


class Mother(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')

        self.startTk()
        self.root = self.tkRoot
        self.root['bg'] = 'black'
        self.root.geometry("1300x680")
        self.root.resizable(False, False)

        self.mother_frame = tk.Canvas(
            self.root, bg='black',
            highlightthickness=0, borderwidth=0)
        self.mother_frame.place(
            x=0, y=0, width=1300, height=680)

        self.the_user = UserBot(self)
        self.the_view = ViewBot(self)
        self.the_chat = TextBot(self)
        self.the_tabs = TabBot(self)
        self.the_system = None
        self.announcements = AOAMarquee(self.root)

        self.load_rpsystem()
        self.initialize_the_view()
        self.ttk_style = get_basic_style(
            self.the_user.player_data.ui_colors)

        self.bg_image_path = 'rec/img/uibg.png'
        self.bg_image = tk.PhotoImage(
            file=self.bg_image_path)
        self.mother_frame.create_image(
            0, 0, anchor=tk.NW, image=self.bg_image)

        self.updateTask = taskMgr.add(
            self.update, "update")

    def initialize_the_view(self):
        props = WindowProperties()
        self.root.update()
        props.setParentWindow(
            self.the_view.viewport.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.openDefaultWindow(props=props)
        self.setBackgroundColor(0.007, 0, 0.007, 1)

    def load_rpsystem(self):
        imp = "RPS."+self.the_user.player_data.current_rps_key
        thesystem = importlib.import_module(imp+'.systembot')
        self.the_system = thesystem.SystemBot(self)

    def update(self, task):
        self.root.update()
        self.the_user.update()
        self.the_system.update()
        self.the_view.update()
        return task.cont


mother = Mother()
mother.root.mainloop()
