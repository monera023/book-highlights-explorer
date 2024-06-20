from server.constants import DbConstants
from server.database_handler import DatabaseHandler


class OperationsManager:
    def __init__(self):
        self.database = DatabaseHandler("book-highlights.db")

    def view_data_sqlite(self):
        rows = self.database.get_data()
        print(f"Got {len(rows)} rows...")
        for row in rows:
            print(row)

    def flush_drop_tables(self):
        drop_tables = [DbConstants.HIGHLIGHTS_FTS]
        flush_tables = [DbConstants.TABLE_BOOK_HIGHLIGHTS]
        for table in drop_tables:
            print(f"Dropping table:: {table}")
            self.database.drop_table(table)

        for table in flush_tables:
            print(f"Flushing tables:: {table}")
            self.database.flush_table(table)


if __name__ == "__main__":
    ops_manager = OperationsManager()
    ops_manager.view_data_sqlite()
    # ops_manager.flush_drop_tables()
