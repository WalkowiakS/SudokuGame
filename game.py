import pygame as pg
import pygame.mouse
from pygame.constants import QUIT
from math import sqrt
import threading
from board import SolveBoard, CreateBoard
from controls import *


class Game:
    # colors
    LINE_THICK = (194, 146, 80)
    LINE_THIN = (194, 146, 80)
    HIGHLIGHT = (44,100,115)
    HIGHLIGHT2 = (113, 120, 148)
    BACK_COLOR = (51,56,78)
    ORIG_NUMS = (177,124,115)
    NUMS = (206,189,163)
    INCORRECT = (148, 56, 56)
    SOLVED = (0, 0, 0)

    # other variables for visuals
    THIN = 1  # thin lines
    THICK = 5  # thick lines
    # font1 = pg.font.Font("Ardeco.ttf", 70)

    # screen dimensions
    WIDTH = 700
    HEIGHT = 900

    def __init__(self, difficulty, size):
        self.difficulty = difficulty
        self.size = size  # width and height of board
        self.block = int(sqrt(self.size))  # size of board sections

        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))  # pygame display
        self.box_size = self.WIDTH // self.size  # pixel size of grid boxes
        self.pos = [0, 0]  # currently selected position in board

        self.orig = []  # original board
        self.board = list(self.orig)  # orig board with user input added
        # TODO note functionality
        self.note = [[0 for x in range(self.size)] for x in range(self.size)]  # user's notes for each square


    def draw_grid(self):
        # draw base grid lines
        # TODO fix offset of board
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


    def fill_grid(self):
        # iterate through list and add numbers to board
        for i in range(self.size*self.size):

        # change color for original numbers
            if self.orig[i] != 0:
                color = self.ORIG_NUMS
            else:
                color = self.NUMS

            self.draw_number(self.board[i], i, color)


    def create_buttons(self):
        button_list = []
        #new game
        btn_new_game = Button(self.screen, "New Game", (300, 750), 30)
        button_list.append(btn_new_game)

        #reset board
        btn_reset = Button(self.screen, "Reset", (300, 850), 20)
        button_list.append(btn_reset)

        #solve board
        btn_solve = Button(self.screen, "Solve", (200, 850), 20)
        button_list.append(btn_solve)

        return button_list


    def draw_number(self, num, pos, color):
        font = pg.font.Font("Ardeco.ttf", self.box_size - (self.box_size//8))
        if num != 0:
            text = font.render(str(num), True, color)
            size = pg.font.Font.size(font, str(num))
            w_offset = (self.box_size - size[0]) / 2
            h_offset = (self.box_size - size[1]) / 2
            y_pos = pos // self.size
            x_pos = pos - (y_pos * self.size)
            self.screen.blit(text, (x_pos * self.box_size + w_offset, y_pos * self.box_size + h_offset))


    def get_selected_block(self):
        #get and set currently selected block
        pos = pg.mouse.get_pos()

        # make sure it is in range
        if pos[1] < (self.size * self.box_size) and pos[0] < (self.size * self.box_size):
            self.pos[0] = pos[0] // self.box_size
            self.pos[1] = pos[1] // self.box_size
            return True

    def highlight(self):
        # TODO add highlight to row and col that box is in
        # highlight the currently selected box
        pg.draw.rect(self.screen, self.HIGHLIGHT, (self.pos[0]*self.box_size,
                                                   self.pos[1]*self.box_size,
                                                   self.box_size,self.box_size))

        #highlight row and col


    def input_num(self, num):
        # ** IMPORTANT ** does not check if position is valid. User is allowed to make mistakes
        # TODO check if user num is in range
        index = self.pos[0] + (self.pos[1] * self.size)

        # test if position is defined in orig board
        if self.orig[index] == 0:
            # add user input to board
            index = self.pos[0] + (self.pos[1]*self.size)
            self.board[index] = num

    # TODO check solution


    def display_solution(self):
        # wipe board
        background = pg.Surface(self.screen.get_size())
        background.fill(self.BACK_COLOR)
        self.screen.blit(background, (0, 0))
        self.draw_grid()

        #get solution
        solver = SolveBoard(list(self.orig))
        solver.solve()
        solved = solver.board

        # show incorrect values
        for i in range(self.size*self.size):
            if self.orig[i] != 0:
                self.draw_number(self.orig[i], i, self.ORIG_NUMS)
            elif self.board[i] == 0:
                self.draw_number(solved[i], i, self.SOLVED)
            elif self.board[i] == solved[i]:
                # user had correct answer
                self.draw_number(solved[i], i, self.NUMS)
            else:
                # user's answer was incorrect. display correct ans next to it
                text = str(self.board[i]) + "|" + str(solved[i])
                self.draw_number(text, i, self.INCORRECT)


    def reset_game(self):
        # get new board
        create = CreateBoard(self.difficulty, self.size)
        create.create_board()

        # reset everything to use new board
        self.orig = create.board
        self.clear_board()

        # start thread to solve puzzle in the background



    def clear_board(self):
        self.board = list(self.orig)
        self.pos = [0, 0]
        self.note = [[0 for x in range(self.size)] for x in range(self.size)]


    def run_game(self):
        # set up visuals
        pg.init()
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(self.BACK_COLOR)
        self.screen.blit(background, (0, 0))

        buttons = self.create_buttons()

        status = 0  # used to control what output is shown

        # get board
        self.reset_game()

        # run game loop
        while 1:
            for event in pg.event.get():
                if event.type == QUIT:
                    return

                # Highlight new selection
                if status == 0:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # click was inside board area
                        if self.get_selected_block():
                            self.highlight()
                        else:
                            # check if button was clicked
                            for button in buttons:
                                if button.back.collidepoint(pg.mouse.get_pos()):
                                    if button.text == "New Game":
                                        self.reset_game()
                                        status = 0
                                    elif button.text == "Reset":
                                        self.clear_board()
                                        status = 0
                                    else:
                                        self.display_solution()
                                        status = 1


                    if event.type == pg.KEYDOWN:
                        # navigate with arrow keys
                        key = event.key
                        if key == pg.K_LEFT:
                            if self.pos[0] != 0:
                                self.pos[0] -= 1
                                self.highlight()
                        if key == pg.K_RIGHT:
                            if self.pos[0] != self.size -1:
                                self.pos[0] += 1
                                self.highlight()
                        if key == pg.K_UP:
                            if self.pos[1] != 0:
                                self.pos[1] -= 1
                                self.highlight()
                        if key == pg.K_DOWN:
                            if self.pos[1] != self.size-1:
                                self.pos[1] += 1
                                self.highlight()

                        # get user input number
                        # TODO figure out numbers for 16x16
                        if key == pg.K_1:
                            self.input_num(1)
                        if key == pg.K_2:
                            self.input_num(2)
                        if key == pg.K_3:
                            self.input_num(3)
                        if key == pg.K_4:
                            self.input_num(4)
                        if key == pg.K_5:
                            self.input_num(5)
                        if key == pg.K_6:
                            self.input_num(6)
                        if key == pg.K_7:
                            self.input_num(7)
                        if key == pg.K_8:
                            self.input_num(8)
                        if key == pg.K_9:
                            self.input_num(9)

                        # other input keys
                        if key == pg.K_0:
                            self.input_num(0) # 0 erases the selected square
                        if key == pg.K_s:
                            self.display_solution()
                            status = 1

                # TODO space to switch to notes

                # refresh screen
                if status == 0:
                    self.screen.blit(background, (0, 0))
                    self.highlight()
                    self.draw_grid()
                    self.fill_grid()
                    for button in buttons:
                        button.draw_button()

                else:
                    buttons[0].draw_button()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # check if new game was clicked
                        if buttons[0].back.collidepoint(pygame.mouse.get_pos()):
                            self.reset_game()
                            status = 0


            pg.display.flip()
