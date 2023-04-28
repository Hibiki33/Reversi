import Roxanne
import time
from copy import deepcopy
from math import sqrt, log

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

    def simulate():
        pass

    def back_propagate():
        pass

    def search(self, board):
        root = TreeNode(None, self.color)

        while time() - self.tick < self.time_limit - 1:
            sim_board = deepcopy(board)
            choice = self.select

    def get_op_color(self, color):
        return 'O' if color == 'X' else 'X'
    
    def UCB(self, win_cnt, sim_cnt, N):
        '''
        Upper Confidence Bound
        c takes the value of sqrt(2), which is a subtle parameter
        its reasonableness is given by the experiment
        '''
        return win_cnt / sim_cnt + sqrt(2 * log(N) / sim_cnt)

