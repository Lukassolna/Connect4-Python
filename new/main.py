# main.py
from player_agent import PlayerAgent
from mimimax_agent import MinimaxAgent
from random_agent import RandomAgent
from game import set_game_setting, start_game

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
ORANGE = (255,100,50)
ROW_COUNT = 5
COLUMN_COUNT = 8
WIN_COUNT = 4
game_setting =(ROW_COUNT, COLUMN_COUNT, WIN_COUNT)


# main program
if __name__ == "__main__":
    set_game_setting(game_setting)
    mini1 = MinimaxAgent(game_setting, ORANGE, 3, "Mini")
    mini2 = MinimaxAgent(game_setting, YELLOW, 5, "Mini")
    rnd = RandomAgent(game_setting, RED)
    user = PlayerAgent(GREEN)
    wins = []
    for i in range(10):
        wins.append(start_game(user, mini2, True))

    wins.sort()