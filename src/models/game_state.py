class GameState:
    def __init__(self, h, w, cat_pos, rat_pos, exit_pos, obstacles, level):
        self.grid_high = h
        self.grid_width = w
        self.cat_pos = tuple(cat_pos)
        self.rat_pos = tuple(rat_pos)
        self.exit = tuple(exit_pos)
        self.obstacles = set(obstacles)
        self.level = level
        
        self.rat_grid = list(rat_pos)
        self.cat_grid = list(cat_pos)
        
        self.rat_speed = 4
        self.cat_speed = 2 + level

        self.game_over = False
        self.message = ""

    def is_valid(self, pos):
        return 0 <= pos[0] < self.grid_high and 0 <= pos[1] < self.grid_width and pos not in self.obstacles
