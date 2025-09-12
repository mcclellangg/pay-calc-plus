"""
Payroll models:
- Paycheck
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paycheck:
    pay_date: datetime
    employee_name: str
    gross_pay: float
    exemptions: int

    def __post_init___(self):
        if self.gross_pay < 0:
            raise ValueError("Gross pay must be positive")
