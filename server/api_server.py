import shutil
import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, Query

from server.markdown_processor import HighLightsFileProcessor, HighlightsMetadata

app = FastAPI()

UPLOADED_FILE_DIR = "uploadFiles"

highlights_processor = HighLightsFileProcessor()

@app.post("/v1/uploadHighlights")
async def upload_highlights(file: UploadFile = File(...),
                            book_name: str = Form(...),
                            author: str = Form(...),
                            year: str = Form(...)):
    uploaded_file_location = f"{UPLOADED_FILE_DIR}/{file.filename}"
    print(f"Saving file .. {file.filename}")
    with open(uploaded_file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"Reading file {file.filename} for parsing..")
    with open(uploaded_file_location, "r", encoding="utf-8") as f:
        file_content = f.read()

    highlights_data = highlights_processor.parse_highlights_from_file(file_content)
    print(f"Parsed highlights.. got count {len(highlights_data)}")
    highlights_processor.store_highlights(HighlightsMetadata(highlights_data, author, book_name, year))
    print(f"Stored highlights in database..")

    if os.path.exists(uploaded_file_location):
        os.remove(uploaded_file_location)
        print("Removed intermediate file..")
    else:
        print("Failed to remove file..")
    return {
        "response": "Highlights Stored successfully.."
    }


@app.get("/v1/fetchHighlights")
async def fetch_highlights():
    highlights = highlights_processor.fetch_highlights()
    return highlights


@app.get('/v1/searchHighlights')
async def search(query: Optional[str] = Query(None, description="Search terms")):
    if query:
        return highlights_processor.search_highlights(query)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
