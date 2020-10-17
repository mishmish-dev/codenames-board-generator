from http import HTTPStatus

from flask import Flask, Response, request
from werkzeug.wsgi import FileWrapper

from generate import generate_pdf, initialize_resources
from words import load_wordlists, split_words
from html_page import WORDS_FILE_INPUT, WORDS_TEXT_INPUT, WORDLIST_INPUT, SHUFFLE_CHECKBOX, COUNT_INPUT
from html_page import WORDLISTS, index_page


initialize_resources("card.png", "PTSansBold.ttf", "PTSansBoldItalic.ttf")
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024


def send_file(buffer, filename, mimetype):
    file_wrapper = FileWrapper(buffer)
    headers = {
        "Content-Disposition": 'attachment; filename="{}"'.format(filename)
    }

    return Response(file_wrapper,
        mimetype=mimetype,
        direct_passthrough=True,
        headers=headers
    )


@app.route("/", methods=["GET", "POST"])
def generate_codenames_board():
    if request.method == "GET":
        return index_page

    elif request.method == "POST":
        if WORDS_FILE_INPUT in request.files:
            words_file = request.files[WORDS_FILE_INPUT]

            try:
                words = split_words(words_file.read().decode("utf-8"))
            except:
                return (
                    "Не удалось прочесть файл. Убедитесь, что он в UTF-8.",
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )

        elif WORDS_TEXT_INPUT in request.form:
            words = split_words(request.form[WORDS_TEXT_INPUT])

        elif WORDLIST_INPUT in request.form:
            try:
                words = WORDLISTS[int(request.form[WORDLIST_INPUT])].wordlist
            except:
                return (
                    "Что-то не так с выбором набора.",
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )

        else:
            return "Request not recognized", HTTPStatus.NOT_FOUND

        try:
            count = int(request.form[COUNT_INPUT])
        except:
            count = None

        buffer = generate_pdf(words, count, request.form.get(SHUFFLE_CHECKBOX))

        return send_file(buffer, "generated_boards.pdf", "application/pdf")

    else:
        return (
            "Unsupported method",
            HTTPStatus.METHOD_NOT_ALLOWED
        )
