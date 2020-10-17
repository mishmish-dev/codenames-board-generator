from typing import List
from words import load_wordlists, NamedWordlist


WORDS_FILE_INPUT = "words_file_input"
WORDS_TEXT_INPUT = "words_text_input"
WORDLIST_INPUT = "wordlist_input"
COUNT_INPUT = "count_input"
SHUFFLE_CHECKBOX = "shuffle_checkbox"
WORDLISTS = load_wordlists("wordlists")


def wordlist_selector_options(wordlists: List[NamedWordlist]) -> str:
    return "\n".join("            <option value={value}>{name}</option>".format(
        value=idx,
        name=name
    ) for (idx, name) in enumerate(w.name for w in wordlists)) + "\n"


index_page = f'''
<!doctype html>
<title>Генератор полей для Коднеймс</title>

<p><b>Слова разделяются запятыми и/или переводами строк.<br>
Слова <i>могут</i> содержать пробелы (лишние мы обрежем).</b></p>

<form method=post enctype=multipart/form-data>
    <fieldset>
        <legend>Для слов из файла (должен быть в UTF-8):</legend>
        <input type=file id="{WORDS_FILE_INPUT}" name="{WORDS_FILE_INPUT}">
        <br>
        <label for="{SHUFFLE_CHECKBOX}">Перемешать:</label>
        <input type=checkbox id="{SHUFFLE_CHECKBOX}" name="{SHUFFLE_CHECKBOX}">
        <br>
        <label for="{COUNT_INPUT}">Макс. число полей (0=неогр.):</label>
        <input type=number min=0 max=200 value=0 id="{COUNT_INPUT}" name="{COUNT_INPUT}">
        <br>
        <input type=submit value="Сгенерировать!">
    </fieldset>
</form>

<br>

<form method=post enctype=multipart/form-data>
    <fieldset>
        <legend>Для слов из набора:</legend>
        <select id="{WORDLIST_INPUT}" name="{WORDLIST_INPUT}">{wordlist_selector_options(WORDLISTS)}</select>
        <br>
        <label for="{SHUFFLE_CHECKBOX}">Перемешать:</label>
        <input type=checkbox id="{SHUFFLE_CHECKBOX}" name="{SHUFFLE_CHECKBOX}" checked=true>
        <br>
        <label for="{COUNT_INPUT}">Макс. число полей (0=неогр.):</label>
        <input type=number min=0 max=200 value=0 id="{COUNT_INPUT}" name="{COUNT_INPUT}">
        <br>
        <input type=submit value="Сгенерировать!">
    </fieldset>
</form>

<br>

<form method=post enctype=multipart/form-data>
    <fieldset>
        <legend>Для слов из текстовой формы:</legend>
        <textarea name={WORDS_TEXT_INPUT} rows=8 style="width:400px"></textarea>
        <br>
        <label for="{SHUFFLE_CHECKBOX}">Перемешать:</label>
        <input type=checkbox id="{SHUFFLE_CHECKBOX}" name="{SHUFFLE_CHECKBOX}">
        <br>
        <label for="{COUNT_INPUT}">Макс. число полей (0=неогр.):</label>
        <input type=number min=0 max=200 value=0 id="{COUNT_INPUT}" name="{COUNT_INPUT}">
        <br>
        <input type=submit value="Сгенерировать!">
    </fieldset>
</form>
'''
