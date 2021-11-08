# class for working with regular sudoku boards (normal rows, columns, and blocks)
# -board size must be a perfect square
from math import sqrt


class Board:
    def __init__(self, board, size):
        self.board = board  # board that will be modified
        self.orig = board  # reference board
        self.size = size  # width and height of board
        self.block_size = int(sqrt(size))  # size of board sections

    def print_board(self):
        # prints board in neat rows
        text = ""
        count = 1
        for num in self.board:
            text = text + "  " + str(num)
            if count % self.block_size == 0:
                text += "|"
            if count == self.size:
                print(text)
                text = ""
                count = 0
            count += 1

    def get_sections(self, pos):
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
        for i in range(0, self.block_size):
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

    def solve(self, pos):
        # last position checked, board is solved
        if self.is_solved():
            return True

        # number is from original board, do not change
        if self.orig[pos] != 0:
            return self.solve(pos+1)

        # unassigned space, try to insert values
        for num in range(1, self.size + 1):

            # see if num is valid
            if self.valid_num(pos, num):
                self.board[pos] = num

                # try solving rest of puzzle with that num in pos
                if self.solve(pos+1):
                    return True

                # solution has failed, undo assignment
                self.board[pos] = 0

        # backtrack and start new path
        return False
