from argparse import ArgumentParser
from sys import stdin
from typing import List

from generate import generate_pdf, register_fonts


def split_words(words_raw: str) -> List[str]:
    splitted = words_raw.replace(",", "\n").splitlines(keepends=False)

    result = []
    for line in splitted:
        parts = line.split()
        if parts:
            result.append(" ".join(parts))

    return result


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help=(
        "input file (supply '-' to read from stdin), "
        "words are separated by commas or newlines"
    ))
    parser.add_argument("--output", "-o", default="output.pdf", help="output PDF file")
    parser.add_argument("--card", "-c", default="card.png", help="word card template image")
    parser.add_argument("--primary-font", "-p", default="PTSansBold.ttf", help="primary font file")
    parser.add_argument("--secondary-font", "-s", default="PTSansBoldItalic.ttf", help="secondary font file")

    args = parser.parse_args()
    if args.input == "-":
        words_raw = stdin.read()
    else:
        with open(args.input) as words_file:
            words_raw = words_file.read()

    words = split_words(words_raw)
    print(*words)

    register_fonts(args.primary_font, args.secondary_font)
    generated_bytes = generate_pdf(args.card, words)

    with open(args.output, "wb") as output_file:
        output_file.write(generated_bytes)

    