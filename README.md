# Local Book Highlights Explorer
Exploring book highlights in different ways

Flow:
There are 2 ways users can upload highlights.
- One through UI Upload File
- Other is through a POST API just pass folder name and the app will store all markdown files(containing highlights).

Ways to explore:
- Highlights Feed
![feed-flow](https://github.com/user-attachments/assets/e8e6d4f9-6ff3-4d1e-ab5d-38556dde83e7)

  
- Search Highlights
![search-flow](https://github.com/user-attachments/assets/2f7140ab-7639-4f2a-aa52-dce5e090c382)


Updates:

1) Highlights are searchable. The search is implemented using fts5 plugin on top sqlite

2) Added basic UI for all the flows. Uses jinja templates + htmx.

3) Also experimented with a React frontend [Deprecated..]

4) Semantic search integration using nomic-embed-text embedding model via ollama and embedding stored in chromaDB
