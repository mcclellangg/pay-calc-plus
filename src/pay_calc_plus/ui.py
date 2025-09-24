"""
Main UI window.
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk
from pay_calc_plus.config import GEOMETRY, TITLE, TREEVIEW, WIDGETS
from pay_calc_plus.payroll_models import Paycheck
from pay_calc_plus.coordinator import PayrollCoordinator


class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {
            "title": TITLE,
            "geometry": GEOMETRY,
            "treeview": TREEVIEW,
            "widgets": WIDGETS,
        }
        self.commands = {"calculate": self.create_paycheck}
        self.widgets = {}
        self.root = tk.Tk()
        self.tree = self.load_tree_view()
        self.coordinator = PayrollCoordinator()
        self.setup()
    
    # SETUP
    def setup(self):
        self.root.title(self.settings["title"])
        self.root.geometry(self.settings["geometry"])
        self.load_widgets()

    def load_widgets(self):
        """
        Load widgets for parent 'self.root'. Widgets instances accessible via self.widgets {
            "widget_name": tk.widgetInstance,
            "name_label" : tk.Label
        }
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

        self.tree = tree
        self.tree.pack()

        return self.tree

    # COORDINATOR
    def create_paycheck(self):
        """
        Store paycheck in coordinator. Update tree display with most recent paycheck.
        """
        paycheck_data = self.convert_entry(self.get_entry_values())
        paycheck = Paycheck(**paycheck_data)
        self.coordinator.add_record(paycheck)
        self.add_paycheck_to_tree_display(paycheck)

    # ENTRY/LABEL
    def get_entry_values(self):
        """Retrieve key and value pairs for all entry widgets."""
        entry_name_to_value = {}

        for widget_name in self.widgets.keys():
            if "entry" in widget_name:
                entry_name_to_value[widget_name] = self.widgets[widget_name].get()

        return entry_name_to_value

    def convert_entry(self, entry: dict) -> dict:
        """
        Create a dict of expected types to create Paycheck object from user input.
        """
        paycheck_data = {
            "employee_name": "",
            "exemptions": 0,
            "gross_pay": 0.0,
            "pay_date": "{:%m/%d/%Y}".format(datetime.now()),
        }
        try:
            paycheck_data["exemptions"] = int(entry["exemptions_entry"])
            paycheck_data["gross_pay"] = float(entry["gross_entry"])
            paycheck_data["employee_name"] = entry["name_entry"]
        except KeyError as e:
            print(f"Key error during entry conversion: {e}")

        return paycheck_data


    # TREEVIEW
    def add_paycheck_to_tree_display(self, paycheck: Paycheck):
        """
        Add paycheck record to tree display. Does not maintain a history of paychecks.
        """
        data = paycheck.to_tree_format()
        self.tree.insert(parent="", index="end", text=paycheck.pay_date, values=data)

    # MAIN
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"ERROR: {e}")
            print("Closing db ...")
            self.coordinator.close_db()
