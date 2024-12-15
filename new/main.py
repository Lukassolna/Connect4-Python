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
    mini1 = MinimaxAgent(game_setting, ORANGE, 1, "Mini")
    mini2 = MinimaxAgent(game_setting, YELLOW, 2, "Mini")
    mini3 = MinimaxAgent(game_setting, YELLOW, 3, "Mini")
    mini4 = MinimaxAgent(game_setting, YELLOW, 4, "Mini")
    qlrn = Qlearning(game_setting,WHITE)
    qlrn2 = Qlearning(game_setting,GREEN)
    rnd = RandomAgent(game_setting, RED)
    user = PlayerAgent(GREEN)
    qlrn.load("new/rnd.pkl")
    #qlrn2.load("vs_multi.pkl")
    #qlrn.epsilon = 0.9
    #qlrn.epsilon = 0
    mr_q_wins = 0
    random_wins = 0
    draws = 0
    num_games = 2000000
    #with open("vsqlrn_samea.txt", "w") as file:
    #    file.write(f"Testing qlrn a={qlrn.alpha}, g={qlrn.gamma} against qlrn2 a={qlrn2.alpha}, g={qlrn2.gamma}")
    for i in range(num_games):
        #print(i)
        winner = start_game(qlrn,rnd, True)
        if winner == 1:
            mr_q_wins += 1
        elif winner == 10:
            draws += 1
        else:
            random_wins += 1
       
        print_count = 1000
        if i % print_count  == 0 and i !=0:
            with open("vsqlrn_samea.txt", "a") as file:
                file.write(f"After {i} games - qlrn: {mr_q_wins/print_count:.1%}, "
                       f"qlrn2: {random_wins/print_count:.1%}, "
                       f"Draws: {draws/print_count:.1%}, "
                       f"epsilon: {qlrn.epsilon}\n")

            random_wins=0
            mr_q_wins=0
            draws=0 
        #if i % 100000 == 0:
        #    qlrn.save(f'qlrn.pkl')