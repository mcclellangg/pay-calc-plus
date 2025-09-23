"""
PayrollCoordinator
"""

from pay_calc_plus.payroll_models import Paycheck
import sqlite3
from pay_calc_plus.config import DB_CONFIG, SQL_COMMANDS


class PayrollCoordinator:
    """
    Event handler and intermediary between MainWindow and database.
    """

    def __init__(self, connection_string: str = DB_CONFIG["prod"]):
        self.paycheck_records = []
        self.db_conn = self.setup_db_connection(connection_string=connection_string)

    def setup_db_connection(self, connection_string: str):
        """
        Connect to db, if no db exists create one.
        """
        connection_string.parent.mkdir(parents=True, exist_ok=True)

        db_conn = sqlite3.connect(str(connection_string))
        c = db_conn.cursor()
        c.execute(
            """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='paychecks' """
        )
        if c.fetchone()[0] == 1:
            print("Table exists")
        else:
            print(
                f"Creating table from cmd: {SQL_COMMANDS["create_paychecks_table"]} . . ."
            )
            c.execute(SQL_COMMANDS["create_paychecks_table"])

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
