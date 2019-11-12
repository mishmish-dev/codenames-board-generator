from http import HTTPStatus

from flask import Flask, request, send_file

from generate import generate_pdf, split_words, initialize_resources


WORDS_INPUT = "words_input"
COUNT_INPUT = "count_input"
SHUFFLE_CHECKBOX = "shuffle_checkbox"


initialize_resources("card.png", "PTSansBold.ttf", "PTSansBoldItalic.ttf")
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def generate_codenames_board():
    if request.method == "GET":
        return """
            <!doctype html>
            <title>Генератор полей для Коднеймс</title>

            <p><b>Слова разделяются запятыми и/или переводами строк.<br>
            Слова <i>могут</i> содержать пробелы (лишние мы обрежем).</b></p>

            <form method=post enctype=multipart/form-data>
                <fieldset>
                    <legend>Для слов из файла (должен быть в UTF-8):</legend>
                    <input type=file name={words}>
                    <br>
                    Перемешать слова в списке:<input type=checkbox name={shuffle}>
                    <br>
                    Сделать не больше N штук (0=неограниченно): <input type=number min=0 max=200 value=0 name={count}>
                    <br>
                    <input type=submit value=Сгенерировать!>
                </fieldset>
            </form>

            <br>

            <form method=post enctype=multipart/form-data>
                <fieldset>
                    <legend>Для слов из текстовой формы:</legend>
                    <textarea name={words} rows=8 style="width:400px"></textarea>
                    <br>
                    Перемешать слова в списке:<input type=checkbox name={shuffle}>
                    <br>
                    Сделать не больше N штук (0=неограниченно): <input type=number min=0 max=200 value=0 name={count}>
                    <br>
                    <input type=submit value=Сгенерировать!>
                </fieldset>
            </form>

        """.format(words=WORDS_INPUT, shuffle=SHUFFLE_CHECKBOX, count=COUNT_INPUT)

    else:
        if WORDS_INPUT in request.files:
            words_file = request.files[WORDS_INPUT]

            try:
                words_raw = words_file.read().decode("utf-8")
            except:
                return (
                    "Не удалось прочесть файл. Убедитесь, что он в UTF-8.",
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )

        elif WORDS_INPUT in request.form:
            words_raw = request.form[WORDS_INPUT]

        else:
            return "Request not recognized", HTTPStatus.NOT_FOUND

        try:
            count = int(request.form[COUNT_INPUT])
        except:
            count = None

        buffer = generate_pdf(split_words(words_raw), count, request.form.get(SHUFFLE_CHECKBOX))
        buffer.name = "generated_boards.pdf"
        
        return send_file(buffer, mimetype="application/pdf")


