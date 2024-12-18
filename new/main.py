# main.py
from player_agent import PlayerAgent
from mimimax_agent import MinimaxAgent
from random_agent import RandomAgent
from q import Qlearning
from game import set_game_setting, start_game

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)


ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4
WAIT_TIME = 1000
game_setting =(ROW_COUNT, COLUMN_COUNT, WIN_COUNT, WAIT_TIME)


# main program
if __name__ == "__main__":
    set_game_setting(game_setting)
    mini1 = MinimaxAgent(game_setting, BLUE, 1, "Mini")
    mini2 = MinimaxAgent(game_setting, YELLOW, 2, "Mini")
    mini3 = MinimaxAgent(game_setting, ORANGE, 3, "Mini")
    mini4 = MinimaxAgent(game_setting, PURPLE, 4, "Mini")
    mini5 = MinimaxAgent(game_setting, CYAN, 5, "Mini")
    qlrn = Qlearning(game_setting, WHITE)
    qlrn_w_helper = Qlearning(game_setting, PINK, helper=True)
    rnd = RandomAgent(game_setting, RED)
    user = PlayerAgent(GREEN)
  
    winner = start_game(user, rnd, True)