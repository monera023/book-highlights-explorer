import os
from typing import List

from server.constants import BookModel
from server.markdown_processor import HighLightsFileProcessor, HighlightsMetadata


class Indexer:
    def __init__(self):
        self.highlights_processor = HighLightsFileProcessor()

    def index_folder(self, folder_name: str, already_indexed_books: List[str]):
        with (os.scandir(folder_name) as itr):
            for entry in itr:
                if entry.is_file() and ".md" in entry.path:
                    print(f"Indexing file = {entry.path}")
                    with open(entry.path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    book: BookModel = self.highlights_processor.parse_highlights_from_file(file_content)
                    print(book.print_details())
                    if book.book_name in already_indexed_books:
                        print(f"Skipping Book..{book.book_name}.. as it is already indexed")
                        # TODO: Find better way to ignore even before complete file parse
                        continue
                    self.highlights_processor.store_highlights(HighlightsMetadata(book.highlights, book.author, book.book_name))
