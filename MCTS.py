import Roxanne

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
        

    def search(self, board):
        
