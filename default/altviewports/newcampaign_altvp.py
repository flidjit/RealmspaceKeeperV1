import tkinter as tk
from MetaNexusv1.default.engine.datatypes import ui_clrs, CampaignData
from MetaNexusv1.default.engine.altvp import AltViewport

"""
ToDo:
    * User selection target.
    * Display selected pin title.
    * Display map name.
"""


class NewCampaignAltVP(AltViewport):
    def __init__(self, master=None, mother=None, partner=None):
        super().__init__(master)
        self.mother = mother
        self.partner = partner
        if mother:
            self.colors = self.mother.the_user.player_data.ui_colors
        else:
            self.colors = ui_clrs
        self.configure(bg=self.colors['BG #4'])

        self.campaign_name_label = tk.Label(
            self, text='Campaign Name:',
            bg=self.colors['BG #4'], fg=self.colors['Dim #4'])
        self.campaign_name_label.place(
            x=10, y=10, width=150, height=20)
        self.campaign_name_entry = tk.Entry(
            self, bg=self.colors['BG #1'], fg=self.colors['Bright #1'],
            borderwidth=0,
            insertbackground=self.colors['Bright #4'],
            insertwidth=5,
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.campaign_name_entry.place(
            x=150, y=10, width=240, height=20)

        self.technology_level_scale = tk.Scale(
            self, from_=0, to=5, orient=tk.HORIZONTAL,
            borderwidth=0, highlightthickness=0,
            background=self.colors['BG #3'],
            foreground=self.colors['Normal #2'],
            troughcolor=self.colors['BG #2'],
            length=200, label='Technology Level:')
        self.technology_level_scale.place(
            x=10, y=40, height=60, width=150)
        self.fantasy_level_scale = tk.Scale(
            self, from_=0, to=5, orient=tk.HORIZONTAL,
            borderwidth=0, highlightthickness=0,
            background=self.colors['BG #3'],
            foreground=self.colors['Normal #2'],
            troughcolor=self.colors['BG #2'],
            length=200, label='Fantasy Level:')
        self.fantasy_level_scale.place(
            x=10, y=110, height=60, width=150)

        self.campaign_description_lbl = tk.Label(
            self, text='Campaign Description / Headline:',
            bg=self.colors['BG #4'],
            fg=self.colors['Normal #1'])
        self.campaign_description_lbl.place(
            x=10, y=180)
        self.campaign_description_text = tk.Text(
            self, bg=self.colors['BG #1'],
            fg=self.colors['Bright #1'],
            borderwidth=0,
            insertbackground=self.colors['Bright #4'],
            insertwidth=5,
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.campaign_description_text.place(
            x=10, y=200, width=380, height=190)

        self.create_campaign_button = tk.Button(
            self, text='Create Campaign',
            bg=self.colors['BG #3'],
            fg=self.colors['Normal #3'],
            command=self.create_new_campaign)
        self.create_campaign_button.place(
            x=640, y=360, height=30, width=150)

        self.technology_level_scale.set(1)
        self.fantasy_level_scale.set(1)

    def create_new_campaign(self):
        cn = self.campaign_name_entry.get()
        tl = self.technology_level_scale.get()
        fl = self.fantasy_level_scale.get()
        ds = self.campaign_description_text.get("1.0", tk.END)
        cp = CampaignData(
            name=cn, description=ds,
            technology_level=tl, fantasy_level=fl)
        self.mother.the_user.new_campaign(campaign_data=cp)
        self.mother.the_tabs.enable_tabs()
        self.exit_me()
        self.mother.the_user.save_campaign_data()
        self.partner.populate_location_list()

    def exit_me(self):
        self.destroy()

# root = tk.Tk()
# root.configure(width=900, height=530, bg='black')
# test = NewCampaignAltVP(root)
# root.mainloop()
