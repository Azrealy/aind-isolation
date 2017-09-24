from io import StringIO
import json

def __get_moves(loc):
    r, c = loc
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    moves = [(r + dr, c + dc) for dr, dc in directions]
    return moves

with open('move_history.log', 'r') as f:

    wins_stat_table = []
    loses_stat_table = []

    line = f.readline()
    # while line:
    #     line = f.readline()
    moves_str = line.split(':')[2]
    moves = json.load(StringIO(moves_str))

    winner = (len(moves) % 2) + 1
    if winner == 1:
        winner_moves = moves[0::2]
        loser_moves = moves[1::2]
    elif winner == 2:
        winner_moves = moves[1::2]
        loser_moves = moves[0::2]

    loser_position = moves[-2]
    last_moves = __get_moves(loser_position)

    forfeit = False
    for m in last_moves:
        if m not in moves:
            forfeit = True

    if not forfeit:
        for m in winner_moves:
            idx = m[0]*7 + m[1]
            wins_stat_table[idx] += 1
        for m in loser_moves:
            idx = m[0]*7 + m[1]
            loses_stat_table[idx] += 1

    print(moves)
    print(wins_stat_table)
    print(loses_stat_table)
