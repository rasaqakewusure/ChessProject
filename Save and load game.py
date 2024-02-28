import pygame
import sys
import random 
import copy 
import pickle 

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BROWN = (150, 105, 25)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Game state variables
game_states = []  # List to store the game state after each move
current_state_index = 0  # Index to keep track of the current state

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


# Function to find the position of the king on the board
def find_king(color, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "K" and color == "white":
                return row, col
            elif piece == "k" and color == "black":
                return row, col

def is_king_in_check(color, board):
    king_position = find_king(color, board)
    opponent_color = "black" if color == "white" else "white"

    # Check if any opponent's piece can attack the king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.islower() == (color == "white"):  # Check if it's an opponent's piece
                moves = get_valid_moves((row, col), board)
                if king_position in moves:
                    return True

    return False

def is_stalemate(color, board):
    # Check if the current player has no legal moves
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (color == "white" and piece.isupper()) or (color == "black" and piece.islower()):
                valid_moves = get_valid_moves((row, col), board)
                if valid_moves:
                    return False  # There is at least one legal move

    # Check if the king is not in check
    return not is_king_in_check(color, board)


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
                    new_board = make_move(board, ((row, col), move))
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


# Function to evaluate the board for the minimax algorithm
def evaluate_board(board):
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0, 'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0}
    evaluation = sum(piece_values.get(piece, 0) for row in board for piece in row)
    return evaluation


# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or is_checkmate("white", board) or is_checkmate("black", board):
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_moves("white", board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_moves("black", board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to get all possible moves for a player
def get_all_moves(player_color, board):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (player_color == "white" and piece.isupper()) or (player_color == "black" and piece.islower()):
                valid_moves = get_valid_moves((row, col), board)
                for move in valid_moves:
                    moves.append(((row, col), move))
    return moves

# Function to make a move on the board
def make_move(board, move):
    start, end = move
    new_board = copy.deepcopy(board)
    new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
    new_board[start[0]][start[1]] = ""
    return new_board

# Minimax AI move function
def minimax_ai_move():
    best_move = None
    best_eval = float('-inf')
    for move in get_all_moves("black", board):
        new_board = make_move(board, move)
        eval = minimax(new_board, 2, False, float('-inf'), float('inf'))
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

# Initialize the font outside the main loop
font = pygame.font.Font(None, 36)

def save_game_state_text(board, current_turn, move_history):
    try:
        with open("saved_game_state.txt", "w") as file:
            file.write(f"Current Turn: {current_turn}\n")
            file.write("Move History:\n")
            for move in move_history:
                if move[0] and move[1]:
                    from_square = chess_coordinates_to_algebraic(move[0])
                    to_square = chess_coordinates_to_algebraic(move[1])
                    file.write(f"{current_turn} move: {from_square} to {to_square}\n")
                else:
                    file.write(f"{current_turn} move\n")
            file.write("Board State:\n")
            for row in board:
                file.write("".join(row) + "\n")
        print("Game state saved successfully!")
    except Exception as e:
        print("Error saving game state:", e)



def load_game_state():
    try:
        with open("saved_game_state.txt", "r") as file:
            lines = file.readlines()
            current_turn = lines[0].split(": ")[1].strip()
            move_history = []
            board = []
            for line in lines[1:]:
                if line.startswith("Board State:"):
                    break
                elif line.startswith(current_turn):
                    parts = line.split()
                    if parts[-1] == "move":
                        move_history.append((None, None))
                    else:
                        move_history.append((algebraic_to_chess_coordinates(parts[1]), algebraic_to_chess_coordinates(parts[3])))
                else:
                    board.append(list(line.strip()))

        print("Game state loaded successfully!")
        return board, current_turn, move_history
    except FileNotFoundError:
        print("No saved game state found.")
        return None, None, None
    except Exception as e:
        print("Error loading game state:", e)
        return None, None, None

# Helper function to convert algebraic notation to chess coordinates
def algebraic_to_chess_coordinates(algebraic):
    file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    rank = 8 - int(algebraic[1])
    file = file_map[algebraic[0]]
    return rank, file

# Helper function to convert chess coordinates to algebraic notation
def chess_coordinates_to_algebraic(coords):
    file_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    rank = 8 - coords[0]
    file = file_map[coords[1]]
    return file + str(rank)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)

# Function to save the game state to a file
def save_game_state():
    with open('chess_game_state.pickle', 'wb') as f:
        pickle.dump((board, current_turn, game_states, current_state_index, move_history), f)

# Function to load the game state from a file
def load_game_state():
    global board, current_turn, game_states, current_state_index, move_history
    with open('chess_game_state.pickle', 'rb') as f:
        board, current_turn, game_states, current_state_index, move_history = pickle.load(f)

# Main game loop
running = True
selected_piece = None
selected_piece_position = None
current_turn = "white"  # Initialize the current turn
game_states = [copy.deepcopy(board)]  # Store the initial game state
current_state_index = 0  # Index to track the current state in the game_states list
move_history = []  # Store move history

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Code for selecting and moving pieces
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

                    # Check for castling and regular moves
                    if target_position in valid_moves:
                        # Save the current state before making a move
                        current_state_index += 1
                        game_states = game_states[:current_state_index]
                        game_states.append(copy.deepcopy(board))

                        # Perform regular move
                        board[selected_piece_position[0]][selected_piece_position[1]] = ""
                        board[target_position[0]][target_position[1]] = selected_piece

                        # Add move to move history
                        move_history.append((selected_piece_position, target_position))

                        # Check for pawn promotion
                        if selected_piece.lower() == "p" and target_position[0] in [0, 7]:
                            pawn_promotion(target_position)

                        current_turn = "black" if current_turn == "white" else "white"

                    selected_piece = None
                    selected_piece_position = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Save game
                save_game_state_text(board, current_turn, move_history)
            elif event.key == pygame.K_l:  # Load game
                board, current_turn, move_history = load_game_state()
            if event.key == pygame.K_b:  # Back button
                if current_state_index > 0:
                    current_state_index -= 1
                # Remove the last move from the move history
                if move_history:
                    move_history.pop()
                # If the current turn is black, remove the AI move from the move history as well
                if current_turn == "black" and move_history:
                    move_history.pop()
                board = copy.deepcopy(game_states[current_state_index])
                current_turn = "white" if current_turn == "black" else "black"
            elif event.key == pygame.K_n:  # Next button
                if current_state_index < len(game_states) - 1:
                    current_state_index += 1
                board = copy.deepcopy(game_states[current_state_index])
                current_turn = "white" if current_turn == "black" else "black"
                # Add next move to move history
                if current_state_index < len(game_states) - 1:
                    move_history.append((None, None))

    # If it's the AI player's turn
    if current_turn == "black":
        ai_move = minimax_ai_move()
        # Update the board and game state with the AI move
        board = make_move(board, ai_move)
        current_turn = "white"  # Switch turn back to player after AI move

    # Code for drawing the board, pieces, highlights, etc.
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

    # Display move history
    font = pygame.font.Font(None, 24)
    move_history_text = "Move History:"
    move_history_text_surface = font.render(move_history_text, True, BLACK)
    screen.blit(move_history_text_surface, (10, 10))
    y_offset = 30
    for move_index, move in enumerate(move_history, start=1):
        if move[0] and move[1]:
            move_text = f"{move_index}. {chess_coordinates_to_algebraic(move[0])} to {chess_coordinates_to_algebraic(move[1])}"
        else:
            move_text = f"{move_index}. {current_turn} move"
        move_text_surface = font.render(move_text, True, BLACK)
        screen.blit(move_text_surface, (10, 10 + y_offset * (move_index + 1)))

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
