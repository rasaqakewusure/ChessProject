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
                screen.blit(piece_image, (col * GRID_SIZE, row * GRID_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()

