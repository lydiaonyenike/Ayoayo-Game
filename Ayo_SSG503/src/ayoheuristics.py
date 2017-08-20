def winnings_safety(state, turn):
    x = 0
    x += state.Winnings[state.Turn] - state.Winnings[1 if not state.Turn else 0]
    x += len([i for i in state.OwnHoles if i > 3 or i == 0])
    x += len([i for i in state.OppHoles if 0 < i <= 3])
    x *= 1 if state.Turn == turn else -1
    return x

def winnings_more(state, turn):
    x = 0
    x += (state.Winnings[state.Turn] - state.Winnings[1 if not state.Turn else 0]) * 3
    x += len([i for i in state.OwnHoles if i > 3 or i == 0])
    x += len([i for i in state.OppHoles if 0 < i <= 3])
    x *= 1 if state.Turn == turn else -1
    return x

def winnings_only(state, turn):
    x = 0
    x += (state.Winnings[state.Turn] - state.Winnings[1 if not state.Turn else 0])
    x *= 1 if state.Turn == turn else -1
    return x

def max_winnings(state, turn):
    x = 0
    x += state.Winnings[state.Turn]
    x *= 1 if state.Turn == turn else -1
    return x