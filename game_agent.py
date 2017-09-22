"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return float(_openboard_dominance(game, player))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return float(_board_dominance(game, player))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return float(_multi_open_move(game, player))

def _board_dominance(game, player):

    board = game.to_string()
    board_width = int(board.split('\n\r')[0][-1])
    board_height = int(board.split('\n\r')[-2][0])

    opponent = game.get_opponent(player)
    y_o, x_o = game.get_player_location(opponent)
    y_p, x_p = game.get_player_location(player)

    x_dominance = 0
    if x_p > x_o:
        x_dominance = board_width - x_p
    elif x_p < x_o:
        x_dominance = x_p

    y_dominance = 0
    if y_p > y_o:
        y_dominance = board_height - y_p
    elif y_p < y_o:
        y_dominance = y_p

    dominance = x_dominance * y_dominance
    return dominance

def _openboard_dominance(game, player):

    board = game.to_string()
    board_width = int(board.split('\n\r')[0][-1])
    board_height = int(board.split('\n\r')[-2][0])

    opponent = game.get_opponent(player)
    y_o, x_o = game.get_player_location(opponent)
    y_p, x_p = game.get_player_location(player)

    blank_spaces = game.get_blank_spaces()

    x_dominant_spaces = []
    if x_p > x_o:
        x_dominant_spaces = [s for s in blank_spaces if s[1] > x_p]
    elif x_p < x_o:
        x_dominant_spaces = [s for s in blank_spaces if s[1] < x_p]

    y_dominant_spaces = []
    if y_p > y_o:
        y_dominant_spaces = [s for s in blank_spaces if s[0] > y_p]
    elif y_p < y_o:
        y_dominant_spaces = [s for s in blank_spaces if s[0] < y_p]

    dominant_spaces = len(x_dominant_spaces) + len(y_dominant_spaces)
    return dominant_spaces

def _multi_open_move(game, player):

    total_player_moves = 0
    total_opponent_moves = 0

    for m in game.get_legal_moves(player):
        total_player_moves += _get_open_move_count(game, m)
    for m in game.get_legal_moves(game.get_opponent(player)):
        total_opponent_moves += _get_open_move_count(game, m)

    return total_player_moves - total_opponent_moves

def _get_open_move_count(game, location):
    # stole code from isolation.py, __get_moves
    r, c = location
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if game.move_is_legal((r + dr, c + dc))]
    return len(valid_moves)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md


        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        # Adopted from lecture solution
        # Weird, this solution does not work successfully for tournament but for upa
        # return max(game.get_legal_moves(),
        #                 key=lambda m: self._min_value(game.forecast_move(m), depth))

        best_score = float("-inf")
        best_move = None
        for m in game.get_legal_moves():
            v = self._min_value(game.forecast_move(m), depth)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move

    def _terminal_test(self, game):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not len(game.get_legal_moves())

    def _max_value(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth -= 1
        if self._terminal_test(game) or not depth:
            return self.score(game, game.active_player)

        v = float("-inf")
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            v = max(v, self._min_value(g, depth))

        return v

    def _min_value(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth -= 1
        if self._terminal_test(game) or not depth:
            return self.score(game, game.inactive_player)

        v = float("inf")
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            v = min(v, self._max_value(g, depth))

        return v


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            while True:
                depth += 1
                best_move = self.alphabeta(game, depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        v = float("-inf")
        ab_move = None
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            state_value = self._min_value(g, depth, alpha, beta)
            if state_value > v:
                v = state_value
                ab_move = m
            if v >= beta:
                return ab_move
            alpha = max(v, alpha)

        return ab_move


    def _terminal_test(self, game):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not len(game.get_legal_moves())

    def _max_value(self, game, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth -= 1
        if self._terminal_test(game) or not depth:
            return self.score(game, game.active_player)

        v = float("-inf")
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            v = max(v, self._min_value(g, depth, alpha, beta))
            if v >= beta:
                return v
            alpha = max(v, alpha)

        return v

    def _min_value(self, game, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth -= 1
        if self._terminal_test(game) or not depth:
            return self.score(game, game.inactive_player)

        v = float("inf")
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            v = min(v, self._max_value(g, depth, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v


