"""
This class is responsible for storing all information about the current state of the chess game. It will also be
responsible for determining the valid moves at the current state. Also keep a move log.
"""


"""
Need to fix random pawn spawns
"""

class GameState():
    def __init__(self):
        # In future make self.board into a numpy array

        # board right now is a 8x8 2 dimensional list, each element contains 2 characters
        # first character represents color of piece and second character represents
        # the type of the piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                              'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.moveLog = []
        self.checkMate = False
        self.staleMate = False
        self.whiteLeftRookMoved = False
        self.whiteRightRookMoved = False
        self.whiteKingMoved = False
        self.blackLeftRookMoved = False
        self.blackRightRookMoved = False
        self.blackKingMoved = False
        self.enpassantPossible = ()

    """
    Takes a move as a parameter and executes it (not working for castle, en passant, and promotion
    """

    def make_move_foresight(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log move
        self.whiteToMove = not self.whiteToMove

        # update king pos
        if move.pieceMoved == "wK" and abs(move.endCol - move.startCol) != 2:
            self.whiteKingLocation = move.endRow, move.endCol
        elif move.pieceMoved == "bK" and abs(move.endCol - move.startCol) != 2:
            self.blackKingLocation = move.endRow, move.endCol

        # white castle king side
        if move.pieceMoved == "wK" and move.startCol == 4 and move.endCol == 6 and not self.whiteKingMoved and not self.whiteRightRookMoved:
            self.whiteKingLocation = move.endRow, move.endCol
            self.board[7][5] = "wR"
            self.board[7][7] = "--"

        # white castle queen side
        if move.pieceMoved == "wK" and move.startCol == 4 and move.endCol == 2 and not self.whiteKingMoved and not self.whiteLeftRookMoved:
            self.whiteKingLocation = move.endRow, move.endCol
            self.board[7][3] = "wR"
            self.board[7][0] = "--"

        # black castle king side
        if move.pieceMoved == "bK" and move.startCol == 4 and move.endCol == 6 and not self.blackKingMoved and not self.blackRightRookMoved:
            self.blackKingLocation = move.endRow, move.endCol
            self.board[0][5] = "bR"
            self.board[0][7] = "--"

        # black castle queen side
        if move.pieceMoved == "bK" and move.startCol == 4 and move.endCol == 2 and not self.blackKingMoved and not self.blackLeftRookMoved:
            self.blackKingLocation = move.endRow, move.endCol
            self.board[0][3] = "bR"
            self.board[0][0] = "--"

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

    def undo_foresight_move(self):
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove

        # update king pos
        if move.pieceMoved == "wK":
            self.whiteKingLocation = move.startRow, move.startCol
        elif move.pieceMoved == "bK":
            self.blackKingLocation = move.startRow, move.startCol

        # undo en passant
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)

        # undo a 2 square pawn advance
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()

        # undo white king side castle
        if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 6 and move.startRow == 7:
            self.board[7][7] = "wR"
            self.board[7][5] = "--"

        # undo white queen side castle
        if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 2 and move.startRow == 7:
            self.board[7][0] = "wR"
            self.board[7][3] = "--"

        # undo black king side castle
        if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 6 and move.startRow == 0:
            self.board[0][7] = "bR"
            self.board[0][5] = "--"

        # undo white queen side castle
        if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 2 and move.startRow == 0:
            self.board[0][0] = "bR"
            self.board[0][3] = "--"

        self.checkMate = False
        self.staleMate = False

    def reset_to_pos(self, board):
        self.board = board

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log move
        self.whiteToMove = not self.whiteToMove

        # check if rooks have moved for castling purposes
        if move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 7:
            self.whiteRightRookMoved += 1
        if move.pieceMoved == "wR" and move.startRow == 7 and move.startCol == 0:
            self.whiteLeftRookMoved += 1
        if move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 7:
            self.blackRightRookMoved += 1
        if move.pieceMoved == "bR" and move.startRow == 0 and move.startCol == 0:
            self.blackLeftRookMoved += 1

        # update king pos
        if move.pieceMoved == "wK" and abs(move.endCol - move.startCol) != 2:
            self.whiteKingLocation = move.endRow, move.endCol
            self.whiteKingMoved += 1
        elif move.pieceMoved == "bK" and abs(move.endCol - move.startCol) != 2:
            self.blackKingLocation = move.endRow, move.endCol
            self.blackKingMoved += 1

        # white castle king side
        if move.pieceMoved == "wK" and move.startCol == 4 and move.endCol == 6 and not self.whiteKingMoved and not self.whiteRightRookMoved and not self.inCheck:
            self.whiteKingLocation = move.endRow, move.endCol
            self.board[7][5] = "wR"
            self.board[7][7] = "--"
            self.whiteKingMoved = True
            self.whiteRightRookMoved = True

        # white castle queen side
        if move.pieceMoved == "wK" and move.startCol == 4 and move.endCol == 2 and not self.whiteKingMoved and not self.whiteLeftRookMoved and not self.inCheck:
            self.whiteKingLocation = move.endRow, move.endCol
            self.board[7][3] = "wR"
            self.board[7][0] = "--"
            self.whiteKingMoved = True
            self.whiteLeftRookMoved = True

        # black castle king side
        if move.pieceMoved == "bK" and move.startCol == 4 and move.endCol == 6 and not self.blackKingMoved and not self.blackRightRookMoved and not self.inCheck:
            self.blackKingLocation = move.endRow, move.endCol
            self.board[0][5] = "bR"
            self.board[0][7] = "--"
            self.blackKingMoved = True
            self.blackRightRookMoved = True

        # black castle queen side
        if move.pieceMoved == "bK" and move.startCol == 4 and move.endCol == 2 and not self.blackKingMoved and not self.blackLeftRookMoved and not self.inCheck:
            self.blackKingLocation = move.endRow, move.endCol
            self.board[0][3] = "bR"
            self.board[0][0] = "--"
            self.blackKingMoved = True
            self.blackLeftRookMoved = True

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

    """
    Undo the last move
    """

    def undo_move(self):
        if (len(self.moveLog) != 0):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update king pos
            if move.pieceMoved == "wK":
                self.whiteKingLocation = move.startRow, move.startCol
                self.whiteKingMoved = False
            elif move.pieceMoved == "bK" :
                self.blackKingLocation = move.startRow, move.startCol
                self.blackKingMoved = False

            # undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo white king side castle
            if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 6 and move.startRow == 7:
                self.board[7][7] = "wR"
                self.board[7][5] = "--"
                self.whiteRightRookMoved = False
                self.whiteKingMoved = False

            # undo white queen side castle
            if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 2 and move.startRow == 7:
                self.board[7][0] = "wR"
                self.board[7][3] = "--"
                self.whiteLeftRookMoved = False
                self.whiteKingMoved = False

            # undo black king side castle
            if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 6 and move.startRow == 0:
                self.board[0][7] = "bR"
                self.board[0][5] = "--"
                self.blackRightRookMoved = False
                self.blackKingMoved = False

            # undo white queen side castle
            if move.pieceMoved[1] == 'K' and move.startCol == 4 and move.endCol == 2 and move.startRow == 0:
                self.board[0][0] = "bR"
                self.board[0][3] = "--"
                self.blackLeftRookMoved = False
                self.blackKingMoved = False
            self.checkMate = False
            self.staleMate = False

    """
    All moves with checks
    """

    def get_valid_moves(self):
        tempEmpassantPossible = self.enpassantPossible
        moves = []
        self.inCheck, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check
                moves = self.get_all_moves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':  # if knight must move or capture
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (
                        kingRow + check[2] * i, kingCol + check[3] * i)  # check[2] and check[3] are check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(kingRow, kingCol, moves)
        else:
            moves = self.get_all_moves()
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True

        if self.whiteToMove:
            # white king side castling
            if self.board[7][5] == '--' and self.board[7][6] == '--' and self.board[7][7][1] == 'R':
                if not self.whiteKingMoved and not self.whiteRightRookMoved:
                    moves.append(Move((7, 4), (7, 6), self.board))
            # white queen side castling
            if self.board[7][1] == '--' and self.board[7][2] == '--' and self.board[7][3] == '--' and self.board[7][0][
                1] == 'R':
                if not self.whiteKingMoved and not self.whiteLeftRookMoved:
                    moves.append(Move((7, 4), (7, 2), self.board))
        else:
            # black king side castling
            if self.board[0][5] == '--' and self.board[0][6] == '--' and self.board[0][7][1] == 'R':
                if not self.blackKingMoved and not self.blackRightRookMoved:
                    moves.append(Move((0, 4), (0, 6), self.board))
            # black queen side castling
            if self.board[0][1] == '--' and self.board[0][2] == '--' and self.board[0][3] == '--' and self.board[0][0][
                1] == 'R':
                if not self.blackKingMoved and not self.blackLeftRookMoved:
                    moves.append(Move((0, 4), (0, 2), self.board))
        self.enpassantPossible = tempEmpassantPossible
        return moves

    """
    All moves without checks
    """

    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color_of_piece = self.board[r][c][0]
                if (color_of_piece == 'w' and self.whiteToMove) or (color_of_piece == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    """
    Get all pawn moves given position and append moves to array
    """

    def get_pawn_moves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False

        if self.board[r + moveAmount][c] == "--":
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnPromotion = True
                moves.append(Move((r, c,), (r + moveAmount, c), self.board, isPawnPromotion=pawnPromotion))
                if r == startRow and self.board[r+2*moveAmount][c] == "--":
                    moves.append(Move((r, c), (r+2*moveAmount, c), self.board))
        if c - 1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r+moveAmount, c-1), self.board, isPawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c-1), self.board, isEnpassantMove=True))
        if c + 1 <= 7:
            if not  piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r+moveAmount, c+1), self.board, isPawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, isEnpassantMove=True))


        # if self.whiteToMove:
        #     if self.board[r - 1][c] == "--":  # can move forward 1
        #         if not piecePinned or pinDirection == (-1, 0):
        #             moves.append(Move((r, c), (r - 1, c), self.board))
        #             if r == 6 and self.board[r - 2][c] == "--":  # can move forward 2
        #                 moves.append(Move((r, c), (r - 2, c), self.board))
        #     if c - 1 >= 0:
        #         if self.board[r - 1][c - 1][0] == 'b':  # can capture to the left
        #             if not piecePinned or pinDirection == (-1, -1):
        #                 moves.append(Move((r, c), (r - 1, c - 1), self.board))
        #         elif (r - 1, c - 1) == self.enpassantPossible:
        #             moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
        #     if c + 1 <= 7:
        #         if self.board[r - 1][c + 1][0] == 'b':  # capture to the right
        #             if not piecePinned or pinDirection == (-1, 1):
        #                 moves.append(Move((r, c), (r - 1, c + 1), self.board))
        #             elif (r - 1, c + 1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))
        #
        # else:  # black pawn moves
        #     if self.board[r + 1][c] == "--":
        #         if not piecePinned or pinDirection == (1, 0):
        #             moves.append(Move((r, c), (r + 1, c), self.board))
        #             if r == 1 and self.board[r + 2][c] == "--":
        #                 moves.append(Move((r, c), (r + 2, c), self.board))
        #     if c - 1 >= 0:
        #         if self.board[r + 1][c - 1][0] == 'w':  # can capture to the left
        #             if not piecePinned or pinDirection == (1, -0):
        #                 moves.append(Move((r, c), (r + 1, c - 1), self.board))
        #             elif (r + 1, c - 1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
        #     if c + 1 <= 7:
        #         if self.board[r + 1][c + 1][0] == 'w':  # capture to the right
        #             if not piecePinned or pinDirection == (1, 1):
        #                 moves.append(Move((r, c), (r + 1, c + 1), self.board))
        #             elif (r + 1, c + 1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    """
    Get all rook moves given position and append moves to array
    """

    def get_rook_moves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                # self.pins.remove(self.pins[i])  not sure if this is needed
                if self.board[r][c][1] != 'Q':  # can't remove pin from queen on rook moves, only on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    """
    Get all queen moves given position and append moves to array
    """

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    """
    Get all knight moves given position and append moves to array
    """

    def get_knight_moves(self, r, c, moves):
        piecePinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Get all bishop moves given position and append moves to array
    """

    def get_bishop_moves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    """
    Get all king moves given position and append moves to array
    """

    def get_king_moves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor and endPiece[1] != 'K':
                    # place king on square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.check_for_pins_and_checks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # move king back to original square
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

    """
    Returns bool inCheck, array of pins, and array of checks
    """

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        # check outward from king for pins checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for i in range(len(directions)):
            d = directions[i]
            possiblePin = ()  # reset possible pins
            for j in range(1, 8):
                endRow = startRow + d[0] * j
                endCol = startCol + d[1] * j
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():  # first ally piece might be in a pin
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # if theres 2 allied pieces in a row no possibility of a pin
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 different possibilities
                        # 1. orthogonally from king from rook
                        # 2. diagonally from king from bishop
                        # 3. 1 square away diagionally from pawn
                        # 4. any direction from queen
                        # 5. any direction 1 square away from king
                        if (0 <= i <= 3 and type == 'R') or \
                                (4 <= i <= 7 and type == 'B') or \
                                (j == 1 and type == 'P' and (
                                        (enemyColor == 'w' and 6 <= i <= 7) or (enemyColor == 'b' and 4 <= i <= 5))) or \
                                (type == 'Q') or (j == 1 and type == 'K'):
                            if possiblePin == ():  # no piece blocking so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not giving check
                            break
                else:
                    break
        # check for knighyt checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isPawnPromotion=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = isPawnPromotion
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    Override equals method
    """

    def __eq__(self, other):
        if isinstance(other, Move):
            if other.moveID == self.moveID:
                return True
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
