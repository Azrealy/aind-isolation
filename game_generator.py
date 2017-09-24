import unittest

import isolation
import game_agent
import sample_players
import random
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)

from importlib import reload
import logging

logging.basicConfig(filename='move_history.log',level=logging.DEBUG)

def test_minimax():
    while True:
        reload(game_agent)
        player1 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
        player2 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
        game = isolation.Board(player1, player2)
        move = random.choice(game.get_legal_moves())
        game.apply_move(move)
        move = random.choice(game.get_legal_moves())
        game.apply_move(move)
        winner, history, outcome = game.play()
        logging.info(history)

if __name__ == '__main__':
    test_minimax()
