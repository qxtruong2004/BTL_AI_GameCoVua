from Board import DisplayBoard
from MiniMax import minimax
from Evaluation import Evalualtion
import chess
import pygame as py

# Các biến chung
MAX, MIN = 100000, -100000
depth = 3

board = chess.Board()
display = DisplayBoard(board)

# Hàm này có thể chạy bất cứ khi nào và sẽ đặt lại trò chơi hoàn toàn.
def setup_game():
    board.reset_board()
    display.main_menu()
    display.update(board)
    run()

def move():
    player_possible_move = display.square_select(py.mouse.get_pos())
    if player_possible_move != None:
        try:
            eval = Evalualtion(board, display.set_up)
            is_late_game = eval.is_late_game()

            if display.set_up == "W":
                makeMoveWhite(player_possible_move, is_late_game)
                makeMoveBlack(player_possible_move, is_late_game)
            else:
                makeMoveBlack(player_possible_move, is_late_game)
                makeMoveWhite(player_possible_move, is_late_game)
        except:
            print("Invalid Move")

def makeMoveWhite(move, is_late_game):

    if display.set_up == "W":
        board.push_uci(move)
    else:
        # Thuộc tính depth phải là số lẻ
        if is_late_game:
            white = minimax(depth + 1, True, MIN, MAX, board, True)
        else:
            white = minimax(depth + 1, True, MIN, MAX, board, True)

        board.push(white)

    display.update(board)

def makeMoveBlack(move, is_late_game):

    if display.set_up == "B":
        board.push_uci(move)
    else:
        # Thuộc tính depth phải là số chẵn
        if is_late_game:
            black = minimax(depth + 2, False, MIN, MAX, board, True)
        else:
            black = minimax(depth, False, MIN, MAX, board, True)
        board.push(black)

    display.update(board)

def is_game_over(board):
    if board.is_game_over():
        display.run = False
        display.game_over = True
        display.game_over_menu()

def run():
    while display.run:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                exit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                move()
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 3:
                display.remove_square_select()



        display.update_screen()
        is_game_over(board)

while run:
    setup_game()

py.quit()


