import pygame as pg
from sys import exit
import math as m

# --- Initialization ---
pg.init()

width = 600
height = 600

sc = pg.display.set_mode((width, height))

pg.display.set_caption("Xavier's Tic-Tac-Toe")

# Load assets (Icon, Board, Pieces, and Fonts)
icon = pg.image.load('TicTacToe/Images/tic-tac-toe.png')
pg.display.set_icon(icon)

# Prepare board image
board = pg.image.load('TicTacToe/Images/tictactoe_board.jpg').convert()
board = pg.transform.scale(board, (360, 360))

# Text rendering setup
font = pg.font.Font('TicTacToe/Fonts/ELEGANT TYPEWRITER Bold.ttf', 40)
info = font.render("Player 1 Turn", True, (255,0,0))
info_rect = info.get_rect(center = (320,50))

# Piece images (using convert_alpha for transparency)
cross = pg.image.load('TicTacToe/Images/cross.png').convert_alpha()
cross = pg.transform.scale(cross, (50,50))
circle = pg.image.load('TicTacToe/Images/circle.png').convert_alpha()
circle = pg.transform.scale(circle, (50,50))

# Reset button setup
button = pg.image.load('TicTacToe/Images/reset.png').convert_alpha()
button = pg.transform.scale(button, (100,100))
button_rect = button.get_rect(center = (300,500))

# Scaling factor constants for placing pieces
blockX = 180
blockY = 170

# --- Game State Variables ---
player1chance = True  # True if X's turn, False if O's
won = False
chances = 0           # Count moves to detect a tie
pos = (0,0)           # Stores mouse click coordinates
result = None         # Stores which grid cell was clicked
pieces = []           # List of [image, x, y] for drawing moves
pos_matrix = [        # 3x3 logic board to track game state
    ['-','-','-'],
    ['-','-','-'],
    ['-','-','-']
]

def checkClicked(pos):
    """
    Maps screen pixel coordinates to grid indices.
    Returns a custom multiplier used for drawing and matrix indexing.
    """
    if (pos[0]>180 and pos[0]<260) and (pos[1]>150 and pos[1]<250):
        return(1,1)
    elif (pos[0]>265 and pos[0]<340) and (pos[1]>150 and pos[1]<250):
        return(1,1.5)
    elif (pos[0]>345 and pos[0]<420) and (pos[1]>150 and pos[1]<250):
        return(1,2)
    elif (pos[0]>180 and pos[0]<260) and (pos[1]>250 and pos[1]<350):
        return(1.6,1)
    elif (pos[0]>265 and pos[0]<340) and (pos[1]>250 and pos[1]<350):
        return(1.6,1.5)
    elif (pos[0]>345 and pos[0]<420) and (pos[1]>250 and pos[1]<350):
        return(1.6,2)
    elif (pos[0]>180 and pos[0]<260) and (pos[1]>350 and pos[1]<450):
        return(2.2,1)
    elif (pos[0]>265 and pos[0]<340) and (pos[1]>350 and pos[1]<450):
        return(2.2,1.5)
    elif (pos[0]>345 and pos[0]<420) and (pos[1]>350 and pos[1]<450):
        return(2.2,2)

    return None

def completeCheck(mat):
    """
    Checks the matrix for win conditions (Rows, Columns, Diagonals).
    Returns (Winning Text, Line Start Point, Line End Point).
    """
    # Check Rows
    for i in range(0,3):
        if mat[i][0] == mat[i][1]==mat[i][2]:
            if mat[i][0]=='X':
                win = 'Player 1 Win'
            elif mat[i][0]=='O':
                win = 'Player 2 Win'
            if mat[i][0]!='-':
                return win,(180,150+(i*100)+50), (420,150+(i*100)+50)
    # Check Columns 
    for i in range(0,3):
        if mat[0][i] == mat[1][i] == mat[2][i]:
            if mat[0][i]=='X':
                win = 'Player 1 Win'
            elif mat[0][i]=='O':
                win = 'Player 2 Win'
            if mat[0][i]!='-':
                return win, (180+(i*90)+35,150), (180+(i*90)+35,450)
    # Check Diagonal 1 (Top-Left to Bottom-Right)
    if mat[0][0]==mat[1][1]==mat[2][2]:
        if mat[0][0]=='X':
                win = 'Player 1 Win'
        elif mat[0][0]=='O':
                win = 'Player 2 Win'
        if mat[0][0]!='-':
            return win, (180,150), (420,450)
    # Check Diagonal 2 (Top-Right to Bottom-Left)
    if mat[0][2]==mat[1][1]==mat[2][0]:
        if mat[0][2]=='X':
                win = 'Player 1 Win'
        elif mat[0][2]=='O':
                win = 'Player 2 Win'
        if mat[0][2]!='-':
            return win, (180,450), (420,150)
    return "It is a Tie", (0,0)

def restart():
    """Resets all game variables to start a fresh match."""
    global player1chance, won, chances, pos, result, pieces, pos_matrix, info
    player1chance = True
    won = False
    chances = 0
    pos = (0,0)
    result = None
    pieces = []
    pos_matrix = [
        ['-','-','-'],
        ['-','-','-'],
        ['-','-','-']
    ]
    info = font.render("Player 1 Turn", True, (255,0,0))

clk = pg.time.Clock()

# --- Main Game Loop ---
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()

        # Update pos only on mouse up to trigger a move
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()

        # Check for Reset button click
        if event.type == pg.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(pg.mouse.get_pos()):
                restart()
    # Determine which grid cell was clicked
    result = checkClicked(pos)      

    if result != None:
        # Calculate matrix indices from the result tuple
        # Only place a piece if the cell is empty
        if pos_matrix[m.ceil(result[0])-1][round(result[1]-0.5)] == '-':
            if player1chance:
                pieces.append([cross,blockX*result[1]+10, blockY*result[0]])
                player1chance = False
                pos_matrix[m.ceil(result[0])-1][round(result[1]-0.5)]='X'
                info = font.render("Player 2 Turn", True, (255,0,0))
            else:
                pieces.append([circle,blockX*result[1]+10, blockY*result[0]])
                player1chance = True
                pos_matrix[m.ceil(result[0])-1][round(result[1]-0.5)]='O'
                info = font.render("Player 1 Turn", True, (255,0,0))

            chances+=1

            # Check if this move ended the game
            temp = completeCheck(pos_matrix)
            if temp[1]!=(0,0):
                info = font.render(temp[0], True, (255,0,0))
                won = True
    # Reset pos so move doesn't repeat every frame
    pos = (0,0)

    # --- Drawing ---
    sc.fill((255, 255, 255))      # Clear screen
    sc.blit(board,(120, 120))     # Draw board
    sc.blit(info, info_rect)      # Draw UI text

    # Draw all pieces placed so far
    for piece in pieces:
        sc.blit(piece[0], (piece[1], piece[2]))

    # End game UI (Winning line and Reset button)
    if won or chances==9:
        if won:
            pg.draw.line(sc, (255,0,0), temp[1], temp[2], 2)
        else:
            # Handle tie scenario
            info = font.render(temp[0], True, (255,0,0))

        sc.blit(button, button_rect)

    pg.display.update()
    clk.tick(60)