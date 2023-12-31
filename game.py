import numpy as np

state = [np.zeros((5, 5)), 1]


def get_turn_player(state):
    return state[1]

def make_play(state, play):
    slice = state[0][:, play]

    for i, x in enumerate(slice):
        if x == 0:
            state[0][i, play] = state[1]
            state[1] *= -1
            break
    return state


def get_plays(state):
    plays = []
    for i, c in enumerate(state[0].T):
        if 0 in c:
            plays.append(i)
    return plays


def check_winner(board):
    # for row in board:
    #     if all(cell == row[0] and cell != blank_character for cell in row):
    #         return True

    # for col in range(3):
    #     if all(row[col] == board[0][col] and row[col] != blank_character for row in board):
    #         return True

    # if all(board[i][i] == board[0][0] and board[i][i] != blank_character for i in range(3)):
    #     return True

    # if all(board[i][2 - i] == board[0][2] and board[i][2 - i] != blank_character for i in range(3)):
    #     return True

    for i in range(5):
        for j in range(5):

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

            if right_X or right_O or up_X or up_O or diag_X or diag_O or diag_L_X or diag_L_O:
                return True

    return False
