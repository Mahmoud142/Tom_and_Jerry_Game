from logic.pathfinding import find_path_a_star, find_path_dijkstra

def process_rat_move(state, dx, dy):
    new_rat_grid = [state.rat_grid[0] + dy, state.rat_grid[1] + dx]
    if state.is_valid((new_rat_grid[0], new_rat_grid[1])):
        state.rat_grid = new_rat_grid
        state.rat_pos = tuple(state.rat_grid)
        return True
    return False

def process_cat_move(state):
    # state.level: 0 = Easy, 1 = Medium, 2 = Hard
    if state.level == 0:
        # Easy level: Now uses Dijkstra Algorithm
        path = find_path_dijkstra(state.cat_pos, state.rat_pos, state)
    else:
        # Medium and Hard level: Now uses A* Algorithm
        path = find_path_a_star(state.cat_pos, state.rat_pos, state)
        
    if path and len(path) > 0:
        state.cat_grid = list(path[0])
        state.cat_pos = tuple(state.cat_grid)

def check_game_over(state):
    # Loss condition: Cat occupies the exact same grid cell as the Rat
    if state.rat_grid[0] == state.cat_grid[0] and state.rat_grid[1] == state.cat_grid[1]:
        state.game_over = True
        state.message = "Game Over! Tom caught Jerry!"
    # Win condition: Rat safely reaches the exit cell
    elif state.rat_grid[0] == state.exit[0] and state.rat_grid[1] == state.exit[1]:
        state.game_over = True
        state.message = "Victory! Jerry safely escaped!"
