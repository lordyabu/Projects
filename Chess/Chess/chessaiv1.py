import random
import ChessEngine


# TO DO set castling as preferred move in min_max
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1, "-": 0, "--": 0}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
global nextMove

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    bestPlayerMove = None
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    random.shuffle(validMoves)
    tempBoard = gs.board
    for playerMove in validMoves:
        gs.make_move_foresight(playerMove)
        opponentsMoves = gs.get_valid_moves()
        if gs.staleMate:
            opponentMaxScore = 0
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.make_move_foresight(opponentsMove)
                gs.get_valid_moves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = 0
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undo_foresight_move()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undo_foresight_move()

    return bestPlayerMove

"""
CHANGE FUNCTION TO CHOOSE AI
"""
def find_best_mov_min_max(gs, validMoves):
    global nextMove
    find_move_mega_max_alpha_beta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

"""
Recursive helper method
"""
def find_move_min_max(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.make_move_foresight(move)
            nextMoves = gs.get_valid_moves()
            score = find_move_min_max(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undo_foresight_move()
        return maxScore
    else:
        minScore = CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.make_move_foresight(move)
            nextMoves = gs.get_valid_moves()
            score = find_move_min_max(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
                    # if nextMove.pieceMoved == "bK":
                    #     castle = Move((nextMove.startRow, nextMove.startCol), (0, 6))
                    #     nextMove
            gs.undo_foresight_move()
        return minScore


def find_move_mega_max(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return whiteToMove * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.make_move_foresight(move)
        nextMoves = gs.get_valid_moves()
        score = -find_move_mega_max(gs, nextMoves, depth - 1, -whiteToMove)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undo_foresight_move()
    return maxScore

def find_move_mega_max_alpha_beta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove
    if depth == 0:
        return whiteToMove * scoreBoard(gs)


    # move ordering - inplement later

    maxScore = -CHECKMATE
    random.shuffle(validMoves)
    for move in validMoves:
        gs.make_move_foresight(move)
        nextMoves = gs.get_valid_moves()
        score = -find_move_mega_max_alpha_beta(gs, nextMoves, depth - 1, -beta, -alpha, -whiteToMove)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undo_foresight_move()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


"""
Better scoreboard, positive score good for white
"""

def scoreBoard(gs):

    if (gs.checkMate):
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return 0


    score = 0
    for r in gs.board:
        for sq in r:
            if sq[0] == 'w':
                score += pieceScore[sq[1]]
            elif sq[0] == 'b':
                score -= pieceScore[sq[1]]

    return score

"""
Score the board on material
"""

def scoreMaterial(board):
    score = 0
    for r in board:
        for sq in r:
            if sq[0] == 'w':
                score += pieceScore[sq[1]]
            else:
                score -= pieceScore[sq[1]]

    return score