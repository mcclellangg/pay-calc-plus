"""
Tests for
- MainWindow
"""

import pytest
from datetime import date
from pay_calc_plus.refactor.ui import MainWindow
from pay_calc_plus.refactor.payroll_models import Paycheck


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

    def test_record_insertion_into_tree(self, sample_paycheck_data):
        paycheck = Paycheck(**sample_paycheck_data)
