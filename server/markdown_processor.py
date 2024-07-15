from typing import List

import markdown
import pandas as pd
from bs4 import BeautifulSoup

from server.constants import BookModel
from server.database_handler import DatabaseHandler
from server.services.semantic_search_service import SemanticSearch
from server.utils import append_book_name, convert_to_highlight_entity
import threading


class HighlightsMetadata:
    def __init__(self, highlights, author: str, book_name: str):
        self.highlights = highlights
        self.author = author
        self.book_name = book_name


class HighLightsFileProcessor:
    def __init__(self):
        self.database = DatabaseHandler("book-highlights.db")
        self.semantic_search_svc = SemanticSearch()

    def get_call(self):
        pass

    def parse_highlights_from_file(self, file) -> BookModel:
        book: BookModel = BookModel()
        html_file = markdown.markdown(file)
        soup = BeautifulSoup(html_file, features="html.parser")
        text_tags_data = []

        for h_tag in soup.find_all('h1'):
            split_h_tag: List[str] = h_tag.get_text().split("by")
            book.book_name = split_h_tag[0].strip()
            book.author = split_h_tag[1].strip()
        for p_tag in soup.find_all('p'):
            if "Tags:" in p_tag.get_text() or "Note:" in p_tag.get_text():
                continue
            else:
                text_tags_data.append(p_tag.get_text())
        book.highlights = text_tags_data
        return book

    def store_highlights(self, highlights_metadata: HighlightsMetadata):
        print(f"Preparing insert data for {highlights_metadata.book_name}")
        insert_data = []
        insert_data_fts = []
        for row in highlights_metadata.highlights:
            insert_data.append((highlights_metadata.book_name, highlights_metadata.author, row))
            insert_data_fts.append((row, highlights_metadata.book_name))

        print(f"Storing highlights of size:: {len(insert_data)}..")
        batch_size = 30
        for i in range(0, len(insert_data), batch_size):
            print(f"Processing batch:: {i}..{i+batch_size}")
            self.database.insert_data(insert_data[i: i + batch_size])
            self.database.insert_data_fts(insert_data_fts[i: i + batch_size])
        print(f"Done inserts... for {highlights_metadata.book_name}")
        dataframe = pd.DataFrame(highlights_metadata.highlights, columns=['highlight'])
        dataframe['highlight'] = dataframe['highlight'].apply(append_book_name, book_name=highlights_metadata.book_name)
        dataframe['embedding'] = dataframe['highlight'].apply(self.semantic_search_svc.generate_embedding)
        print(f"Starting background thread for Indexing highlights embeddings..")
        semantic_search_thread = threading.Thread(target=self.semantic_search_svc.index, args=(dataframe, {"book_name": highlights_metadata.book_name}))
        semantic_search_thread.start()

    def fetch_highlights(self):
        highlights = self.database.get_data()
        formatted_output = convert_to_highlight_entity(highlights)
        return formatted_output

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
