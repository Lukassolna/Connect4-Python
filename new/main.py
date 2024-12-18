# main.py
from player_agent import PlayerAgent
from minimax_agent import MinimaxAgent
from random_agent import RandomAgent
from q import QlearningAgent
from game import set_game_setting, start_game

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (125, 125, 125)
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
    mini1 = MinimaxAgent(game_setting, GREY, 1, "myname")
    mini2 = MinimaxAgent(game_setting, YELLOW, 2)
    mini3 = MinimaxAgent(game_setting, ORANGE, 3)
    mini4 = MinimaxAgent(game_setting, PURPLE, 4)
    mini5 = MinimaxAgent(game_setting, CYAN, 5)
    qlrn = QlearningAgent(game_setting, WHITE)
    qlrn_w_helper = QlearningAgent(game_setting, PINK, helper=True)
    rnd = RandomAgent(game_setting, RED)
    user = PlayerAgent(GREEN)
  
    winner = start_game(user, mini2, True)
  
    model_path = "a"
    qlrn.train(1000, rnd, model_path, print_res=True)
  
    start_game(qlrn, rnd, True)