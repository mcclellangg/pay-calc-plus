# pay-calc.py

import tkinter as tk
from tkinter import ttk
import calculations as calc
import db_commands as db
import datetime


root = tk.Tk()
root.title("Pay-Calc+")
root.geometry("750x450")

count = 0  # iid for paychecks in treeview UNIQUE

# Command functions
def create_paycheck():
    """Takes the user inputs, passes them to the calculate function, and generates a paycheck object that is
    ready to display or add to the database."""
    global count
    # Get info from entry fields, and clean it for calc function
    user_input = {
        "name": nameField.get(),
        "exemptions": int(exemptionsField.get()),
        "gross pay": round(float(grossField.get()), 2),
    }
    paycheck = calc.calculate_deductions(user_input)
    # Insert the paycheck directly into the tree view:
    tree_display.insert(
        parent="",
        index="end",
        iid=count,
        text=("{:%m/%d/%Y}".format(datetime.datetime.now())),
        values=(
            paycheck["name"],
            paycheck["exemptions"],
            paycheck["gross pay"],
            paycheck["federal"],
            paycheck["social security"],
            paycheck["medicare"],
            paycheck["state"],
            paycheck["net"],
            paycheck["net pay"],
        ),
    )
    count += 1


def insert_paychecks():
    """Will take paychecks from tree display and add them to sqlite database."""
    for child in tree_display.get_children():
        record = {
            "date": tree_display.item(child)["text"],
            "employee": tree_display.item(child)["values"][0],
            "exemptions": tree_display.item(child)["values"][1],
            "gross_pay": tree_display.item(child)["values"][2],
            "federal": tree_display.item(child)["values"][3],
            "social": tree_display.item(child)["values"][4],
            "medicare": tree_display.item(child)["values"][5],
            "state": tree_display.item(child)["values"][6],
            "net_deduct": tree_display.item(child)["values"][7],
            "net_pay": tree_display.item(child)["values"][8],
        }
        db.submit(record)


nameLbl = tk.Label(root, text="Enter employee name : ", anchor="w")
nameField = tk.Entry(root)
exemptionsLbl = tk.Label(root, text="Enter exemptions :  ", anchor="w")
exemptionsField = tk.Entry(root)
grossLbl = tk.Label(root, text="Enter gross pay: ", anchor="w")
grossField = tk.Entry(root)
calcBtn = tk.Button(root, text="Calculate", command=create_paycheck)
addRecordsBtn = tk.Button(root, text="Add All Entries", command=insert_paychecks)


nameLbl.config(width=18)
nameField.config(width=40)
exemptionsLbl.config(width=18)
exemptionsField.config(width=40)
grossLbl.config(width=18)
grossField.config(width=40)
calcBtn.config(width=25)
addRecordsBtn.config(width=20)


nameLbl.grid(row=0, column=0, padx=(20, 8), pady=(20, 8))
nameField.grid(row=0, column=1, pady=(20, 8))
exemptionsLbl.grid(row=1, column=0, padx=(20, 8), pady=(0, 8))
exemptionsField.grid(row=1, column=1, pady=(0, 8))
grossLbl.grid(row=2, column=0, padx=(20, 8), pady=(0, 12))
grossField.grid(row=2, column=1, pady=(0, 12))
calcBtn.grid(row=3, column=0, padx=(60, 8), pady=(0, 8))
addRecordsBtn.grid(row=5, column=0, pady=(8, 8))


# Add the tree:
displayFrame = tk.LabelFrame(root, text="Paychecks")
displayFrame.grid(row=4, column=0, columnspan=2, padx=(30, 0))
tree_display = ttk.Treeview(displayFrame)

# Define the Columns:
tree_display["columns"] = (
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
tree_display.column("#0", width=80, minwidth=25)  # '#0' is the phantom column
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
tree_display.heading("#0", text="Timestamp", anchor="w")
tree_display.heading("Name", text="Name", anchor="w")
tree_display.heading("Exemptions", text="Exemptions", anchor="w")
tree_display.heading("Gross Pay", text="Gross Pay", anchor="w")
tree_display.heading("Federal", text="Federal", anchor="center")
tree_display.heading("Social", text="Social", anchor="center")
tree_display.heading("Medicare", text="Medicare", anchor="center")
tree_display.heading("State", text="State", anchor="center")
tree_display.heading("Net", text="Net", anchor="center")
tree_display.heading("Net Pay", text="Net Pay", anchor="center")

tree_display.pack()

root.mainloop()
