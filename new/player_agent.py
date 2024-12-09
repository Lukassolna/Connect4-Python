import math
from game import SQUARESIZE
#Player controlled class
class PlayerAgent:
    def __init__(self, color):
        self.name="Player"
        self.color = color
    
    def get_move(self, board, event):
        posx = event.pos[0]
        col = int(math.floor(posx/SQUARESIZE))
        return col
    def find_move(self, board, piece):
        return None  # Wait for mouse input