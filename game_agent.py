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
    # return float(_openboard_dominance(game, player))
    # return float(_improved_multi_open_move(game, player, 1))
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return _next_open_move(game, player)
    # return float(_improved_multi_open_move(game, player, 2, False))
    # return sample_players.improved_score(game, player)

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
    # return float(_board_dominance(game, player))
    # return float(_improved_multi_open_move(game, player, 2))
    # return float(_board_dominance(game, player))
    # return float(_board_dominance(game, player))
    # return sample_players.improved_score(game, player)

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return _board_dominance(game, player)




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
    # return float(_next_open_move(game, player))
    # return float(_improved_multi_open_move(game, player, 3))
    # return float(_multi_open_move(game, game.get_player_location(player), 2))
    # return sample_players.improved_score(game, player)

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return _next_open_scored_move(game, player)

    # _board_dominance_open_move(game, player)


def _board_dominance(game, player):

    opponent = game.get_opponent(player)
    y_o, x_o = game.get_player_location(opponent)
    y_p, x_p = game.get_player_location(player)

    x_dominance = (game.width-1)/2
    if x_p > x_o:
        x_dominance = (game.width-1) - x_p
    elif x_p < x_o:
        x_dominance = x_p

    y_dominance = (game.height-1)/2
    if y_p > y_o:
        y_dominance = (game.height-1) - y_p
    elif y_p < y_o:
        y_dominance = y_p

    dominance = x_dominance * y_dominance
    return float(dominance)

def _openboard_dominance(game, player):

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
    return float(dominant_spaces)

def _board_dominance_open_move(game, player):
    return float(_multi_open_move(game, game.get_player_location(player), 1)*
                 _board_dominance(game, player))

def _next_open_move(game, player):

    total_player_moves = 0
    total_opponent_moves = 0

    for m in game.get_legal_moves(player):
        total_player_moves += len(_get_valid_moves(game, m))
    for m in game.get_legal_moves(game.get_opponent(player)):
        total_opponent_moves += len(_get_valid_moves(game, m))

    return float(total_player_moves - total_opponent_moves)

def _next_open_scored_move(game, player):


    total_player_moves = 0
    total_opponent_moves = 0

    for m in game.get_legal_moves(player):
        for vm in _get_valid_moves(game, m):
            total_player_moves += _move_value(game, vm)
    for m in game.get_legal_moves(game.get_opponent(player)):
        for vm in _get_valid_moves(game, m):
            total_opponent_moves += _move_value(game, vm)

    return float(total_player_moves - total_opponent_moves)

def _multi_open_move(game, location, depth, past_moves=[]):

    moves_count = 0
    open_moves = _get_valid_moves(game, location)

    if past_moves:
        open_moves = list(set(open_moves) - set(past_moves))
        past_moves.extend(open_moves)
        for move in open_moves:
            moves_count += _move_value(game, move)
            depth -= 1
            if depth > 0:
                moves_count += _multi_open_move(game, move, depth, past_moves)
    else:
        for move in open_moves:
            moves_count += _move_value(game, move)
            depth -= 1
            if depth > 0:
                moves_count += _multi_open_move(game, move, depth)

    return float(moves_count)

def _improved_multi_open_move(game, player, depth, memorized=False):
    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))

    if memorized:
        player_moves = _multi_open_move(game, player_location, depth, [player_location])
        opponent_moves = _multi_open_move(game, opponent_location, depth, [opponent_location])
    else:
        player_moves = _multi_open_move(game, player_location, depth)
        opponent_moves = _multi_open_move(game, opponent_location, depth)

    return float(player_moves - opponent_moves)


def _get_valid_moves(game, location):
    # stole code from isolation.py, __get_moves
    r, c = location
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if game.move_is_legal((r + dr, c + dc))]
    return valid_moves

def _improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    own_move_score = 0
    for m in own_moves:
        own_move_score += _move_value(game, m)

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_move_score = 0
    for m in opp_moves:
        opp_move_score += _move_value(game, m)

    return float(own_move_score - opp_move_score)

# def _move_value(game, location):
#     # board = game.to_string()
#     # width = int(board.split('\n\r')[0][-1])
#     # height = int(board.split('\n\r')[-2][0])
#
#     width = 6
#     height = 6
#
#     corner = -12
#     corner_edge = -4
#     mid_edge = -1
#     center_edge = 0
#     edge = 2
#     near_edge = 4
#     near_center = 8
#     center = 12
#
#     if location == (0, 0) or location == (0, width) \
#             or location == (height, 0) or location == (height, width):
#         return corner
#     elif location[0] == 0 or location[0] == height \
#             or location[1] == 0 or location[1] == width:
#         return edge
#     elif location[0] == 1 or location[0] == height - 1 \
#             or location[1] == 1 or location[1] == width - 1:
#         return near_edge
#     elif location[0] == height/2 and location[1] == width/2:
#         return center
#     elif (height/2 - 1 <= location[0] <= height/2 + 1) \
#             and (width/2 - 1 <= location[1] <= width/2 + 1):
#         return near_center


def _move_value(game, location):
    board_values = [-11, -4, -2, 0, -1, -5, -11, -5, 0, 2, 4, 3, 0, -4, -1, 2, 7, 8, 8, 3, -1, 0, 3, 9, 9, 9, 4, 0, -2, 2, 7, 8, 8, 2, 0, -4, 1, 2, 4, 3, 0, -4, -12, -5, -1, 0, -1, -4, -12]
    idx = location[0] + location[1]*game.width
    return board_values[idx]

def _best_heuristic(game, player, depth, memorized=False):

    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)
    if len(opponent_moves) == 1 and opponent_moves[0] in game.get_legal_moves(player):
        return float("inf")

    _improved_multi_open_move(game, player, depth, memorized)





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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=25.):
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
        legal_moves = game.get_legal_moves()
        if len(legal_moves) > 0:
            best_move = legal_moves[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            move = self.minimax(game, self.search_depth)
            if move is not None:
                return move

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
        legal_moves = game.get_legal_moves()
        best_move = (-1, -1)
        if len(legal_moves) > 0:
            best_move = legal_moves[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            while True:
                move = self.alphabeta(game, depth)
                if move is not None:
                    best_move = move
                depth += 1

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

        best_value = float("-inf")
        best_move = None
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            v = self._min_value(g, depth, alpha, beta)
            if v > best_value:
                best_value = v
                best_move = m
            if best_value >= beta:
                return best_move
            alpha = max(v, alpha)

        return best_move


    def _terminal_test(self, game):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not len(game.get_legal_moves())

    def _max_value(self, game, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        depth -= 1
        if self._terminal_test(game) or depth <= 0:
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
        if self._terminal_test(game) or depth <= 0:
            return self.score(game, game.inactive_player)

        v = float("inf")
        for m in game.get_legal_moves():
            g = game.forecast_move(m)
            v = min(v, self._max_value(g, depth, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v


