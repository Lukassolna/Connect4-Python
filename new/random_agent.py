import random
from game import is_valid_location

# simple random class ( will be useful for statistics later)
class RandomAgent:
    def __init__(self, game_setting,color):
        self.name="Random"
        self.cols = game_setting[1]
        self.rows = game_setting[0]
        self.color = color
        
    def get_move(self, board, event=None):
        # Return random column (0-6)
        col= random.randint(0, self.cols-1)
        while not is_valid_location(board,col, self.rows): 
            col =random.randint(0, self.cols-1) 

        return col
    
    def find_move(self, board, piece):
        # Alternate method name for compatibility
        return self.get_move(board)