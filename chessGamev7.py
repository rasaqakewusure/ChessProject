import pygame
import sys

#-----------------------------------------------------------
#CHECKLIST

#- Add bishops, queen, kings
#- Make player moves in turns (white first or black first etc...)
#- Display green box for valid moves
#- Create a check move
#- Add en passent and castlings
# - Split functions into seperate files and import it 
# - Add test functions 
#------------------------------------------------------------
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BROWN = (150, 105, 25)
GREEN = (0, 255, 0)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load chess piece images
images = {
    "P": pygame.image.load("wp.png"),
    "R": pygame.image.load("wR.png"),
    "N": pygame.image.load("wN.png"),
    "B": pygame.image.load("wB.png"),
    "Q": pygame.image.load("wQ.png"),
    "K": pygame.image.load("wK.png"),
    "p": pygame.image.load("bp.png"),
    "r": pygame.image.load("br.png"),
    "n": pygame.image.load("bn.png"),
    "b": pygame.image.load("bb.png"),
    "q": pygame.image.load("bq.png"),
    "k": pygame.image.load("bk.png"),
}

# Chessboard state
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# Function to convert pixel coordinates to chessboard coordinates
def pixel_to_chessboard(pos):
    x, y = pos
    col = x // GRID_SIZE
    row = 7 - y // GRID_SIZE
    return row, col

# Legal move function for pawns
def is_valid_pawn_move(start, end, board):
    row_start, col_start = start
    row_end, col_end = end
    piece = board[row_start][col_start]

    # Determine the direction of movement (up or down based on the piece)
    if piece.islower():
        direction = 1  # Black pawn moves down
    else:
        direction = -1  # White pawn moves up

    # Check if the target square is one square forward and empty
    if col_start == col_end and row_end == row_start + direction and board[row_end][col_end] == "":
        return True

    # Check if the target square is one square diagonally forward and has an opponent's piece
    if abs(col_end - col_start) == 1 and row_end == row_start + direction and board[row_end][col_end].islower() != piece.islower():
        return True

    # Handle the initial two-square move for pawns
    if (
        (row_start == 1 and piece.islower()) or (row_start == 6 and piece.isupper())
    ) and col_start == col_end and row_end == row_start + 2 * direction and board[row_start + direction][col_start] == "":
        return True

    return False

# Legal move function for rooks
def is_valid_rook_move(start, end, board):
    row_start, col_start = start
    row_end, col_end = end

    # Rook can move either horizontally or vertically
    if row_start == row_end:
        # Moving horizontally
        step = 1 if col_end > col_start else -1
        for col in range(col_start + step, col_end, step):
            if board[row_start][col] != "":
                return False
        return True
    elif col_start == col_end:
        # Moving vertically
        step = 1 if row_end > row_start else -1
        for row in range(row_start + step, row_end, step):
            if board[row][col_start] != "":
                return False
        return True

    return False

# Legal move function for knights
def is_valid_knight_move(start, end, board):
    row_start, col_start = start
    row_end, col_end = end

    # Knights can move in diagnolly
    if (abs(row_end - row_start) == 2 and abs(col_end - col_start) == 1) or (abs(row_end - row_start) == 1 and abs(col_end - col_start) == 2):
        return True

    return False

# Main game loop
running = True
selected_piece = None
selected_piece_position = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            position = pixel_to_chessboard((x, y))

            if not selected_piece:
                piece = board[position[0]][position[1]]
                if piece:
                    selected_piece = piece
                    selected_piece_position = position
            else:
                target_position = position

                if target_position != selected_piece_position:
                    # Check if the move is valid for the selected piece
                    if selected_piece.lower() == "p":
                        valid_move = is_valid_pawn_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "r":
                        valid_move = is_valid_rook_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "n":
                        valid_move = is_valid_knight_move(selected_piece_position, target_position, board)
                    else:
                        valid_move = False  # Add validation for other piece types

                    if valid_move:
                        board[selected_piece_position[0]][selected_piece_position[1]] = ""
                        board[target_position[0]][target_position[1]] = selected_piece

                selected_piece = None
                selected_piece_position = None

    screen.fill(WHITE)

    # Draw the chessboard
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BROWN
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the chess pieces on the board
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                piece_image = images[piece]
                screen.blit(piece_image, (col * GRID_SIZE, (7 - row) * GRID_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()
