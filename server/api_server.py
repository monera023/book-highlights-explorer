import shutil
import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, Query, Request
from fastapi.templating import Jinja2Templates

from server.constants import AppConstants
from server.markdown_processor import HighLightsFileProcessor, HighlightsMetadata

app = FastAPI()
templates = Jinja2Templates(directory="templates")


highlights_processor = HighLightsFileProcessor()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request, "title": "Book Highlights Explorer", "heading": "Highlights Explorer", "content": "Explore highlight of your books using search and explore options."})


@app.post("/v1/uploadHighlights")
async def upload_highlights(file: UploadFile = File(...),
                            book_name: str = Form(...),
                            author: str = Form(...),
                            year: str = Form(...)):
    uploaded_file_location = f"{AppConstants.UPLOADED_FILE_DIR}/{file.filename}"
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
async def fetch_highlights(request: Request):
    highlights = highlights_processor.fetch_highlights()
    return templates.TemplateResponse("highlights.html", {"request": request, "highlights": highlights})


@app.get('/v1/searchHighlights')
async def search(request: Request, query: Optional[str] = Query(None, description="Search terms")):
    search_results = highlights_processor.search_highlights(query) if query else []
    print(f"Got response {len(search_results)}")
    return templates.TemplateResponse("search.html", {"request": request, "search_results": search_results})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
