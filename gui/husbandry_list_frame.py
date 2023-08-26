import tkinter as tk
from tkinter import ttk

from gui.vertical_scrolled_frame import VerticalScrolledFrame
from animal_organization import AnimalHusbandry, AnimalCluster

class ClusterFrame(ttk.Frame):
    def __init__(self, master, cluster):
        super().__init__(master)

        self.stLabel = ttk.Label(self, text=cluster.subType.subType)
        self.stLabel.grid(column=0, row=0, columnspan=2, sticky=(tk.EW))

        self.countLabel = ttk.Label(self, text="Count: " + str(cluster.count))
        self.countLabel.grid(column=0, row=1, sticky=(tk.EW))

        self.ageLabel = ttk.Label(self, text="Age: " + str(cluster.age))
        self.ageLabel.grid(column=1, row=1, sticky=(tk.EW))

class HusbandryElementFrame(ttk.Frame):
    def __init__(self, master, husbandry):
        super().__init__(master)

        s = ttk.Style()
        s.configure('Title.TLabel', background='gray', borderwidth=5, font='helvetica 18')

        self.husbandry = husbandry

        self.title = ttk.Label(self, text=husbandry.name, style="Title.TLabel")
        self.title.grid(column=0, row=0, sticky=(tk.EW))

        self.clusterElements = []

        self.enabledVar = tk.BooleanVar()
        self.enabledVar.set(husbandry.enabled)
        self.enabledCheck = ttk.Checkbutton(self, command=self.enabledChanged, variable=self.enabledVar)
        self.enabledCheck.grid(column=1, row=0)

        for idx, cluster in enumerate(husbandry.clusters):
            self.clusterElements.append(ClusterFrame(self, cluster))
            self.clusterElements[idx].grid(column=0, row=idx+1, columnspan=2, sticky=(tk.EW))
        
    def enabledChanged(self):
        self.husbandry.enabled = self.enabledVar.get()
        self.master.master.master.forwardRecalc()

class HusbandryListFrame(VerticalScrolledFrame):
    def __init__(self, master, height, husbandries):
        super().__init__(master, height)

        self.husbandryElements = []

        for idx, husbandry in enumerate(husbandries):
            self.husbandryElements.append(HusbandryElementFrame(self.interior, husbandry))
            self.husbandryElements[idx].grid(column=0, row=idx, padx=5, pady=5, sticky=(tk.EW))

    def forwardRecalc(self):
        self.master.forwardRecalc()


        
