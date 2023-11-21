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

last_moved_pawn_position = None

# Legal move function for pawns
def is_valid_pawn_move(start, target, board):
    row_start, col_start = start
    row_target, col_target = target
    piece = board[row_start][col_start]
    direction = 1 if piece.islower() else -1

    valid_moves = []

    # Check if the target square is one square forward and empty
    if 0 <= row_target <= 7 and board[row_target][col_target] == "":
        valid_moves.append((row_target, col_target))

    # Check for capturing moves diagonally
    for col_offset in [-1, 1]:
        col = col_start + col_offset
        if 0 <= row_target <= 7 and 0 <= col <= 7 and board[row_target][col] and board[row_target][col].islower() != piece.islower():
            valid_moves.append((row_target, col))

    # Handle the initial two-square move for pawns
    initial_two_square_move = (
        (row_start == 1 and piece.islower()) or (row_start == 6 and piece.isupper())
    ) and col_start == col_target and abs(row_target - row_start) == 2

    if initial_two_square_move and board[row_target][col_target] == "":
        valid_moves.append((row_target, col_target))

    # Check for en passant
    if (
        last_moved_pawn_position
        and last_moved_pawn_position[0] == row_start
        and abs(last_moved_pawn_position[1] - col_start) == 2
        and row_target == last_moved_pawn_position[2]
        and col_target == last_moved_pawn_position[3]
    ):
        valid_moves.append((row_target, col_target))

    return valid_moves

def pawn_promotion(target_position):
    promotion_pieces = ["Q", "R", "N", "B"]  # Queen, Rook, Knight, Bishop

    # Pygame initialization for the promotion menu
    promotion_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pawn Promotion")

    font = pygame.font.Font(None, 36)

    while True:
        promotion_screen.fill(WHITE)

        # Draw squares on the promotion screen similar to the chessboard
        for row in range(8):
            for col in range(8):
                square_color = WHITE if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(promotion_screen, square_color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        text = font.render("Choose a piece:", True, (0, 0, 0))
        promotion_screen.blit(text, (10, 10))

        for i, piece in enumerate(promotion_pieces):
            text = font.render(piece, True, (0, 0, 0))
            promotion_screen.blit(text, (10, 50 + i * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected_piece = None

                for i, _ in enumerate(promotion_pieces):
                    if 10 <= x <= 100 and 50 + i * 30 <= y <= 80 + i * 30:
                        selected_piece = promotion_pieces[i]
                        break

                if selected_piece is not None:
                    # Adjust the color of the promoted piece based on the original piece color
                    if board[target_position[0]][target_position[1]].islower():
                        selected_piece = selected_piece.lower()

                    board[target_position[0]][target_position[1]] = selected_piece
                    return
  

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

def is_valid_castling(king_position, target_position, board):
    # Ensure the king and rook haven't moved
    row, col = king_position
    if board[row][col].lower() != 'k' or board[row][col + 3].lower() != 'r':
        return False

    # Ensure there are no pieces between the king and rook
    if col < target_position[1]:
        for c in range(col + 1, target_position[1]):
            if board[row][c] != "":
                return False
    else:
        for c in range(target_position[1] + 1, col):
            if board[row][c] != "":
                return False

    # Ensure the squares the king moves through are not under attack
    if is_square_under_attack(king_position, 'white', board):
        return False

    # Ensure the king doesn't move through, end up in, or start in check
    for c in range(col, col + 2):
        if is_square_under_attack((row, c), 'white', board):
            return False

    # Return True if all conditions are met
    return True

def is_square_under_attack(square, attacker_color, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.islower() == (attacker_color == "white"):  # Check if it's an opponent's piece
                valid_moves = get_valid_moves((row, col), board)
                if square in valid_moves:
                    return True
    return False

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
                    valid_moves = is_valid_pawn_move(selected_piece_position, target_position, board)
                    # Check for en passant
                    if (
                        selected_piece.lower() == "p"
                        and target_position in valid_moves
                        and abs(target_position[0] - selected_piece_position[0]) == 2
                    ):
                        last_moved_pawn_position = (
                            selected_piece_position[0],
                            selected_piece_position[1],
                            target_position[0],
                            target_position[1],
                        )

                    # Perform the regular move
                    board[selected_piece_position[0]][selected_piece_position[1]] = ""
                    board[target_position[0]][target_position[1]] = selected_piece

                    # Check for pawn promotion
                    if selected_piece.lower() == "p" and target_position[0] in [0, 7]:
                        pawn_promotion(target_position)

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