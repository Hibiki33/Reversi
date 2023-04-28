import random
from Board import Board

class Roxanne(object):
    '''
    Analysis of Monte Carlo Techniques in Othello
    Contributor: R. Roxanne
    https://www.cs.rit.edu/~rlc/
    '''

    def __init__(self, color):
        self.roxanne_table = [
            ['A1', 'H1', 'A8', 'H8'],
            ['C3', 'F3', 'C6', 'F6'],
            ['C4', 'F4', 'C5', 'F5', 'D3', 'E3', 'D6', 'E6'],
            ['A3', 'H3', 'A6', 'H6', 'C1', 'F1', 'C8', 'F8'],
            ['A4', 'H4', 'A5', 'H5', 'D1', 'E1', 'D8', 'E8'],
            ['B3', 'G3', 'B6', 'G6', 'C2', 'F2', 'C7', 'F7'],
            ['B4', 'G4', 'B5', 'G5', 'D2', 'E2', 'D7', 'E7'],
            ['B2', 'G2', 'B7', 'G7'],
            ['A2', 'H2', 'A7', 'H7', 'B1', 'G1', 'B8', 'G8']
        ]
        self.color = color

    def select(self, board):
        board_list = list(board.get_legal_board(self.color))
        if len(board_list) == 0:
            return None
        else:
            for move_list in self.roxanne_table:
                random.shuffle(move_list)
                for move in move_list:
                    if move in board_list:
                        return move


if __name__ == '__main__':
    board = Board()
    board.board[3][5] = 'X'
    board.display()

    roxanne = Roxanne('X')
    print(roxanne.select(board))
