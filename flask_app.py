from http import HTTPStatus

from flask import Flask, request, send_file

from generate import generate_pdf, split_words, initialize_resources


WORDS_FILE_INPUT = "words_file"
WORDS_TEXT_INPUT = "words_text"


initialize_resources("card.png", "PTSansBold.ttf", "PTSansBoldItalic.ttf")
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def generate_codenames_board():
    if request.method == "GET":
        return """
            <!doctype html>
            <title>Generate printable Codenames board(s)</title>
            <h2>Submit your words</h2>
            
            <form method=post enctype=multipart/form-data>
                <fieldset>
                    <legend>From a text file in UTF-8:</legend>
                    must be in UTF-8
                    <br />
                    <input type=file name={words_file}>
                    <input type=submit value=Generate!>
                </fieldset>
            </form>

            <br />

            <form method=post enctype=multipart/form-data>
                <fieldset>
                    <legend>Via form:</legend>
                    words are separated by commas or newlines
                    <br />
                    <textarea name={words_text} rows=5 columns=50></textarea>
                    <br />
                    <input type=submit value=Generate!>
                </fieldset>
            </form>

        """.format(words_file=WORDS_FILE_INPUT, words_text=WORDS_TEXT_INPUT)

    else:
        if WORDS_FILE_INPUT in request.files:
            words_file = request.files[WORDS_FILE_INPUT]

            try:
                words_raw = words_file.read().decode("utf-8")
            except:
                return (
                    "Could not decode the text file. Make sure that your file is UTF-8.",
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )

        elif WORDS_TEXT_INPUT in request.form:
            words_raw = request.form[WORDS_TEXT_INPUT]

        else:
            return "Request not recognized", HTTPStatus.NOT_FOUND

        buffer = generate_pdf(split_words(words_raw))
        buffer.name = "generated_boards.pdf"
        
        return send_file(buffer, mimetype="application/pdf")


