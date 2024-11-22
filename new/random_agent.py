import random


# simple random class ( will be useful for statistics later)
class RandomAgent:
    def __init__(self):
        pass
        
    def get_move(self, board, event=None):
        # Return random column (0-6)
        return random.randint(0, 6)
    
    def find_move(self, board):
        # Alternate method name for compatibility
        return self.get_move(board)