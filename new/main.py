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


def train_model(episodes, q_agent, opponent, model_name=None, print_res = None,  result_path=None):
    print_frequency = episodes / 100
    opp_wins=0
    mr_q_wins=0
    draws=0 
    if result_path:
        with open("result_path", "w") as file:
            file.write(f"Game Mode: {WIN_COUNT} in a row on {ROW_COUNT}x{COLUMN_COUNT}\n")
            file.write(f"Testing {q_agent.name} with a={q_agent.alpha}, g={q_agent.gamma} against {opponent.name}\n")
    for i in range(episodes):
        winner = start_game(q_agent,opponent, False)
        if winner == 1:
            mr_q_wins += 1
        elif winner == 10:
            draws += 1
        else:
            opp_wins += 1
       
        if i % print_frequency  == 0 and i !=0:
            if result_path:
                with open(result_path, "a") as file:
                    file.write(f"After {i} games - {q_agent.name}: {mr_q_wins/print_frequency:.1%}, "
                           f"{opponent.name}: {opp_wins/print_frequency:.1%}, "
                           f"Draws: {draws/print_frequency:.1%}, "
                           f"epsilon: {q_agent.epsilon}\n")
            elif print_res:
                print(f"After {i} games - {q_agent.name}: {mr_q_wins/print_frequency:.1%}, "
                           f"{opponent.name}: {opp_wins/print_frequency:.1%}, "
                           f"Draws: {draws/print_frequency:.1%}, "
                           f"epsilon: {q_agent.epsilon}")
                opp_wins=0
                mr_q_wins=0
                draws=0 
                
    if model_name:
        qlrn.save(f'{model_name}.pkl')


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
    train_model(1000, qlrn, rnd, model_path, print_res=True)
  
    trained_agent=QlearningAgent(game_setting, WHITE,model=model_path)
    start_game(trained_agent, rnd, True)