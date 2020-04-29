# Surrounded

Welcome to Surrounded! This is a two player game created using the pygame module. The game is played on a local network through a TCP socket. On the board each player starts out with eight circular pieces. The objective of the game is to capture your enemies pieces until they only have at most one left. 

On each turn, a player can move any one of their pieces up to two spots in any direction, including diagonally. They can not land on a space occupied by another piece regardless of whose it is, but can move over other pieces. To capture enemy pieces a player must surround a row or column of enemy pieces from both sides. 

Pretend the following array is a row of the board where 1's represent one player's pieces and 2's represent the other player's pieces.

`[0, 1, 2, 2, 2, 1, 0, 0]`

Because the 2's are surrounded on both sides by the 1's they would all be captured and removed from the board. You can capture any number of pieces by surrounding them. You can also capture pieces by surrounding them vertically. A player can only move one piece a turn and must make a move each turn. 
## Setup

To play the game one person must run `server.py` and then the other play must run `client.py`. It is important that the server is running before the client tries to connect to it. The client will try to find the server on the current local network. **In `client.py` you will have to change the `SERVER` variable (located near the top of the file) to match what the current local network IP address is. When you run `server.py` it will print the current local IP address to the console.**

The connection may also not be working because a firewall on one of the player's computers may be stopping the TCP socket code from working. In that case you will have to enable your firewall to let this program run. 

Once the client has connected to the server, the game will begin and the pygame window will launch for both people. Whoever is running the server is player 1 and they have the red pieces. The client is player 2 and has the blue pieces. Player 1 goes first. If either player exits the game and closes the pygame window, the pygame window will also close for the other player.

## How the Game Works

This program uses the pygame module to create and help run the game. Both the server and client call on `game.py` to create the game. This file creates what is referred to as the `board` variable. The `board` variable is a python list of lists that represents the board as a 2D array. Each position in the array says if it is occupied by either player or is empty. This list is responsible for checking current positions, if moves are valid, and if pieces were captured. It is also sent over the network so the other player can update their screen and know the current state of the game.

In addition, `game.py` also creates the `screen` variable which holds sets up the initial visuals for the game (the ten by ten grid of green squares with red and blue pieces). When a player clicks on the pygame window the coordinates are converted into what cell it would correspond to in the `board` array. This allows the pygame visuals to interact with the board that contains the actual game information. 

The `screen` is used during the game to update what is displayed on the pygame window. The pygame window knows what updates to draw often by looking at the `board` variable. The file `helper.py` contains all of the functions that help to update the game by changing what the `screen` shows and what values are in the `board`. 

## How the Connection Works

This game uses a TCP socket to form a connection between the server and client. When the connection is made a new thread is made in `server.py` and `client.py`. This thread is a daemon thread and keeps checking if something has been received over through the socket. This allows one thread to be focused on the game while the other thread can check to receive information over the socket. 

When a player complete's their turn, their own screen will update (showing where the piece moved and pieces that got captured and moved to the board). Then, the `board` variable will be serialized with the pickle module. That serialized variable is then sent through the TCP socket. The other player has their thread which is looking for information that is sent. When the serialized object is received, pickle is used to deserialize the object and get the original board back. 

Then that board is used to update the the pygame window and update the current state of the game. In addition, a boolean variable is changed so that now the player can make a move.  