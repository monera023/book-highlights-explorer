import os

from server.constants import BookModel
from server.markdown_processor import HighLightsFileProcessor, HighlightsMetadata


class Indexer:
    def __init__(self):
        self.highlights_processor = HighLightsFileProcessor()

    def index_folder(self, folder_name: str):
        with (os.scandir(folder_name) as itr):
            for entry in itr:
                if entry.is_file() and ".md" in entry.path:
                    print(f"Indexing file = {entry.path}")
                    with open(entry.path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    book: BookModel = self.highlights_processor.parse_highlights_from_file(file_content)
                    print(book.print_details())
                    self.highlights_processor.store_highlights(HighlightsMetadata(book.highlights, book.author, book.book_name))
