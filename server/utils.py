from server.constants import HighlightEntity


def generate_tr_html_content(results):
    html_content = "".join(
        f"<tr class='hover:bg-gray-50'>"
        f"<td class='px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900'>{row[0]}</td>"
        f"<td class='px-6 py-4 whitespace-normal text-sm text-gray-500'>{row[1]}</td>"
        f"</tr>"
        for row in results
    )
    return html_content


def append_book_name(sentence, book_name):
    updated_sentence = book_name + " " + sentence
    return updated_sentence


def convert_to_highlight_entity(db_rows):
    output = []
    for row in db_rows:
        output.append(HighlightEntity(book_name=row[0], author=row[1], year=row[2], highlight=row[3]))
    return output
