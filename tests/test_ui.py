"""
Tests for
- MainWindow
- RecordWindow
"""

import pytest
import tkinter as tk
from tkinter import Toplevel, ttk
from pay_calc_plus.ui import ButtonFrame, MainWindow, RecordWindow


class TestButtonFrame:
    """
    Tests for ButtonFrame class focusing on logic and configuration.
    """

    @pytest.fixture
    def parent_window(self):
        """Create a parent window."""
        window = tk.Tk()
        yield window
        window.destroy()

    @pytest.fixture
    def simple_callback_handler(self):
        """Create a simple callback handler for testing."""

        class TestHandler:
            def handle_btn_add_all_entries(self):
                pass

            def handle_btn_clear_all_entries(self):
                pass

            def handle_btn_display_records(self):
                pass

        return TestHandler()

    @pytest.fixture
    def button_frame(self, parent_window, simple_callback_handler):
        """Create ButtonFrame instance for testing."""
        frame = ButtonFrame(parent_window, simple_callback_handler)
        yield frame

    def test_buttons_loaded_from_config(self, button_frame):
        """Test that expected buttons are created from config."""
        # Verify buttons dictionary is populated
        assert len(button_frame.buttons) > 0

        # Check expected buttons exist (based on typical config)
        expected_buttons = ["add", "clear", "display"]

        for button_name in expected_buttons:
            assert (
                button_name in button_frame.buttons
            ), f"Button {button_name} not found"
            assert isinstance(button_frame.buttons[button_name], tk.Button)

    def test_command_mapping_logic(self, button_frame):
        """Test that commands dictionary maps to correct methods."""
        expected_commands = {
            "add_all": button_frame.add_all_entries,
            "clear_all": button_frame.clear_all_entries,
            "display_records": button_frame.display_records,
        }

        for cmd_key, expected_method in expected_commands.items():
            assert cmd_key in button_frame.commands
            assert button_frame.commands[cmd_key] == expected_method

    def test_frame_setup(self, button_frame):
        """Test that frame is properly configured."""
        assert button_frame.frame is not None
        assert isinstance(button_frame.frame, tk.Frame)
        assert button_frame.parent is not None
        assert button_frame.callback_handler is not None


class TestRecordWindow:
    """
    Tests for RecordWindow class focusing on current implementation.
    """

    @pytest.fixture
    def record_window(self):
        """Create RecordWindow instance for testing."""
        # Create root window first (required for Toplevel)
        root = tk.Tk()
        window = RecordWindow()
        yield window
        # Cleanup
        window.top.destroy()
        root.destroy()

    def test_toplevel_window_created(self, record_window):
        """Test that Toplevel window is created."""
        assert record_window.top is not None
        assert isinstance(record_window.top, Toplevel)

    def test_settings_configuration(self, record_window):
        """Test that settings are loaded correctly from config."""
        assert "title" in record_window.settings
        assert "geometry" in record_window.settings
        assert "treeview" in record_window.settings

        # Verify settings have expected types
        assert isinstance(record_window.settings["title"], str)
        assert isinstance(record_window.settings["geometry"], str)
        assert isinstance(record_window.settings["treeview"], dict)


class TestMainWindow:
    """
    Tests for MainWindow class.
    """

    @pytest.fixture
    def main_window(self):
        """
        Create a MainWindow instance for testing.

        NOTE: scope is not set to class so that functionalities are tested independently.
        """
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

    # INTEGRATION TESTS
    def test_button_frame_with_main_window(self, main_window):
        """Test ButtonFrame integration with MainWindow."""
        # Verify ButtonFrame is created and connected to MainWindow
        assert main_window.button_frame is not None
        assert main_window.button_frame.callback_handler == main_window

        # Verify buttons exist and are configured
        button_frame = main_window.button_frame
        assert len(button_frame.buttons) > 0

        # Test that callback handler methods exist on MainWindow
        assert hasattr(main_window, "handle_btn_add_all_entries")
        assert hasattr(main_window, "handle_btn_clear_all_entries")
        assert hasattr(main_window, "handle_btn_display_records")

        # Verify methods are callable
        assert callable(main_window.handle_btn_add_all_entries)
        assert callable(main_window.handle_btn_clear_all_entries)
        assert callable(main_window.handle_btn_display_records)

    def test_callback_handler_delegation(self, main_window):
        """Test that ButtonFrame methods properly call MainWindow handlers."""
        button_frame = main_window.button_frame

        # Test add_all_entries delegation
        try:
            button_frame.add_all_entries()
            # If no exception, delegation works (actual functionality tested elsewhere)
        except Exception as e:
            # Allow expected exceptions from coordinator/db operations
            if "coordinator" not in str(e).lower():
                pytest.fail(f"Unexpected error in add_all_entries delegation: {e}")

        # Test clear_all_entries delegation
        try:
            button_frame.clear_all_entries()
        except Exception as e:
            if "coordinator" not in str(e).lower():
                pytest.fail(f"Unexpected error in clear_all_entries delegation: {e}")

        # Test display_records delegation
        try:
            button_frame.display_records()
        except Exception as e:
            if "coordinator" not in str(e).lower():
                pytest.fail(f"Unexpected error in display_records delegation: {e}")

    def test_record_window_opening(self, main_window):
        """Test that MainWindow can create RecordWindow."""
        # Initially no record window
        assert main_window.record_window is None

        # Call handler to create record window
        main_window.handle_btn_display_records()

        # Verify record window was created
        assert main_window.record_window is not None

        # Cleanup - destroy the record window
        if main_window.record_window:
            main_window.record_window.top.destroy()
