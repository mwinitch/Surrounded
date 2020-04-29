import socket
import pickle
import pygame
import game
import sys
import helper
import threading
from socket import error

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


PORT = 6025
SERVER = socket.gethostbyname(socket.gethostname())
print("Server Address: {}".format(SERVER))
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()
print("Server is looking for connections...")

conn, addr = server.accept()
print("Connection from {}".format(addr))

pygame.init()
pygame.display.set_caption("Player 1")
playing = True
last_click = None  # Tuple of the board coordinates of the piece you have selected (if there is one)
moving = False  # True when you have selected your own piece and can therefore move
current_player = 1  # This is player 1
screen, board = game.setup()
is_player_turn = True  # Means this player can make a move

def receive_data():
    global board, is_player_turn, playing
    while True:
        try:
            board = pickle.loads(conn.recv(4096))
            helper.update_screen(screen, board, 2)
            is_player_turn = True
        # The client has terminated the game
        except error:
            playing = False

# This thread will be responsible for checking if the client has sent data indicating they finished their turn
thread = threading.Thread(target=receive_data)
thread.daemon = True
thread.start()

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Checks if it's the current player's turn and they clicked
        if is_player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            # x and y must be flipped to accommodate the array board
            x_pos = event.pos[1] // 51
            y_pos = event.pos[0] // 51

            # This checks that a valid position was clicked
            if x_pos < 10:
                # If the player clicked on one of their own pieces but then clicks on a different one
                if last_click and helper.valid_pos(board, x_pos, y_pos, current_player):
                    helper.draw_outline(screen, last_click[0], last_click[1], BLACK)
                    helper.draw_outline(screen, x_pos, y_pos, YELLOW)
                    last_click = (x_pos, y_pos)

                # If you have selected a piece and moved it
                elif moving and helper.valid_move(board, last_click, x_pos, y_pos):
                    helper.make_movement(screen, board, last_click, x_pos, y_pos, current_player)
                    helper.check_captures(screen, board, x_pos, y_pos, current_player)
                    last_click = None
                    moving = False
                    helper.adjust_player(screen, current_player)
                    pygame.display.flip()
                    conn.send(pickle.dumps(board))
                    is_player_turn = False

                # You have clicked on your own piece
                elif helper.valid_pos(board, x_pos, y_pos, current_player):
                    helper.draw_outline(screen, x_pos, y_pos, YELLOW)
                    last_click = (x_pos, y_pos)
                    moving = True

    pygame.display.flip()

conn.close()
pygame.quit()