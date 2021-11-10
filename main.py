from board import *
from game import *

if __name__ == '__main__':
    board = CreateBoard('E', 9)
    board.create_board()
    board = board.board

    g = Game(board, 9)
    g.run_game()
