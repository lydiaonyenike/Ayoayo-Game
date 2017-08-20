from ayofunctions import *
from ayoaisearch import *
from ayoheuristics import *
import ayorandomai as dumb_ai


class __State:
    def __init__(self, board: list, turn: int, winnings: list):
        self.Board = board
        self.Turn = turn
        self.Winnings = winnings
        self.OwnHoles = board[0:6] if turn == 0 else board[6:12]
        self.OppHoles = board[0:6] if turn == 1 else board[6:12]
        self.Depth = 0
        self.Parent = None
        self.Action = -1
        self.Utility = (self.Winnings[turn] - self.Winnings[1 if not turn else 0]) * 12

    def id(self):
        return ''.join([str(i) for i in self.Board]) + str(self.Turn)


def __score(state):
    return __heuristic(state, __turn)


def __transition(state: __State, action: int) -> __State:
    if is_end(state.Board, state.Turn, state.Winnings):
        return None

    winnings = state.Winnings.copy()

    new_board, end_position = move(state.Board, action)

    if is_gain(new_board, state.Turn, end_position):
        new_board, winnings = gain(new_board, end_position, state.Turn, winnings)

    turn = 1 if not state.Turn else 0

    new_state = __State(new_board, turn, winnings)
    new_state.Depth = state.Depth + 1
    new_state.Action = action
    return new_state


def __ply(current_state: __State):
    return possible_moves(current_state.Board, current_state.Turn)


def __get_move(state: __State) -> int:
    return __search(state, __score, __max_depth, __ply, __transition)


__max_depth = 10
__p1_holes = range(6)
__p2_holes = range(6, 12)
__turn = -1
__search = min_max
__heuristic = max_winnings


def choose(board: list, turn: int, winnings: list) -> int:
    global __turn
    global __search
    global __max_depth
    global __heuristic

    __turn = turn
    __heuristic = winnings_safety if turn else max_winnings
    __search = min_max if turn else bfs
    __max_depth = 7 if turn else 6
    if len(set(board)) == 1 and not turn:
        return dumb_ai.choose(board, turn, winnings)
    state = __State(board, turn, winnings)
    return __get_move(state)
