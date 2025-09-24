"""
Tests for
- MainWindow
"""

import pytest
from datetime import date
import tkinter as tk
from tkinter import ttk
from pay_calc_plus.ui import MainWindow
from pay_calc_plus.payroll_models import Paycheck


class TestMainWindow:
    """Tests for MainWindow class."""

    @pytest.fixture
    def sample_paycheck_data(self):
        return {
            # "deductions": "a bad value",
            "employee_name": "John Doe",
            "exemptions": 2,
            "gross_pay": 900.0,
            "net_pay": None,
            "pay_date": date(2024, 1, 15),
        }

    @pytest.fixture
    def main_window(self):
        """Create a MainWindow instance for testing."""
        window = MainWindow()
        yield window
        # Cleanup: destroy the tkinter window after test
        window.root.destroy()

    def test_load_widgets(self, main_window):
        """Test that all widgets are loaded correctly from config."""
        # Verify that widgets dictionary is populated
        assert len(main_window.widgets) > 0

        # Check that expected widgets from config are created
        expected_widgets = [
            "name_label",
            "name_entry",
            "exemptions_label",
            "exemptions_entry",
            "gross_label",
            "gross_entry",
            "calc_button",
        ]

        for widget_name in expected_widgets:
            assert widget_name in main_window.widgets, f"Widget {widget_name} not found"

        # Verify widget types are correct
        assert isinstance(main_window.widgets["name_label"], tk.Label)
        assert isinstance(main_window.widgets["name_entry"], tk.Entry)
        assert isinstance(main_window.widgets["exemptions_label"], tk.Label)
        assert isinstance(main_window.widgets["exemptions_entry"], tk.Entry)
        assert isinstance(main_window.widgets["gross_label"], tk.Label)
        assert isinstance(main_window.widgets["gross_entry"], tk.Entry)
        assert isinstance(main_window.widgets["calc_button"], tk.Button)

        # # Test that button command is properly assigned
        # calc_button = main_window.widgets["calc_button"]
        # assert calc_button["command"] == main_window.create_paycheck

        # Verify widget text content
        assert main_window.widgets["name_label"]["text"] == "Enter employee name : "
        assert main_window.widgets["exemptions_label"]["text"] == "Enter exemptions :  "
        assert main_window.widgets["gross_label"]["text"] == "Enter gross pay : "
        assert main_window.widgets["calc_button"]["text"] == "Calculate"

    def test_load_treeview(self, main_window):
        """Test that treeview is loaded correctly with proper columns."""
        # Verify tree exists and is a Treeview instance
        assert main_window.tree is not None
        assert isinstance(main_window.tree, ttk.Treeview)

        # Check that columns are configured correctly from config
        expected_columns = [
            "Name",
            "Exemptions",
            "Gross Pay",
            "Federal",
            "Social",
            "Medicare",
            "State",
            "Net",
            "Net Pay",
        ]

        tree_columns = list(main_window.tree["columns"])
        assert tree_columns == expected_columns

        # Verify that headings are set correctly
        for col in expected_columns:
            heading_text = main_window.tree.heading(col)["text"]
            assert heading_text == col

        # Check that the phantom column #0 is configured
        phantom_heading = main_window.tree.heading("#0")["text"]
        assert phantom_heading == "Date"

        # Verify tree is packed (visible)
        pack_info = main_window.tree.pack_info()
        assert pack_info  # Should not be empty if packed

        # Check that tree parent frame exists and has correct text
        tree_parent = main_window.tree.master
        assert isinstance(tree_parent, tk.LabelFrame)
        assert tree_parent["text"] == "Paychecks"
