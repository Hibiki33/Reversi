from time import time
from copy import deepcopy
from math import sqrt, log
from Game import SimGame
from Roxanne import Roxanne

class TreeNode():
    
    def __init__(self, parent, color):
        self.parent = parent
        self.color = color
        self.win_cnt = 0
        self.sim_cnt = 0
        self.child = dict()
     

class MCTS(object):
    '''
    Monte Carlo Tree Search
    '''

    def __init__(self, color, time_limit=4):
        self.time_limit = time_limit
        self.tick = 0
        self.sim_black = Roxanne('X')
        self.sim_white = Roxanne('O')
        self.color = color

    def select(self, node, board):
        if len(node.child) == 0:
            return node
        else:
            max_score = -1
            tgt_move = None
            for key in node.child.keys():
                if node.child[key].sim_cnt == 0:
                    tgt_move = key
                    break
                else:
                    N = node.sim_cnt
                    sim_cnt = node.child[key].sim_cnt
                    win_cnt = node.child[key].win_cnt
                    score = self.UCB(win_cnt, sim_cnt, N)
                    if score > max_score:
                        max_score = score
                        tgt_move = key

            board.move(tgt_move, node.color)
            return self.select(node.child[tgt_move], board)

    def expand(self, node, board):
        for m in board.get_legal_board(node.color):
            node.child[m] = TreeNode(node, self.get_op_color(node.color))

    def simulate(self, node, board):
        cur_player = None
        if node.color == 'O':
            cur_player = self.sim_black
        else:
            cur_player = self.sim_white
        sim_game = SimGame(self.sim_black, self.sim_white, board, cur_player)
        return sim_game.run()

    def back_propagate(self, node, score):
        node.sim_cnt += 1
        node.win_cnt += score
        if node.parent is not None:
            self.back_propagate(node.parent, 1 - score)

    def search(self, board):
        root = TreeNode(None, self.color)

        while time() - self.tick < self.time_limit - 1:
            sim_board = deepcopy(board)
            choice = self.select(root, sim_board)
            self.expand(choice, sim_board)
            winner, diff = self.simulate(choice, sim_board)
            back_score = [1, 0, 0.5][winner]
            if choice.color == 'X':
                back_score = 1 - back_score
            self.back_propagate(choice, back_score)

        best_sim_cnt = -1
        best_move = None
        for key in root.child.keys():
            if root.child[key].sim_cnt > best_sim_cnt:
                best_sim_cnt = root.child[key].sim_cnt
                best_move = key
        
        return best_move

    def get_move(self, board):
        self.tick = time()
        move = self.search(deepcopy(board))
        return move

    def get_op_color(self, color):
        return 'O' if color == 'X' else 'X'
    
    def UCB(self, win_cnt, sim_cnt, N):
        '''
        Upper Confidence Bound
        c takes the value of sqrt(2), which is a subtle parameter
        its reasonableness is given by the experiment
        '''
        return win_cnt / sim_cnt + sqrt(2 * log(N) / sim_cnt)

