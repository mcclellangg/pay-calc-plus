"""
Main UI window.
"""

import tkinter as tk
from tkinter import ttk
from config import GEOMETRY, TITLE, WIDGETS


class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {"title": TITLE, "geometry": GEOMETRY, "widgets": WIDGETS}
        self.commands = {"calculate": self.calculate_paycheck}
        self.root = tk.Tk()
        self.setup()

    def calculate_paycheck(self):
        """To be imported from separate module"""
        print("calculating paycheck ...")

    def setup(self):
        self.root.title(self.settings["title"])
        self.root.geometry(self.settings["geometry"])
        self.load_widgets()
        self.load_tree_view()

    def load_widgets(self):
        """
        Load widgets for parent 'self.root'.
        """
        widget_types = {
            "label": tk.Label,
            "entry": tk.Entry,
            "button": tk.Button,
        }
        self.widgets = {}

        for name, widget_config in self.settings["widgets"].items():
            wtype = widget_config["type"]
            params = widget_config.get("params")
            parent = self.root

            if wtype == "button":
                try:
                    cmd_key = params["command"]
                    params["command"] = self.commands[cmd_key]
                except KeyError as e:
                    print(f"ERROR button requires command: {e}")

            widget_class = widget_types[wtype]
            widget = widget_class(parent, **params)
            self.widgets[name] = widget
            widget.grid(**widget_config["coordinates"])

    def load_tree_view(self):
        df = tk.LabelFrame(self.root, text="Paychecks")
        df.grid(row=4, column=0, columnspan=2, padx=(30, 0))
        tree = ttk.Treeview(df)
        tree["columns"] = "Name"
        print(tree["columns"])

        # tree.pack()

    def run(self):
        self.root.mainloop()
