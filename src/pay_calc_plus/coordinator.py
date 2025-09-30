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
        self.records_in_error = []
        self.db_conn = self.setup_db_connection(connection_string=connection_string)

    # SETUP
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

    # DB UTILS
    def query_db(self, cmd: str):
        """
        Execute given command on db.
        utility method to directly test interactions with sqlite db.
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
        """Close database connection."""
        self.report_records_in_error()
        self.db_conn.close()
        return "db connection closed."

    def add_single_record_to_db(self, paycheck: Paycheck):
        """
        Add record to db, rollback if unsuccessful.
        """
        c = self.db_conn.cursor()
        try:
            paycheck_data = paycheck.to_sql_record()
            c.execute(SQL_COMMANDS["insert_paycheck"], paycheck_data)
            self.db_conn.commit()
            print(
                f"Successfully added paycheck for {paycheck.employee_name} to database."
            )
        except Exception as e:
            print(f"ERROR adding paycheck to database: {e}")
            self.db_conn.rollback()
            return e

    def get_all_records_from_db(self) -> list[tuple]:
        """
        Select all paychecks from db and return list of tuple values.
        Returns empty list if no records or on error.
        """
        query = SQL_COMMANDS["get_all_paychecks"]
        c = self.db_conn.cursor()
        print(f"Retrieving records with query: {query}")
        try:
            c.execute(query)
            records = c.fetchall()  # Will this return empty list?
            print(f"Records retrieved successfully")
            return records
        except Exception as e:
            print(f"ERROR retrieving records: {e}")
            return []

    # CALLBACK HANDLER
    def add_current_records_to_db(self):
        """
        Callback handler, method passed from ButtonFrame->MainWindow->PayrollCoordinator.

        Add all records into db. Clear record cache when complete.
        """
        if not self.paycheck_records:
            print("paycheck_records empty, nothing to add to db.")
            return self.paycheck_records
        else:
            print("Adding records ...")
            for p in self.paycheck_records:
                try:
                    print(f"Adding paycheck: {p}")
                    self.add_single_record_to_db(paycheck=p)
                except Exception as e:
                    print(f"ERROR adding paycheck: {p}: {e}")
                    self.records_in_error.append(p)
                    return e
            # BUG: unsuccessful addition will be cleared.
            self.clear_all_records()

    # RECORD HANDLERS
    def add_record(self, paycheck: Paycheck):
        """Updates list with Paycheck object."""
        self.paycheck_records.append(paycheck)

    def get_all_records(self):
        """Returns a list of Paycheck objects."""
        return self.paycheck_records

    def clear_all_records(self):
        """
        Part of a callback sequence from ButtonFrame -> MainWindow (handle_btn_clear_all_entries).

        Clears all paycheck_records
        """
        self.paycheck_records.clear()
        print(
            "Records cleared successfully - coordinator"
        )  # BUG: print this once (see handler)

    def report_records_in_error(self):
        """Display records that were not written to db."""
        if self.records_in_error:
            print("The following records were in error")
            for p in self.records_in_error:
                print(p)
            return self.records_in_error
        else:
            print("No records in error")
            return []
