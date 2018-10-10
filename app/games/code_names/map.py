import random

import more_itertools as mit
from PIL import Image, ImageFont

from app.utils import resource, ctx_if
from app.games.code_names import config
from app.games.code_names.cell import Cell


class Map:

    def __init__(self, cells):
        self.cells = cells
        self._dict = None

    def __getitem__(self, word):
        if self._dict is None:
            self._build_dict()

        y, x = self._dict[word]
        return self.cells[y][x]

    def as_img(self, reveal=False):
        map_img = Image.new('RGB', config.MAP_SIZE)

        font = ImageFont.truetype(
            font=resource.font(config.FONT),
            size=config.FONT_SIZE
        )

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                with ctx_if(reveal, cell.color_up()):
                    cell_img = cell.as_img(font=font)
                    box = (
                        y * config.CELL_WIDTH,
                        x * config.CELL_HEIGHT,
                        (y + 1) * config.CELL_WIDTH,
                        (x + 1) * config.CELL_HEIGHT,
                    )
                    map_img.paste(cell_img, box)

        return map_img

    def _build_dict(self):
        self._dict = {
            cell.word: (y, x)
            for y, row in enumerate(self.cells)
            for x, cell in enumerate(row)
        }

    @classmethod
    def random(cls, words):
        assert len(words) >= config.TOTAL_CELLS

        words = random.sample(words, config.TOTAL_CELLS)

        cells = [
            Cell(word=words.pop(), color=config.COLOR_BLUE)
            for _ in range(config.BLUE_CELLS)
        ] + [
            Cell(word=words.pop(), color=config.COLOR_RED)
            for _ in range(config.RED_CELLS)
        ] + [
            Cell(word=words.pop(), color=config.COLOR_WHITE)
            for _ in range(config.WHITE_CELLS)
        ] + [
            Cell(word=words.pop(), color=config.COLOR_BLACK)
            for _ in range(config.BLACK_CELLS)
        ]

        random.shuffle(cells)
        matrix = mit.chunked(cells, config.CELLS_IN_ROW)

        return cls(cells=list(matrix))
