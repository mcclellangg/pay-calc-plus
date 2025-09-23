"""
Payroll models:
- Paycheck
- Deductions
"""

from pay_calc_plus.calculations import (
    calc_federal_withholding,
    calc_state_withholding,
)
from dataclasses import asdict, astuple, dataclass, field
from datetime import datetime
from typing import Any, List

MEDICARE_PERCENTAGE = 0.0145
SOCIAL_PERCENTAGE = 0.062


@dataclass
class Deductions:
    federal: float = 0.0
    state: float = 0.0
    social: float = 0.0
    medicare: float = 0.0

    @property
    def total(self) -> float:
        return round((self.federal + self.state + self.social + self.medicare), 2)


@dataclass
class Paycheck:
    deductions: Deductions = field(default_factory=Deductions)
    employee_name: str = ""
    exemptions: int = 0
    gross_pay: float = 0.0
    net_pay: float = 0.0
    pay_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.gross_pay < 0:
            raise ValueError("Gross pay must be positive")
        self.execute_calculations()

    def calculate_deductions(self):
        """
        Calculate and update deductions based on employee gross pay, and exemptions.
        """
        gross = self.gross_pay
        exemptions = self.exemptions

        self.deductions.federal = calc_federal_withholding(g=gross, e=exemptions)
        self.deductions.state = calc_state_withholding(g=gross, e=exemptions)
        self.deductions.social = round((gross * SOCIAL_PERCENTAGE), 2)
        self.deductions.medicare = round((gross * MEDICARE_PERCENTAGE), 2)

    def calculate_net_pay(self):
        """Calculates and updates net pay."""
        self.net_pay = self.gross_pay - self.deductions.total

    def execute_calculations(self):
        self.calculate_deductions()
        self.calculate_net_pay()

    def to_tuple(self):
        """
        tuple format:
        ((75.0, 41.0, 55.8, 13.05), 'John Doe', 2, 900.0, 715.15, datetime.date(2024, 1, 15))
        """
        return astuple(self)

    def to_dict(self):
        """
        dict format:
        {'deductions': {'federal': 75.0, 'state': 41.0, 'social': 55.8, 'medicare': 13.05}, 'employee_name': 'John Doe', 'exemptions': 2, 'gross_pay': 900.0, 'net_pay': 715.15, 'pay_date': datetime.date(2024, 1, 15)}
        """
        return asdict(self)

    def to_tree_format(self) -> List[Any]:
        """
        Return a list in the order expected by TreeView columns:

        ["name", "exemptions", "gross", "fed", "social", "medicare", "state", "net", "net_pay"]

        NOTE: ideally this would come from CONFIG (since Tree cols are there), however I currently never expect these to change. Additionally type hints would indicate that list values would all be of expected type.
        """
        return [
            self.employee_name,
            self.exemptions,
            self.gross_pay,
            self.deductions.federal,
            self.deductions.social,
            self.deductions.medicare,
            self.deductions.state,
            self.deductions.total,
            self.net_pay,
        ]
