import pygame
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Checks that a user clicked a position they have their own piece is on
def valid_pos(board, x, y, current_player):
    return board[x][y] == current_player

# If a user has selected a piece and clicks on a spot to move the piece, this function checks that
# new spot is valid by checking if its empty and within 2 spots of the current piece's position
def valid_move(board, last_move, x, y):
    if board[x][y] != 0:
        return False
    if abs(last_move[0] - x) < 3 and abs(last_move[1] - y) < 3:
        return True
    return False

# Draws an outline around one of the squares of the board
def draw_outline(screen, x, y, color):
    c1 = x * 51
    c2 = (x * 51) + 51
    c3 = y * 51
    c4 = (y * 51) + 51
    pygame.draw.line(screen, color, (c3, c1), (c3, c2))
    pygame.draw.line(screen, color, (c4, c1), (c4, c2))
    pygame.draw.line(screen, color, (c3, c2), (c4, c2))
    pygame.draw.line(screen, color, (c3, c1), (c4, c1))

# Draws a circle (which represents a game piece) at a specific spot in the board or can cover up
# a piece by drawing over with a green circle
def draw_circle(screen, x, y, color):
    y_draw = 26 + (x * 51)
    x_draw = 26 + (y * 51)
    pygame.draw.circle(screen, color, (x_draw, y_draw), 20)

# Called when a piece makes a move. Removes the highlighting the piece had, updates the board object, and
# calls the drawing function to update the pygame display
def make_movement(screen, board, last_click, x, y, current_player):
    draw_outline(screen, last_click[0], last_click[1], BLACK)
    board[last_click[0]][last_click[1]] = 0
    board[x][y] = current_player
    draw_circle(screen, last_click[0], last_click[1], GREEN)
    if current_player == 1:
        draw_circle(screen, x, y, RED)
    else:
        draw_circle(screen, x, y, BLUE)

def switch_player(current_player):
    if current_player == 1:
        return 2
    return 1

# Updates which player's turn it is by coloring over the old text and updating with new text
def adjust_player(screen, current_player):
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render('Current Player: ' + str(current_player), True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (255, 550)
    screen.blit(text, text_rect)
    nxt = switch_player(current_player)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render('Current Player: ' + str(nxt), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (255, 550)
    screen.blit(text, text_rect)

# Goes through all of the pieces of the board and updates the pygame screen. This function is used
# at the beginning of a player's turn to receives updates from the previous player's turn
def update_screen(screen, board, player):
    adjust_player(screen, player)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                draw_circle(screen, i, j, RED)
            elif board[i][j] == 2:
                draw_circle(screen, i, j, BLUE)
            else:
                draw_circle(screen, i, j, GREEN)

# Checks if the enemies pieces are between two of the current player's pieces in a given row
def check_row_captures(screen, board, x_pos, player):
    row = board[x_pos]
    capture_num = switch_player(player)
    capture_pos = []
    for i in range(len(row)):
        if row[i] == player:
            capture_pos.append(i)
    if len(capture_pos) > 1:
        upper = 1
        while upper < len(capture_pos):
            val = True
            first = capture_pos[upper-1]
            sec = capture_pos[upper]
            if first == sec - 1:
                val = False
            for i in range(first + 1, sec):
                if row[i] != capture_num:
                    val = False
                    break
            if val:
                for i in range(first + 1, sec):
                    board[x_pos][i] = 0
                    draw_circle(screen, x_pos, i, GREEN)
                return
            upper += 1

# Checks if the enemies pieces are between two of the current player's pieces in a given column
def check_column_captures(screen, board, y_pos, player):
    col = []
    for i in range(len(board[0])):
        col.append(board[i][y_pos])
    capture_num = switch_player(player)
    capture_pos = []
    for i in range(len(col)):
        if col[i] == player:
            capture_pos.append(i)
    if len(capture_pos) > 1:
        upper = 1
        while upper < len(capture_pos):
            val = True
            first = capture_pos[upper - 1]
            sec = capture_pos[upper]
            if first == sec - 1:
                val = False
            for i in range(first + 1, sec):
                if col[i] != capture_num:
                    val = False
                    break
            if val:
                for i in range(first + 1, sec):
                    board[i][y_pos] = 0
                    draw_circle(screen, i, y_pos, GREEN)
                return
            upper += 1

# When a player makes a move this function checks if that resulted in any pieces getting captures
def check_captures(screen, board, x_pos, y_pos, player):
    check_row_captures(screen, board, x_pos, player)
    check_column_captures(screen, board, y_pos, player)

