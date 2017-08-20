from ayofunctions_edited import *
import ayorandomai as ai


def main():
    game_board, players, turn = initialize_game()
    previous_states = []
    
    # game loop
    while True:
        display(game_board)

        if is_end(game_board, turn, players, previous_states):
            print("Game over!")
            print("Final winnings: player 1 (", players[0], "-", players[1], ") player 2")
            print()
            print("Restart? yes(Y) or no (N):")
            if input().lower() == 'y':
                game_board, players, turn = initialize_game()
                continue
            else:
                break

            previous_states.append(game_board)
        print("Player winnings:", players[0], ":", players[1])
        print("Player", turn + 1, "'s turn")
        try:
            position = choose() if turn == 0 else ai.choose(game_board, turn, players)
            print(position)
        except ValueError:
            print("Select a number between 0 and 11 to play")
            continue

        if not position in possible_moves(game_board, turn):
            print("Your move is not valid.")
            continue
        game_board, end = move(game_board, position)

        game_board, players = gain(game_board, end, turn, players)  # Then apply the gain function

        turn = 1 if not turn else 0  # Switch Turns before returning to top given that all was fine.


if __name__ == '__main__':
    main()
