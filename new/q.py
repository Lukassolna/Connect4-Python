import numpy as np
import pickle
import sys
class Qlearning:
    def __init__(self,piece):
        
        self.total_states_in_q_table = 0
        self.piece = piece
        self.name = "Mr.Q"
        self.COLUMN_COUNT = 7
        self.ROW_COUNT = 6 
        self.WINDOW_LENGTH = 4
        self.alpha = 0.5  
        self.gamma = 0.5  
        self.epsilon = 0.05 # 5% random choises
        self.q_table = {}
    def save(self, filename='C:/Users/lukas/Downloads/q_agent.pkl'):
        print("saving the trained model please wait")
        print(f"Number of states in Q-table: {len(self.q_table)}")
        print(f"Q-table size: {sys.getsizeof(self.q_table)/(1024*1024):.2f} MB")
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    # loads a trained model
    def load(self, filename='C:/Users/lukas/Downloads/q_agent.pkl'):
        print("loading the model please wait")
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
            print("Model loaded succesfully")

     # find a open_row to place the piece vertically
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 10 #prev value 4

        return score

    # give a score for the current position by looking through all possible directions
    def score_position(self, board, piece):
        score = 0

        # Center column gets extra reward
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(self.COLUMN_COUNT-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(self.ROW_COUNT-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Positive diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Negative diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score
        

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if board[self.ROW_COUNT-1][col] == 0:
                valid_locations.append(col)
        return valid_locations

    def winning_move(self, board, piece):
        # Horizontal
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and \
                   board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Vertical
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and \
                   board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Diagonals
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and \
                   board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and \
                   board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
        return False


    

    def grid_to_key(self, grid, is_my_turn):
        # Include whose turn it is in the state representation
        return (tuple(map(tuple, grid)), is_my_turn)
    
    def find_move(self, board, piece):
        grid = board
        state = self.grid_to_key(grid, True)
        
        if state not in self.q_table:
            self.q_table[state] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}

        valid_moves = self.get_valid_locations(grid)
        
        # Epsilon-greedy strategy
        if np.random.random() < self.epsilon:
            # Exploration: choose random move
            column_to_place = np.random.choice(valid_moves)
        else:
            # Exploitation: choose best move
            q_values = {move: self.q_table[state][move] for move in valid_moves}
            if all(value == 0 for value in q_values.values()):
                column_to_place = np.random.choice(valid_moves)
            else:
                column_to_place = max(q_values, key=q_values.get)
        row = self.get_next_open_row(board, column_to_place)
        b_copy = board.copy()
        self.drop_piece(b_copy, row, column_to_place, piece)

        self.last_state = state
        self.last_action = column_to_place

        next_state = self.grid_to_key(b_copy, False)  # False because it will be opponents turn
        
        if next_state not in self.q_table:
            self.q_table[next_state] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}

        next_max_q = min(self.q_table[next_state].values())
        reward = self.score_position(b_copy, piece)
        if self.winning_move(b_copy, piece):
            reward = 1000
            
        self.q_table[state][column_to_place] += self.alpha * (reward + self.gamma * next_max_q - self.q_table[state][column_to_place])
        
        return column_to_place
    
    def update_after_opponent_move(self, board, opponent_won, opponent_piece):
        if hasattr(self, 'last_state') and hasattr(self, 'last_action'):
            reward = -1000 if opponent_won else self.score_position(board, self.piece)
            
            next_state = self.grid_to_key(board, True)  # True because it will be our turn again
            if next_state not in self.q_table:
                self.q_table[next_state] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
            
            self.q_table[self.last_state][self.last_action] += self.alpha * (
                reward + self.gamma * max(self.q_table[next_state].values()) 
                - self.q_table[self.last_state][self.last_action]
            )