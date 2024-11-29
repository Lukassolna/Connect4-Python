import numpy as np

current_player_pos_x = 0
current_player_pos_y = 0

def create_simple_grid(x, y):
    grid = np.zeros((4, 4), dtype=int)
    holes = [(1,1), (1,3), (2,3), (3,0)]
    for r, c in holes:
        grid[r][c] = 1
    grid[y][x] = 2
    grid[3][3] = 3
    return grid

def find_valid_moves(grid, current_player_pos_y, current_player_pos_x):
    valid_moves = ["right", "left", "up", "down"]
    if current_player_pos_x >= 3: valid_moves.remove("right")
    if current_player_pos_x <= 0: valid_moves.remove("left")
    if current_player_pos_y <= 0: valid_moves.remove("up")
    if current_player_pos_y >= 3: valid_moves.remove("down")
    return valid_moves

def make_move(move, grid):
    global current_player_pos_x, current_player_pos_y
    old_x, old_y = current_player_pos_x, current_player_pos_y

    if move == "right": current_player_pos_x = min(current_player_pos_x + 1, 3)
    elif move == "left": current_player_pos_x = max(current_player_pos_x - 1, 0)
    elif move == "up": current_player_pos_y = max(current_player_pos_y - 1, 0)
    elif move == "down": current_player_pos_y = min(current_player_pos_y + 1, 3)

    piece_at_current_pos = grid[current_player_pos_y, current_player_pos_x]
    
    if piece_at_current_pos == 1:
        return grid, -1
    if piece_at_current_pos == 3:
        print("WINNER WINNER CHICKEN DINNER")
        grid[current_player_pos_y][current_player_pos_x] = 2
        grid[old_y][old_x] = 0
        return grid, 1
    if piece_at_current_pos == 0:
        grid[current_player_pos_y][current_player_pos_x] = 2
        grid[old_y][old_x] = 0
        return grid, 0
    return grid, 0

def grid_to_key(grid):
    return tuple(map(tuple, grid))

import numpy as np

current_player_pos_x = 0
current_player_pos_y = 0

def create_simple_grid(x, y):
    grid = np.zeros((4, 4), dtype=int)
    holes = [(1,1), (1,3), (2,3), (3,0)]
    for r, c in holes:
        grid[r][c] = 1
    grid[y][x] = 2
    grid[3][3] = 3
    return grid

def find_valid_moves(grid, current_player_pos_y, current_player_pos_x):
    valid_moves = ["right", "left", "up", "down"]
    if current_player_pos_x >= 3: valid_moves.remove("right")
    if current_player_pos_x <= 0: valid_moves.remove("left")
    if current_player_pos_y <= 0: valid_moves.remove("up")
    if current_player_pos_y >= 3: valid_moves.remove("down")
    return valid_moves

def make_move(move, grid):
    global current_player_pos_x, current_player_pos_y
    old_x, old_y = current_player_pos_x, current_player_pos_y

    if move == "right": current_player_pos_x = min(current_player_pos_x + 1, 3)
    elif move == "left": current_player_pos_x = max(current_player_pos_x - 1, 0)
    elif move == "up": current_player_pos_y = max(current_player_pos_y - 1, 0)
    elif move == "down": current_player_pos_y = min(current_player_pos_y + 1, 3)

    piece_at_current_pos = grid[current_player_pos_y, current_player_pos_x]
    
    if piece_at_current_pos == 1:
        return grid, -1
    if piece_at_current_pos == 3:
        print("WINNER WINNER CHICKEN DINNER")
        grid[current_player_pos_y][current_player_pos_x] = 2
        grid[old_y][old_x] = 0
        return grid, 1
    if piece_at_current_pos == 0:
        grid[current_player_pos_y][current_player_pos_x] = 2
        grid[old_y][old_x] = 0
        return grid, 0
    return grid, 0

def grid_to_key(grid):
    return tuple(map(tuple, grid))

def q_learning():
    global current_player_pos_x, current_player_pos_y
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor
    epsilon = 0.1  # exploration rate
    episodes = 10000
    q_table = {}
    
    for episode in range(episodes):
        current_player_pos_x, current_player_pos_y = 0, 0
        grid = create_simple_grid(0, 0)
        steps = 0
        
        while steps < 100:  # Limit steps per episode
            state = grid_to_key(grid)
            if state not in q_table:
                q_table[state] = {"up": 0.0, "down": 0.0, "left": 0.0, "right": 0.0}
            
            valid_moves = find_valid_moves(grid, current_player_pos_y, current_player_pos_x)
            
            # epsilon greedy selection to be more creative
            if np.random.random() < epsilon:  # Explore
                action = np.random.choice(valid_moves)
            else:  # Exploit
                valid_q_values = {move: q_table[state][move] for move in valid_moves}
                action = max(valid_q_values.items(), key=lambda x: x[1])[0]
            
            new_grid, outcome = make_move(action, grid.copy())
            reward = -1  # Small penalty for each move 
            
            if outcome == 1:  # Reached goal
                reward = 1000
                if episode % 1000 == 0:
                    print(f"Found goal in episode {episode}")
            elif outcome == -1:  # Hit hole
                reward = -100
            
            next_state = grid_to_key(new_grid)
            if next_state not in q_table:
                q_table[next_state] = {"up": 0.0, "down": 0.0, "left": 0.0, "right": 0.0}
            # here we updated the q table
        
            next_max_q = max(q_table[next_state].values())
            q_table[state][action] += alpha * (reward + gamma * next_max_q - q_table[state][action])
            
            grid = new_grid
            steps += 1
            
            if outcome != 0:
                break
                
    return q_table



def walk_with_q_table(q_table):
    global current_player_pos_x, current_player_pos_y
    current_player_pos_x, current_player_pos_y = 0, 0
    grid = create_simple_grid(0, 0)
    
    while True:
        print(grid)
        state_key = grid_to_key(grid)
        valid_moves = find_valid_moves(grid, current_player_pos_y, current_player_pos_x)
        
        if state_key not in q_table:
            print("Unknown state")
            break
            
        valid_q_values = {move: q_table[state_key][move] for move in valid_moves}
        best_move = max(valid_q_values.items(), key=lambda x: x[1])[0]
        
        print(f"Best move: {best_move}")
        grid, outcome = make_move(best_move, grid)
        
        if outcome != 0:
            print(grid)
            break

# Run


q_table = q_learning()
print(q_table)
walk_with_q_table(q_table)