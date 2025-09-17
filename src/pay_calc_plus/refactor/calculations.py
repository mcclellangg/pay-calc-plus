"""
Calculations:
- state withholding (VA)
- federal withholding
- medicare
- social security
"""


def calc_state_withholding(g: float, e: int) -> float:
    """
    Source: https://www.tax.virginia.gov/sites/default/files/inline-files/Employer%20Withholding%20Instructions.pdf

    Params: g (gross_pay)
            e (exemptions)
    Returns: state_withholding amount
    Formulas:
        (g)P - [$3,000 + (e X $930) + (E2 X 800)] = T   # original # NOTE: What was E2?
        (g)P - [$3,000 + (e X $930)] = T                # modified
    """
    P = 52
    W = 0  # Annualized tax to be withheld

    # Calculate Annualized taxable income(T):
    T = (g * P) - (3000 + (e * 930))
    # Use T to calculate W (annualized tax to be withheld):
    if T < 3000:
        W = T * 0.02
    elif T >= 3000 and T < 5000:
        W = ((T - 3000) * 0.03) + 60
    elif T >= 5000 and T < 17000:
        W = ((T - 5000) * 0.05) + 120
    elif T >= 17000:
        W = ((T - 17000) * 0.0575) + 720

    withholding_amount = round((W / P))

    return float(withholding_amount)


def calc_federal_withholding(g: float, e: int) -> float:
    """
    Takes gross pay and number of exemptions as arguments.

    A function designed to calculate federal withholding amounts on a weekly basis.
    For simplicity sake, this function will be designed to work for Single or Married Filing separately individuals only.
    It will also assume that the employee does not have multiple jobs (Using a W-4 form that is from before 2019 or 2020
    and beyond but not checking the box in step 2 on that form). This formula will also only solve for someone with an annual
    salary range of $0 - $90,325.
    Source: https://www.irs.gov/pub/irs-pdf/p15t.pdf

    Formula:
    (g)P - (e X $4300) = T

    Then check table and calculate excess

    LIMITATIONS: DOES NOT CHECK FOR NEGATIVE INPUTS
    """

    P = 52
    W = 0  # Annualized tax to be withheld

    # Calculate Annualized taxable income(T):
    T = (g * P) - (e * 4300)
    # Use T to calculate W (annualized tax to be withheld):
    if T < 3950:
        W = 0
    elif T >= 3950 and T < 13900:
        W = (T - 3950) * 0.10
    elif T >= 13900 and T < 44475:
        W = ((T - 13900) * 0.12) + 995
    elif T >= 44475 and T < 90325:
        W = ((T - 44475) * 0.22) + 4664

    withholding_amount = round((W / P))

    return float(withholding_amount)
