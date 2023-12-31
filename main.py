# Run pip3 install discord.py

import discord
import random
from discord.ext import commands

# Define the bot prefix and create a bot instance with intents
intents = discord.Intents.default()
intents.message_content = True

# Define the bot prefix and create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store ongoing Tic-Tac-Toe games
games = {}

blank_character = '~'
X_char = 'x'
O_char = 'o'


# Function to check for a winner in the Tic-Tac-Toe board
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
                if board[(i + k) % 5][j] != X_char:
                    right_X = False

                if board[(i + k) % 5][j] != O_char:
                    right_O = False

                if board[i][(j + k) % 5] != X_char:
                    up_X = False

                if board[i][(j + k) % 5] != O_char:
                    up_O = False

                if board[(i + k) % 5][(j + k) % 5] != X_char:
                    diag_X = False

                if board[(i + k) % 5][(j + k) % 5] != O_char:
                    diag_O = False

                if board[(i - k) % 5][(j + k) % 5] != X_char:
                    diag_L_X = False

                if board[(i - k) % 5][(j + k) % 5] != O_char:
                    diag_L_O = False

            if right_X or right_O or up_X or up_O or diag_X or diag_O or diag_L_X or diag_L_O:
                return True

    return False


# Function to display the Tic-Tac-Toe board
def display_board(board):
    rb = board[::-1]
    s = '\n'.join([' '.join(row) for row in rb])
    print("Board: ")
    print(s)
    return s


# Command to start a new Tic-Tac-Toe game
@bot.command(name='5x5')
async def tictactoe(ctx, opponent: discord.Member):
    print(opponent)

    if ctx.author == opponent:
        await ctx.send("You cannot play against yourself!")
        return

    if ctx.channel.id in games:
        await ctx.send("There's already a game in progress in this channel!")
        return

    # Initialize a new game
    game_board = [[blank_character for _ in range(5)] for _ in range(5)]
    turn = random.choice([ctx.author, opponent])
    games[ctx.channel.id] = {'board': game_board, 'turn': turn, 'players': (ctx.author, opponent)}

    # Send the initial game state
    message = f"{turn.mention}'s turn.\n{display_board(game_board)}"
    await ctx.send(message)


# Command to make a move in the Tic-Tac-Toe game
@bot.command(name='move')
async def move(ctx, col: int):
    print("Called move (%d)" % (col))

    channel_id = ctx.channel.id

    if channel_id not in games:
        await ctx.send("No 5x5 game in progress in this channel. Use !5x5 to start a new game.")
        return

    game = games[channel_id]
    board = game['board']
    turn = game['turn']
    players = game['players']

    if ctx.author != turn:
        await ctx.send("It's not your turn")
        return

    col = col - 1

    if not (0 <= col < 5):
        await ctx.send("Invalid move")
        return

    for row in range(5):
        if board[row][col] == blank_character:
            break
        elif row == 5 - 1:
            await ctx.send("Column is full")
            return

    # Make the move
    symbol = X_char if turn == players[0] else O_char
    board[row][col] = symbol

    # Check for a winner or a draw
    if check_winner(board):
        winner = ctx.author
        # winner = ctx.author if turn == players[0] else players[0]
        await ctx.send(f"Game over! {winner.mention} wins!\n{display_board(board)}")
        del games[channel_id]
        return
    elif all(cell != blank_character for row in board for cell in row):
        await ctx.send("It's a draw!\n" + display_board(board))
        del games[channel_id]
        return

    # Switch the turn
    game['turn'] = players[0] if turn == players[1] else players[1]

    # Send the updated game state
    message = f"{game['turn'].mention}'s turn.\n{display_board(board)}"
    await ctx.send(message)


# Command to stop the Tic-Tac-Toe game
@bot.command(name='stop')
async def stop_tictactoe(ctx):
    channel_id = ctx.channel.id

    if channel_id in games:
        game = games[channel_id]
        players = game['players']

        if ctx.author in players:
            del games[channel_id]
            await ctx.send("Game has been stopped.")
        else:
            await ctx.send("You are not a player in the current game.")
    else:
        await ctx.send("No game in progress in this channel.")


@bot.command(name='help_5x5')
async def help(ctx):
    await ctx.send("`!5x5 @opponent` to play. `!move col` to place. `!stop` to stop.")


# Run the bot with your token from the file
with open("token", "r") as token_file:
    bot_token = token_file.read().strip()

bot.run(bot_token)
