import numpy as np
import pygame
import random
import sys

BLUE = (0,0,255)
BLACK = (0,0,0)
WIN_COUNT = None
ROW_COUNT = None
COLUMN_COUNT= None
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
WAIT_TIME = None


def set_game_setting(game_settings):
    global ROW_COUNT, COLUMN_COUNT, WIN_COUNT, WAIT_TIME
    ROW_COUNT = game_settings[0]
    COLUMN_COUNT = game_settings[1]
    WIN_COUNT = game_settings[2]
    WAIT_TIME = game_settings[3]

def winning_move(board, piece):
    # Horizontal
    def check_horizontal_count(col, row):
        for i in range(WIN_COUNT):
            if board[row][col+i] != piece:
                return False
        return True        

    for c in range(COLUMN_COUNT-(WIN_COUNT-1)):
        for r in range(ROW_COUNT):
            if check_horizontal_count(c,r) == True:
                return True
    

    # Vertical
    def check_vertical_count(col, row):
        for i in range(WIN_COUNT):
            if board[row+i][col] != piece:
                return False
        return True        
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-(WIN_COUNT-1)):
            if check_vertical_count(c,r) == True:
                return True

    # Positive diagonal
    def check_pos_diagonal_count(col, row):
        for i in range(WIN_COUNT):
            if board[row+i][col+i] != piece:
                return False
        return True        
    for c in range(COLUMN_COUNT-(WIN_COUNT-1)):
        for r in range(ROW_COUNT-(WIN_COUNT-1)):
            if check_pos_diagonal_count(c,r) == True:
                return True

    # Negative diagonal
    def check_neg_diagonal_count(col, row):
        for i in range(WIN_COUNT):
            if board[row-i][col+i] != piece:
                return False
        return True        
    for c in range(COLUMN_COUNT-(WIN_COUNT-1)):
        for r in range(WIN_COUNT-1, ROW_COUNT):
            if check_neg_diagonal_count(c,r) == True:
                return True

    return False


def evaluate_window(window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == WIN_COUNT:
            score += 100
        elif window.count(piece) == WIN_COUNT-1 and window.count(0) == 1:
            score += 5
        elif WIN_COUNT>3 and window.count(piece) == WIN_COUNT-2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == WIN_COUNT-1 and window.count(0) == 1:
            score -= 10 #prev value 4

        return score

# give a score for the current position by looking through all possible directions
def score_position(board, piece):
    score = 0
    # Center column gets extra reward
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-(WIN_COUNT-1)):
            window = row_array[c:c+WIN_COUNT]
            score += evaluate_window(window, piece)
    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-(WIN_COUNT-1)):
            window = col_array[r:r+WIN_COUNT]
            score += evaluate_window(window, piece)
    # Positive diagonal
    for r in range(ROW_COUNT-(WIN_COUNT-1)):
        for c in range(COLUMN_COUNT-(WIN_COUNT-1)):
            window = [board[r+i][c+i] for i in range(WIN_COUNT)]
            score += evaluate_window(window, piece)
    # Negative diagonal
    for r in range(ROW_COUNT-(WIN_COUNT-1)):
        for c in range(COLUMN_COUNT-(WIN_COUNT-1)):
            window = [board[r+(WIN_COUNT-1)-i][c+i] for i in range(WIN_COUNT)]
            score += evaluate_window(window, piece)
    return score


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



def draw_board(board, screen,  height,agent1_color,agent2_color):
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):     
            if board[r][c] == 1:
                pygame.draw.circle(screen, agent1_color, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, agent2_color, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def start_game(agent1, agent2, use_gui=True):
    if (COLUMN_COUNT == None or ROW_COUNT == None or WIN_COUNT == None or WAIT_TIME == None):
        raise RuntimeError("Set game settings before starting")
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
        draw_board(board, screen, height, agent1.color,agent2.color)
        myfont = pygame.font.SysFont("monospace", 75)
    while not game_over:
        if use_gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        if count == max_count:
            #print("DRAW")
            return 10
        count += 1
        # check if game is over

        # set current agent and current piece 
        current_agent = agent1 if turn == 0 else agent2
        current_piece = 1 if turn == 0 else 2

        
        # player needs to be handled seperately, since we need input
        if current_agent.__class__.__name__ == 'PlayerAgent':
            col = None
            while col is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        posx = event.pos[0]
                        pygame.draw.circle(screen, current_agent.color, (posx, int(SQUARESIZE/2)), RADIUS)
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

            # if its a winning move
            if winning_move(board, current_piece):
                other_agent = agent1 if current_agent == agent2 else agent2
                if other_agent.__class__.__name__ == 'Mr.Q':
                    other_agent.update_after_loss(board)
                #print winner
   ###############             #print(f"{current_agent.name} wins!")#

                # show it visually
                if use_gui:
                    label = myfont.render(f"{current_agent.name} wins!", 1, current_agent.color)
                    screen.blit(label, (0,10))
                
                # set game_over to True in order to finish our main game loop.
                game_over = True

            # after the piece has been placed, show it visually 
            if use_gui:
                draw_board(board, screen,  height,agent1.color,agent2.color)
                pygame.time.wait(WAIT_TIME)  # Add delay to visualize moves

            # not sure what this does, probably switch whose turn it is but seems like a weird way to do it
            turn = (turn + 1) % 2

        # if the game is over, we want to wait a while in order for the user to have time to see who won
        if game_over:
            if use_gui:
                pygame.time.wait(WAIT_TIME*2)
            return current_piece
        