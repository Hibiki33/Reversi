from Board import Board

class Player(object):

    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        while True:
            action = input()
            if len(action) > 2:
                print('Invalid input!')
            elif action == 'Q' or action == 'q':
                print('Quit!')
                return 'Q'
            else:
                row, col = action[1].upper(), action[0].upper()
                if row in '12345678' and col in 'ABCDEFGH':
                    if action in board.get_legal_board(self.color):
                        return action
                print('Invalid position!')


if __name__ == '__main__':
    board = Board()
    board.board[3][5] = 'X'
    board.display()

    player = Player('O')
    player.get_move(board)
