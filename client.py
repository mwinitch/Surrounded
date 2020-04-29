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

# Here is the SERVER variable you change to connect to the server on your local network
SERVER = '10.0.1.156'
PORT = 6025
ADDR = (SERVER, PORT)


pygame.init()
pygame.display.set_caption("Player 2")
screen, board = game.setup()
playing = True
last_click = None  # Tuple of the board coordinates of the piece you have selected (if there is one)
moving = False  # True when you have selected your own piece and can therefore move
pygame.display.flip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
is_player_turn = False  # Means this player can make a move
current_player = 2  # This is player 2

def receive_data():
    global board, is_player_turn, playing
    while True:
        try:
            board = pickle.loads(client.recv(4096))
            helper.update_screen(screen, board, 1)
            is_player_turn = True
        # The server has terminated the game
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

        # x and y must be flipped to accommodate the array board
        if is_player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = event.pos[1] // 51
            y_pos = event.pos[0] // 51
            # print("x: {}   y: {}".format(x_pos, y_pos))
            # This checks that a valid position was clicked --MAY NEED TO CHANGE IF A BUTTON IS ADDED --
            if x_pos < 10:
                if last_click and helper.valid_pos(board, x_pos, y_pos, current_player):
                    helper.draw_outline(screen, last_click[0], last_click[1], BLACK)
                    helper.draw_outline(screen, x_pos, y_pos, YELLOW)
                    last_click = (x_pos, y_pos)

                elif moving and helper.valid_move(board, last_click, x_pos, y_pos):
                    helper.make_movement(screen, board, last_click, x_pos, y_pos, current_player)
                    helper.check_captures(screen, board, x_pos, y_pos, current_player)
                    last_click = None
                    moving = False
                    helper.adjust_player(screen, current_player)
                    pygame.display.flip()
                    # current_player = helper.switch_player(current_player)
                    client.sendall(pickle.dumps(board))
                    is_player_turn = False

                # You have clicked on your own piece
                elif helper.valid_pos(board, x_pos, y_pos, current_player):
                    helper.draw_outline(screen, x_pos, y_pos, YELLOW)
                    last_click = (x_pos, y_pos)
                    moving = True

    pygame.display.flip()

client.close()
pygame.quit()

