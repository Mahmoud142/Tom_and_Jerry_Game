import pygame
import sys
from views.menu_view import draw_menu
from views.game_view import GameView
from logic.map_engine import generate_map
from models.game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Tom and Jerry - GUI Version")
    
    font_title = pygame.font.SysFont("comicsansms", 64, bold=True)
    font_button = pygame.font.SysFont("arial", 36, bold=True)
    
    levels = ["Easy", "Medium", "Hard", "Exit"]

    while True:
        in_menu = True
        selected = 0
        while in_menu:
            mouse_pos = pygame.mouse.get_pos()
            button_rects = draw_menu(screen, font_title, font_button, levels, selected)
            
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(mouse_pos):
                    selected = i

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            if selected == len(levels) - 1:
                                pygame.quit()
                                sys.exit()
                            in_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(levels)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(levels)
                    elif event.key == pygame.K_RETURN:
                        if selected == len(levels) - 1:
                            pygame.quit()
                            sys.exit()
                        in_menu = False

        map_height, map_width, map_cat, map_rat, map_exit, map_obstacles = generate_map(selected)
        state = GameState(map_height, map_width, map_cat, map_rat, map_exit, map_obstacles, selected)
        view = GameView(state, screen)
        
        if not view.loop():
            break

if __name__ == "__main__":
    main()
