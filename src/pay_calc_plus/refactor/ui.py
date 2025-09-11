"""
Main UI window.
"""

import tkinter as tk
from tkinter import ttk
from config import GEOMETRY, TITLE, TREEVIEW, WIDGETS


class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {
            "title": TITLE,
            "geometry": GEOMETRY,
            "treeview": TREEVIEW,
            "widgets": WIDGETS,
        }
        self.commands = {"calculate": self.calculate_paycheck}
        self.widgets = {}
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
        """
        Create LabelFrame and mount treeview from config settings.
        """
        df = tk.LabelFrame(self.root, text="Paychecks")
        df.grid(row=4, column=0, columnspan=2, padx=(30, 0))

        tree = ttk.Treeview(df)

        tree_name = "record_display"
        column_configs = self.settings["treeview"][tree_name]
        column_names = [name for name in column_configs.keys()]
        column_names.remove("#0")  # Ensure phantom column is not added twice

        tree["columns"] = column_names  # Columns must be added before they are modified

        for col, params in column_configs.items():
            col_params = params["column_params"]
            heading_params = params["heading_params"]
            if col_params:
                tree.column(**col_params)
            if heading_params:
                tree.heading(**heading_params)

        tree.pack()

    def run(self):
        self.root.mainloop()
