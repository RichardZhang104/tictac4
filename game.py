import copy
import numpy as np


class Game():
    def __init__(self):
        self.state = (((0,)*5,)*5, 1)

    @staticmethod
    def to_arrray(state):
        state = copy.deepcopy(state)
        state = [np.array([list(x) for x in state[0]]), state[1]]
        return state

    @staticmethod
    def get_turn_player(state):
        return state[1]

    def make_play(self, state, play):
        state = self.to_arrray(state)
        slice = state[0][:,play]

        for i, x in enumerate(slice):
            if x == 0:
                state[0][i][play] = state[1]
                state[1] *= -1
                break
        return tuple([tuple(x) for x in state[0]]), state[1]

    @staticmethod
    def get_plays(state):
        state = copy.deepcopy(state)
        state = [np.array([list(x) for x in state[0]]), state[1]]
        plays = []
        for i, c in enumerate(state[0].T):
            if 0 in c:
                plays.append(i)
        return plays

    def check_game_over(self, state):
        board = state[0]
        board_full = True
        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    board_full = False

                right_X = True
                right_O = True
                up_X = True
                up_O = True
                diag_X = True
                diag_O = True

                diag_L_X = True
                diag_L_O = True

                for k in range(4):
                    if board[(i + k) % 5][j] != 1:
                        right_X = False

                    if board[(i + k) % 5][j] != -1:
                        right_O = False

                    if board[i][(j + k) % 5] != 1:
                        up_X = False

                    if board[i][(j + k) % 5] != -1:
                        up_O = False

                    if board[(i + k) % 5][(j + k) % 5] != 1:
                        diag_X = False

                    if board[(i + k) % 5][(j + k) % 5] != -1:
                        diag_O = False

                    if board[(i - k) % 5][(j + k) % 5] != 1:
                        diag_L_X = False

                    if board[(i - k) % 5][(j + k) % 5] != -1:
                        diag_L_O = False

                if right_X or up_X or diag_X or diag_L_X:
                    return 1
                if right_O or up_O or diag_O or diag_L_O:
                    return -1

        if board_full:
            return 0
        return None


if __name__ == "__main__":
    game = Game()

    while True:
        print(game.state)
        print("game over state: ", game.check_game_over(game.state))
        play = int(input("insert play: "))
        game.state = game.make_play(game.state, play)




