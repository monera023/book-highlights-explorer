import markdown
from bs4 import BeautifulSoup
from server.database_handler import DatabaseHandler


class HighlightsMetadata:
    def __init__(self, highlights, author: str, book_name: str, year: str):
        self.highlights = highlights
        self.author = author
        self.book_name = book_name
        self.year = year


class HighLightsFileProcessor:
    def __init__(self):
        self.database = DatabaseHandler("book-highlights.db")

    def get_call(self):
        pass

    def parse_highlights_from_file(self, file):
        html_file = markdown.markdown(file)
        soup = BeautifulSoup(html_file, features="html.parser")
        text_tags_data = []
        for p_tag in soup.find_all('p'):
            if "Tags:" in p_tag.get_text() or "Note:" in p_tag.get_text():
                continue
            else:
                text_tags_data.append(p_tag.get_text())
        return text_tags_data

    def store_highlights(self, highlights_metadata: HighlightsMetadata):
        print(f"Preparing insert data..")
        insert_data = []
        insert_data_fts = []
        for row in highlights_metadata.highlights:
            insert_data.append((highlights_metadata.book_name, highlights_metadata.author,
                                highlights_metadata.year, row))
            insert_data_fts.append((row,))

        print(f"Storing highlights of size:: {len(insert_data)}..")
        batch_size = 30
        for i in range(0, len(insert_data), batch_size):
            print(f"Processing batch:: {i}..{i+batch_size}")
            self.database.insert_data(insert_data[i: i + batch_size])
            self.database.insert_data_fts(insert_data_fts[i: i + batch_size])
        print(f"Done inserts...")

    def fetch_highlights(self):
        highlights = self.database.get_data()
        return highlights

    def search_highlights(self, query_term):
        response = self.database.fts_query(query_term)
        search_results = [row[0] for row in response]
        return search_results


def view_data_sqlite(database):
    rows = database.get_data()
    print(f"Got {len(rows)} rows...")
    for row in rows:
        print(row)
    database.flush_table()


if __name__ == "__main__":
    file = "file"
    # process_file(file)
    database = DatabaseHandler("book-highlights.db")
    # database.connect()
    view_data_sqlite(database)
