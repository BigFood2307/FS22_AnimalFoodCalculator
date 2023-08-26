import tkinter as tk
from tkinter import ttk

class ConfigFrame(ttk.Frame):
    def __init__(self, master, ageFilter, daysPerMonth, timeframe):
        super().__init__(master)

        self.configTitle = ttk.Label(self, text="Configuration:")
        self.configTitle.grid(column=0, row=0)

        # Days Per Month

        self.daysPerMonthVar = tk.StringVar()
        self.daysPerMonthVar.set(int(daysPerMonth))

        self.daysPerMonthTitle = ttk.Label(self, text="Days per Month: ")
        self.daysPerMonthTitle.grid(column=0, row=1)

        self.daysPerMonthEntry = tk.Entry(self, textvariable=self.daysPerMonthVar)
        self.daysPerMonthEntry.grid(column=1, row=1)

        # Timeframe

        self.timeframeVar = tk.StringVar()
        self.timeframeVar.set(int(timeframe))

        self.timeframeTitle = ttk.Label(self, text="Timeframe: ")
        self.timeframeTitle.grid(column=0, row=2)

        self.timeframeEntry = tk.Entry(self, textvariable=self.timeframeVar)
        self.timeframeEntry.grid(column=1, row=2)

        # Age Filter

        self.ageFilterTitle = ttk.Label(self, text="Age Filter: ")
        self.ageFilterTitle.grid(column=0, row=3)

        self.ageFilterMinVar = tk.StringVar()
        self.ageFilterMinVar.set(str(ageFilter[0]))

        self.ageFilterMin = ttk.Entry(self, textvariable=self.ageFilterMinVar)
        self.ageFilterMin.grid(column=1, row=3)

        self.ageFilterMaxVar = tk.StringVar()
        self.ageFilterMaxVar.set(str(ageFilter[1]))

        self.ageFilterMax = ttk.Entry(self, textvariable=self.ageFilterMaxVar)
        self.ageFilterMax.grid(column=3, row=3)

        self.ageFilterTo = ttk.Label(self, text=" - ")
        self.ageFilterTo.grid(column=2, row=3)

        # Recalc Button

        self.recalcButton = ttk.Button(self, text="Recalculate!", command=master.recalcProducts)
        self.recalcButton.grid(column=0, row=4, columnspan=4)