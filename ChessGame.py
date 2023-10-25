import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BROWN= (150, 105, 25)

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

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

