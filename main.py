import pygame
import sys
import os
import pickle
from player_mechanics import Player
from exploration_mechanics import explore
from battle_mechanics import try_weapon
from purchase_mechanics import Shop

pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trail Dungeon Hero")

# Fonts
FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Directory for saving profiles
PROFILE_DIR = "profiles"
if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def save_profile(player, profile_name):
    with open(f"{PROFILE_DIR}/{profile_name}.pkl", 'wb') as f:
        pickle.dump(player, f)

def load_profile(profile_name):
    with open(f"{PROFILE_DIR}/{profile_name}.pkl", 'rb') as f:
        return pickle.load(f)

def list_profiles():
    return [f[:-4] for f in os.listdir(PROFILE_DIR) if f.endswith('.pkl')]

def title_screen():
    click = False
    while True:
        screen.fill(WHITE)
        draw_text('Trail Dungeon Hero', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        mx, my = pygame.mouse.get_pos()
        button_new_game = pygame.Rect(300, 250, 200, 50)
        button_load_game = pygame.Rect(300, 320, 200, 50)
        button_exit = pygame.Rect(300, 390, 200, 50)

        if button_new_game.collidepoint((mx, my)):
            if click:
                new_game()
        if button_load_game.collidepoint((mx, my)):
            if click:
                load_game()
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, GRAY, button_new_game)
        pygame.draw.rect(screen, GRAY, button_load_game)
        pygame.draw.rect(screen, GRAY, button_exit)
        draw_text('New Game', FONT, BLACK, screen, SCREEN_WIDTH // 2, 275)
        draw_text('Load Game', FONT, BLACK, screen, SCREEN_WIDTH // 2, 345)
        draw_text('Exit', FONT, BLACK, screen, SCREEN_WIDTH // 2, 415)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def new_game():
    screen.fill(WHITE)
    draw_text('Enter Profile Name:', FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    profile_name = input_text()
    if profile_name:
        player = Player()
        save_profile(player, profile_name)
        main_game(player, profile_name)

def load_game():
    profiles = list_profiles()
    if not profiles:
        screen.fill(WHITE)
        draw_text('No profiles found. Please create a new game.', FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(2000)
        return

    click = False
    while True:
        screen.fill(WHITE)
        draw_text('Select Profile:', FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        mx, my = pygame.mouse.get_pos()
        profile_buttons = []
        for i, profile in enumerate(profiles):
            button = pygame.Rect(300, 300 + i * 50, 200, 50)
            profile_buttons.append((button, profile))

        for button, profile in profile_buttons:
            if button.collidepoint((mx, my)):
                if click:
                    player = load_profile(profile)
                    main_game(player, profile)
            pygame.draw.rect(screen, GRAY, button)
            draw_text(profile, FONT, BLACK, screen, SCREEN_WIDTH // 2, button.y + 25)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def input_text():
    input_box = pygame.Rect(300, 300, 200, 50)
    color_inactive = GRAY
    color_active = BLACK
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        draw_text('Enter Profile Name:', FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        txt_surface = FONT.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

def main_game(player, profile_name):
    click = False
    shop = Shop()
    while True:
        screen.fill(WHITE)
        draw_text('Main Menu', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        mx, my = pygame.mouse.get_pos()
        button_explore = pygame.Rect(300, 250, 200, 50)
        button_battle = pygame.Rect(300, 320, 200, 50)
        button_shop = pygame.Rect(300, 390, 200, 50)
        button_status = pygame.Rect(300, 460, 200, 50)
        button_save = pygame.Rect(300, 530, 200, 50)
        button_exit = pygame.Rect(300, 600, 200, 50)

        if button_explore.collidepoint((mx, my)):
            if click:
                explore(player)
        if button_battle.collidepoint((mx, my)):
            if click:
                try_weapon(player)
        if button_shop.collidepoint((mx, my)):
            if click:
                shop.interact(player)
        if button_status.collidepoint((mx, my)):
            if click:
                player.show_status()
        if button_save.collidepoint((mx, my)):
            if click:
                save_profile(player, profile_name)
                draw_text('Game Saved!', FONT, BLACK, screen, SCREEN_WIDTH // 2, 700)
                pygame.display.update()
                pygame.time.wait(1000)
        if button_exit.collidepoint((mx, my)):
            if click:
                save_profile(player, profile_name)
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, GRAY, button_explore)
        pygame.draw.rect(screen, GRAY, button_battle)
        pygame.draw.rect(screen, GRAY, button_shop)
        pygame.draw.rect(screen, GRAY, button_status)
        pygame.draw.rect(screen, GRAY, button_save)
        pygame.draw.rect(screen, GRAY, button_exit)
        draw_text('Explore', FONT, BLACK, screen, SCREEN_WIDTH // 2, 275)
        draw_text('Battle', FONT, BLACK, screen, SCREEN_WIDTH // 2, 345)
        draw_text('Shop', FONT, BLACK, screen, SCREEN_WIDTH // 2, 415)
        draw_text('Status', FONT, BLACK, screen, SCREEN_WIDTH // 2, 485)
        draw_text('Save Game', FONT, BLACK, screen, SCREEN_WIDTH // 2, 555)
        draw_text('Exit', FONT, BLACK, screen, SCREEN_WIDTH // 2, 625)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_profile(player, profile_name)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_profile(player, profile_name)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

if __name__ == "__main__":
    title_screen()

