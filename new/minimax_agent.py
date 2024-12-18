import random
from game import winning_move, score_position


# minimax class with alpha beta pruning

class MinimaxAgent:
    # default depth of 5, but can be changed
    def __init__(self,game_setting, color, depth=5, name="Minimax"):
        self.ROW_COUNT = game_setting[0]
        self.COLUMN_COUNT = game_setting[1]
        self.depth = depth
        self.color = color
        self.WINDOW_LENGTH = game_setting[2]
        if name == "Minimax":
            self.name= name + " " + str(depth)
        else:
            self.name = name
    

    # find all valid locations
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if board[self.ROW_COUNT-1][col] == 0:
                valid_locations.append(col)
        return valid_locations
    
    # Check if its a winning move or if the board is full ( in that case we can stop the search)
    def is_terminal_node(self, board):
        p1 = winning_move(board,1)
        p2 = winning_move(board,2)
        d = len(self.get_valid_locations(board)) == 0
        if p1 or p2 or d:
            return True
        return False
    # the main minimax logic. Lets look through it
    # I think it alternates between maximizingPlayer and else, until alpha and beta are equal.
    def minimax(self, board, depth, alpha, beta, maximizingPlayer, piece):
        opp_piece = 1 if piece == 2 else 2
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            # if its a end node, check who won
            if is_terminal:
                if winning_move(board, piece):
                    return (None, 1000000 * pow(10,depth))
                elif winning_move(board, opp_piece):
                    return (None, -1000000 * pow(10,depth))
                else:
                    return (None, 0)
            else:
                return (None, score_position(board, piece))

        if maximizingPlayer:
            value = float('-inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, piece)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False, piece)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = float('inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, opp_piece)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True, piece)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    # find a open_row to place the piece vertically
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    # this winning move is used by the main minimax algorrithm with self.winning_move()
    # I think this is duplicated in is_terminal_node but its not a big issue since this one uses self

    # find_move
    #the main function
    def find_move(self, board, piece):
        col, _ = self.minimax(board, self.depth, float('-inf'), float('inf'), True, piece)
        return col