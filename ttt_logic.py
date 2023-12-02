import random


def choose_player():
    return random.choice(["X", "O"])


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)


def get_grid_state(board):
    D = dict()
    for i in range(3):
        for j in range(3):
            D[(str(i), str(j))] = board[i][j]
    return D


def check_winner(board):
    # Check rows, columns, and diagonals
    for player in ["X", "O"]:
        for i in range(3):
            if all(cell == player for cell in board[i]) or all(
                board[j][i] == player for j in range(3)
            ):
                return player
        if all(board[i][i] == player for i in range(3)) or all(
            board[i][2 - i] == player for i in range(3)
        ):
            return player
        elif is_board_full(board):
            return "tie"
    return ""


def is_board_full(board):
    return all(all(cell != " " for cell in row) for row in board)


def get_player_move():
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            if 1 <= move <= 9:
                return (move - 1) // 3, (move - 1) % 3  # Convert to row, col
            else:
                print("Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]


def get_ai_move(board):
    bestScore = float("-inf")
    bestMove = None

    for move in get_available_moves(board):
        if board[move[0]][move[1]] == " ":
            board[move[0]][move[1]] = "O"
            score = minimax(board, 0, False)
            if score > bestScore:
                bestScore = score
                bestMove = (move[0], move[1])
            board[move[0]][move[1]] = " "

    return bestMove


def minimax(board, depth, is_maximizing):
    scores = {"X": -1, "O": 1, "tie": 0}

    winner = check_winner(board)
    if winner:
        return scores[winner]

    if is_maximizing:
        bestScore = float("-inf")
        for move in get_available_moves(board):
            if board[move[0]][move[1]] == " ":
                board[move[0]][move[1]] = "O"
                score = minimax(board, depth + 1, False)
                board[move[0]][move[1]] = " "  # Corrected: Reset the board
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float("inf")
        for move in get_available_moves(board):
            if board[move[0]][move[1]] == " ":
                board[move[0]][move[1]] = "X"
                score = minimax(board, depth + 1, True)
                board[move[0]][move[1]] = " "  # Corrected: Reset the board
                bestScore = min(score, bestScore)
        return bestScore


def play_tic_tac_toe():
    board = [[" " for i in range(3)] for j in range(3)]
    players = ["X", "O"]
    current_player = players[0]

    while True:
        print_board(board)

        # print(get_grid_state(board))

        if current_player == "X":
            row, col = get_player_move()
        else:
            print("AI is thinking...")
            ai_move = get_ai_move(board)
            if ai_move:
                row, col = ai_move

        if board[row][col] == " ":
            board[row][col] = current_player
            winner = check_winner(board)
            if winner:
                print_board(board)
                if winner == "X":
                    print("You win!")
                elif winner == "tie":
                    print("Its a tie!")
                elif winner == "O":
                    print("AI Wins!")
                break
            elif is_board_full(board):
                print_board(board)
                print("It's a tie!")
                break
            else:
                current_player = (
                    players[1] if current_player == players[0] else players[0]
                )
        else:
            print("Invalid move. The space is already taken. Try again.")


if __name__ == "__main__":
    play_tic_tac_toe()
