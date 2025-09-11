"""
Main UI window.
"""
import tkinter
from config import GEOMETRY, TITLE, WIDGETS

class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {"title": TITLE, "geometry": GEOMETRY, "widgets": WIDGETS}
        self.commands = {
            "calculate": self.calculate_paycheck
        }
        self.tk = tkinter.Tk()
        self.setup()
    
    def calculate_paycheck(self):
        """To be imported from separate module"""
        print("calculating paycheck ...")
    
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
            
            elif widget_config["type"] == "button":
                try:
                    cmd_key = params["command"]
                    params["command"] = self.commands[cmd_key]
                except KeyError as e:
                    print(f"ERROR button requires command: {e}")
                tkinter.Button(self.tk, **params).grid(**coordinates)

    def run(self):
        self.tk.mainloop()