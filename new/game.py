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



def set_game_setting(game_settings):
    global ROW_COUNT, COLUMN_COUNT, WIN_COUNT
    ROW_COUNT = game_settings[0]
    COLUMN_COUNT = game_settings[1]
    WIN_COUNT = game_settings[2]

def winning_move(board, piece):
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
    if (COLUMN_COUNT == None or ROW_COUNT == None or WIN_COUNT == None):
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
        if count == max_count:
            print("DRAW")
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

        
        # player needs to be handled seperately, since we need input
        if current_agent.__class__.__name__ == 'PlayerAgent':
            col = None
            while col is None:
                for event in pygame.event.get():
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
                #print winner
                print(f"{current_agent.name} wins!")
                # show it visually
                if use_gui:
                    label = myfont.render(f"{current_agent.name} wins!", 1, current_agent.color)
                    screen.blit(label, (0,10))
                
                # set game_over to True in order to finish our main game loop.
                game_over = True

            # after the piece has been placed, show it visually 
            if use_gui:
                draw_board(board, screen,  height,agent1.color,agent2.color)
                pygame.time.wait(500)  # Add delay to visualize moves

            # not sure what this does, probably switch whose turn it is but seems like a weird way to do it
            turn = (turn + 1) % 2

        # if the game is over, we want to wait a while in order for the user to have time to see who won
        if game_over and use_gui:
            pygame.time.wait(5000)
            return current_piece