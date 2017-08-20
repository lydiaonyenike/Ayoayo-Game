import random as r


def choose(board, turn, winnings):
    possible_moves = range(6) if turn == 0 else range(6, 12)
    position = r.choice(possible_moves)
    return position
