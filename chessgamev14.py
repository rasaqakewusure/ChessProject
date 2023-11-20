import pygame
import sys

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BROWN = (150, 105, 25)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

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

def is_valid_pawn_move(start, board):
    row_start, col_start = start
    piece = board[row_start][col_start]
    direction = 1 if piece.islower() else -1

    valid_moves = []

    # Check if the target square is one square forward and empty
    if 0 <= row_start + direction <= 7 and board[row_start + direction][col_start] == "":
        valid_moves.append((row_start + direction, col_start))

    # Check for capturing moves diagonally
    for col_offset in [-1, 1]:
        col = col_start + col_offset
        if 0 <= row_start + direction <= 7 and 0 <= col <= 7 and board[row_start + direction][col] and board[row_start + direction][col].islower() != piece.islower():
            valid_moves.append((row_start + direction, col))

    # Handle the initial two-square move for pawns
    if (
        (row_start == 1 and piece.islower()) or (row_start == 6 and piece.isupper())
    ) and board[row_start + direction][col_start] == "":
        valid_moves.append((row_start + 2 * direction, col_start))

    return valid_moves

def pawn_promotion():
    promotion_pieces = ["Q", "R", "N", "B"]  # Queen, Rook, Knight, Bishop

    print("Pawn promotion! Choose a piece:")
    for i, piece in enumerate(promotion_pieces, start=1):
        print(f"{i}. {piece}")

    choice = int(input("Enter the number of your choice: "))
    while choice not in range(1, len(promotion_pieces) + 1):
        print("Invalid choice. Please choose again.")
        choice = int(input("Enter the number of your choice: "))

    board[target_position[0]][target_position[1]] = promotion_pieces[choice - 1]

# Legal move function for rooks
def is_valid_rook_move(start, board):
    row_start, col_start = start

    valid_moves = []

    # Check horizontally
    for col in range(col_start - 1, -1, -1):
        if board[row_start][col] == "":
            valid_moves.append((row_start, col))
        else:
            if board[row_start][col].islower() != board[row_start][col_start].islower():
                valid_moves.append((row_start, col))
            break

    for col in range(col_start + 1, 8):
        if board[row_start][col] == "":
            valid_moves.append((row_start, col))
        else:
            if board[row_start][col].islower() != board[row_start][col_start].islower():
                valid_moves.append((row_start, col))
            break

    # Check vertically
    for row in range(row_start - 1, -1, -1):
        if board[row][col_start] == "":
            valid_moves.append((row, col_start))
        else:
            if board[row][col_start].islower() != board[row_start][col_start].islower():
                valid_moves.append((row, col_start))
            break

    for row in range(row_start + 1, 8):
        if board[row][col_start] == "":
            valid_moves.append((row, col_start))
        else:
            if board[row][col_start].islower() != board[row_start][col_start].islower():
                valid_moves.append((row, col_start))
            break

    return valid_moves

# Legal move function for knights
def is_valid_knight_move(start, board):
    row_start, col_start = start

    valid_moves = []

    moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    for row_offset, col_offset in moves:
        row, col = row_start + row_offset, col_start + col_offset
        if 0 <= row <= 7 and 0 <= col <= 7 and (board[row][col] == "" or board[row][col].islower() != board[row_start][col_start].islower()):
            valid_moves.append((row, col))

    return valid_moves

# Legal move function for bishops
def is_valid_bishop_move(start, board):
    row_start, col_start = start

    valid_moves = []

    # Check diagonally
    for row_offset, col_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        row, col = row_start + row_offset, col_start + col_offset
        while 0 <= row <= 7 and 0 <= col <= 7:
            if board[row][col] == "":
                valid_moves.append((row, col))
            else:
                if board[row][col].islower() != board[row_start][col_start].islower():
                    valid_moves.append((row, col))
                break
            row += row_offset
            col += col_offset

    return valid_moves

