"""
This is our driver file. IT will be responsible for handling user input and displaying the current GameState object
"""

import pygame as p
from Chess import ChessEngine, chessaiv1

WIDTH = HEIGHT = 512  # can change to 400 if too small
DIMENSION = 8  # 8 x 8 board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later
IMAGES = {}

"""
Initialize a global dictionary of images. Will only be called once
"""


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wP']'


"""
The main driver for the code, will handle user input and graphics
"""


def main():
    p.init()
    screen = p.display.set_mode(size=(WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.get_valid_moves()
    moveMade = False  # flag variable for when move is made
    animate = False  # flag variable for when to animate
    load_images()
    running = True
    gameOver = False
    playerOne = True  # if human is white, then this will be true, if AI then false
    playerTwo = False
    sqSelected = ()  # keep track of last click of user(tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)]
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # (x,y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):  # user has clicked the same square twice
                        sqSelected = ()  # deselect
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both first and second clicks
                    if len(playerClicks) == 2:  # after second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.get_chess_notation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.make_move(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo last move with z
                    gs.undo_move()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:  # reset board when r
                    gs = ChessEngine.GameState()
                    validMoves = gs.get_valid_moves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        # Ai move finder
        if not gameOver and not humanTurn:
            AIMove = chessaiv1.find_best_mov_min_max(gs, validMoves)
            # if AIMove is None:
            #     AIMove = chessaiv1.findRandomMove(validMoves)
            gs.make_move(AIMove)
            moveMade = True
            animate = True


        if moveMade:
            if animate:
                animate_move(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.get_valid_moves()
            moveMade = False
            animate = False
        draw_game_state(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


"""
Highlight squares selected and moves
"""


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('dark green'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


"""
Responsible for all the graphics within a current game state.
"""


def draw_game_state(screen, gs, validMoves, sqSelected):
    draw_board(screen)  # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    draw_pieces(screen, gs.board)  # draw pieces on top of the squares


"""
Draw squares on the board
"""


def draw_board(screen):
    global colors
    colors = [p.Color("white"), p.Color("light gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # piece not an empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animate_move(move, screen, board, clock):
    global colors
    coords = []  # list of coordinates that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase piece from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
