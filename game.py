import pygame
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

WIDTH = 50
HEIGHT = 50
MARGIN = 1

# This function creates the pygame screen used in the game as well as the board. The board is a list of lists where
# each nested list is size 10. The resulting 10 x 10 matrix represents the board for the game. A 1 in the position
# represents the red player, a 2 represents the blue player, and a 0 means the spot is empty.
def setup():
    WINDOW_SIZE = [511, 600]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill(BLACK)

    # Creates a list of lists that represents the board for the game
    board = [[0 for i in range(10)] for j in range(10)]

    # Setting up the initial red spots on the board
    for i in range(1, 9):
        board[1][i] = 1

    # Setting up the initial blue spots on the board
    for j in range(1, 9):
        board[-2][j] = 2

    # Draws the pygame screen by drawing the 100 green squared spaced a little bit apart to give a margin
    for row in range(10):
        for column in range(10):
            pygame.draw.rect(screen, GREEN, [(MARGIN + WIDTH) * column + MARGIN,
                                             (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

    # Draws player 1 (the red circles) onto the board
    for i in range(8):
        val = 77 + (i * 51)
        pygame.draw.circle(screen, RED, (val, 77), 20)

    # Draws player 2 (the blue circles) onto the board
    for i in range(8):
        val = 77 + (i * 51)
        pygame.draw.circle(screen, BLUE, (val, 434), 20)

    # Information on the screen saying who the current player is. Player 1 starts first
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render('Current Player: 1', True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (255, 550)
    screen.blit(text, text_rect)
    return screen, board