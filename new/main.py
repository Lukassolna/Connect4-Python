# main.py
from player_agent import PlayerAgent
from mimimax_agent import MinimaxAgent
from random_agent import RandomAgent
from q import Qlearning
from game import set_game_setting, start_game

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
ORANGE = (255,100,50)
WHITE = (255,255,255)
ROW_COUNT = 5
COLUMN_COUNT = 6
WIN_COUNT = 4
WAIT_TIME = 1000
game_setting =(ROW_COUNT, COLUMN_COUNT, WIN_COUNT, WAIT_TIME)


# main program
if __name__ == "__main__":
    set_game_setting(game_setting)
    mini1 = MinimaxAgent(game_setting, ORANGE, 3, "Mini")
    mini2 = MinimaxAgent(game_setting, YELLOW, 5, "Mini")
    qlrn = Qlearning(game_setting,WHITE)
    qlrn2 = Qlearning(game_setting,GREEN)
    rnd = RandomAgent(game_setting, RED)
    user = PlayerAgent(GREEN)
    qlrn.load("withhelper_vs_random.pkl")
    #qlrn2.load("vs_multi.pkl")
    #qlrn.epsilon = 0.9
    mr_q_wins = 0
    random_wins = 0
    draws = 0
    num_games = 100000
    for i in range(num_games):
        #print(i)
        winner = start_game(qlrn,rnd, True)
        if winner == 1:
            mr_q_wins += 1
        elif winner == 10:
            draws += 1
        else:
            random_wins += 1
       
        if i % 1000  == 0 and i !=0:
            print(f"After {i} games - Mr.Q: {mr_q_wins/(1000):.1%}, Random: {random_wins/(1000):.1%}, Draws: {draws/(10000):.1%} , epsilon {qlrn.epsilon}")
            random_wins=0
            mr_q_wins=0
            draws=0 
        if i % 1000 == 0:
            qlrn.save(f'withhelper_vs_random.pkl')