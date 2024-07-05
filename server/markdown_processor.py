import markdown
import pandas as pd
from bs4 import BeautifulSoup
from server.database_handler import DatabaseHandler
from server.services.semantic_search_service import SemanticSearch
from server.utils import append_book_name


class HighlightsMetadata:
    def __init__(self, highlights, author: str, book_name: str, year: str):
        self.highlights = highlights
        self.author = author
        self.book_name = book_name
        self.year = year


class HighLightsFileProcessor:
    def __init__(self):
        self.database = DatabaseHandler("book-highlights.db")
        self.semantic_search_svc = SemanticSearch()

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
            insert_data_fts.append((row, highlights_metadata.book_name))

        print(f"Storing highlights of size:: {len(insert_data)}..")
        batch_size = 30
        for i in range(0, len(insert_data), batch_size):
            print(f"Processing batch:: {i}..{i+batch_size}")
            self.database.insert_data(insert_data[i: i + batch_size])
            self.database.insert_data_fts(insert_data_fts[i: i + batch_size])
        print(f"Done inserts...")
        dataframe = pd.DataFrame(highlights_metadata.highlights, columns=['highlight'])
        dataframe['highlight'] = dataframe['highlight'].apply(append_book_name, book_name=highlights_metadata.book_name)
        dataframe['embedding'] = dataframe['highlight'].apply(self.semantic_search_svc.generate_embedding)
        print(f"Indexing highlights embeddings to db..")
        self.semantic_search_svc.index(dataframe, {"book_name": highlights_metadata.book_name})
        print(f"Indexing of embeddings done..")

    def fetch_highlights(self):
        highlights = self.database.get_data()
        return highlights

    def search_highlights(self, query_term):
        response = self.database.fts_query(query_term)
        search_results = [(row[0], row[1]) for row in response]

        semantic_result = self.semantic_search_svc.query(query_term)
        for index, row in enumerate(semantic_result['documents'][0]):
            search_results.append((semantic_result['metadatas'][0][index]['book_name'], semantic_result['documents'][0][index]))

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
