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
