"""
Tests for
- PayrollCoordinator
"""

import pytest
from datetime import datetime, date
from pay_calc_plus.refactor.payroll_models import Paycheck
from pay_calc_plus.refactor.coordinator import PayrollCoordinator


class TestPayrollCoordinator:
    @pytest.fixture
    def sample_paycheck_data(self):
        return [
            {
                # "deductions": "a bad value",
                "employee_name": "Sue Smith",
                "exemptions": 1,
                "gross_pay": 1235.0,
                "net_pay": None,
                "pay_date": date(2024, 1, 15),
            },
            {
                # "deductions": "a bad value",
                "employee_name": "John Doe",
                "exemptions": 2,
                "gross_pay": 900.0,
                "net_pay": None,
                "pay_date": date(2024, 1, 15),
            },
            {
                # "deductions": "a bad value",
                "employee_name": "Jim Doe",
                "exemptions": 3,
                "gross_pay": 1200.0,
                "net_pay": None,
                "pay_date": date(2024, 1, 15),
            },
        ]

    def test_adding_single_paycheck(self, sample_paycheck_data):
        coordinator = PayrollCoordinator()
        paycheck_1 = Paycheck(**sample_paycheck_data[0])
        coordinator.add_record(paycheck=paycheck_1)
        all_paychecks = coordinator.get_all_records()
        assert len(all_paychecks) == 1

    def test_adding_multiple_paychecks(self, sample_paycheck_data):
        coordinator = PayrollCoordinator()
        for paycheck in sample_paycheck_data:
            coordinator.add_record(Paycheck(**paycheck))
        all_paychecks = coordinator.get_all_records()
        assert len(all_paychecks) == 3
