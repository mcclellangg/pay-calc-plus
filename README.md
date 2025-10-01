# PAY-CALC+

## Overview

This is a desktop GUI app made with python, and tkinter. It takes input from the user (employee name, gross pay, exemptions)
and calculates weekly paycheck deductions automatically. The calculated paychecks can optionally be stored in a sqlite database.
The Display Records button will then open a new window and display the paychecks in the tkinter tree display.

State deductions are calculated using formulas from the [Virginia Income Tax Withholding Guide](https://www.tax.virginia.gov/sites/default/files/inline-files/Employer%20Withholding%20Instructions.pdf).

Federal deductions are calculated using percentage method tables for automated payroll systems. These are described in
in detail on page 8 of [Federal Income Tax Withholding Methods](https://www.irs.gov/pub/irs-pdf/p15t.pdf).

## Details

Limitations and issues:
- Formulas will need to be updated for 2022
- Assumes employees are paid on a weekly period
- Federal formula makes the following assumptions about employee:
  - W-4 is from 2019 or earlier
  - Or if W-4 is from 2020 or beyond, employee has not checked box in Step 2 of W-4 (multiple jobs)
  - Salary is in the range of $0 - $90,325

## Demo
![main-screen-pic](https://raw.githubusercontent.com/mcclellangg/pay-calc-plus/dev/images/calc.png)
![records-screen-pic](https://raw.githubusercontent.com/mcclellangg/pay-calc-plus/dev/images/records.png)

## Install
Assuming `uv`,`python`, and `just` are installed.

1. Clone this repo `git clone https://github.com/mcclellangg/pay-calc-plus.git`
2. `cd pay-calc-plus`
3. Create a virtual environment `python -m venv .venv`
4. Activate venv (Windows) `.\.venv\Scripts\Activate.ps1` (Linux) `source .venv/bin/activate`
5. Run `uv sync` to update dependencies
6. Run `uv pip install -e .` to perform editable install
7. Run app `just run`
    -  OR manually execute run cmd `python -m pay_calc_plus.main`
