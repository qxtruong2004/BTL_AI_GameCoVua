from Piece_Development_Values import BoardValues

class Evalualtion():

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.boardValues = BoardValues() # Đối tượng chứa giá trị của quân cờ trên bàn cờ
        self.lateGameWhite = False 
        self.lateGameBlack = False 

        # Tạo danh sách BoardLayout rỗng để có thể so sánh dữ liệu.
            
        self.boardLayout = [None] * 64

        # Điền BoardLayout với dữ liệu từ boardString.
       
        self.populate()
     # Phương thức populate(): Tạo danh sách BoardLayout dựa trên dữ liệu từ bàn cờ.
    def populate(self):

        boardString = self.board.fen()

        # Loại bỏ dữ liệu không cần thiết ở cuối chuỗi
        boardString = boardString[0:boardString.find(' ')]
        boardString = boardString + '/'

         # Chuỗi cơ bản để xác định vị trí của mỗi quân cờ trên bàn cờ 
        counter = 0

        for y in range(8):
            dash = boardString.find('/')
            rawCode = boardString[0:dash]
            boardString = boardString[dash + 1:len(boardString)]

            for char in rawCode:
                if char.isdigit():
                    counter += int(char)
                else:
                    self.boardLayout[counter] = char
                    counter += 1

    # Phương thức materialComp(): Tính toán giá trị dựa trên loại và số lượng quân cờ trên bàn cờ.
    def materialComp(self):

        total = 0
        boardString = self.board.fen()

        # Loại bỏ dữ liệu không cần thiết ở cuối chuỗi
        boardString = boardString[0:boardString.find(' ')]

        # Chuỗi cơ bản để xác định vị trí của mỗi quân cờ trên bàn cờ
        for i in boardString:
            if str(i) == "P": total += 100
            elif str(i) == "N": total += 320
            elif str(i) == "B": total += 330
            elif str(i) == "R": total += 500
            elif str(i) == "Q": total += 900
            elif str(i) == "K": total += 20000

            elif str(i) == "p": total -= 100
            elif str(i) == "n": total -= 320
            elif str(i) == "b": total -= 330
            elif str(i) == "r": total -= 500
            elif str(i) == "q": total -= 900
            elif str(i) == "k": total -= 20000
            else: pass

        return total

    # Phương thức development(): Đánh giá giá trị phát triển của bàn cờ.
    def development(self):
        total = 0
        counter = 0

        numberOfMinorPiecesWhite = 0
        numberOfMinorPiecesBlack = 0

        # Duyệt qua mỗi ô trên bàn cờ và tính toán giá trị phát triển
        for piece in self.boardLayout:
            if piece != None:
                if str(piece) == "P":
                    total += self.boardValues.Pawn[counter]
                elif str(piece) == "N":
                    total += self.boardValues.Knight[counter]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "B":
                    total += self.boardValues.Bishop[counter]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "R":
                    total += self.boardValues.Rook[counter]
                    numberOfMinorPiecesWhite += 1
                elif str(piece) == "Q":
                    total += self.boardValues.Queen[counter]
                    numberOfMinorPiecesWhite += 1

                #######################################################################

                elif str(piece) == "p":
                    total += self.boardValues.Pawn[counter]
                elif str(piece) == "n":
                    total += self.boardValues.Knight[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "b":
                    total += self.boardValues.Bishop[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "r":
                    total += self.boardValues.Rook[counter]
                    numberOfMinorPiecesBlack += 1
                elif str(piece) == "q":
                    total += self.boardValues.Queen[counter]
                    numberOfMinorPiecesBlack += 1

            counter += 1

        counter = 0
        # Duyệt qua mỗi ô trên bàn cờ lần nữa để tính toán giá trị cho vua
        for piece in self.boardLayout:
            if piece != None:
                # If True it is still early game.
                if str(piece) == "k":
                    if (numberOfMinorPiecesBlack >= 3):
                        total += self.boardValues.KingEarly[counter]
                    else:
                        total += self.boardValues.KingLate[counter]
                        self.lateGameBlack = True
                        print("Black LAte")

                # If True it is still early game.
                elif str(piece) == "K":
                    if (numberOfMinorPiecesWhite >= 3):
                        total += self.boardValues.KingEarly[counter]
                    else:
                        total += self.boardValues.KingLate[counter]
                        self.lateGameWhite = True

            counter += 1

        return total

    def checkmate(self):
        """
        Kiểm tra xem bàn cờ có ở trong tình trạng chiếu hết hay không.
        Nếu có, thì trả về điểm tương ứng cho chiếu hết (checkmate).
        Điểm dương nếu đang là quân trắng và chiếu hết, và điểm âm nếu là quân đen và chiếu hết.
        """
        total = 0

        if self.board.is_checkmate():
            if self.color == "W":
                total += 50000
            else:
                total -= 50000

        return total

    def is_late_game(self):
        self.development()
        if (self.lateGameBlack) and (self.lateGameWhite):
            return True
        else:
            return False

    def result(self):
        """
        Tổng hợp điểm từ ba yếu tố: materialComp, development, và checkmate.
        Trả về tổng điểm cuối cùng của tình trạng bàn cờ.
        """
        total = 0

        # 1. materialComp đánh giá điểm dựa trên loại quân cờ còn lại trên bàn.
        total += self.materialComp()

        # 2. development đánh giá điểm dựa trên vị trí của các quân cờ trên bàn.
        total += self.development()

        # 3. checkmate đánh giá điểm dựa trên tình trạng chiếu hết.
        total += self.checkmate()

        return total

