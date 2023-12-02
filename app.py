from flask import Flask, render_template, redirect, request, session
from constants import Const
import ttt_logic as ttt

C = Const()

current_player = None
board = []
p1_score = 0
p2_score = 0


app = Flask(__name__)


@app.route("/")
def index():
    global p1_score, p2_score
    p1_score = 0
    p2_score = 0
    return render_template("index.html")


@app.route("/wordle", methods=["GET", "POST"])
def wordle():
    global C
    if request.method == "POST":
        chr_states = []
        word = request.form.get("word")
        print(C.ANSWER)
        if len(word) == 5 and word.upper() in C.VALID_WORDS and C.WIN == False:
            for i in range(len(word)):
                if word[i] == C.ANSWER[i]:
                    chr_states.append((word[i], 2))
                elif word[i] in C.ANSWER:
                    chr_states.append((word[i], 1))
                elif word[i] not in C.ANSWER:
                    chr_states.append((word[i], 0))
        if chr_states:
            C.USER_WORDS.append(chr_states)
            C.ATTEMPTS -= 1
            C.VALID_WORD = True
        else:
            C.VALID_WORD = False
        if word.upper() == C.ANSWER.upper():
            C.WIN = True

        print(chr_states)
    else:
        C = Const()

    return render_template(
        "wordle.html",
        user_words=C.USER_WORDS,
        valid_word=C.VALID_WORD,
        won=C.WIN,
        attemps=C.ATTEMPTS,
        answer=C.ANSWER.upper(),
    )


@app.route("/words")
def words():
    return render_template("words.html", words=C.USER_WORDS)


@app.route("/tictactoe-home")
def ttt_home():
    return render_template("tictactoe-home.html")


@app.route("/tictactoe/ai", methods=["GET", "POST"])
def ttt_ai():
    global current_player, board, p1_score, p2_score

    if request.method == "GET":
        board = [[" " for i in range(3)] for j in range(3)]
        current_player = "X"
        return render_template(
            "tictactoe/ai.html",
            player=current_player,
            board=ttt.get_grid_state(board),
            p1_score=p1_score,
            p2_score=p2_score,
        )
    elif request.method == "POST":
        p_move = request.form.get("grid_el")
        p_row, p_col = p_move[0], p_move[1]

        if board[int(p_row)][int(p_col)] == " ":
            board[int(p_row)][int(p_col)] = "X"
            winner = ttt.check_winner(board)

        ai_move = ttt.get_ai_move(board)
        if ai_move:
            ai_row, ai_col = ai_move[0], ai_move[1]

        try:
            if board[int(ai_row)][int(ai_col)] == " ":
                board[int(ai_row)][int(ai_col)] = "O"
                winner = ttt.check_winner(board)
        except:
            pass

        if winner:
            if winner == "X":
                p1_score += 1
            elif winner == "tie":
                pass
            elif winner == "O":
                p2_score += 1

        print(ttt.get_grid_state(board))

        return render_template(
            "tictactoe/ai.html",
            board=ttt.get_grid_state(board),
            player=current_player,
            winner=winner,
            p1_score=p1_score,
            p2_score=p2_score,
        )


@app.route("/tictactoe/multiplayer", methods=["GET", "POST"])
def ttt_multi():
    global current_player, board, p1_score, p2_score

    if request.method == "GET":
        board = [[" " for i in range(3)] for j in range(3)]
        current_player = ttt.choose_player()
        return render_template(
            "tictactoe/multiplayer.html",
            player=current_player,
            board=ttt.get_grid_state(board),
            p1_score=p1_score,
            p2_score=p2_score,
        )
    elif request.method == "POST":
        print(ttt.get_grid_state(board))

        move = request.form.get("grid_el")
        row, col = move[0], move[1]

        if board[int(row)][int(col)] == " ":
            board[int(row)][int(col)] = current_player
            winner = ttt.check_winner(board)
            if winner:
                if winner == "X":
                    p1_score += 1
                elif winner == "tie":
                    pass
                elif winner == "O":
                    p2_score += 1

        current_player = "X" if current_player == "O" else "O"

        return render_template(
            "tictactoe/multiplayer.html",
            board=ttt.get_grid_state(board),
            player=current_player,
            winner=winner,
            p1_score=p1_score,
            p2_score=p2_score,
        )
