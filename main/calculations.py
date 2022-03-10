# calculations
"""
   A module created to store all of the paycheck calculations. The calculate function, will be
   a master function of sorts that combines all of the smaller deduction calculations, all calculations
   will be based on gross pay, and number of exemptions set by the user.
"""
import datetime

def calc_state(G: float, E1: int) -> float:
    """
    Source: https://www.tax.virginia.gov/sites/default/files/inline-files/Employer%20Withholding%20Instructions.pdf

    A function to calculate state withholding amount each week.
    Will take gross pay(G), and # of exemptions as arguments(E1), and return
    the amount to be withheld for this pay period. This function will assume
    that the pay periods(P) occur on a weekly basis. This function also assumes there will
    be no calculations for people 65+, or taking blind exemptions.

    Original Formula:
    (G)P - [$3,000 + (E1 X $930) + (E2 X 800)] = T

    Modified Formula:
    (G)P - [$3,000 + (E1 X $930)] = T
    """
    P = 52
    W = 0  # Annualized tax to be withheld

    # Calculate Annualized taxable income(T):
    T = (G * P) - (3000 + (E1 * 930))
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


def calc_fed(G: float, E1: int) -> float:
    """
    Takes gross pay and number of exemptions as arguments.

    A function designed to calculate federal withholding amounts on a weekly basis.
    For simplicity sake, this function will be designed to work for Single or Married Filing Seperately individuals only.
    It will also assume that the employee does not have multiple jobs (Using a W-4 form that is from before 2019 or 2020
    and beyond but not checking the box in step 2 on that form). This formula will also only solve for someone with an annual
    salary range of $0 - $90,325.
    Source: https://www.irs.gov/pub/irs-pdf/p15t.pdf

    Formula:
    (G)P - (E1 X $4300) = T

    Then check table and calculate excess

    LIMITATIONS: DOES NOT CHECK FOR NEGATIVE INPUTS
    """

    P = 52
    W = 0  # Annualized tax to be withheld

    # Calculate Annualized taxable income(T):
    T = (G * P) - (E1 * 4300)
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


def calculate_deductions(user_input: dict) -> dict:
    """Takes the user input generated from the create paycheck function, and performs the necessary
    calculations to create a paycheck object in the following format:

    {'timestamp': 'DATETIME object',
    'name': STRING,
    'exemptions': INTEGER,
    'gross pay': FLOAT round 2,
    'federal': FLOAT round 2,
    'social security': FLOAT round 2,
    'medicare': FLOAT round 2,
    'state': FLOAT round 2,
    'net': FLOAT round 2,
    'net pay': FLOAT round 2
    }
    """
    # Initialize variables to be passed to functions:
    paycheck = {}
    try:
        name = user_input["name"]
        G = user_input["gross pay"]
        E1 = user_input["exemptions"]
    except KeyError:
        print("Could not access user input")
    # Perform all deductions and store them in the paycheck object:
    paycheck["timestamp"] = "{: %m/%d/%Y }".format(datetime.datetime.now())
    paycheck["name"] = name
    paycheck["exemptions"] = E1
    paycheck["gross pay"] = G
    paycheck["federal"] = calc_fed(G, E1)
    paycheck["social security"] = round((G * 0.062), 2)
    paycheck["medicare"] = round((G * 0.0145), 2)
    paycheck["state"] = calc_state(G, E1)
    paycheck["net"] = round(
        (
            paycheck["federal"]
            + paycheck["social security"]
            + paycheck["medicare"]
            + paycheck["state"]
        ),
        2,
    )
    paycheck["net pay"] = paycheck["gross pay"] - paycheck["net"]

    return paycheck
