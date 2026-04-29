import random

def manhattan_distance(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def generate_map(map_level):
    if map_level == 0:
        # Easy level
        map_width = random.randint(5,10)
        map_height = random.randint(5,10)
        num_obs = random.randint(1,3)
        cat_dist = 2
    elif map_level == 1:
        # Medium level
        map_width = random.randint(10,15)
        map_height = random.randint(10,15)
        num_obs = random.randint(3,6)
        cat_dist = 3
    else:
        # Optimized Hard level: Larger grid with significantly more obstacles
        map_width = random.randint(20,25)
        map_height = random.randint(15,20)
        num_obs = random.randint(15,30)
        cat_dist = 6

    map_exit = (random.randint(0,map_height-1),random.randint(0,map_width-1))
    
    # Randomly place the rat, ensuring it doesn't instantly spawn on the exit
    while True:
        map_rat = (random.randint(0,map_height-1),random.randint(0,map_width-1))
        if map_rat != map_exit:
            break
            
    # Place the cat far enough from the rat (cat_dist), and ensure the rat is
    # closer to the exit than the cat is, keeping the game fair.
    while True:
        map_cat = (random.randint(0,map_height-1),random.randint(0,map_width-1))
        if map_cat != map_exit and map_cat != map_rat and manhattan_distance(map_cat,map_rat) > cat_dist and manhattan_distance(map_rat,map_exit) < manhattan_distance(map_cat,map_exit):
            break
            
    map_obstacles = []
    # Procedurally scatter distinct obstacles around the grid, avoiding entities
    for i in range(num_obs):
        while True:
            obstacle = (random.randint(0,map_height-1),random.randint(0,map_width-1))
            if obstacle != map_exit and obstacle != map_rat and obstacle != map_cat and obstacle not in map_obstacles:
                map_obstacles.append(obstacle)
                break
                
    return map_height, map_width, map_cat, map_rat, map_exit, map_obstacles
