import shutil
import os
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, File, UploadFile, Form, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

from server.constants import AppConstants, DbConstants
from server.markdown_processor import HighLightsFileProcessor, HighlightsMetadata
from server.utils import generate_tr_html_content

app = FastAPI()
templates = Jinja2Templates(directory="templates")


highlights_processor = HighLightsFileProcessor()

all_books = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    book_names_query = f"select distinct(book_name) from {DbConstants.TABLE_BOOK_HIGHLIGHTS}"
    book_names = highlights_processor.database.run_raw_query(book_names_query)
    all_books.extend([book[0] for book in book_names])
    print(f"Got all book..{all_books}")


@app.get("/v1/htmx.min.js")
async def server_htmx_js():
    return FileResponse("templates/htmx.min.js", media_type="application/javascript")

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


@app.get('/v1/search')
async def search_template(request: Request):
    return templates.TemplateResponse("search_htmx.html", {"request": request})


@app.get('/v1/searchHighlights')
async def search(query: Optional[str] = Query(None, description="Search terms"), books: Optional[List[str]] = Query(None, description="Selected books")):
    print(f"Got book query:: {books}")
    search_results = highlights_processor.search_highlights(query) if query else []

    filtered_results = [row for row in search_results if row[0] in books] if books else search_results
    print(f"Got response {len(filtered_results)}")

    html_content = generate_tr_html_content(filtered_results)

    return HTMLResponse(content=html_content)


@app.post("/v2/uploadHighlights")
async def upload_highlights_v2(file: UploadFile = File(...),
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


@app.get("/v2/fetchHighlights")
async def fetch_highlights_v2(request: Request):
    highlights = highlights_processor.fetch_highlights()
    return highlights


@app.get('/v2/searchHighlights')
async def search_v2(request: Request, query: Optional[str] = Query(None, description="Search terms"), books: Optional[List[str]] = Query(None, description="Selected books")):
    print(f"Got book query:: {books}")
    search_results = highlights_processor.search_highlights(query) if query else []

    filtered_results = [row for row in search_results if row[0] in books] if books else search_results

    print(f"Got response {len(filtered_results)}")
    return filtered_results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
