def generate_tr_html_content(results):
    html_content = "".join(
        f"<tr><td>{row[0]}</td> <td>{row[1]}</td></tr>"
        for row in results
    )
    return html_content


def append_book_name(sentence, book_name):
    updated_sentence = book_name + " " + sentence
    return updated_sentence
