import tkinter as tk
from tkinter import ttk
from animal_types import AnimalSubType
from gui.husbandry_list_frame import HusbandryListFrame
from gui.product_list_frame import ProductListFrame
from gui.config_frame import ConfigFrame

from utility import calcInOut

class AnimalFoodFrame(ttk.Frame):
    def __init__(self, master, height, subTypes, husbandries, daysPerMonth, timeframe, ageFilter, subTypeFilter):
        super().__init__(master)        
        self.subTypes = subTypes
        self.husbandries = husbandries

        self.daysPerMonth = daysPerMonth
        self.timeframe = timeframe

        self.ageFilter = ageFilter
        self.subTypeFilter = subTypeFilter

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(1, weight=5)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.husbandryList = HusbandryListFrame(self, height, self.husbandries)
        self.husbandryList.grid(column=0, row=0, rowspan=2, sticky=tk.NSEW)

        self.configFrame = ConfigFrame(self, self.ageFilter, self.daysPerMonth, self.timeframe)
        self.configFrame.grid(column=2, row=0, rowspan=2, sticky=tk.NSEW)

        self.recalcProducts()

        self.grid(column=0, row=0, sticky=(tk.NSEW))
    
    def recalcProducts(self):

        self.ageFilter[0] = int(self.configFrame.ageFilterMin.get())
        self.ageFilter[1] = int(self.configFrame.ageFilterMax.get())

        self.daysPerMonth = int(self.configFrame.daysPerMonthVar.get())
        self.timeframe = int(self.configFrame.timeframeVar.get())

        inputs, outputs = calcInOut(self.husbandries, self.ageFilter, self.subTypeFilter, self.timeframe)

        self.inputList = ProductListFrame(self, "Inputs", inputs, self.daysPerMonth, self.timeframe)
        self.inputList.grid(column=1, row=0, sticky=(tk.NSEW))

        self.outputList = ProductListFrame(self, "Outputs", outputs, self.daysPerMonth, self.timeframe)
        self.outputList.grid(column=1, row=1, sticky=(tk.NSEW))

    def forwardRecalc(self):
        self.recalcProducts()

