import random
import sys
from alpha_beta import Position
import alpha_beta
from connect4 import GameBoard

def random_choice(position):
    moves = position.gameboard.find_legal_columns()
    return random.choice(moves)

def compare_strategies(depth1, depth2, count, prob):
    p1_wins = 0
    p2_wins = 0

    for i in range(count):
        game_board = GameBoard()
        position = Position(game_board, False, None, 1, None)

        while not position.is_terminal:
            if random.random() >= prob:
                t_table = dict()
                if position.player == 1:
                    move = alpha_beta.alpha_beta(position, depth1, float('-inf'), float('inf'), t_table)
                else:
                    move = alpha_beta.alpha_beta(position, depth2, float('-inf'), float('inf'), t_table)
                move_to_make = move[1][1]
            else:
                move_to_make = random_choice(position)
        

            if position.player == 1:
                piece = "R"
                next_player = 2
                value = 100000000
            else:
                piece = "Y"
                next_player = 1
                value = -100000000

            inserted_coordinates = game_board.insert_piece(move_to_make, piece)


            if game_board.has_won(inserted_coordinates):
                position = Position(game_board, True, value, next_player, inserted_coordinates)
            else:
                position = Position(game_board, False, None, next_player, inserted_coordinates)

        if position.player == 2:
            #player 1 made the winning move
            p1_wins += 1 
        else:
            p2_wins += 1    
    return p1_wins / count


def test_game(count, depth1, depth2, prob):
    win_pct = compare_strategies(depth1, depth2, count, prob)
    print(win_pct)


if __name__ == '__main__':
    depth1 = int(sys.argv[1])
    depth2 = int(sys.argv[2])
    count = int(sys.argv[3]) # no. of iterations we want to run
    prob = float(sys.argv[4])# probability of random move
    test_game(count, depth1, depth2, prob)