from board import Board

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = [5, 0, 0, 0, 8, 3, 7, 6, 9,
            0, 9, 3, 0, 0, 0, 1, 0, 0,
            0, 1, 0, 5, 0, 4, 0, 0, 3,
            0, 0, 2, 3, 5, 8, 0, 0, 7,
            0, 7, 0, 0, 2, 0, 0, 5, 8,
            9, 5, 8, 0, 0, 7, 0, 3, 0,
            2, 0, 0, 4, 0, 0, 0, 7, 6,
            4, 0, 9, 0, 0, 0, 5, 0, 0,
            7, 0, 0, 2, 1, 0, 3, 0, 0
            ]

    test_board = Board(test, 9)
    test_board.print_board()
    print()
    test_board.solve(0)
    test_board.print_board()
