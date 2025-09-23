# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

# Run black on src py files: venv must be activated!
format:
    black src\pay_calc_plus\*.py
    black tests\*.py

# Run dev
dev:
    python src\pay_calc_plus\main.py