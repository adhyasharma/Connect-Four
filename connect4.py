class GameBoard:
    def __init__(self, board = None):
        if board == None:
            self.board = [["0" for i in range(7)] for j in range(6)]
        else:
            self.board = board
        self.tuple_board = self.convert_to_tuple()

    
    def print_board(self):
        """
        Displays the board.
        """
        for row in self.board:
            print("+--+--+--+--+--+--+--+")
            row_to_print = []
            for element in row:
                row_to_print.append("| ")
                row_to_print.append(element)
            for ele in row_to_print:
                print(ele, end = "")
            print("|")
        print("+--+--+--+--+--+--+--+")

    def print_sample_board(self):
        """
        Prints sample board for user.
        """
        print("* Top Row Left")
        for row in self.board:
            print("+--+--+--+--+--+--+--+")
            row_to_print = []
            for element in row:
                row_to_print.append("| ")
                row_to_print.append(element)
            for ele in row_to_print:
                print(ele, end = "")
            print("|")
        print("+--+--+--+--+--+--+--+")
        print("                     ^ Bottom Row Right")
    

    def convert_to_tuple(self):
        """
        Converts board to tuple form so that it can be used 
        for hashing in the transposition table.
        """
        new_board = self.deep_copy_board()
        for i in range(len(new_board)):
            new_board[i] = tuple(new_board[i])
        new_board = tuple(new_board)
        return new_board

        
    def find_legal_columns(self):
        """
        Finds all the columns where a piece can be entered.
        """
        legal_columns = []
        for index, ele in enumerate(self.board[0]):
            if ele == "0":
                legal_columns.append(index)
        return legal_columns 
    
    def insert_piece(self, column_index, piece):
        """
        Inserts a piece into the board.
        """
        for row_index in range(5, -1, -1):
            row = self.board[row_index]
            if row[column_index] == "0":
                row[column_index] = piece
                return (row_index, column_index)
        return (-1, -1) #if it failed for some reason
    
    def horizantal_line(self, x, y, piece):
        """
        Checks if winning move by checking for four 
        in horizantal line.
        """
        count = 1 #1 is the piece itself
        #check left:
        for col in range(y - 1, -1, -1):
            if self.board[x][col] == piece:
                count += 1 
            else:
                break
        #check right:
        for col in range(y + 1, len(self.board[x])):
            if self.board[x][col] == piece:
                count += 1 
            else:
                break 
        if count >= 4:
            return True 
        return False 
    
    def vertical_line(self, x, y, piece):
        """
        Checks if winning move by checking 
        for four in vertical line.
        """
        count = 1 #1 is the piece 
        #check below:
        for row in range(x + 1, 6):
            if self.board[row][y] == piece:
                count += 1 
            else:
                break 
        if count >= 4:
            return True 
        return False 

    def diagonal_line(self, x, y, piece):
        """
        Checks if winning move by checking for 
        four in diagonal line.
        """
        #check one diagonal:
        count_one = 1
        for c_x, c_y in [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5)]:
            new_x, new_y = c_x + x, c_y + y 
            if new_x < 0 or new_y > 6:
                break 
            if self.board[new_x][new_y] == piece:
                count_one += 1 
            else:
                break 
        # print(count_one)
        for c_x, c_y in [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5)]:
            new_x, new_y = c_x + x, c_y + y
            if new_x > 5 or new_y < 0:
                break 
            if self.board[new_x][new_y] == piece:
                count_one += 1 
            else:
                break 
        # print(count_one)
        if count_one >= 4:
            return True 
        
        #check other diagonal:
        count_two = 1 
        for c_x, c_y in [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5)]:
            new_x, new_y = c_x + x, c_y + y 
            if new_x < 0 or new_y < 0:
                break 
            if self.board[new_x][new_y] == piece:
                count_two += 1 
            else:
                break
        # print(count_two)
        for c_x, c_y in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]:
            new_x, new_y = c_x + x, c_y + y
            if new_x > 5 or new_y > 6:
                break 
            if self.board[new_x][new_y] == piece:
                count_two += 1 
            else:
                break
        if count_two >= 4:
            return True
        return False  

    def has_won(self, position):
        """
        Returns true if move is a winning 
        move. Else returns false.
        """
        x, y = position[0], position[1]
        piece = self.board[x][y]
        if self.horizantal_line(x, y, piece) or self.vertical_line(x, y, piece) or self.diagonal_line(x, y, piece):
            return True 
        return False 

    
    def deep_copy_board(self):
        """
        Deep copies the board.
        """
        new_board = []
        for row in self.board:
            new_row = []
            for ele in row:
                new_row.append(ele)
            new_board.append(new_row)
        return new_board

if __name__ == "__main__":
    while True:
        print("Do you want to play a game of Connect-4? (Type \"y\" to play and \"n\" to exit)")
        answer = input()
        if answer == "y":
            print("Let's play!!!")
            print("Player 1 is the Red player, and Player 2 is the Blue player.")
            game_board = GameBoard()
            while True:
                game_board.print_board()
                print("Red player's turn:")
                legal_columns = game_board.find_legal_columns()
                print("Possible columns to drop a piece in", legal_columns)
                print("Pick a column number to insert your piece:")
                column = int(input())
                while column not in legal_columns:
                    print("Not a valid move - try again")
                    column = int(input())
                position_inserted = game_board.insert_piece(column, "R")
                if game_board.has_won(position_inserted):
                    game_board.print_board()
                    print("Red won!!!")
                    break
                game_board.print_board()
                print("Yellow player's turn:")
                legal_columns = game_board.find_legal_columns()
                print("Possible columns to drop a piece in", legal_columns)
                print("Pick a column number to insert your piece:")
                column = int(input())
                while column not in legal_columns:
                    print("Not a valid move - try again")
                    column = int(input())
                position_inserted = game_board.insert_piece(column, "Y")
                if game_board.has_won(position_inserted):
                    game_board.print_board()
                    print("Yellow won!!!")
                    break 
        else:
            print("Session over!")
            break 
