import math

#Player controlled class
class PlayerAgent:
    def __init__(self, squaresize):
        self.name="Player"
        self.SQUARESIZE = squaresize
    
    def get_move(self, board, event):
        posx = event.pos[0]
        col = int(math.floor(posx/self.SQUARESIZE))
        return col
    def find_move(self, board):
        return None  # Wait for mouse input