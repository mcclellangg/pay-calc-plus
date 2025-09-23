"""
PayrollCoordinator
"""

from pay_calc_plus.refactor.payroll_models import Paycheck


class PayrollCoordinator:
    """
    Event handler and intermediary between MainWindow and database.
    """

    def __init__(self):
        self.paycheck_records = []

    def add_record(self, paycheck: Paycheck):
        self.paycheck_records.append(paycheck)

    def get_all_records(self):
        return self.paycheck_records
