"""
Tests for
- PayrollCoordinator with sqlite db
"""

import pytest
from datetime import datetime, date
from pay_calc_plus.refactor.coordinator import PayrollCoordinator


class TestDbCommands:
    def test_db_setup(self):
        TEST_CONNECTION_STRING = "test_payroll.db"
        coordinator = PayrollCoordinator(TEST_CONNECTION_STRING)  # Override the default

        result = coordinator.query_db("SELECT 1")
        fetched_result = result.fetchone()[0]

        assert fetched_result == 1
        coordinator.close_db()
