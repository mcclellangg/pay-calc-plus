"""
Tests for
- Paycheck
- calculations
"""

import pytest
from datetime import datetime, date
from pay_calc_plus.refactor.payroll_models import Deductions, Paycheck


class TestPaycheck:
    """Tests for the Paycheck class."""

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

    def test_paycheck_creation_valid_data(self, sample_paycheck_data):
        paycheck = Paycheck(**sample_paycheck_data)
        assert paycheck.employee_name == "John Doe"
        assert paycheck.gross_pay == 900.0
        assert paycheck.exemptions == 2
        assert paycheck.pay_date == date(2024, 1, 15)

    # def test_paycheck_creation_invalid_gross_pay(self, sample_paycheck_data):
    #     sample_paycheck_data["gross_pay"] = -100.0
    #     with pytest.raises(ValueError, match="Gross pay must be positive"):
    #         Paycheck(**sample_paycheck_data)

    def test_paycheck_deduction_calculations(self, sample_paycheck_data):
        paycheck = Paycheck(**sample_paycheck_data)
        paycheck.execute_calculations()
        assert paycheck.deductions.federal == float(75.0)
        assert paycheck.deductions.social == float(55.8)
        assert paycheck.deductions.medicare == float(13.05)
        assert paycheck.deductions.state == float(41.0)
        assert paycheck.deductions.total == float(184.85)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
