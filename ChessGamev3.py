import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BROWN = (150, 105, 25)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load chess piece images
images = {
   "P": pygame.image.load("bP.png"),
    "R": pygame.image.load("bR.png"),
    "N": pygame.image.load("bK.png"),
    "B": pygame.image.load("bB.png"),
    "Q": pygame.image.load("bQ.png"),
    "K": pygame.image.load("bK.png"),
    "p": pygame.image.load("wp.png"),
    "r": pygame.image.load("wR.png"),
    "n": pygame.image.load("wK.png"),
    "b": pygame.image.load("wB.png"),
    "q": pygame.image.load("wQ.png"),
    "k": pygame.image.load("wK.png"),
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

# Variables to store dragged piece information
dragging = False
dragged_piece = None
start_pos = None

valid_move_squares = []

def draw_labels():
    font = pygame.font.Font(None, 12)
    for i in range(8):
        row_label = font.render(str(8 - i), True, (0, 0, 0))
        col_label = font.render(chr(ord('a') + i), True, (0, 0, 0))
        screen.blit(row_label, (8 * 8 + 10, GRID_SIZE * i))
        screen.blit(col_label, (GRID_SIZE * i, GRID_SIZE * 8 + 10))



# Function to get valid moves for a pawn
def get_valid_pawn_moves(row, col):
    valid_moves = []
    piece = board[row][col]
    direction = 1 if piece.isupper() else -1  # Determine the direction for the pawn based on its color

    # Move one square forward
    if board[row + direction][col] == "":
        valid_moves.append((row + direction, col))

    # Move two squares forward (for the initial move)
    if (
        ((direction == 1 and row == 1) or (direction == -1 and row == 6))
        and board[row + direction][col] == ""
        and board[row + 2 * direction][col] == ""
    ):
        valid_moves.append((row + 2 * direction, col))

    # Capture diagonally
    for delta_col in [-1, 1]:
        target_row = row + direction
        target_col = col + delta_col
        if 0 <= target_row < 8 and 0 <= target_col < 8 and board[target_row][target_col] != "":
            valid_moves.append((target_row, target_col))

    return valid_moves

# Function to get valid moves for a rook
def get_valid_rook_moves(row, col):
    valid_moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "":
                valid_moves.append((r, c))
                r, c = r + dr, c + dc
            else:
                if board[r][c].islower() != board[row][col].islower():
                    valid_moves.append((r, c))
                break

    return valid_moves

# Function to get valid moves for a knight
def get_valid_knight_moves(row, col):
    valid_moves = []
    knight_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]

    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "" or board[r][c].islower() != board[row][col].islower():
                valid_moves.append((r, c))

    return valid_moves

# Function to get valid moves for a bishop
def get_valid_bishop_moves(row, col):
    valid_moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "":
                valid_moves.append((r, c))
                r, c = r + dr, c + dc
            else:
                if board[r][c].islower() != board[row][col].islower():
                    valid_moves.append((r, c))
                break

    return valid_moves

# Function to get valid moves for a queen
def get_valid_queen_moves(row, col):
    rook_moves = get_valid_rook_moves(row, col)
    bishop_moves = get_valid_bishop_moves(row, col)
    return rook_moves + bishop_moves

# Function to get valid moves for a king
def get_valid_king_moves(row, col):
    valid_moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "" or board[r][c].islower() != board[row][col].islower():
                valid_moves.append((r, c))

    return valid_moves

def calculate_valid_moves(row, col, piece):
    if piece.lower() == 'p':
        return get_valid_pawn_moves(row, col)
    elif piece.lower() == 'r':
        return get_valid_rook_moves(row, col)
    elif piece.lower() == 'n':
        return get_valid_knight_moves(row, col)
    elif piece.lower() == 'b':
        return get_valid_bishop_moves(row, col)
    elif piece.lower() == 'q':
        return get_valid_queen_moves(row, col)
    elif piece.lower() == 'k':
        return get_valid_king_moves(row, col)
    else:
        return []  # Return an empty list for an unknown piece (e.g., empty square)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not dragging:
            x, y = pygame.mouse.get_pos()
            col = x // GRID_SIZE
            row = y // GRID_SIZE
            if 0 <= row < 8 and 0 <= col < 8:
                piece = board[7 - row][col]
                if piece:
                    dragging = True
                    dragged_piece = piece
                    start_pos = (row, col)
                    board[7 - row][col] = ""  # Remove the piece from its original position
                    valid_move_squares = calculate_valid_moves(7 - row, col, piece)
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            x, y = pygame.mouse.get_pos()
            col = x // GRID_SIZE
            row = y // GRID_SIZE
            if 0 <= row < 8 and 0 <= col < 8 and board[7 - row][col] == "":
                board[7 - row][col] = dragged_piece  # Move the piece to the new position
            else:
                # Move the piece back to its original position if the move is invalid
                board[start_pos[0]][start_pos[1]] = dragged_piece
            dragging = False
            dragged_piece = None
            start_pos = None

    screen.fill(WHITE)

    # Draw the labels for rows and columns
    draw_labels()

    # Draw the chessboard
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BROWN
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

     # Draw the translucent overlay on valid move squares
    for move_square in valid_move_squares:
        row, col = move_square
        overlay_color = (0, 255, 0, 100)  # Green with 100 alpha for transparency
        pygame.draw.rect(screen, overlay_color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the chess pieces on the board
    for row in range(8):
        for col in range(8):
            piece = board[7 - row][col]
            if piece:
                piece_image = images[piece]
                screen.blit(piece_image, (col * GRID_SIZE, row * GRID_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()
