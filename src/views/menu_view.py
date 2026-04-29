import pygame
from config import *

def draw_menu(screen, font_title, font_button, levels, selected):
    screen.fill(COLOR_BG_MENU)
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    title_shadow = font_title.render("Tom and Jerry", True, COLOR_TITLE_SHADOW)
    title = font_title.render("Tom and Jerry", True, COLOR_TITLE)
    
    # Calculate title position based on screen width/height
    title_x = screen_width // 2
    title_y = screen_height // 8
    
    screen.blit(title_shadow, (title_x - title_shadow.get_width()//2 + 4, title_y + 4))
    screen.blit(title, (title_x - title.get_width()//2, title_y))
    
    button_rects = []
    
    for i, lvl in enumerate(levels):
        btn_width = 240
        btn_height = 60
        btn_x = screen_width // 2 - btn_width // 2
        btn_y = title_y + 140 + i * 80
        rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        button_rects.append(rect)
        
        # Hovering/Selection logic: Highlight button if the user's cursor or keyboard selected it
        if i == selected:
            btn_color = COLOR_BTN_PLAY if lvl != "Exit" else COLOR_BTN_EXIT
            txt_color = COLOR_WHITE
        else:
            btn_color = COLOR_BTN_NORMAL
            txt_color = COLOR_TEXT_NORMAL
            
        pygame.draw.rect(screen, btn_color, rect, border_radius=15)
        pygame.draw.rect(screen, (20, 25, 30), rect, width=3, border_radius=15)
        
        text = font_button.render(lvl, True, txt_color)
        screen.blit(text, (screen_width // 2 - text.get_width()//2, btn_y + (btn_height - text.get_height()) // 2))
        
    return button_rects
