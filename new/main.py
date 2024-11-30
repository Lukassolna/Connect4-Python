# main.py
import numpy as np
import pygame
import random
import sys
from player_agent import PlayerAgent
from mimimax_agent import MinimaxAgent
from random_agent import RandomAgent
from q import Qlearning
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
WIN_COUNT = 4
RADIUS = int(SQUARESIZE/2 - 5)
    


def create_board(ROW_COUNT, COLUMN_COUNT):
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col, ROW_COUNT):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col, ROW_COUNT):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece, ROW_COUNT, COLUMN_COUNT):
    # Horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and \
               board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and \
               board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and \
               board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and \
               board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def draw_board(board, screen, COLUMN_COUNT, ROW_COUNT, SQUARESIZE, RADIUS, height):
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):     
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def start_game(agent1, agent2, use_gui=True):

    # flag to know if we are running q agent or not
    q_agent = None
    if hasattr(agent1, 'name') and agent1.name == "Mr.Q":
        q_agent = agent1
    elif hasattr(agent2, 'name') and agent2.name == "Mr.Q":
        q_agent = agent2

    
    
    board = create_board(ROW_COUNT, COLUMN_COUNT)
    game_over = False
    turn = random.randint(0, 1)
    max_count = ROW_COUNT * COLUMN_COUNT
    count =1
    if use_gui:
        pygame.init()
        width = COLUMN_COUNT * SQUARESIZE
        height = (ROW_COUNT+1) * SQUARESIZE
        size = (width, height)
        screen = pygame.display.set_mode(size)
        draw_board(board, screen, COLUMN_COUNT, ROW_COUNT, SQUARESIZE, RADIUS, height)
        myfont = pygame.font.SysFont("monospace", 75)
    while not game_over:
        if count == max_count:
            #print("DRAW")
            return 10
        count += 1
        # check if game is over
        if use_gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

        # set current agent and current piece 
        current_agent = agent1 if turn == 0 else agent2
        current_piece = 1 if turn == 0 else 2
        current_color = RED if turn == 0 else YELLOW 
        
        # player needs to be handled seperately, since we need input
        if current_agent.__class__.__name__ == 'PlayerAgent':
            col = None
            while col is None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        posx = event.pos[0]
                        pygame.draw.circle(screen, current_color, (posx, int(SQUARESIZE/2)), RADIUS)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = current_agent.get_move(board, event)
        # if its not a player, use the agent interface. They all share find_move()
        else:
            col = current_agent.find_move(board, current_piece)
        
        # now we have a column, so lets find out which row to place it
        if is_valid_location(board, col, ROW_COUNT):
            row = get_next_open_row(board, col, ROW_COUNT)
            drop_piece(board, row, col, current_piece) # place the piece on the known row and column in our board
            # after the piece has been placed, show it visually 
            if use_gui:
                draw_board(board, screen, COLUMN_COUNT, ROW_COUNT, SQUARESIZE, RADIUS, height)
                pygame.time.wait(500)  # Add delay to visualize moves
            # if its a winning move
            if winning_move(board, current_piece, ROW_COUNT, COLUMN_COUNT):
                # If opponent won, update Q-learner with negative reward
                if q_agent and current_agent != q_agent:
                    q_agent.update_after_opponent_move(board, True, current_piece)
                if use_gui:
                    color = (255,0,0) if current_piece == 1 else (255,255,0)
                    label = myfont.render(f"Player {current_agent.name} wins!", 1, color)
                    screen.blit(label, (40,10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    pygame.quit()
                 # set game_over to True in order to finish our main game loop.
                
                game_over = True
                return current_agent.name
                
                

                
            
            # If it's not a winning move and this was opponent's move, update Q-learner
            if q_agent and current_agent != q_agent:
                q_agent.update_after_opponent_move(board, False, current_piece)
            
                
               

            

            # not sure what this does, probably switch whose turn it is but seems like a weird way to do it
            turn = (turn + 1) % 2

        # if the game is over, we want to wait a while in order for the user to have time to see who won
        if game_over and use_gui:
            pygame.time.wait(5000)
           


# main program
if __name__ == "__main__":
    minimax_player1 = MinimaxAgent(ROW_COUNT, COLUMN_COUNT, WIN_COUNT, 1, "lesssmart")
    minimax_player2 = MinimaxAgent(ROW_COUNT, COLUMN_COUNT, WIN_COUNT, 2, "smarter")
    random_player = RandomAgent(COLUMN_COUNT)
    user_player = PlayerAgent(SQUARESIZE)
    q_learner = Qlearning(piece=2)  # Right now this only works if q_learner goes second i think?? 
    # we need to fix this piece thing

    #q_learner.load()
    
    board = create_board(ROW_COUNT, COLUMN_COUNT)
    
   
    mr_q_wins = 0
    random_wins = 0
    draws = 0
    num_games = 1000000

    for i in range(num_games):
        #print(i)
        winner = start_game(random_player,q_learner, False)
        #print(winner)
        if winner == 'Mr.Q':
            mr_q_wins += 1
        elif winner == 10:
            draws += 1
        else:
            random_wins += 1
    
        if i % 1000  == 0 and i !=0:
           
            print(f"After {i} games - Mr.Q: {mr_q_wins/(1000):.1%}, Random: {random_wins/(1000):.1%}, Draws: {draws/(1000):.1%}")
            random_wins=0
            mr_q_wins=0
            draws=0 