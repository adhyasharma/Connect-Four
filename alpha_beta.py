from connect4 import GameBoard

class Position:
    """
    Class that keeps track of each position in the game.
    """
    def __init__(self, gameboard, is_terminal, value, player, previous_move):
        self.gameboard = gameboard 
        self.is_terminal = is_terminal 
        self.value = value 
        self.player = player
        self.previous_move = previous_move
    
    def calculate_score(self, ls):
        """
        When 3 pieces are together, score = 100. 
        When 2 pieces are connected, score = 50.
        When opponent has 3 pieces connected, score = -50. 
        When opponent has 2 pieces connected, score = -25.
        """
        score = 0
        own_piece = "R"
        other_piece = "Y"

        #checking for own pieces together in the given list
        if ls.count(own_piece) == 3 and ls.count("0") == 1:
            score += 100 
        elif ls.count(own_piece) == 2 and ls.count("0") == 2:
            score += 50
        
        #checking for opponents pieces together in the given list:
        if ls.count(other_piece) == 3 and ls.count("0") == 1:
            score -= 100
        elif ls.count(other_piece) == 2 and ls.count("0") == 2:
            score -= 50
        return score
        


    def heuristic(self):
        """
        An estimate for the value of the position. 
        Always calculated w.r.t the Red Player (player 1). 
        The Red Player always maximizes and 
        Yellow Player tries to minimize.
        """
        score = 0
        piece = "R" #always determines score for player 1. Player 2 will subsequently try to minimze it. 

        #calculating number of pieces in middle row and doubling the score 
        middle_row = self.gameboard.board[len(self.gameboard.board)//2]
        middle_row_count = middle_row.count(piece)
        score += (middle_row_count * 2)

        #calculating number of pieces in middle column and doubling the score 
        middle_col = [self.gameboard.board[i][len(self.gameboard.board[0])//2] for i in range(6)]
        middle_col_count = middle_col.count(piece)
        score += (middle_col_count * 2)

        #score horizantal windows
        for r in range(6):
            row = self.gameboard.board[r]
            for c in range(4):
                ls = row[c:c+4]
                score += self.calculate_score(ls)
        
        #score vertical windows
        for c in range(7):
            col = [self.gameboard.board[i][c] for i in range(6)]
            for r in range(3):
                ls = col[r:r+4]
                score += self.calculate_score(ls)
        
        #score diagonal type 1
        for r in range(3):
            for c in range(4):
                ls = [self.gameboard.board[r+i][c+i] for i in range(4)]
                score += self.calculate_score(ls)
        
        #score diagonal type 2
        for r in range(3):
            for c in range(4):
                ls = [self.gameboard.board[r+3-i][c+i] for i in range(4)]
                score += self.calculate_score(ls)
        
        return score
        


def alpha_beta(position, depth, alpha, beta, t_table):
    """
    Does Alpha-Beta pruning with a transposition table.
    """
    if position.gameboard.tuple_board in t_table and t_table[position.gameboard.tuple_board][2] >= depth:
        if t_table[position.gameboard.tuple_board][3] == "exact":
            return (t_table[position.gameboard.tuple_board][0], t_table[position.gameboard.tuple_board][1])
        elif t_table[position.gameboard.tuple_board][3] == "upper_bound" and t_table[position.gameboard.tuple_board][0] <= alpha:
            return (t_table[position.gameboard.tuple_board][0], t_table[position.gameboard.tuple_board][1])
        elif t_table[position.gameboard.tuple_board][3] == "lower_bound" and t_table[position.gameboard.tuple_board][0] >= beta:
            return (t_table[position.gameboard.tuple_board][0], t_table[position.gameboard.tuple_board][1])

    #check if it is a terminal position. if yes, return the value. 
    if position.is_terminal:
        return (position.value, position.previous_move)
    
    #check if depth is equal to 0. if yes, return heuristic value. 
    if depth == 0:
        return (position.heuristic(), position.previous_move)


    #player 1:
    if position.player == 1:
        a = (float('-inf'), None)
        legal_moves = position.gameboard.find_legal_columns()
        pos = 0
        while pos < len(legal_moves) and alpha < beta:
            new_board = position.gameboard.deep_copy_board()
            new_gameboard = GameBoard(new_board)
            inserted_coordinates = new_gameboard.insert_piece(legal_moves[pos], "R") #red player
            if new_gameboard.has_won(inserted_coordinates):
                next_position = Position(new_gameboard, True, 100000000, 2, inserted_coordinates)
            else:
                next_position = Position(new_gameboard, False, None, 2, inserted_coordinates)
            result = alpha_beta(next_position, depth - 1, alpha, beta, t_table)
            if result[0] > a[0]:  
                a = (result[0], inserted_coordinates)
            alpha = max(alpha, a[0])
            pos += 1
        if a[0] >= beta:
            t_table[position.gameboard.tuple_board] = [a[0], a[1], depth, "lower_bound"]
        elif a[0] <= alpha: 
            t_table[position.gameboard.tuple_board] = [a[0], a[1], depth, "upper_bound"]
        else:
            t_table[position.gameboard.tuple_board] = [a[0], a[1], depth, "exact"]
        return a
    else: #player 2:
        b = (float('inf'), None)
        legal_moves = position.gameboard.find_legal_columns()
        pos = 0
        while pos < len(legal_moves) and alpha < beta:
            new_board = position.gameboard.deep_copy_board()
            new_gameboard = GameBoard(new_board)
            inserted_coordinates = new_gameboard.insert_piece(legal_moves[pos], "Y") #yellow player
            if new_gameboard.has_won(inserted_coordinates):
                next_position = Position(new_gameboard, True, -100000000, 1, inserted_coordinates)
            else:
                next_position = Position(new_gameboard, False, None, 1, inserted_coordinates)
            result = alpha_beta(next_position, depth - 1, alpha, beta, t_table)
            if b[0] > result[0]:
                b = (result[0], inserted_coordinates)
            beta = min(beta, b[0])
            pos += 1
        if b[0] >= beta:
            t_table[position.gameboard.tuple_board] = [b[0], b[1], depth, "lower_bound"]
        elif b[0] <= alpha: 
            t_table[position.gameboard.tuple_board] = [b[0], b[1], depth, "upper_bound"]
        else:
            t_table[position.gameboard.tuple_board] = [b[0], b[1], depth, "exact"]
        return b

def accept_board():
    """
    Accepts a board from the user. 
    A Position will subsequently be created out of it.
    """
    new_board = []
    for i in range(6):
        new_row = []
        for j in range(7):
            print("Row:", i, "Column:", j, "(R/Y/0)")
            ele = input()
            new_row.append(ele)
        new_board.append(new_row)
    return new_board

if __name__ == "__main__":
    #main
    print("Looking for the next best move from your current non-terminal position?")
    print("I can help!")
    print("Enter what the game board looks like, entering values from LEFT to RIGHT and TOP to BOTTOM of the board.")
    print("Here is an example:\n")
    board = [["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["R","0","0","0","0","0","0"], ["R", "Y", "R", "0","0","0","0"], ["Y", "Y", "R", "R", "Y", "Y", "R"], ["R", "Y", "R", "Y", "R", "Y", "R"]]
    sample_game_board = GameBoard(board)
    sample_game_board.print_sample_board()
    print("\n")
    print("Make sure to use the CORRECT FORMAT - a piece CANNOT be above empty space!")
    print("The pieces are represented by R and Y. Empty spaces are represented by 0.")
    print("Remember that players alternate, and so, should have either an equal number of pieces or differ by one.")
    new_board = accept_board()
    game_board = GameBoard(new_board)
    game_board.print_board()
    print("Which player goes next? (R/Y)")
    print("Note: Please remember that in your board, both players should have the same number of pieces or differ by one, with the player going next having one piece less.")
    player = input()
    if player == "R":
        position = Position(game_board, False, None, 1, None)
    else:
        position = Position(game_board, False, None, 2, None)
    t_table = dict()
    final_answer = alpha_beta(position, 1000, float('-inf'), float('inf'), t_table)
    print("The best move is:", final_answer[1])
    print("Session over!")
