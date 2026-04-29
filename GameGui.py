import pygame
import heapq
import os
import math

TILE_SIZE = 40

class GameGUI:
    def __init__(self, h, w, cat, rat, exit_pos, obs, level, screen):
        self.grid_high = h
        self.grid_width = w
        self.cat_pos = cat
        self.rat_pos = rat
        self.exit = exit_pos
        self.obstacles = obs
        self.level = level
        self.screen = screen
        
        # Try to load sprites, fallback to colors
        self.rat_img = None
        self.cat_img = None
        self.exit_img = None
        self.obs_img = None
        try:
            if os.path.exists("assets/jerry.png"):
                self.rat_img = pygame.transform.scale(pygame.image.load("assets/jerry.png").convert_alpha(), (TILE_SIZE-4, TILE_SIZE-4))
            if os.path.exists("assets/tom.png"):
                self.cat_img = pygame.transform.scale(pygame.image.load("assets/tom.png").convert_alpha(), (TILE_SIZE-4, TILE_SIZE-4))
            if os.path.exists("assets/exit.png"):
                self.exit_img = pygame.transform.scale(pygame.image.load("assets/exit.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
            if os.path.exists("assets/obs.png"):
                self.obs_img = pygame.transform.scale(pygame.image.load("assets/obs.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            pass
            
        # Calculate offsets to center the map
        self.offset_x = (screen.get_width() - (w * TILE_SIZE)) // 2
        self.offset_y = (screen.get_height() - (h * TILE_SIZE)) // 2

        # Convert grid positions to exact pixel coordinates
        self.rat_px = [self.offset_x + rat[1] * TILE_SIZE, self.offset_y + rat[0] * TILE_SIZE]
        self.cat_px = [self.offset_x + cat[1] * TILE_SIZE, self.offset_y + cat[0] * TILE_SIZE]
        
        self.rat_speed = 4
        self.cat_speed = 2 + level  # Cat gets faster with level

        # Create Rects for obstacles to do pixel-perfect collisions
        self.obs_rects = []
        for obs_pos in self.obstacles:
            r = pygame.Rect(self.offset_x + obs_pos[1]*TILE_SIZE, self.offset_y + obs_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            self.obs_rects.append(r)
        
        self.exit_rect = pygame.Rect(self.offset_x + self.exit[1]*TILE_SIZE, self.offset_y + self.exit[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def is_valid(self, pos):
        return 0 <= pos[0] < self.grid_high and 0 <= pos[1] < self.grid_width and pos not in self.obstacles

    def play(self):
        running = True
        game_over = False
        message = ""

        # Player Rect
        rat_rect = pygame.Rect(self.rat_px[0] + 5, self.rat_px[1] + 5, TILE_SIZE - 10, TILE_SIZE - 10)
        
        # UI Buttons for game over
        btn_font = pygame.font.SysFont(None, 40)
        restart_text = btn_font.render("Restart", True, (255, 255, 255))
        exit_text = btn_font.render("Exit", True, (255, 255, 255))
        
        restart_rect = restart_text.get_rect(center=(self.screen.get_width()//2 - 100, 150))
        exit_rect = exit_text.get_rect(center=(self.screen.get_width()//2 + 100, 150))

        # We will keep track of grid position explicitly for logic
        self.rat_grid = list(self.rat_pos)
        self.cat_grid = list(self.cat_pos)
        
        # Pixels for smooth interpolation visually
        self.rat_px = [self.offset_x + self.rat_grid[1] * TILE_SIZE, self.offset_y + self.rat_grid[0] * TILE_SIZE]
        self.cat_px = [self.offset_x + self.cat_grid[1] * TILE_SIZE, self.offset_y + self.cat_grid[0] * TILE_SIZE]

        def get_pixel_from_grid(grid):
            return [self.offset_x + grid[1] * TILE_SIZE, self.offset_y + grid[0] * TILE_SIZE]

        while running:
            # Smooth visual interpolation towards target grid
            target_rat_px = get_pixel_from_grid(self.rat_grid)
            target_cat_px = get_pixel_from_grid(self.cat_grid)

            # Move visual closer to logic grid
            self.rat_px[0] += (target_rat_px[0] - self.rat_px[0]) * 0.2
            self.rat_px[1] += (target_rat_px[1] - self.rat_px[1]) * 0.2
            self.cat_px[0] += (target_cat_px[0] - self.cat_px[0]) * 0.15 # Cat is slightly slower visually
            self.cat_px[1] += (target_cat_px[1] - self.cat_px[1]) * 0.15

            rat_rect.x = self.rat_px[0] + 5
            rat_rect.y = self.rat_px[1] + 5
            
            cat_rect = pygame.Rect(self.cat_px[0] + 5, self.cat_px[1] + 5, TILE_SIZE - 10, TILE_SIZE - 10)

            # Game logic logic match
            if self.rat_grid[0] == self.cat_grid[0] and self.rat_grid[1] == self.cat_grid[1]:
                game_over = True
                message = "Game Over! You were eaten."
            elif self.rat_grid[0] == self.exit[0] and self.rat_grid[1] == self.exit[1]:
                game_over = True
                message = "You Won! Escaped!"
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                if game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_rect.collidepoint(event.pos):
                            return True
                        if exit_rect.collidepoint(event.pos):
                            return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return True
                        if event.key == pygame.K_ESCAPE:
                            return False
                
                # Move on Key Press
                if not game_over and event.type == pygame.KEYDOWN:
                    moved = False
                    new_rat_grid = list(self.rat_grid)
                    
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        new_rat_grid[0] -= 1
                        moved = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        new_rat_grid[0] += 1
                        moved = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        new_rat_grid[1] -= 1
                        moved = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        new_rat_grid[1] += 1
                        moved = True
                    
                    # If valid move, execute Rat move then Cat move
                    if moved and self.is_valid((new_rat_grid[0], new_rat_grid[1])):
                        self.rat_grid = new_rat_grid
                        
                        # AI Turn based logic
                        # First update positions because find_path relies on self.rat_pos and self.cat_pos
                        self.rat_pos = tuple(self.rat_grid)
                        self.cat_pos = tuple(self.cat_grid)
                        
                        # Cat Moves towards the Rat
                        path = self.find_path(self.cat_pos, self.rat_pos)
                        if path and len(path) > 0:
                            self.cat_grid = list(path[0])
                        
                        self.cat_pos = tuple(self.cat_grid)

            # Draw
            self.screen.fill((50, 50, 50))
            self.draw_grid(rat_rect, cat_rect)
            
            if game_over:
                # Dim the screen a bit
                s = pygame.Surface((800,600))
                s.set_alpha(128)
                s.fill((0,0,0))
                self.screen.blit(s, (0,0))
                
                text = self.font.render(message, True, (255, 255, 255))
                rect = text.get_rect(center=(self.screen.get_width()//2, 80))
                self.screen.blit(text, rect)
                
                # Draw Buttons
                pygame.draw.rect(self.screen, (0, 150, 0), restart_rect.inflate(40, 20))
                self.screen.blit(restart_text, restart_rect)
                
                pygame.draw.rect(self.screen, (150, 0, 0), exit_rect.inflate(40, 20))
                self.screen.blit(exit_text, exit_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        return False

    def draw_grid(self, rat_rect, cat_rect):
        # Draw background tiles
        for i in range(self.grid_high):
            for j in range(self.grid_width):
                rect = pygame.Rect(self.offset_x + j*TILE_SIZE, self.offset_y + i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        # Draw obstacles
        for obs in self.obs_rects:
            if self.obs_img:
                self.screen.blit(self.obs_img, obs)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), obs)

        # Draw Exit
        if self.exit_img:
            self.screen.blit(self.exit_img, self.exit_rect)
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), self.exit_rect)
        
        # Draw Rat (Jerry)
        if self.rat_img:
            self.screen.blit(self.rat_img, rat_rect)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), rat_rect)
        
        # Draw Cat (Tom)
        if self.cat_img:
            self.screen.blit(self.cat_img, cat_rect)
        else:
            pygame.draw.rect(self.screen, (255, 0, 0), cat_rect)

    def find_path(self, start, end):
        # Optimized A* using heapq
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = (current[0] + di, current[1] + dj)
                if self.is_valid(neighbor):
                    tentative_g = g_score[current] + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + heuristic(neighbor, end)
                        heapq.heappush(open_list, (f_score, neighbor))
                        came_from[neighbor] = current
        return []

    def move_cat_smooth(self):
        # Update Cat grid pos
        self.cat_pos = (
            int(round((self.cat_px[1] - self.offset_y) / TILE_SIZE)),
            int(round((self.cat_px[0] - self.offset_x) / TILE_SIZE))
        )

        path_to_rat = self.find_path(self.cat_pos, self.rat_pos)
        
        target_px = self.rat_px
        
        # If there's a path, go to the very next node pixel center
        if path_to_rat and len(path_to_rat) > 0:
            target_node = path_to_rat[0]
            target_px = [
                self.offset_x + target_node[1] * TILE_SIZE,
                self.offset_y + target_node[0] * TILE_SIZE
            ]
        
        # Move slightly towards target_px depending on speed
        dx = target_px[0] - self.cat_px[0]
        dy = target_px[1] - self.cat_px[1]
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            self.cat_px[0] += (dx / dist) * self.cat_speed
            self.cat_px[1] += (dy / dist) * self.cat_speed
