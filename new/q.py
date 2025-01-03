import numpy as np
import pickle
import sys
from game import winning_move, score_position, start_game
from minimax_agent import MinimaxAgent

class QlearningAgent:
    def __init__(self, game_settings,color, model = None, helper = False):
        self.helper = MinimaxAgent(game_settings, color, 5)
        self.use_helper = helper
        self.total_states_in_q_table = 0
        self.name = "Mr.Q"
        self.ROW_COUNT = game_settings[0] 
        self.COLUMN_COUNT = game_settings[1]
        self.WINDOW_LENGTH = game_settings[2]
        self.color = color
        self.alpha = 0.1
        self.gamma = 0.9
        self.initial_epsilon = 1  # Starting epsilon value
        self.epsilon = self.initial_epsilon  # Current epsilon value
        self.epsilon_decay = 0.999999  # Decay rate
        self.q_table = {}
        if model:
            model += ".pkl"
            self.load(model)
    def decay_epsilon(self):
        """Apply decay to epsilon after each iteration"""
        self.epsilon *= self.epsilon_decay
    def print_qtable_state(self, num_states=5):
        """Print grid and Q-values for first n states"""
        for i, (key, actions) in enumerate(list(self.q_table.items())[:num_states]):
            print(f"\nState {i}:")
            print(self.key_to_grid(key))
            print("Q-values:", actions)
    def key_to_grid(self, key):
        # Split turn information if present
        if '_' in key:
            grid_str = key.split('_')[0]
        else:
            grid_str = key
            
        # Convert string to integers
        cells = [int(char) for char in grid_str]
        
        # Reshape into 6x7 grid
        return np.array(cells).reshape(self.ROW_COUNT, self.COLUMN_COUNT)

    def save(self, filename):
        print("Saving the trained model, please wait...")
        try:
            # Convert all dictionary keys to strings before saving
            serializable_q_table = {}
            for state, actions in self.q_table.items():
                if isinstance(state, tuple):
                    # If we still have any tuple states, convert them ( should never happen but checking just in case)
                    grid, is_my_turn = state
                    state_key = self.grid_to_key(grid, is_my_turn)
                else:
                    # If it already is a string, use it as is
                    state_key = state
                serializable_q_table[state_key] = actions
            
            with open(filename, 'wb') as f:
                pickle.dump({
                    'q_table': serializable_q_table,
                    'epsilon': self.epsilon,
                    'total_states': len(serializable_q_table)
                }, f)
            
            print(f"Model saved successfully!")
            print(f"Number of states in Q-table: {len(serializable_q_table)}")
            print(f"Q-table size: {sys.getsizeof(serializable_q_table)/(1024*1024):.2f} MB")
        except Exception as e:
            print(f"Error saving model: {e}")

    def load(self, filename):
        print("Loading the model, please wait...")
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.q_table = data['q_table']
                self.epsilon = data['epsilon']
            print("Model loaded successfully!")
            print(f"Loaded {len(self.q_table)} states")
            print(f"Current epsilon: {self.epsilon}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.q_table = {}  # Reset to empty if load fails


     # find a open_row to place the piece vertically
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if board[self.ROW_COUNT-1][col] == 0:
                valid_locations.append(col)
        return valid_locations



    
    

    def grid_to_key(self, grid, is_my_turn):
        # Convert numpy array to a string representation
        # Each cell is converted to a character: '0' for empty, '1' for player 1, '2' for player 2
        state_str = ''.join(str(int(cell)) for row in grid for cell in row)
        return f"{state_str}_{int(is_my_turn)}"
    

    def update_after_opponent_move(self, board, opponent_won, piece):

        if hasattr(self, 'last_state') and hasattr(self, 'last_action'):
    
            reward = -1 if opponent_won else score_position(board, piece)
            
            next_state = self.grid_to_key(board, True)  # True because it will be our turn again
            #print(next_state)
            if next_state not in self.q_table:
                self.q_table[next_state] = {col: 0.0 for col in range(self.COLUMN_COUNT)}
            
            
            self.q_table[self.last_state][self.last_action] += self.alpha * (
                reward + self.gamma * max(self.q_table[next_state].values()) 
                - self.q_table[self.last_state][self.last_action]
            )
    
    def find_move(self, board, piece):
        opp_piece = 1 if piece == 2 else 2  # This is correct
        self.update_after_opponent_move(board, winning_move(board,opp_piece), piece)
        #if winning_move(board,opp_piece):
         #   return
        grid = board
        state = self.grid_to_key(grid, True)

        #print("\nCurrent state:")
        #print(np.flip(self.key_to_grid(state), axis=0))
        #print("Q-values:", self.q_table.get(state, "State not in Q-table"))
        
      
        if state not in self.q_table:
                self.q_table[state] = {col: 0.0 for col in range(self.COLUMN_COUNT)}

     
        valid_moves = self.get_valid_locations(grid)
            # Epsilon-greedy strategy with decaying epsilon
        if np.random.random() < self.epsilon:
        # Exploration: choose random move
            column_to_place = np.random.choice(valid_moves)
        else:
        # Exploitation: choose best move
            q_values = {move: self.q_table[state][move] for move in valid_moves}
            if all(value == 0 for value in q_values.values()):
                if self.use_helper:
                    column_to_place = self.helper.find_move(board, piece)
                else:
                    column_to_place = np.random.choice(valid_moves)
            else:
                column_to_place = max(q_values, key=q_values.get)
      
        # Apply epsilon decay after making a move
        self.decay_epsilon()
        
        row = self.get_next_open_row(board, column_to_place)
        b_copy = board.copy()
        self.drop_piece(b_copy, row, column_to_place, piece)

        self.last_state = state
        self.last_action = column_to_place

        ## intermediate
        reward = score_position(b_copy, piece)
        if winning_move(b_copy, piece):
            reward = 1000
        self.q_table[state][column_to_place] += self.alpha*(reward - self.q_table[state][column_to_place])
            
        
        return column_to_place
    

    def update_after_loss(self, board):
        next_state = self.grid_to_key(board, True)  # True because it will be our turn again
        reward = -1000
            #print(next_state)
        if next_state not in self.q_table:
            self.q_table[next_state] = {col: 0.0 for col in range(self.COLUMN_COUNT)}
            
            
        self.q_table[self.last_state][self.last_action] += self.alpha * (
        reward + self.gamma * max(self.q_table[next_state].values()) 
            - self.q_table[self.last_state][self.last_action])
        
        
    def train(self, episodes, opponent, model_name=None, print_res = None,  result_path=None):
        print_frequency = episodes / 100
        opp_wins=0
        mr_q_wins=0
        draws=0 
        if result_path:
            with open("result_path", "w") as file:
                file.write(f"Game Mode: {self.WINDOW_LENGTH} in a row on {self.ROW_COUNT}x{self.COLUMN_COUNT}\n")
                file.write(f"Testing {self.name} with a={self.alpha}, g={self.gamma} against {opponent.name}\n")
        for i in range(episodes):
            winner = start_game(self,opponent, False)
            if winner == 1:
                mr_q_wins += 1
            elif winner == 10:
                draws += 1
            else:
                opp_wins += 1
        
            if i % print_frequency  == 0 and i !=0:
                if result_path:
                    with open(result_path, "a") as file:
                        file.write(f"After {i} games - {self.name}: {mr_q_wins/print_frequency:.1%}, "
                            f"{opponent.name}: {opp_wins/print_frequency:.1%}, "
                            f"Draws: {draws/print_frequency:.1%}, "
                            f"epsilon: {self.epsilon}\n")
                elif print_res:
                    print(f"After {i} games - {self.name}: {mr_q_wins/print_frequency:.1%}, "
                            f"{opponent.name}: {opp_wins/print_frequency:.1%}, "
                            f"Draws: {draws/print_frequency:.1%}, "
                            f"epsilon: {self.epsilon}")
                    opp_wins=0
                    mr_q_wins=0
                    draws=0 
                    
        if model_name:
            self.save(f'{model_name}.pkl')
