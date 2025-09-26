"""
UI components
- MainWindow
- ButtonFrame
"""

from datetime import datetime
import tkinter as tk
from tkinter import Toplevel, ttk
from pay_calc_plus.config import BUTTON_FRAME, GEOMETRY, TITLE, TREEVIEW, WIDGETS
from pay_calc_plus.payroll_models import Paycheck
from pay_calc_plus.coordinator import PayrollCoordinator


class ButtonFrame:
    def __init__(self, parent, callback_handler):
        self.buttons = {}
        self.callback_handler = callback_handler
        self.commands = {
            "add_all": self.add_all_entries,
            "clear_all": self.clear_all_entries,
            "display_records": self.display_records,
        }
        self.frame = tk.Frame(parent)
        self.parent = parent
        self.settings = BUTTON_FRAME
        self.setup()

    def setup(self):
        """
        Load frame to parent window, call load_buttons.
        """
        try:
            self.frame.grid(**self.settings["coordinates"])
        except KeyError as e:
            print(f"ERROR: {e}")

        self.load_buttons()

    def load_buttons(self):
        """
        Load buttons from config.
        Button instances accessible via self.buttons["button_name"]
        """
        for name, button_config in self.settings["button_configs"].items():
            params = button_config.get("params")

            if "command" in params:
                cmd_key = params["command"]
                try:
                    params["command"] = self.commands[cmd_key]
                except KeyError as e:
                    print(f"ERROR: Button command not found: {e}")
                    # Fallback to a placeholder function
                    params["command"] = lambda: print(
                        f"Command '{cmd_key}' not implemented"
                    )

            # Create button
            button = tk.Button(self.frame, **params)
            self.buttons[name] = button
            button.grid(**button_config["coordinates"])

    # CMD METHODS
    def add_all_entries(self):
        """
        Callback method via MainWindow -> PayrollCoordinator

        Adds all current entries (in payroll_records) as sql_records.
        """
        print("Calling parent to add all entries")
        self.callback_handler.handle_btn_add_all_entries()

    def clear_all_entries(self):
        """Clear all entry widgets."""
        print("Calling parent to clear all entries")
        self.callback_handler.handle_btn_clear_all_entries()

    def display_records(self):
        """Display all records in the treeview."""
        print("Calling parent to display records")
        self.callback_handler.handle_btn_display_records()


class RecordWindow:
    """
    Top level widget used to display all records from the db.

    Creates a tree display with same config from MainWindow.
    """

    def __init__(self, records: list = []):
        self.settings = {
            "title": TITLE,
            "geometry": GEOMETRY["record_window"],
            "treeview": TREEVIEW,
        }
        self.records = records
        self.top = Toplevel()
        self.table = None
        self.setup()

    def setup(self):
        self.top.title = self.settings["title"]
        self.top.geometry(self.settings["geometry"])
        self.table = TreeTable(parent=self.top, records=self.records)


class TreeTable:
    """
    Treeview widget used as a table by MainWindow and RecordWindow to display Paychecks created by user and loaded from db.

    Contains a LabelFrame and Treeview widget.
    """

    def __init__(self, parent, records: list, callback_handler=None):
        self.call_back_handler = callback_handler
        self.config = TREEVIEW
        self.label_frame = None  # should this be None on init?
        self.parent = parent
        self.records = records
        self.tree_table = None  # should this be None on init?
        self.setup()

    def setup(self):
        print("Setting up TreeTable ...")
        self.label_frame = tk.LabelFrame(self.parent, text="TABLE")
        self.tree_table = ttk.Treeview(self.label_frame)
        table_config = self.get_config()
        self.load_table_cols(config=table_config)
        self.load_records()
        self.label_frame.pack(fill="x")
        self.tree_table.pack(fill="x")  # Fit width of frame (horizontal fill)
        print("TreeTable setup complete")

    def get_config(self) -> dict:
        """Copy config so unwanted cols can be filtered on load."""
        try:
            column_configs = self.config[
                "record_display"
            ].copy()  # DON'T alter config directly
            return column_configs
        except KeyError as e:
            print(f"ERROR in parse_config: {e}")
            return e

    def load_table_cols(self, config: dict):
        """
        Remove phantom col name and update tree_table with cols.

        NOTE: phantom col is filtered from names since it already exists in TreeView (by default) and does not need to be re-added.
        """

        PHANTOM_COL = "#0"
        col_names = [name for name in config.keys()]
        col_names.remove(PHANTOM_COL)

        # Columns must be added before they are modified
        self.tree_table["columns"] = col_names

        for col, params in config.items():
            col_params = params["column_params"]
            heading_params = params["heading_params"]
            if col_params:
                self.tree_table.column(**col_params)
            if heading_params:
                self.tree_table.heading(**heading_params)

    def load_records(self):
        """Update table with provided records.

        NOTE: record[0] is the date value and is set via text
        """
        if not self.records:
            print("No records to load")
            return None
        print(f"Loading records to table ...")
        for record in self.records:
            date = record[0]
            values = record[1:]
            self.tree_table.insert(parent="", index="end", values=(values), text=date)
        print("Records loaded successfully")


class MainWindow:
    def __init__(self):
        # Read data from config and run app
        self.settings = {
            "title": TITLE,
            "geometry": GEOMETRY["main_window"],
            "treeview": TREEVIEW,
            "widgets": WIDGETS,
        }
        self.commands = {"calculate": self.create_paycheck}
        self.widgets = {}
        self.root = tk.Tk()
        self.tree = self.load_tree_view()
        self.record_window = (
            None  # NOTE: currently not able to track number of instances open
        )
        self.coordinator = PayrollCoordinator()
        self.button_frame = ButtonFrame(parent=self.root, callback_handler=self)
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

    # CALLBACK HANDLERS
    def handle_btn_add_all_entries(self):
        """
        Callback from ButtonFrame tp PayrollCoordinator.

        BUG: Does not update tree display.
        """
        self.coordinator.add_current_records_to_db()

    def handle_btn_clear_all_entries(self):
        """Callback from ButtonFrame to clear PayrollCoordinator records and tree display."""
        try:
            self.coordinator.clear_all_records()
            self.clear_tree_display()
            print(
                "Records cleared successfully - handler"
            )  # BUG: print this in one place
        except Exception as e:
            print(f"ERROR with clear entries btn: {e}")

    def handle_btn_display_records(self):
        """
        Callback from ButtonFrame to open new Toplevel widget RecordWindow.

        Only one RecordWindow should be open at a time.
        """
        # BUG: You can open multiple instances of RecordWindow, ideally there would only be one at a time.

        payroll_records = self.coordinator.get_all_records_from_db()
        self.record_window = RecordWindow(records=payroll_records)

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

    def clear_tree_display(self):
        self.tree.delete(*self.tree.get_children())

    # MAIN
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"ERROR: {e}")
            print("Closing db ...")
            self.coordinator.close_db()
