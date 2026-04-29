import pygame
import os
from config import *
from logic.game_engine import process_rat_move, process_cat_move, check_game_over

class GameView:
    def __init__(self, state, screen):
        self.state = state
        self.screen = screen
        
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
        except Exception:
            pass

        self.update_offsets()
        self.rat_px = [self.offset_x + state.rat_grid[1] * self.tile_size, self.offset_y + state.rat_grid[0] * self.tile_size]
        self.cat_px = [self.offset_x + state.cat_grid[1] * self.tile_size, self.offset_y + state.cat_grid[0] * self.tile_size]

        self.font = pygame.font.SysFont(None, 36)
        
    def update_offsets(self):
        # Dynamically scale sizes and update grid offset to ensure 
        # the entire map fits and remains centered in the window
        margin = 40
        avail_width = max(100, self.screen.get_width() - margin)
        avail_height = max(100, self.screen.get_height() - margin)
        
        tile_w = avail_width // self.state.grid_width
        tile_h = avail_height // self.state.grid_high
        
        new_tile_size = max(5, min(tile_w, tile_h, TILE_SIZE))
        
        # Reload/rescale images if tile size changed
        if not hasattr(self, 'tile_size') or self.tile_size != new_tile_size:
            self.tile_size = new_tile_size
            try:
                if os.path.exists("assets/jerry.png"):
                    self.rat_img = pygame.transform.scale(pygame.image.load("assets/jerry.png").convert_alpha(), (self.tile_size-4, self.tile_size-4))
                if os.path.exists("assets/tom.png"):
                    self.cat_img = pygame.transform.scale(pygame.image.load("assets/tom.png").convert_alpha(), (self.tile_size-4, self.tile_size-4))
                if os.path.exists("assets/exit.png"):
                    self.exit_img = pygame.transform.scale(pygame.image.load("assets/exit.png").convert_alpha(), (self.tile_size, self.tile_size))
                if os.path.exists("assets/obs.png"):
                    self.obs_img = pygame.transform.scale(pygame.image.load("assets/obs.png").convert_alpha(), (self.tile_size, self.tile_size))
            except Exception:
                pass

        self.offset_x = (self.screen.get_width() - (self.state.grid_width * self.tile_size)) // 2
        self.offset_y = (self.screen.get_height() - (self.state.grid_high * self.tile_size)) // 2


    def draw_grid(self, rat_rect, cat_rect):
        self.update_offsets()
        
        for i in range(self.state.grid_high):
            for j in range(self.state.grid_width):
                rect = pygame.Rect(self.offset_x + j*self.tile_size, self.offset_y + i*self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)

        for obs_pos in self.state.obstacles:
            r = pygame.Rect(self.offset_x + obs_pos[1]*self.tile_size, self.offset_y + obs_pos[0]*self.tile_size, self.tile_size, self.tile_size)
            if self.obs_img: self.screen.blit(self.obs_img, r)
            else: pygame.draw.rect(self.screen, COLOR_OBS_FALLBACK, r)

        exit_r = pygame.Rect(self.offset_x + self.state.exit[1]*self.tile_size, self.offset_y + self.state.exit[0]*self.tile_size, self.tile_size, self.tile_size)
        if self.exit_img: self.screen.blit(self.exit_img, exit_r)
        else: pygame.draw.rect(self.screen, COLOR_EXIT_FALLBACK, exit_r)
        
        if self.rat_img: self.screen.blit(self.rat_img, rat_rect)
        else: pygame.draw.rect(self.screen, COLOR_RAT_FALLBACK, rat_rect)
        
        if self.cat_img: self.screen.blit(self.cat_img, cat_rect)
        else: pygame.draw.rect(self.screen, COLOR_CAT_FALLBACK, cat_rect)

    def loop(self):
        clock = pygame.time.Clock()
        rat_rect = pygame.Rect(0, 0, self.tile_size - 10, self.tile_size - 10)
        
        btn_font = pygame.font.SysFont(None, 40)
        restart_text = btn_font.render("Restart", True, COLOR_WHITE)
        exit_text = btn_font.render("Exit", True, COLOR_WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen.get_width()//2 - 100, 150))
        exit_rect = exit_text.get_rect(center=(self.screen.get_width()//2 + 100, 150))

        def get_pixel_from_grid(grid):
            # Converts grid coordinates directly to screen pixels using current offsets
            return [self.offset_x + grid[1] * self.tile_size, self.offset_y + grid[0] * self.tile_size]

        game_over_selected = 0

        while True:
            target_rat_px = get_pixel_from_grid(self.state.rat_grid)
            target_cat_px = get_pixel_from_grid(self.state.cat_grid)

            # Linear interpolation (lerp) for smooth easing between grid cells
            self.rat_px[0] += (target_rat_px[0] - self.rat_px[0]) * 0.2
            self.rat_px[1] += (target_rat_px[1] - self.rat_px[1]) * 0.2
            self.cat_px[0] += (target_cat_px[0] - self.cat_px[0]) * 0.15
            self.cat_px[1] += (target_cat_px[1] - self.cat_px[1]) * 0.15

            rat_rect = pygame.Rect(self.rat_px[0] + 5, self.rat_px[1] + 5, self.tile_size - 10, self.tile_size - 10)
            cat_rect = pygame.Rect(self.cat_px[0] + 5, self.cat_px[1] + 5, self.tile_size - 10, self.tile_size - 10)

            check_game_over(self.state)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return False
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_offsets()
                    restart_rect = restart_text.get_rect(center=(self.screen.get_width()//2 - 100, 150))
                    exit_rect = exit_text.get_rect(center=(self.screen.get_width()//2 + 100, 150))
                    
                if self.state.game_over:
                    if event.type == pygame.MOUSEMOTION:
                        if restart_rect.inflate(40, 20).collidepoint(event.pos):
                            game_over_selected = 0
                        elif exit_rect.inflate(40, 20).collidepoint(event.pos):
                            game_over_selected = 1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_rect.inflate(40, 20).collidepoint(event.pos): return True
                        if exit_rect.inflate(40, 20).collidepoint(event.pos): return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                            game_over_selected = 1 - game_over_selected # Toggle 0 or 1
                        elif event.key == pygame.K_RETURN: 
                            return True if game_over_selected == 0 else False
                        elif event.key == pygame.K_ESCAPE: return False
                
                if not self.state.game_over and event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key in (pygame.K_UP, pygame.K_w): dy = -1
                    elif event.key in (pygame.K_DOWN, pygame.K_s): dy = 1
                    elif event.key in (pygame.K_LEFT, pygame.K_a): dx = -1
                    elif event.key in (pygame.K_RIGHT, pygame.K_d): dx = 1
                    
                    if (dx != 0 or dy != 0) and process_rat_move(self.state, dx, dy):
                        process_cat_move(self.state)

            self.screen.fill(COLOR_BG_GAME)
            self.draw_grid(rat_rect, cat_rect)
            
            if self.state.game_over:
                s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
                s.set_alpha(128)
                self.screen.blit(s, (0,0))
                
                text = self.font.render(self.state.message, True, COLOR_WHITE)
                rect = text.get_rect(center=(self.screen.get_width()//2, 80))
                self.screen.blit(text, rect)
                
                r_rect_inf = restart_rect.inflate(40, 20)
                e_rect_inf = exit_rect.inflate(40, 20)
                
                r_color = (0, 200, 0) if game_over_selected == 0 else (0, 150, 0)
                e_color = (200, 0, 0) if game_over_selected == 1 else (150, 0, 0)
                
                pygame.draw.rect(self.screen, r_color, r_rect_inf, border_radius=10)
                if game_over_selected == 0:
                    pygame.draw.rect(self.screen, COLOR_WHITE, r_rect_inf, width=3, border_radius=10)
                else:
                    pygame.draw.rect(self.screen, (20, 20, 20), r_rect_inf, width=2, border_radius=10)
                self.screen.blit(restart_text, restart_rect)
                
                pygame.draw.rect(self.screen, e_color, e_rect_inf, border_radius=10)
                if game_over_selected == 1:
                    pygame.draw.rect(self.screen, COLOR_WHITE, e_rect_inf, width=3, border_radius=10)
                else:
                    pygame.draw.rect(self.screen, (20, 20, 20), e_rect_inf, width=2, border_radius=10)
                self.screen.blit(exit_text, exit_rect)

            pygame.display.flip()
            clock.tick(60)
