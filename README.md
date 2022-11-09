# Connect-Four

### Summary:
I have designed an alpha-beta pruning agent (that uses a transposition table) for the game Connect-4 that outputs the best move to make from a certain non-terminal position. I offer 2 modes: one mode allows 2 human players to play against each other (no alpha-beta agent involved) and the other mode returns the best move given a certain position in the game. I also offer a mechanism to compare performance for different search depths in my test script.

### Results:
1. Alpha-Beta agent with transposition table searching to depth 20 wins against alpha-beta agent with transposition table searching to depth 5 80% of the time in 
10 games, when moves are random with 10% probability. 
2. Alpha-Beta agent with transposition table searching to depth 15 wins against alpha-beta agent with transposition table searching to depth 3 60% of the time in 
10 games, when moves are random with 10% probability. 
3. Alpha-Beta agent with transposition table searching to depth 20 wins against alpha-beta agent with transposition table searching to depth 1 60% of the time in 
5 games, when moves are random with 30% probability. 

### Description of the game:
Connect-4 is a 2-player, turn-based game. The Red Player ("R") starts off by placing their piece in one of the available spaces. Next, it 
is the Yellow Player's turn ("Y"). The goal of each player is to get 4 of their pieces in a row, either horizantally, vertically, or diagonally. 
The player to achieve this first wins the game. 


### How to run code:
1. Running test script: Type in 'python3 test_connect4.py <depth1> <depth2> <no. of games> <probability of random move>' into the terminal. 
Not that probability of random move should be a decimal. The result will be the percentage of times 
alpha-beta agent searching till depth1 wins against agent searching till depth2, when moves are random with probability given. 

2. Mode 1 (game between 2 human players without alpha-beta pruning agent):
Type 'python3 connect4.py' into terminal. Follow the instructions that pop up to play the game. Type "y" to play and "n" to exit. 

3. Mode 2 (get best move from your current non-terminal position):
Type 'python3 alpha_beta.py' into terminal. Instructions will be displayed in the terminal. 
Enter what the game board currently looks like. This is done by entering what piece is at a position in the board from left to right
going top to bottom. The piece can be "R", "Y", or "0" indicating empty. Next, enter which player ("R" or "Y") must move next. 
The program will output the best move to make. 
