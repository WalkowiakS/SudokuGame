import pygame as pg
from pygame.constants import QUIT
from math import sqrt


class Game:
    # colors
    LINE_THICK = (0, 0, 0)
    LINE_THIN = (128, 128, 128)
    HIGHLIGHT = (153, 255, 153)
    BACK_COLOR = (255, 255, 255)
    ORIG_NUMS = (0, 0, 0)

    # other variables for visuals
    THIN = 2  # thin lines
    THICK = 5  # thick lines

    # screen dimensions
    WIDTH = 700
    HEIGHT = 900

    def __init__(self, board, size):
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))  # pygame display
        self.box_size = self.WIDTH // size  # pixel size of grid boxes

        self.size = int(sqrt(len(board)))  # width and height of board
        self.block = int(sqrt(self.size))  # size of board sections
        self.orig = board  # original board
        self.board = board  # orig board with user input added
        self.note = [[0 for x in range(size)] for x in range(size)]  # user's notes for each square

    def draw_grid(self):
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(self.BACK_COLOR)
        self.screen.blit(background, (0, 0))

        # draw base grid lines
        # offset = (self.WIDTH - (self.box_size * self.size)) / 2
        offset = 0

        for i in range(self.size + 1):
            if i % self.block == 0:
                width = self.THICK
                color = self.LINE_THICK
            else:
                color = self.LINE_THIN
                width = self.THIN

            pg.draw.line(self.screen, color, (offset, i * self.box_size),
                         (offset + self.size * self.box_size, i * self.box_size), width)
            pg.draw.line(self.screen, color, (i * self.box_size, offset),
                         (i * self.box_size, self.size * self.box_size + offset), width)

        pg.display.flip()

    def fill_grid(self):
        font1 = pg.font.Font("OTR type/fonts/otf/OTRtypeGX.ttf", 60)
        x = 0
        y = 0

        # iterate through list and add numbers to board
        for num in self.board:
            if x == self.size:
                x = 0
                y += 1

            if num != 0:
                text = font1.render(str(num), 1, self.ORIG_NUMS)
                size = pg.font.Font.size(font1, str(num))
                w_offset = (self.box_size - size[0]) / 2
                h_offset = (self.box_size - size[1]) / 2
                self.screen.blit(text, (x * self.box_size + w_offset, y * self.box_size + h_offset))

            x += 1

        pg.display.flip()

    def run_game(self):
        # set up visuals
        pg.init()
        self.draw_grid()
        self.fill_grid()

        # display screen

        # run game loop
        while 1:
            for event in pg.event.get():
                if event.type == QUIT:
                    return
