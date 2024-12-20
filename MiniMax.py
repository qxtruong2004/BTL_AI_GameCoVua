from Evaluation import Evalualtion

MAX, MIN = 100000, -100000

# Trả về giá trị tối ưu cho người chơi hiện tại
# (Ban đầu được gọi cho nút gốc và người tối đa hóa)
def minimax(depth, maximizingPlayer, alpha, beta, board, firstMove):

    # Điều kiện dừng. Tức là
    # đến nút lá
    if (depth == 0) or (board.is_game_over()):

        if maximizingPlayer:
            eval = Evalualtion(board, "W")
        else:
            eval = Evalualtion(board, "B")

        return eval.result()

      # Mã lệnh sau đây chỉ chạy nếu cây vẫn chưa đạt đến nút lá

    if maximizingPlayer:

        best = MIN
        # Lặp qua từng nước đi hợp lệ
        for i in board.legal_moves:

            board.push(i)

            if checkmate(board) and firstMove:
                return i
            val = minimax(depth - 1, False, alpha, beta, board, False)
            board.pop()

            if val > best:
                best = val
                best_move_white = i

            alpha = max(alpha, best)

            # Cắt tỉa Alpha Beta
            if beta <= alpha:
                break

        if firstMove:
            print(best_move_white)
            return best_move_white
        else:
            return best

    else:

        best = MAX
        for i in board.legal_moves:

            board.push(i)

            if checkmate(board) and firstMove:
                return i

            val = minimax(depth - 1, True, alpha, beta, board, False)
            board.pop()

            if val < best:
                best = val
                best_move_black = i

            beta = min(beta, best)

            # Cắt tỉa Alpha Beta
            if beta <= alpha:
                break

        if firstMove:
            print(best_move_black)
            return best_move_black
        else:
            return best

def checkmate(board):
    if board.is_checkmate():
        return True
    else:
        return False