# Legal move function for queens
def is_valid_queen_move(start, board):
    row_start, col_start = start

    valid_moves = []

    # Check horizontally
    for col in range(col_start - 1, -1, -1):
        if board[row_start][col] == "":
            valid_moves.append((row_start, col))
        else:
            if board[row_start][col].islower() != board[row_start][col_start].islower():
                valid_moves.append((row_start, col))
            break

    for col in range(col_start + 1, 8):
        if board[row_start][col] == "":
            valid_moves.append((row_start, col))
        else:
            if board[row_start][col].islower() != board[row_start][col_start].islower():
                valid_moves.append((row_start, col))
            break

    # Check vertically
    for row in range(row_start - 1, -1, -1):
        if board[row][col_start] == "":
            valid_moves.append((row, col_start))
        else:
            if board[row][col_start].islower() != board[row_start][col_start].islower():
                valid_moves.append((row, col_start))
            break

    for row in range(row_start + 1, 8):
        if board[row][col_start] == "":
            valid_moves.append((row, col_start))
        else:
            if board[row][col_start].islower() != board[row_start][col_start].islower():
                valid_moves.append((row, col_start))
            break

    # Check diagonally
    for row_offset, col_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        row, col = row_start + row_offset, col_start + col_offset
        while 0 <= row <= 7 and 0 <= col <= 7:
            if board[row][col] == "":
                valid_moves.append((row, col))
            else:
                if board[row][col].islower() != board[row_start][col_start].islower():
                    valid_moves.append((row, col))
                break
            row += row_offset
            col += col_offset

    return valid_moves

# Legal move function for kings
def is_valid_king_move(start, board):
    row_start, col_start = start

    valid_moves = []

    moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for row_offset, col_offset in moves:
        row, col = row_start + row_offset, col_start + col_offset
        if 0 <= row <= 7 and 0 <= col <= 7 and (board[row][col] == "" or board[row][col].islower() != board[row_start][col_start].islower()):
            valid_moves.append((row, col))

    return valid_moves

# Function to determine whose turn it is
def is_white_turn():
    white_pieces = "RNBQKP"
    black_pieces = "rnbqkp"
    white_count = sum(row.count(piece) for row in board for piece in white_pieces)
    black_count = sum(row.count(piece) for row in board for piece in black_pieces)
    return white_count == black_count

# Function to check if a king is in check
def is_king_in_check(color, board):
    king_position = find_king(color, board)
    opponent_color = "black" if color == "white" else "white"

    # Check if any opponent's piece can attack the king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.islower() == (color == "white"):  # Check if it's an opponent's piece
                valid_moves = get_valid_moves((row, col), board)
                if king_position in valid_moves:
                    return True

    return False

# Function to find the position of the king on the board
def find_king(color, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "K" and color == "white":
                return row, col
            elif piece == "k" and color == "black":
                return row, col

# Function to check if a player is in checkmate
def is_checkmate(color, board):
    # Check if the king is in check
    if not is_king_in_check(color, board):
        return False

    # Check if any move can get the king out of check
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == color[0]:
                piece_moves = get_valid_moves((row, col), board)
                for move in piece_moves:
                    new_board = [row[:] for row in board]
                    new_board[move[0]][move[1]] = new_board[row][col]
                    new_board[row][col] = ""
                    if not is_king_in_check(color, new_board):
                        return False

    return True

    # Function to get valid moves for a piece
def get_valid_moves(start, board):
    piece = board[start[0]][start[1]]
    if piece.lower() == "p":
        return is_valid_pawn_move(start, board)
    elif piece.lower() == "r":
        return is_valid_rook_move(start, board)
    elif piece.lower() == "n":
        return is_valid_knight_move(start, board)
    elif piece.lower() == "b":
        return is_valid_bishop_move(start, board)
    elif piece.lower() == "q":
        return is_valid_queen_move(start, board)
    elif piece.lower() == "k":
        return is_valid_king_move(start, board)
    # Add validation for other piece types

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
                    valid_moves = get_valid_moves(selected_piece_position, board)

                    if target_position in valid_moves:
                        board[selected_piece_position[0]][selected_piece_position[1]] = ""
                        board[target_position[0]][target_position[1]] = selected_piece

                        # Check for pawn promotion
                        if selected_piece.lower() == "p" and target_position[0] in [0, 7]:
                            pawn_promotion()

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
                piece_rect = piece_image.get_rect(
                    center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
                screen.blit(piece_image, piece_rect.topleft)

    if selected_piece_position:
        x, y = selected_piece_position
        pygame.draw.rect(screen, GREEN, (y * GRID_SIZE, (7 - x) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 4)

        # Get the valid moves for the selected piece
        valid_moves = get_valid_moves(selected_piece_position, board)

        # Highlight valid move squares
        for move in valid_moves:
            row, col = move
            pygame.draw.rect(screen, GREEN, (col * GRID_SIZE, (7 - row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 4)

    # Check for check and checkmate
    if is_king_in_check(current_turn, board):
        check_indicator = "CHECK!"
        if is_checkmate(current_turn, board):
            check_indicator = "CHECKMATE!"

        font = pygame.font.Font(None, 36)
        text = font.render(check_indicator, True, (255, 0, 0))
        screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
