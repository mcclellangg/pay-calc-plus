TITLE = "Pay-Calc+"
GEOMETRY = "750x450+250+250"


def foo_cmd():
    print("Button clicked!")


WIDGETS = {
    "name_label": {
        "type": "label",
        "coordinates": {"row": 0, "column": 0, "padx": (20, 8), "pady": (20, 8)},
        "params": {"text": "Enter employee name : ", "anchor": "w", "width": 18},
    },
    "name_entry": {
        "type": "entry",
        "coordinates": {"row": 0, "column": 1, "pady": (20, 8)},
        "params": {"width": 40},
    },
    "exemptions_label": {
        "type": "label",
        "coordinates": {"row": 1, "column": 0, "padx": (20, 8), "pady": (0, 8)},
        "params": {"text": "Enter exemptions :  ", "anchor": "w", "width": 18},
    },
    "exemptions_entry": {
        "type": "entry",
        "coordinates": {"row": 1, "column": 1, "pady": (0, 8)},
        "params": {"width": 40},
    },
    "gross_label": {
        "type": "label",
        "coordinates": {"row": 2, "column": 0, "padx": (20, 8), "pady": (0, 12)},
        "params": {"text": "Enter gross pay : ", "anchor": "w", "width": 18},
    },
    "gross_entry": {
        "type": "entry",
        "coordinates": {"row": 2, "column": 1, "pady": (0, 12)},
        "params": {"width": 40},
    },
    "calc_button": {
        "type": "button",
        "coordinates": {"row": 3, "column": 0, "padx": (60, 8), "pady": (0, 8)},
        "params": {"text": "Calculate", "command": "calculate", "width": 25},
    },
}

TREEVIEW = {"record_display": {}}
