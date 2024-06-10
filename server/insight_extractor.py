import markdown
from scrapegraphai.graphs import SmartScraperGraph


def use_scrape_graph_ai(content):
    graph_config = {
        "llm": {
            "api_key": "<key>",
            "model": "gpt-3.5-turbo"
        },
        "headless": True
    }
    ssgraph = SmartScraperGraph(
        prompt="<prompt>",
        source=content,
        config=graph_config
    )

    print(f"Before run...{ssgraph.get_execution_info()}")
    result = ssgraph.run()
    print(result)
    print(f"After run...{ssgraph.get_execution_info()}")


def extract_insights_from_markdown(file_content):
    html_content = markdown.markdown(file_content)
    # Wrap the HTML content inside the <body> tag
    html_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Converted Markdown</title>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    use_scrape_graph_ai(html_output)


if __name__ == "__main__":
    file_name = ""
    with open(file_name, "r", encoding="utf-8") as file:
        fc = file.read()
    extract_insights_from_markdown(fc)
