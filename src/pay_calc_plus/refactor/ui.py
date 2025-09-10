"""
Main UI window.
"""
import tkinter
from config import GEOMETRY, TITLE, WIDGETS

class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {"title": TITLE, "geometry": GEOMETRY, "widgets": WIDGETS}
        self.tk = tkinter.Tk()
        self.setup()
    
    def setup(self):
        self.tk.title(self.settings["title"])
        self.tk.geometry(self.settings["geometry"])
        self.load_widgets()
    
    def load_widgets(self):
        """ 
        Load widgets from config.
        """
        for widget_config in self.settings["widgets"].values():
            coordinates = widget_config["coordinates"]
            params = widget_config["params"]
            if widget_config["type"] == "label":
                tkinter.Label(self.tk, **params).grid(**coordinates)

            elif widget_config["type"] == "entry":
                tkinter.Entry(self.tk, **params).grid(**coordinates)

    def run(self):
        self.tk.mainloop()