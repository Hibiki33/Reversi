from Board import Board
import datetime  
from copy import deepcopy
from func_timeout import func_timeout, FunctionTimedOut

class Game(object):

    def __init__(self, black_player, white_player):
        self.board = Board()  
        self.current_player = None
        self.black_player = black_player  
        self.white_player = white_player  
        self.black_player.color = 'X'
        self.white_player.color = 'O'

    def switch_player(self, black_player, white_player):
        if self.current_player is None:
            return black_player
        else:
            if self.current_player == self.black_player:
                return white_player
            else:
                return black_player

    def print_winner(self, winner):
        print(['BLACK WIN!', 'WHITE WIM!', 'DRAW!'][winner])

    def force_loss(self, is_timeout=False, is_board=False, is_legal=False):
        if self.current_player == self.black_player:
            win_color = 'WHITE - O'
            loss_color = 'BLACK - X'
            winner = 1
        else:
            win_color = 'BLACK - X'
            loss_color = 'WHITE - O'
            winner = 0

        if is_timeout:
            print('\n{} Time exceed 60s, {} Win'.format(loss_color, win_color))
        if is_legal:
            print('\n{} Not meet the rule over 3 times, therefore {} Win'.format(loss_color, win_color))
        if is_board:
            print('\n{} Unauthorized changes to the board result, therefore {} Win'.format(loss_color, win_color))

        diff = 0
        return winner, diff

    def run(self):
        total_time = {'X': 0, 'O': 0}
        step_time = {'X': 0, 'O': 0}
        winner = None

        print('\n=====Game Start!=====\n')
        self.board.display()
        while True:
            self.current_player = self.switch_player(self.black_player, self.white_player)
            start_time = datetime.datetime.now()
            color = 'X' if self.current_player == self.black_player else 'O'
            legal_actions = list(self.board.get_legal_board(color))
            if len(legal_actions) == 0:
                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break
                else:
                    continue

            board = deepcopy(self.board.board)

            try:
                for _ in range(0, 3):
                    action = func_timeout(60, self.current_player.get_move, kwargs={'board': self.board})
                    if action == 'Q':
                        break
                    if action not in legal_actions:
                        print('Invaid Position!')
                        continue
                    else:
                        break
                else:
                    winner, diff = self.force_loss(is_legal=True)
                    break
            except FunctionTimedOut:
                winner, diff = self.force_loss(is_timeout=True)
                break

            end_time = datetime.datetime.now()
            if board != self.board.board:
                winner, diff = self.force_loss(is_board=True)
                break
            if action == 'Q':
                winner, diff = self.board.get_winner()
                break

            if action is None:
                continue
            else:
                es_time = (end_time - start_time).seconds
                if es_time > 60:
                    print('\n{} Time exceed 60s'.format(self.current_player))
                    winner, diff = self.force_loss(is_timeout=True)
                    break

                self.board.move(action, color)
                if self.current_player == self.black_player:
                    step_time['X'] = es_time
                    total_time['X'] += es_time
                else:
                    step_time['O'] = es_time
                    total_time['O'] += es_time
                self.board.display()

                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break

        print('\n=====Game over!=====\n')
        self.board.display(step_time, total_time)
        self.print_winner(winner)

    def game_over(self):
        b_list = list(self.board.get_legal_board('X'))
        w_list = list(self.board.get_legal_board('O'))
        is_over = len(b_list) == 0 and len(w_list) == 0 
        return is_over

class SimGame(Game):

    def __init__(self, black_player, white_player, board=Board(), current_player=None):
        self.board = deepcopy(board) 
        self.current_player = current_player
        self.black_player = black_player
        self.white_player = white_player
        self.black_player.color = 'X'
        self.white_player.color = 'O'

    def run(self):
        winner = None
        diff = -1

        while True:
            self.current_player = self.switch_player(self.black_player, self.white_player)
            color = 'X' if self.current_player == self.black_player else 'O'
            legal_actions = list(self.board.get_legal_board(color))
            if len(legal_actions) == 0:
                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break
                else:
                    continue

            action = self.current_player.select(self.board)

            if action is None:
                continue
            else:
                self.board.move(action, color)
                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break

        return winner, diff
    
