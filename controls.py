# contains all classes related to game controls
import pygame as pg

class Button:
    # button colors
    BACK = (194, 146, 80)
    HIGHLIGHT = (111, 119, 159)
    SHADOW = (23,28,53)
    TEXT = (51,56,78)

    OUTLINE_WIDTH = 4
    PADDING_W = .75    # used to calc space between button edge and button text
    PADDING_H = .25

    def __init__(self, screen,text, pos, font_size):
        self.screen = screen
        self.pos = pos
        self.back = pg.Rect((pos[0], pos[1]), (1, 1))
        self.text = text
        self.font_size = font_size
        self.width = 1      # default width and height. will be changed to fit text
        self.height = 1



    def draw_button(self):
        # font settings
        # TODO adjust button size by text size
        font = pg.font.Font("Ardeco.ttf", self.font_size)
        size = pg.font.Font.size(font, self.text)  # get size of string in selected font
        text = font.render(self.text, True, self.TEXT)

        # get and set button size based on text string length and height
        self.width = size[0]+ (size[1] * self.PADDING_W)
        self.height = size[1] + (size[1] * self.PADDING_H)
        self.back.update(self.pos[0], self.pos[1], self.width, self.height)

        # draw button shape
        pg.draw.rect(self.screen, self.BACK, self.back)

        # highlight lines
        pg.draw.line(self.screen, self.HIGHLIGHT,
                     (self.pos[0], self.pos[1] - (self.OUTLINE_WIDTH // 2)),
                     (self.pos[0] + self.width + (self.OUTLINE_WIDTH // 2), self.pos[1] - (self.OUTLINE_WIDTH // 2)),
                     self.OUTLINE_WIDTH)
        pg.draw.line(self.screen, self.HIGHLIGHT,
                     (self.pos[0] - (self.OUTLINE_WIDTH // 2), self.pos[1] - self.OUTLINE_WIDTH),
                     (self.pos[0] - (self.OUTLINE_WIDTH // 2), self.pos[1] + self.height + self.OUTLINE_WIDTH),
                     self.OUTLINE_WIDTH)

        # shadow lines
        pg.draw.line(self.screen, self.SHADOW,
                     (self.pos[0], self.pos[1] + self.height+(self.OUTLINE_WIDTH//2)),
                     (self.pos[0] + self.width, self.pos[1]+self.height + (self.OUTLINE_WIDTH//2)),
                     self.OUTLINE_WIDTH)
        pg.draw.line(self.screen, self.SHADOW,
                     (self.pos[0]+self.width + (self.OUTLINE_WIDTH//2), self.pos[1]),
                     (self.pos[0]+self.width + (self.OUTLINE_WIDTH//2), self.pos[1]+ self.height+self.OUTLINE_WIDTH),
                     self.OUTLINE_WIDTH)

        # draw text
        text_pos = [0,0]
        # text_pos[0] = self.pos[0] + (self.width - (size[0]//2))
        text_pos[0] = self.pos[0] + ((self.width - size[0])//2)
        text_pos[1] = self.pos[1] + (self.height - size[1])//2
        self.screen.blit(text, text_pos)


class RadioBtn:
    # dimensions and colors
    RADIUS = 10
    OUTLINE_WIDTH = 2

    BACK = (206,189,163)
    OUTLINE = (23,28,53)
    SELECTED = (44,100,115)


    def __init__(self, screen, text, pos, selected):
        self.screen = screen
        self.text = text    # text is a list of all button names in group
        self.pos = pos
        self.selected = selected    # default selection


    def draw_radio_list(self):
        pass

    def radio_btn_item(self):
        pass

    def change_selected(self):
        pass

    def get_selected(self):
        pass

