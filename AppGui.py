import pygame
import os
import GameGui

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tom and Jerry - GUI Version")
    
    font_title = pygame.font.SysFont("comicsansms", 64, bold=True)
    font_button = pygame.font.SysFont("arial", 36, bold=True)
    clock = pygame.time.Clock()
    
    levels = ["Easy", "Medium", "Hard", "Exit"]

    while True:
        in_menu = True
        selected = 0
        while in_menu:
            screen.fill((40, 44, 52)) # Sleek dark background
            
            # Draw Title with Shadow
            title_shadow = font_title.render("Tom and Jerry", True, (20, 22, 26))
            title = font_title.render("Tom and Jerry", True, (241, 196, 15))
            screen.blit(title_shadow, (400 - title_shadow.get_width()//2 + 4, 84))
            screen.blit(title, (400 - title.get_width()//2, 80))
            
            mouse_pos = pygame.mouse.get_pos()
            button_rects = []
            
            for i, lvl in enumerate(levels):
                btn_width = 240
                btn_height = 60
                btn_x = 400 - btn_width // 2
                btn_y = 220 + i * 80
                rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
                button_rects.append(rect)
                
                # Check hover for mouse support
                if rect.collidepoint(mouse_pos):
                    selected = i
                    
                # Setup Colors
                if i == selected:
                    # Highlights: Green for Play, Red for Exit
                    btn_color = (46, 204, 113) if lvl != "Exit" else (231, 76, 60)
                    txt_color = (255, 255, 255)
                else:
                    btn_color = (70, 80, 90)
                    txt_color = (200, 200, 200)
                    
                # Draw Button with rounded corners
                pygame.draw.rect(screen, btn_color, rect, border_radius=15)
                pygame.draw.rect(screen, (20, 25, 30), rect, width=3, border_radius=15) # Border
                
                text = font_button.render(lvl, True, txt_color)
                screen.blit(text, (400 - text.get_width()//2, btn_y + (btn_height - text.get_height()) // 2))
                
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            if selected == len(levels) - 1:
                                pygame.quit()
                                return
                            in_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(levels)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(levels)
                    elif event.key == pygame.K_RETURN:
                        if selected == len(levels) - 1:
                            pygame.quit()
                            return
                        in_menu = False

        # Start Game
        import Maps
        map_height, map_width, map_cat, map_rat, map_exit, map_obstacles = Maps.generate_map(selected)
        game = GameGui.GameGUI(map_height, map_width, map_cat, map_rat, map_exit, map_obstacles, selected, screen)
        # play() will return True if "Restart" was clicked, False if "Exit"
        if not game.play():
            break

if __name__ == "__main__":
    main()
