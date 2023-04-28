from Player import Player
from MCTS import MCTS
from Game import Game

if __name__ == '__main__':
    human_player = Player('X')
    AI_player = MCTS('O')
    game = Game(human_player, AI_player)
    game.run()
