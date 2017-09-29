from io import StringIO
import json

def __get_moves(loc):
    r, c = loc
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    moves = [(r + dr, c + dc) for dr, dc in directions]
    return moves

with open('move_history.log', 'r') as f:

    wins_stat_table = [0 for _ in range(49)]
    loses_stat_table = [0 for _ in range(49)]

    line = f.readline()
    while line:
        moves_str = line.split(':')[2]
        # print(moves_str)
        moves = json.load(StringIO(moves_str))

        winner = (len(moves) % 2)
        if winner == 1:
            winner_moves = moves[0::2]
            loser_moves = moves[1::2]
        elif winner == 0:
            winner_moves = moves[1::2]
            loser_moves = moves[0::2]

        if len(moves) > 1:
            loser_position = moves[-2]
        else:
            loser_position = None

        if loser_position is not None:
            last_moves = __get_moves(loser_position)

            forfeit = True
            for m in last_moves:
                if m not in moves:
                    forfeit = False

            if not forfeit:
                move_threshold = 2
                move_count = 0
                for m in winner_moves:
                    move_count += 1
                    if move_count >= move_threshold:
                        idx = m[0]*7 + m[1]
                        wins_stat_table[idx] += 1
                move_count = 0
                for m in loser_moves:
                    move_count += 1
                    if move_count >= move_threshold:
                        idx = m[0]*7 + m[1]
                        loses_stat_table[idx] += 1

        line = f.readline()


    diff_table = [0 for _ in range(49)]
    i = 0
    for a, b in zip(wins_stat_table, loses_stat_table):
        diff_table[i] = int(100*(a-b)/(a+b))
        i += 1

    for i in range(49):
        print("{:>5}".format(diff_table[i]), end='')
        if (i % 7) == 6:
            print("\n")

    print(diff_table)

