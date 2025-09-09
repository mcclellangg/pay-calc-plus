"""
Main UI window.
"""
import tkinter
from config import FORM_FIELDS, GEOMETRY, TITLE

class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {"title": TITLE, "geometry": GEOMETRY, "form_fields": FORM_FIELDS}
        self.tk = tkinter.Tk()
        self.setup()
    
    def setup(self):
        self.tk.title(self.settings["title"])
        self.tk.geometry(self.settings["geometry"])
        self.form_widget()
    
    def form_widget(self):
        """ 
        Cleanup.
        """
        for field, widgets in self.settings["form_fields"].items():
            for widget in widgets:
                if widget["type"] == "label":
                    tkinter.Label(self.tk, text=widget["text"], anchor=widget["anchor"], width=widget["width"])
                elif widget["type"] == "entry":
                    tkinter.Entry(self.tk, width=widget["width"])

    def run(self):
        self.tk.mainloop()