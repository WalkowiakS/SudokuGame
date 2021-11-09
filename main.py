from board import *

if __name__ == '__main__':
    board = CreateBoard('E', 9)
    board.create_board()
    print("solve")

    test_board = SolveBoard(board.board)
    test_board.solve()
    test_board.print_board()
