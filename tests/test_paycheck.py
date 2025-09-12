"""
Tests for
- Paycheck
- calculations
"""

import pytest
from datetime import datetime, date
from pay_calc_plus.refactor.payroll_models import Paycheck


class TestPaycheck:
    """Tests for the Paycheck class."""

    @pytest.fixture
    def sample_paycheck_data(self):
        return {
            "employee_name": "John Doe",
            "gross_pay": 1000.0,
            "exemptions": 2,
            "pay_date": date(2024, 1, 15),
        }

    def test_paycheck_creation_valid_data(self, sample_paycheck_data):
        paycheck = Paycheck(**sample_paycheck_data)
        assert paycheck.employee_name == "John Doe"
        assert paycheck.gross_pay == 1000.0
        assert paycheck.exemptions == 2
        assert paycheck.pay_date == date(2024, 1, 15)

    # def test_paycheck_creation_invalid_gross_pay(self, sample_paycheck_data):
    #     sample_paycheck_data["gross_pay"] = -100.0
    #     with pytest.raises(ValueError, match="Gross pay must be positive"):
    #         Paycheck(**sample_paycheck_data)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
