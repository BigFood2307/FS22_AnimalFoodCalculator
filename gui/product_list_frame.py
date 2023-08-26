import tkinter as tk
from tkinter import ttk
from gui.vertical_scrolled_frame import VerticalScrolledFrame


class ProductListFrame(ttk.Frame):
    def __init__(self, master, title, productList, daysPerMonth, timeframe):
        super().__init__(master)

        self.productElements = []

        self.titleFrame = ttk.Label(self, text=title)
        self.titleFrame.grid(column=0, row=0, columnspan=5)
        
        self.nameTitle = ttk.Label(self, text="Product")
        self.nameTitle.grid(column=0, row=1, sticky=tk.EW)
        
        self.overallTitle = ttk.Label(self, text="Overall")
        self.overallTitle.grid(column=2, row=1, sticky=tk.EW)
        
        self.perDayTitle = ttk.Label(self, text="Per Day")
        self.perDayTitle.grid(column=4, row=1, sticky=tk.EW)
        
        self.nameLabels = []
        self.overallLabels = []
        self.perDayLabels = []

        for idx, product in enumerate(productList.keys()):
              
            self.nameLabels.append(ttk.Label(self, text=product))
            self.nameLabels[idx].grid(column=0, row=idx+2, sticky=tk.EW)
            
            self.overallLabels.append(ttk.Label(self, text=str(productList[product])))
            self.overallLabels[idx].grid(column=2, row=idx+2, sticky=tk.EW)
            
            self.perDayLabels.append(ttk.Label(self, text=str(productList[product]/(timeframe*daysPerMonth))))
            self.perDayLabels[idx].grid(column=4, row=idx+2, sticky=tk.EW)
        
        self.sep1 = ttk.Separator(self, orient=tk.VERTICAL)
        self.sep1.grid(column=1, row=1, rowspan=len(productList)+1, sticky=tk.NS)
        
        self.sep2 = ttk.Separator(self, orient=tk.VERTICAL)
        self.sep2.grid(column=3, row=1, rowspan=len(productList)+1, sticky=tk.NS)
