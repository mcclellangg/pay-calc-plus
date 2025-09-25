from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

DB_CONFIG = {"prod": DATA_DIR / "payroll.db", "test": DATA_DIR / "test_payroll.db"}

SQL_COMMANDS = {
    "create_paychecks_table": """CREATE TABLE paychecks (
        date text,
        employee text,
        exemptions integer,
        gross_pay float,
        federal float,
        social float,
        medicare float,
        state float,
        net_deduct float,
        net_pay float
    )""",
    "insert_paycheck": """INSERT INTO paychecks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
}


TITLE = "Pay-Calc+"
GEOMETRY = "750x450+250+250"

BUTTON_FRAME = {
    "coordinates": {
        "row": 6,
        "column": 0,
        "padx": (0, 0),
        "pady": (20, 0),
        "columnspan": 2,
    },
    "button_configs": {
        "add_button": {
            "type": "button",
            "coordinates": {"row": 0, "column": 0, "padx": (0, 10), "pady": (0, 0)},
            "params": {"text": "Add All Entries", "command": "add_all", "width": 20},
        },
        "clear_button": {
            "type": "button",
            "coordinates": {"row": 0, "column": 1, "padx": (0, 10), "pady": (0, 0)},
            "params": {
                "text": "Clear All Entries",
                "command": "clear_all",
                "width": 20,
            },
        },
        "display_button": {
            "type": "button",
            "coordinates": {"row": 0, "column": 2, "padx": (0, 0), "pady": (0, 0)},
            "params": {
                "text": "Display Records",
                "command": "display_records",
                "width": 20,
            },
        },
    },
}


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

TREEVIEW = {
    "record_display": {
        "#0": {
            "column_params": {
                "column": "#0",
                "width": 60,
                "stretch": "no",
                "anchor": "w",
            },
            "heading_params": {"column": "#0", "text": "Date", "anchor": "w"},
        },
        "Name": {
            "column_params": {"column": "Name", "anchor": "w", "width": 60},
            "heading_params": {"column": "Name", "text": "Name", "anchor": "w"},
        },
        "Exemptions": {
            "column_params": {"column": "Exemptions", "anchor": "center", "width": 80},
            "heading_params": {
                "column": "Exemptions",
                "text": "Exemptions",
                "anchor": "w",
            },
        },
        "Gross Pay": {
            "column_params": {"column": "Gross Pay", "anchor": "w", "width": 60},
            "heading_params": {
                "column": "Gross Pay",
                "text": "Gross Pay",
                "anchor": "w",
            },
        },
        "Federal": {
            "column_params": {"column": "Federal", "anchor": "center", "width": 60},
            "heading_params": {
                "column": "Federal",
                "text": "Federal",
                "anchor": "center",
            },
        },
        "Social": {
            "column_params": {"column": "Social", "anchor": "center", "width": 60},
            "heading_params": {
                "column": "Social",
                "text": "Social",
                "anchor": "center",
            },
        },
        "Medicare": {
            "column_params": {"column": "Medicare", "anchor": "center", "width": 60},
            "heading_params": {
                "column": "Medicare",
                "text": "Medicare",
                "anchor": "center",
            },
        },
        "State": {
            "column_params": {"column": "State", "anchor": "center", "width": 60},
            "heading_params": {"column": "State", "text": "State", "anchor": "center"},
        },
        "Net": {
            "column_params": {"column": "Net", "anchor": "center", "width": 60},
            "heading_params": {"column": "Net", "text": "Net", "anchor": "center"},
        },
        "Net Pay": {
            "column_params": {"column": "Net Pay", "anchor": "center", "width": 60},
            "heading_params": {
                "column": "Net Pay",
                "text": "Net Pay",
                "anchor": "center",
            },
        },
    }
}
