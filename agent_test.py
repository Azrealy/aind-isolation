"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

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

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    # def setUp(self):
    #     reload(game_agent)
    #     self.player1 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
    #     self.player2 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
    #     self.game = isolation.Board(self.player1, self.player2)

    def test_minimax(self):
        while True:
            reload(game_agent)
            self.player1 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
            self.player2 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
            self.game = isolation.Board(self.player1, self.player2)
            move = random.choice(self.game.get_legal_moves())
            self.game.apply_move(move)
            move = random.choice(self.game.get_legal_moves())
            self.game.apply_move(move)
            winner, history, outcome = self.game.play()
            print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
            print(self.game.to_string())
            print("Move history:\n{!s}".format(history))
            logging.info(history)



if __name__ == '__main__':
    unittest.main()
