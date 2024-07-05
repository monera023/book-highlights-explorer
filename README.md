# book-highlights-explorer
Exploring book highlights in different ways

Flow:
- Upload a markdown file with book highlights
- The file is parsed using markdown and bs4 to get only highlights text
- Highlights are then store in sqlite

Updates:

1) After upload highlights are now searchable. The search is implemented using fts5 plugin on top sqlite

2) Added basic UI for all the flows. Uses jinja templates + htmx.

3) Also experimented with a React frontend

4) Semantic search integration using nomic-embed-text embedding model via ollama and embedding stored in chromaDB
