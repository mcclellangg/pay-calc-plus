"""
Commands for interacting with sqlite database.
"""

import sqlite3

# Initialize db and connection
conn = sqlite3.connect("payroll.db")
c = conn.cursor()

c.execute(
    """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='paychecks' """
)
if c.fetchone()[0] == 1:
    print("Table exists.")
else:
    print("Creating table . . .")
    c.execute(
        """CREATE TABLE paychecks (
            date text,
            employee text,
            exemptions integer,
            gross_pay integer,
            federal integer,
            social integer,
            medicare integer,
            state integer,
            net_deduct integer,
            net_pay integer
            )"""
    )

conn.commit()
conn.close()


# Command Functions
def submit(record):
    """Takes record object created from tree and inserts it into the db."""
    conn = sqlite3.connect("payroll.db")
    c = conn.cursor()

    c.execute(
        """INSERT INTO paychecks VALUES(
            :date, :employee, :exemptions, :gross_pay, :federal, :social, :medicare, :state, :net_deduct, :net_pay)""",
        {
            "date": record["date"],
            "employee": record["employee"],
            "exemptions": record["exemptions"],
            "gross_pay": record["gross_pay"],
            "federal": record["federal"],
            "social": record["social"],
            "medicare": record["medicare"],
            "state": record["state"],
            "net_deduct": record["net_deduct"],
            "net_pay": record["net_pay"],
        },
    )
    # Commit changes and close connection:
    conn.commit()
    conn.close()

    print(f"Paycheck Added! {record}")


def query():
    print("Initiating query connection...")
    conn = sqlite3.connect("payroll.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM paychecks")
    records = c.fetchall()

    conn.commit()
    conn.close()

    return records
