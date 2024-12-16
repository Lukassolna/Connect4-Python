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
ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4
WAIT_TIME = 1000
game_setting =(ROW_COUNT, COLUMN_COUNT, WIN_COUNT, WAIT_TIME)


# main program
if __name__ == "__main__":
    set_game_setting(game_setting)
    mini1 = MinimaxAgent(game_setting, ORANGE, 1, "Mini") #should not use, too stupid
    mini2 = MinimaxAgent(game_setting, YELLOW, 2, "Mini")
    mini3 = MinimaxAgent(game_setting, YELLOW, 3, "Mini")
    mini4 = MinimaxAgent(game_setting, YELLOW, 4, "Mini")
    qlrn = Qlearning(game_setting,WHITE)
    qlrn.alpha = 0.9
    qlrn.gamma = 0.1
    qlrn2 = Qlearning(game_setting,GREEN)
    rnd = RandomAgent(game_setting, RED)
    user = PlayerAgent(GREEN)
    user2 = PlayerAgent(WHITE)
    #qlrn.load("new/rnd.pkl")
    #qlrn2.load("vs_multi.pkl")
    #qlrn.epsilon = 0.9
    #qlrn.epsilon = 0
    mr_q_wins = 0
    random_wins = 0
    draws = 0
    num_games = 1000001
    with open("4inarowhighalpha.txt", "w") as file:
        file.write(f"Game Mode: {WIN_COUNT} in a row on {COLUMN_COUNT}x{ROW_COUNT}\n")
        file.write(f"Testing qlrn a={qlrn.alpha}, g={qlrn.gamma} against random\n")
    for i in range(num_games):
        #print(i)
        winner = start_game(qlrn,rnd, False)
        if winner == 1:
            mr_q_wins += 1
        elif winner == 10:
            draws += 1
        else:
            random_wins += 1
       
        print_count = 10000
        if i % print_count  == 0 and i !=0:
            with open("4inarowhighalpha.txt", "a") as file:
                file.write(f"After {i} games - qlrn: {mr_q_wins/print_count:.1%}, "
                       f"mini3: {random_wins/print_count:.1%}, "
                       f"Draws: {draws/print_count:.1%}, "
                       f"epsilon: {qlrn.epsilon}\n")

            random_wins=0
            mr_q_wins=0
            draws=0 
      
    #qlrn.save(f'qlrn3inarowvsmini3.pkl')