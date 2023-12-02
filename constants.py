import random
import ttt_logic as ttt


class Const:
    def __init__(self):
        # ------- CONSTANTS -------
        self.USER_WORDS = []
        self.VALID_WORDS = []
        self.VALID_WORD = True
        self.ANSWER = ""
        self.ATTEMPTS = 6
        self.WIN = False
        self.GAME_OVER = False

        # ----- RANDOM ANSWER CODE -----
        with open("wordle-answers.txt", "r") as f:
            data = f.read().split()
            self.ANSWER = data[random.randint(1, len(data))].lower()

        # ------ VALID WORDS CODE ------
        with open("sgb-words.txt", "r") as f:
            self.VALID_WORDS = f.read().split()
