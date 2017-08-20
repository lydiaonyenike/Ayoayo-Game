from queue import *
import ayorandomai as dumb_ai
from ayofunctions import is_end


def dfs(state, score, max_depth, ply, transition) -> int:
    stack = [state]
    best_state = None
    best_score = -1
    visited_states = []

    while len(stack):
        current_state = stack.pop()
        value = score(current_state)
        if value > best_score and current_state.Depth == max_depth:
            best_state = current_state
            best_score = value
        if current_state.id() in visited_states or current_state.Depth == max_depth:
            continue

        actions = ply(current_state)
        for action in actions:
            new_state = transition(current_state, action)
            if not new_state: continue
            new_state.Parent = current_state
            stack.append(new_state)
        visited_states.append(current_state.id())

    if not best_state:
        return dumb_ai.choose(state.Board, state.Turn, state.Winnings)
    while best_state.Depth > 1:
        best_state = best_state.Parent
    print(len(visited_states), "nodes searched")
    return best_state.Action


def bfs(state, score, max_depth, ply, transition) -> int:
    queue = Queue()
    queue.put(state)
    best_state = None
    best_score = -1
    visited_states = []

    while not queue.empty():
        current_state = queue.get()
        value = score(current_state)
        if value > best_score and current_state.Depth == max_depth:
            best_state = current_state
            best_score = value
        if current_state.id() in visited_states or current_state.Depth == max_depth:
            continue

        actions = ply(current_state)
        for action in actions:
            new_state = transition(current_state, action)
            if not new_state: continue
            new_state.Parent = current_state
            queue.put(new_state)
        visited_states.append(current_state.id())

    if not best_state:
        return dumb_ai.choose(state.Board, state.Turn, state.Winnings)
    while best_state.Depth > 1:
        best_state = best_state.Parent
    print(len(visited_states), "nodes searched")
    return best_state.Action


def best_first_search(state, score, max_depth, ply, transition) -> int:
    unvisited = [state]
    best_state = None
    best_score = -1
    visited_states = []

    while len(unvisited):
        unvisited.sort(key=lambda x: score(x), reverse=True)
        unvisited = unvisited[0:3]
        current_state = unvisited.pop(0)
        value = score(current_state)
        if value > best_score and current_state.Depth == max_depth:
            best_state = current_state
            best_score = value
        if current_state.id() in visited_states or current_state.Depth == max_depth:
            continue

        actions = ply(current_state)
        for action in actions:
            new_state = transition(current_state, action)
            if not new_state: continue
            new_state.Parent = current_state
            unvisited.append(new_state)
        visited_states.append(current_state.id())

    if not best_state:
        return dumb_ai.choose(state.Board, state.Turn, state.Winnings)

    while best_state.Depth > 1:
        best_state = best_state.Parent
    print(len(visited_states), "nodes searched")
    return best_state.Action


def min_max(state, score, max_depth, ply, transition) -> int:
    alpha = float('inf') * -1
    beta = float('inf')
    book = {}
    successors = [transition(state, i) for i in ply(state)]
    ponder = {}
    for i in successors:
        ponder[i] = __value(i, score, ply, transition, max_depth, alpha, beta, book)

    best_move = max(ponder, key=lambda x: ponder[x])
    best_move = max([i for i in successors if book[i.id()] >= book[best_move.id()]], key=lambda x:score(x))
    return best_move.Action


def __is_terminal(state):
    if is_end(state.Board, state.Turn, state.Winnings):
        return True
    return False

def __is_cutoff(state, max_depth):
    if state.Depth == max_depth:
        return True
    if state.Utility < -5:
        return True
    return False


def __is_max_state(state):
    return True if state.Depth % 2 == 1 else False


def __max_value(state, score, ply, transition, max_depth, alpha, beta, book):
    m = float('inf') * -1
    actions = ply(state)
    for action in actions:
        new_state = transition(state, action)
        if not new_state: continue
        new_state.Parent = state
        v = __value(new_state, score, ply, transition, max_depth, alpha, beta, book)
        m = max(m, v)
        if m >= beta:
            return m
        alpha = max(alpha, m)
    return m


def __min_value(state, score, ply, transition, max_depth, alpha, beta, book):
    m = float('inf')
    actions = ply(state)
    for action in actions:
        new_state = transition(state, action)
        if not new_state: continue
        new_state.Parent = state
        v = __value(new_state, score, ply, transition, max_depth, alpha, beta, book)
        m = min(m, v)
        if m <= alpha:
            return m
        beta = min(beta, m)
    return m


def __value(state, score, ply, transition, max_depth, alpha, beta, book) -> int:
    if state.id() in book:
        return book[state.id()]
    if __is_cutoff(state, max_depth):
        s = score(state)
        book[state.id()] = s
        return s
    if __is_terminal(state):
        s = state.Utility
        s = s if __is_max_state(state) else s*-1
        book[state.id()] = s
        return s
    if __is_max_state(state):
        s = __max_value(state, score, ply, transition, max_depth, alpha, beta, book)
        book[state.id()] = s
        return s
    else:
        s = __min_value(state, score, ply, transition, max_depth, alpha, beta, book)
        book[state.id()] = s
        return s
