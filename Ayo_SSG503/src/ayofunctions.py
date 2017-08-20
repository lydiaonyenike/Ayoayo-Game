def initialize_board():
    return [4 for _ in range(12)]


def display(board: list):
    if not board:
        return
    
    print(*board[11:5:-1])
    print(*board[0:6])


def choose():
    print("Choose a position to pick: ")
    return int(input())


def move(board: list, position: int):
    board = board.copy()
    if position > 11:
        print("Position cannot be greater than 11")
        return board, position

    hand = board[position]
    skip = -1

    if hand == 0:
        print("No seeds are in hole", position)
        return board, position
    if hand >= 12:
        skip = position

    board[position] = 0
    position += 1

    while hand > 0:
        position = position if position <= 11 else 0
        if position == skip:  # 12 seeds skip rule
            position += 1
            continue
        board[position] += 1
        hand -= 1
        position += 1
    return board, position - 1


def initialize_game():
    players = [0, 0]
    turn = 0
    game_board = initialize_board()
    return game_board, players, turn


def gain(board: list, position: int, turn: int, players: list):
    new_board = board.copy()
    new_players = players.copy()
    while is_gain(new_board, turn, position):
        new_players[turn] += new_board[position]
        new_board[position] = 0
        position -= 1

    if turn == 0 and sum([i for i in __p2_holes]) == 0 or turn == 1 and sum([i for i in __p1_holes]) == 0:
        return board, players

    return new_board, new_players


def is_end(board: list, turn: int, players: list) -> bool:
    if max(players) >= 25:  # 25 win rule
        return True
    if players[0] == players[1] == 24:
        return True
    if sum(board) <= 3:
        return True
    if len(possible_moves(board, turn)) == 0:
        return True
    return False


def possible_moves(board, turn) -> list:
    possible_moves = range(6) if turn == 0 else range(6, 12)
    x = [i for i in possible_moves if board[i] > 0]
    output = []
    if sum([board[i] for i in __p1_holes]) == 0 and turn == 1:
        for i in x:
            b, end = move(board, i)
            if end in __p1_holes:
                output.append(i)
    elif sum([board[i] for i in __p2_holes]) == 0 and turn == 0:
        for i in x:
            b, end = move(board, i)
            if end in __p2_holes:
                output.append(i)
    else:
        output = x.copy()
    return output


def is_gain(board: list, turn: int, end: int) -> bool:
    return True if ((turn == 1 and end in __p1_holes) or (turn == 0 and end in __p2_holes)) and 2 <= board[
        end] <= 3 else False


__p1_holes = range(6)
__p2_holes = range(6, 12)
