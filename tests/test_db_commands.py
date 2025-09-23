"""
Tests for
- PayrollCoordinator with sqlite db
"""

import pytest
from pay_calc_plus.coordinator import PayrollCoordinator
from pay_calc_plus.config import DB_CONFIG


class TestDbCommands:
    @pytest.fixture(scope="class")
    def test_coordinator(self):
        """
        Fixture to setup and teardown test database with PayrollCoordinator
        """
        test_db_path = DB_CONFIG["test"]

        # Ensure data directory exists
        test_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Remove existing test db if it exists
        if test_db_path.exists():
            test_db_path.unlink()

        coordinator = PayrollCoordinator(test_db_path)
        yield coordinator

        coordinator.close_db()
        if test_db_path.exists():
            test_db_path.unlink()

    def test_db_setup(self, test_coordinator):
        """Test that database is properly setup and can execute basic queries"""
        result = test_coordinator.query_db("SELECT 1")
        fetched_result = result.fetchone()[0]

        assert fetched_result == 1

    def test_table_exists(self, test_coordinator):
        """Test that the paychecks table was created"""
        result = test_coordinator.query_db(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='paychecks'"
        )
        table_count = result.fetchone()[0]

        assert table_count == 1

    def test_table_structure(self, test_coordinator):
        """Test that the paychecks table has the expected columns"""
        result = test_coordinator.query_db("PRAGMA table_info(paychecks)")
        columns = result.fetchall()

        expected_columns = [
            "date",
            "employee",
            "exemptions",
            "gross_pay",
            "federal",
            "social",
            "medicare",
            "state",
            "net_deduct",
            "net_pay",
        ]

        actual_columns = [col[1] for col in columns]  # Column names are at index 1

        assert actual_columns == expected_columns
