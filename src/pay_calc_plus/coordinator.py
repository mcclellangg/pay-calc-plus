"""
PayrollCoordinator
"""

from pay_calc_plus.payroll_models import Paycheck
import sqlite3

DB_CONNECTION_STRING = "payroll.db"
CREATE_TABLE_CMD = """CREATE TABLE paychecks (date text,employee text,exemptions integer,gross_pay integer,federal integer,social integer,medicare integer,state integer,net_deduct integer,net_pay integer)
"""


class PayrollCoordinator:
    """
    Event handler and intermediary between MainWindow and database.
    """

    def __init__(self, connection_string: str = DB_CONNECTION_STRING):
        self.paycheck_records = []
        self.db_conn = self.setup_db_connection(connection_string=connection_string)

    def setup_db_connection(self, connection_string: str):
        """
        Connect to db, if no db exists create one.
        """
        db_conn = sqlite3.connect(connection_string)
        c = db_conn.cursor()
        c.execute(
            """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='paychecks' """
        )
        if c.fetchone()[0] == 1:
            print("Table exists")
        else:
            print(f"Creating table from cmd: {CREATE_TABLE_CMD} . . .")
            c.execute(CREATE_TABLE_CMD)

        db_conn.commit()
        return db_conn

    def query_db(self, cmd: str):
        """
        Execute given command on db.
        """
        c = self.db_conn.cursor()
        try:
            result = c.execute(cmd)
        except Exception as e:
            print(f"ERROR: {e}")
            self.close_db()
            return e
        return result

    def close_db(self):
        self.db_conn.close()
        return "db connection closed."

    def add_record(self, paycheck: Paycheck):
        self.paycheck_records.append(paycheck)

    def get_all_records(self):
        return self.paycheck_records
