import pygame
import sys

# -----------------------------------------------------------
# CHECKLIST
# - Display green box for valid moves
# - Create a check move
# - Add en passant and castlings
# -----------------------------------------------------------
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
    if abs(col_end - col_start) == 1 and row_end == row_start + direction:
        target_piece = board[row_end][col_end]
        if target_piece and target_piece.islower() != piece.islower():
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
    piece = board[row_start][col_start]

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
    piece = board[row_start][col_start]

    # Knights can move diagonally
    if (abs(row_end - row_start) == 2 and abs(col_end - col_start) == 1) or (abs(row_end - row_start) == 1 and abs(col_end - col_start) == 2):
        return True

    return False

# Legal move function for bishops
def is_valid_bishop_move(start, end, board):
    row_start, col_start = start
    row_end, col_end = end
    piece = board[row_start][col_start]

    # Bishop can move diagonally
    if abs(row_end - row_start) == abs(col_end - col_start):
        step_row = 1 if row_end > row_start else -1
        step_col = 1 if col_end > col_start else -1
        row, col = row_start + step_row, col_start + step_col
        while row != row_end:
            if board[row][col] != "":
                return False
            row += step_row
            col += step_col
        return True

    return False

# Legal move function for queens
def is_valid_queen_move(start, end, board):
    row_start, col_start = start
    row_end, col_end = end
    piece = board[row_start][col_start]

    # Queen can move horizontally, vertically, or diagonally
    if row_start == row_end or col_start == col_end or abs(row_end - row_start) == abs(col_end - col_start):
        if row_start == row_end:
            step_col = 1 if col_end > col_start else -1
            col = col_start + step_col
            while col != col_end:
                if board[row_start][col] != "":
                    return False
                col += step_col
        elif col_start == col_end:
            step_row = 1 if row_end > row_start else -1
            row = row_start + step_row
            while row != row_end:
                if board[row][col_start] != "":
                    return False
                row += step_row
        else:
            step_row = 1 if row_end > row_start else -1
            step_col = 1 if col_end > col_start else -1
            row, col = row_start + step_row, col_start + step_col
            while row != row_end:
                if board[row][col] != "":
                    return False
                row += step_row
                col += step_col
        return True

    return False

# Legal move function for kings
def is_valid_king_move(start, end, board):
    row_start, col_start = start
    row_end, col_end = end
    piece = board[row_start][col_start]

    # King can move one square in any direction
    if abs(row_end - row_start) <= 1 and abs(col_end - col_start) <= 1:
        return True

    return False

# Function to determine whose turn it is
def is_white_turn():
    white_pieces = "RNBQKP"
    black_pieces = "rnbqkp"
    white_count = sum(row.count(piece) for row in board for piece in white_pieces)
    black_count = sum(row.count(piece) for row in board for piece in black_pieces)
    return white_count == black_count

# Main game loop
running = True
selected_piece = None
selected_piece_position = None
current_turn = "white"  # Initialize the current turn

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            position = pixel_to_chessboard((x, y))

            if not selected_piece:
                piece = board[position[0]][position[1]]
                if piece and ((current_turn == "white" and piece.isupper()) or (current_turn == "black" and piece.islower())):
                    selected_piece = piece
                    selected_piece_position = position
            else:
                target_position = position

                if target_position != selected_piece_position:
                    # Check if the move is valid for the selected piece
                    valid_move = False  # Initialize as invalid
                    if selected_piece.lower() == "p":
                        valid_move = is_valid_pawn_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "r":
                        valid_move = is_valid_rook_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "n":
                        valid_move = is_valid_knight_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "b":
                        valid_move = is_valid_bishop_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "q":
                        valid_move = is_valid_queen_move(selected_piece_position, target_position, board)
                    elif selected_piece.lower() == "k":
                        valid_move = is_valid_king_move(selected_piece_position, target_position, board)

                    # Check if the target square is either empty or occupied by an opponent's piece
                    if valid_move and (board[target_position[0]][target_position[1]] == "" or board[target_position[0]][target_position[1]].islower() != selected_piece.islower()):
                        board[selected_piece_position[0]][selected_piece_position[1]] = ""
                        board[target_position[0]][target_position[1]] = selected_piece
                        current_turn = "black" if current_turn == "white" else "white"

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
            piece = board[7 - row][col]
            if piece:
                piece_image = images[piece]
                piece_rect = piece_image.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
                screen.blit(piece_image, piece_rect.topleft)

    pygame.display.flip()

pygame.quit()
sys.exit()
