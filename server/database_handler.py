import sqlite3

class DatabaseHandler(object):
    TABLE_NAME = "book_highlights"
    INSERT_QUERY = f"INSERT INTO {TABLE_NAME} (book_name, author, year, highlight) VALUES (?, ?, ?, ?)"
    SELECT_COLUMNS = "book_name, author, year, highlight"

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name = ?"
        cursor = self.conn.cursor()
        cursor.execute(check_table_query, (self.TABLE_NAME,))

        table_exists = cursor.fetchone()
        if table_exists:
            print("Table present..")
        else:
            print(f"Table not present.. creating table: {self.TABLE_NAME}")
            self.create_table()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        create_table_query = '''
         CREATE TABLE IF NOT EXISTS book_highlights (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          book_name TEXT,
          author TEXT,
          year TEXT,
          highlight TEXT
         )
        '''
        cursor.execute(create_table_query)
        self.conn.commit()
        cursor.close()

    def insert_data(self, data):
        print(f"Inserting data for size:: {len(data)}")
        cursor = self.conn.cursor()
        # Data as list of tuples
        cursor.executemany(self.INSERT_QUERY, data)
        self.conn.commit()
        cursor.close()

    def flush_table(self):
        cursor = self.conn.cursor()
        flush_table_query = f"DELETE FROM {self.TABLE_NAME}"
        cursor.execute(flush_table_query)

        reset_autoincre_query = f"DELETE FROM sqlite_sequence WHERE name = '{self.TABLE_NAME}'"
        cursor.execute(reset_autoincre_query)

        self.conn.commit()
        cursor.close()
        print("Done flush for table..")

    def get_data(self):
        cursor = self.conn.cursor()

        select_all_query = f"SELECT {self.SELECT_COLUMNS} FROM {self.TABLE_NAME}"
        cursor.execute(select_all_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows


