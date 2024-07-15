from typing import List, Optional

from pydantic import BaseModel

class DbConstants:
    HIGHLIGHTS_FTS = "highlights_fts"
    TABLE_BOOK_HIGHLIGHTS = "book_highlights"


class AppConstants:
    UPLOADED_FILE_DIR = "uploadFiles"
    SUPPORTED_MIME_TYPES = ["text/markdown"]


class HighlightEntity(BaseModel):
    book_name: str
    author: str
    year: str
    highlight: str


class IndexFolderRequest(BaseModel):
    folder_name: str


class BookModel(BaseModel):
    book_name: Optional[str] = None
    author: Optional[str] = None
    highlights: Optional[List[str]] = None

    def print_details(self):
        print(f"Name = {self.book_name}....\n"
              f"Author = {self.author}....\n"
              f"Total Highlights = {len(self.highlights)}....\n"
              f"Peek of Highlights = {self.highlights[:2]}...")
