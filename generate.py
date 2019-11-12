from io import BytesIO
from random import shuffle
from typing import Iterable, Iterator, List, Optional, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
SIDE_MARGIN = 0.5*mm
TOP_MARGIN = 15*mm

CARD_WIDTH, CARD_HEIGHT = 67*mm, 43*mm
CARD_VERTICAL_OFFSET = 48*mm

BOARD_WORD_COUNT = 25

PRIMARY_FONT_NAME = "PrimaryFaceBlah"
SECONDARY_FONT_NAME = "SecondaryFaceBlah"

PRIMARY_TEXT_MAX_WIDTH = 51.5*mm
PRIMARY_TEXT_DEFAULT_SIZE = 9*mm
PRIMARY_TEXT_COLOR = black

SECONDARY_TEXT_MAX_WIDTH = 37*mm
SECONDARY_TEXT_DEFAULT_SIZE = 6.5*mm
SECONDARY_TEXT_COLOR = HexColor(0x877250)


_card_image: Optional[ImageReader] = None


def initialize_resources(card_image_path: str, primary_font_path: str, secondary_font_path: str) -> None:
    pdfmetrics.registerFont(TTFont(PRIMARY_FONT_NAME, primary_font_path))
    pdfmetrics.registerFont(TTFont(SECONDARY_FONT_NAME, secondary_font_path))

    global _card_image
    _card_image = ImageReader(card_image_path)


def split_words(words_raw: str) -> List[str]:
    splitted = words_raw.replace(",", "\n").splitlines(keepends=False)

    result = []
    for line in splitted:
        parts = line.split()
        if parts:
            result.append(" ".join(parts))

    return result


class BoardPdfBuilder:
    def __init__(self, output_file) -> None:
        self.canvas = Canvas(output_file, pagesize=A4)


    def draw_primary_text(self, x, y, text: str) -> None:
        textobj = self.canvas.beginText()
        
        size = PRIMARY_TEXT_DEFAULT_SIZE
        width = self.canvas.stringWidth(text, PRIMARY_FONT_NAME, size)
        if width >= PRIMARY_TEXT_MAX_WIDTH:
            size *= PRIMARY_TEXT_MAX_WIDTH / width
            width = self.canvas.stringWidth(text, PRIMARY_FONT_NAME, size)

        textobj.setFont(PRIMARY_FONT_NAME, size)

        textobj.setTextOrigin(x - width / 2, y - 0.35 * size)
        
        textobj.textOut(text)

        self.canvas.setFillColor(PRIMARY_TEXT_COLOR)
        self.canvas.drawText(textobj)


    def draw_secondary_text(self, x, y, text: str) -> None:
        textobj = self.canvas.beginText()
        
        size = SECONDARY_TEXT_DEFAULT_SIZE
        width = self.canvas.stringWidth(text, SECONDARY_FONT_NAME, size)
        if width >= SECONDARY_TEXT_MAX_WIDTH:
            size *= SECONDARY_TEXT_MAX_WIDTH / width
            width = self.canvas.stringWidth(text, SECONDARY_FONT_NAME, size)

        textobj.setFont(SECONDARY_FONT_NAME, size)

        textobj.setTextOrigin(-x - width / 2, -y - 0.7 * size)
        
        textobj.textOut(text)

        self.canvas.saveState()
        self.canvas.rotate(180)

        self.canvas.setFillColor(SECONDARY_TEXT_COLOR)
        self.canvas.drawText(textobj)

        self.canvas.restoreState()


    def draw_card(self, row: int, column: int, word: str) -> None:
        if column == 0:
            x = SIDE_MARGIN
        elif column == 1:
            x = PAGE_WIDTH / 2 - CARD_WIDTH / 2
        else:
            x = PAGE_WIDTH - CARD_WIDTH - SIDE_MARGIN

        y = PAGE_HEIGHT - CARD_HEIGHT - row * CARD_VERTICAL_OFFSET - TOP_MARGIN

        self.canvas.drawImage(_card_image, x, y, CARD_WIDTH, CARD_HEIGHT)

        self.draw_primary_text(x + CARD_WIDTH / 2, y + 11.8*mm, word)
        self.draw_secondary_text(x + 26.5*mm, y + 22.7*mm, word)

    def draw_column(self, column: int, words_iterator: Iterator[str]) -> None:
        for row in range(5):
            self.draw_card(row, column, next(words_iterator).upper())

    def add_board(self, words: Iterable[str]) -> None:
        it = iter(words)

        for column in range(3):
            self.draw_column(column, it)

        self.canvas.showPage()

        for column in range(1, 3):
            self.draw_column(column, it)

        self.canvas.showPage()

    def build(self) -> None:
        self.canvas.save()


def generate_pdf(words: Iterable[str], count: Optional[int] = None, shuffle_words: bool = True) -> bytes:
    buffer = BytesIO()
    builder = BoardPdfBuilder(buffer)

    words = list(words)
    if shuffle_words:
        shuffle(words)
        
    if count is not None:
        words = words[:(count * BOARD_WORD_COUNT)]

    for i in range(len(words) // BOARD_WORD_COUNT):
        builder.add_board(words[(i * BOARD_WORD_COUNT):((i + 1) * BOARD_WORD_COUNT)])

    builder.build()

    buffer.seek(0)
    return buffer.read()