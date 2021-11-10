# classes for working with regular sudoku boards (normal rows, columns, and blocks)
# SolveBoard and CreateBoard classes
from math import sqrt
import random


class SolveBoard:
    # -board size must be a perfect square
    def __init__(self, board):
        self.board = board  # board that will be modified
        self.orig = board  # reference board
        self.size = int(sqrt(len(board)))  # width and height of board
        self.block_size = int(sqrt(self.size))  # size of board sections

    def get_sections(self, pos):
        # gets row, column, and block that pos is a part of
        # returns them as 3 lists

        # get row that contains number at pos~~~~~~~~~~~~~~~~~~~~~~~~~~
        row_num = pos // self.size
        beginning = row_num * self.size
        row = self.board[beginning: (beginning + self.size)]

        # get column that contains number at pos~~~~~~~~~~~~~~~~~~~~~~~
        col_num = pos - (row_num * self.size)
        column = self.board[col_num:: self.size]

        # get block that contains number at pos~~~~~~~~~~~~~~~~~~~~~~~~~
        block_row = row_num // self.block_size
        block_col = col_num // self.block_size

        # find index of upper left number in block that pos is in
        start = (block_row * self.size * self.block_size) + (block_col * self.block_size)

        # make list from numbers in block
        block = []
        for i in range(self.block_size):
            block += self.board[start: (start + self.block_size)]
            start += self.size

        return row, column, block

    def valid_num(self, pos, num):
        # checks if a number (num) is valid in the proposed position (pos)
        # get sections to check num against
        row, col, block = self.get_sections(pos)

        # check row
        for n in row:
            if n == num:
                return False

        # check column
        for n in col:
            if n == num:
                return False

        # check block
        for n in block:
            if n == num:
                return False

        # passes all tests, num is valid
        return True

    def is_solved(self):
        # checks if board is complete (no blank spaces) and returns true if complete, false if not
        solved = True
        for num in self.board:
            if num == 0:
                solved = False
        return solved

    def solve(self, pos=0):
        # solves board using backtracking

        # last position checked, board is solved
        if self.is_solved():
            return True

        # number is from original board, do not change
        if self.orig[pos] != 0:
            return self.solve(pos + 1)

        # unassigned space, try to insert values
        for num in range(1, self.size + 1):

            # see if num is valid
            if self.valid_num(pos, num):
                self.board[pos] = num

                # try solving rest of puzzle with that num in pos
                if self.solve(pos + 1):
                    return True

                # solution has failed, undo assignment
                self.board[pos] = 0

        # backtrack and start new path
        return False


class CreateBoard:
    FILE_NAME = "SeedBoards.txt"  # file that contains seed boards

    # all boards in the file begin with two digits that represent the board size
    # next is a character that represents the difficulty
    # followed by numbers that are in the actual board
    # ex: 09E00078000... (this is a size 9x9 board with a difficulty of easy

    def __init__(self, difficulty, size):
        self.level = difficulty
        self.size = size
        self.board = self.get_seed()

    def get_seed(self):
        with open(self.FILE_NAME, 'r') as reader:
            text = reader.readlines()

        # make list with all boards that meet the size and difficulty criteria
        board_list = []
        for line in text:
            line = line.strip()
            if int(line[0:2]) == self.size and line[2:3] == self.level:
                board_list += [line[3:]]

        # choose random board from list
        board = list(random.choice(board_list))

        # convert board elements to ints
        board = [int(i) for i in board]

        return board

    def create_board(self):
        # Takes a seed board and transforms it so the user won't be able to recognize it
        # Randomizes numbers, rotates a random amount and flips a random amount

        # randomize numbers~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # create list of possible numbers for board size and shuffle
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)

        # create dictionary that pairs number list with random number list
        num_key = {0: 0}
        for i in range(1, self.size + 1):
            num_key.update({i: nums[i - 1]})

        # replace numbers in board with the new numbers
        temp = []
        for i in self.board:
            temp += [num_key.get(i)]

        self.board = temp

        # rotate board~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4 possible rotations, 0, 90, 180, 270
        rotation = random.randint(0, 3)  # 0=0 degree, 1=90 degree, 2=180, 3=270

        # slice board into columns, reverse numbers in column, create new board using columns as rows
        # repeat until desired rotation
        for i in range(rotation):
            columns = []
            for j in range( self.size):
                col = self.board[j:: self.size]
                col.reverse()
                columns += [col]
            # re-make board with reversed columns
            self.board = []
            for k in range(self.size):
                self.board += columns[k]

        # flip horizontally, vertically, or both ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        flip = random.randint(0, 3)  # 0= flip both ways, 1= horizontal, 2= vertical, 3= no flip

        # Horizontal flip
        if flip == 0 or flip == 1:
            temp = []
            # reverse each row
            for i in range(self.size):
                temp += reversed(self.board[(i * self.size):((i + 1) * self.size)])
            self.board = temp

        # vertical flip
        if flip == 0 or flip == 2:
            temp = []
            # reverse order of rows
            for i in reversed(range(self.size)):
                temp += self.board[(i * self.size):((i + 1) * self.size)]

            self.board = temp

        # ADD ROW AND COL SWAPPING
