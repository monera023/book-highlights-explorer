import sqlite3
from sqlite3 import OperationalError
from typing import List


class DatabaseHandler(object):
    TABLE_BOOK_HIGHLIGHTS = "book_highlights"
    HIGHLIGHTS_FTS = "highlights_fts"
    INSERT_QUERY = f"INSERT INTO {TABLE_BOOK_HIGHLIGHTS} (book_name, author, highlight) VALUES (?, ?, ?)"
    SELECT_COLUMNS = "book_name, author, highlight"
    FTS_INSERT_QUERY = f"INSERT INTO {HIGHLIGHTS_FTS} (highlight, book_name) VALUES (?, ?)"

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.setup_done = False
        self.setup_db()

    def setup_db(self):
        print(f"Setting up DB..")
        if not self.setup_done:
            check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name = ?"
            cursor = self.conn.cursor()
            cursor.execute(check_table_query, (self.TABLE_BOOK_HIGHLIGHTS,))

            table_exists = cursor.fetchone()
            if table_exists:
                print("Table present..")
            else:
                print(f"Table not present.. creating table: {self.TABLE_BOOK_HIGHLIGHTS}")
                self.create_table()
            self.create_table_for_fts()
            self.setup_done = True
        else:
            print("DB Setup already done..")

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
          highlight TEXT
         )
        '''
        cursor.execute(create_table_query)
        self.conn.commit()
        cursor.close()

    def create_table_for_fts(self):
        print(f"Creating fts table")
        cursor = self.conn.cursor()
        try:
            create_fts_table_query = '''
            CREATE VIRTUAL TABLE highlights_fts USING fts5(highlight, book_name, tokenize = 'porter ascii', prefix=3);
            '''
            cursor.execute(create_fts_table_query)
            self.conn.commit()
            print(f"Fts table created..")
        except OperationalError as e:
            if str(e).find('already exists') == -1:
                print(f"Got error for sqlite.. {e}")
            else:
                print(f"{e}")
        finally:
            cursor.close()

    def insert_data(self, data):
        print(f"Inserting data for size:: {len(data)}")
        cursor = self.conn.cursor()
        # Data as list of tuples
        cursor.executemany(self.INSERT_QUERY, data)
        self.conn.commit()
        cursor.close()

    def insert_data_fts(self, data):
        print(f"Inserting data into fts table for size:: {len(data)}")
        cursor = self.conn.cursor()
        cursor.executemany(self.FTS_INSERT_QUERY, data)
        self.conn.commit()
        cursor.close()

    def flush_table(self, table_name):
        cursor = self.conn.cursor()
        flush_table_query = f"DELETE FROM {table_name}"
        cursor.execute(flush_table_query)

        reset_autoincre_query = f"DELETE FROM sqlite_sequence WHERE name = '{table_name}'"
        cursor.execute(reset_autoincre_query)

        self.conn.commit()
        cursor.close()
        print("Done flush for table..")

    def drop_table(self, table_name):
        cursor = self.conn.cursor()
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_table_query)
        self.conn.commit()
        cursor.close()
        print(f"Dropped table..{table_name} from db")

    def get_data(self, feed_ids: List[int]):
        cursor = self.conn.cursor()
        placeholders = ','.join('?' for _ in feed_ids)
        select_all_query = f"SELECT {self.SELECT_COLUMNS} FROM {self.TABLE_BOOK_HIGHLIGHTS} WHERE id in ({placeholders})"
        cursor.execute(select_all_query, feed_ids)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def count_query(self):
        cursor = self.conn.cursor()

        count_query = f"select count(*) from {self.TABLE_BOOK_HIGHLIGHTS}"
        cursor.execute(count_query)
        output = cursor.fetchone()
        print(output)
        return output

    def fts_query(self, match_keyword):
        cursor = self.conn.cursor()
        prefix_match_keyword = match_keyword + '*'
        fts_match_query = f"SELECT book_name, highlight(highlights_fts,0, '<b>', '</b>') highlight FROM {self.HIGHLIGHTS_FTS} WHERE {self.HIGHLIGHTS_FTS} MATCH '{prefix_match_keyword}'"
        cursor.execute(fts_match_query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def run_raw_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

