# records_window.py

import db_commands as db
from tkinter import Toplevel, ttk
import tkinter as tk

records = db.query()


def open_records_window():
    top = Toplevel()
    top.title("Records Display")
    top.geometry("750x450+850+250")

    displayFrame = tk.LabelFrame(top, text="Paycheck Records")
    tree_display = ttk.Treeview(displayFrame)

    tree_display["columns"] = (
        "Date",
        "Name",
        "Exemptions",
        "Gross Pay",
        "Federal",
        "Social",
        "Medicare",
        "State",
        "Net",
        "Net Pay",
    )

    # Format the columns:
    tree_display.column("#0", width=0, stretch="NO")
    tree_display.column("Date", width=80, minwidth=25)
    tree_display.column("Name", anchor="w", width=60)
    tree_display.column("Exemptions", anchor="center", width=80)
    tree_display.column("Gross Pay", anchor="w", width=60)
    tree_display.column("Federal", anchor="center", width=60)
    tree_display.column("Social", anchor="center", width=60)
    tree_display.column("Medicare", anchor="center", width=60)
    tree_display.column("State", anchor="center", width=60)
    tree_display.column("Net", anchor="center", width=60)
    tree_display.column("Net Pay", anchor="center", width=60)

    # Create Headings:
    tree_display.heading("#0", text="", anchor="center")
    tree_display.heading("Date", text="Date", anchor="w")
    tree_display.heading("Name", text="Name", anchor="w")
    tree_display.heading("Exemptions", text="Exemptions", anchor="w")
    tree_display.heading("Gross Pay", text="Gross Pay", anchor="w")
    tree_display.heading("Federal", text="Federal", anchor="center")
    tree_display.heading("Social", text="Social", anchor="center")
    tree_display.heading("Medicare", text="Medicare", anchor="center")
    tree_display.heading("State", text="State", anchor="center")
    tree_display.heading("Net", text="Net", anchor="center")
    tree_display.heading("Net Pay", text="Net Pay", anchor="center")

    for record in records:
        tree_display.insert(parent="", index="end", values=(record))

    displayFrame.pack()
    tree_display.pack()
