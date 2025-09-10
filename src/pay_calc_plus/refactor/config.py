TITLE = "Pay-Calc+"
GEOMETRY = "750x450+250+250"
FORM_FIELDS = {
    "name": [
        {"type": "label", "text": "Enter employee name: ", "anchor": "w", "width": 18},
        {"type": "entry", "width": 40},
    ]
}

WIDGETS = {
    "name_label": {
        "type": "label",
        "coordinates": {"row":0, "column":0, "padx":(20, 8), "pady":(20, 8)},
        "params": {
            "text": "Enter employee name: ", "anchor": "w", "width": 18
        }
    },
    "name_entry": {
        "type": "entry",
        "coordinates": {"row":0, "column":1, "padx":(20, 8)},
        "params": {"width": 40}
    }
}