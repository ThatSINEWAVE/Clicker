import pygame
import pygame_menu
import sys
import os
import json
from pprint import pprint
import webbrowser

# Initialize Pygame
pygame.init()

# Constants
DEFAULT_RESOLUTION = (1280, 720)
LOGO_SIZE_RATIO = 1 / 3
CLICK_IMAGE_RATIO = 1 / 3
BUTTON_SIZE = (50, 50)
BUTTON_MARGIN = 20
FADE_SPEED = 5

# Paths
LOGO_PATH = "assets/startup/logo.png"
CLICK_IMAGE_PATH = "assets/clicker/click_image.png"
SETTINGS_ICON_PATH = "assets/icons/Settings.png"
DISCORD_ICON_PATH = "assets/icons/Discord.png"
STORE_ICON_PATH = "assets/icons/Store.png"
SAVE_DATA_PATH = "save_data.json"
WINDOW_ICON_PATH = "assets/app/window_icon.png"
TASKBAR_ICON_PATH = "assets/app/taskbar_icon.ico"

# Set the taskbar icon
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('my_game_id')
pygame.display.set_icon(pygame.image.load(WINDOW_ICON_PATH))


# Available Resolutions
RESOLUTIONS = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1280, 800),
    (1366, 768),
    (1440, 900),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
]

# Load Save Data
def load_save_data():
    try:
        with open(SAVE_DATA_PATH, "r") as file:
            data = json.load(file)
            click_count = data.get("click_count", 0)
            resolution = tuple(data.get("resolution", DEFAULT_RESOLUTION))
            return click_count, resolution
    except FileNotFoundError:
        return 0, DEFAULT_RESOLUTION


def save_data(click_count, resolution):
    data = {
        "click_count": click_count,
        "resolution": [resolution[0], resolution[1]]
    }
    with open(SAVE_DATA_PATH, "w") as file:
        json.dump(data, file, indent=2)
        if sys.platform == 'win32':
            pprint(data, sys.stdout)
        else:
            pprint(data, sys.stdout.buffer)


# Screen Setup
screen = pygame.display.set_mode(DEFAULT_RESOLUTION)
pygame.display.set_caption("SINEWAVE's Clicker Game")
clock = pygame.time.Clock()

# Load Images
logo = pygame.image.load(LOGO_PATH)
click_image = pygame.image.load(CLICK_IMAGE_PATH)
settings_icon = pygame.image.load(SETTINGS_ICON_PATH)
discord_icon = pygame.image.load(DISCORD_ICON_PATH)
store_icon = pygame.image.load(STORE_ICON_PATH)
window_icon = pygame.image.load(WINDOW_ICON_PATH)
pygame.display.set_icon(window_icon)

# Resize Images
def resize_image(image, ratio, screen):
    return pygame.transform.scale(
        image, (int(screen.get_width() * ratio), int(screen.get_height() * ratio))
    )


logo = resize_image(logo, LOGO_SIZE_RATIO, screen)
click_image = resize_image(click_image, CLICK_IMAGE_RATIO, screen)

# Position Elements
def center_image(image, screen):
    return image.get_rect(center=screen.get_rect().center)


logo_rect = center_image(logo, screen)
click_image_rect = center_image(click_image, screen)

# Buttons
def position_buttons(screen):
    screen_rect = screen.get_rect()
    button_y = screen_rect.bottom - BUTTON_MARGIN - BUTTON_SIZE[1]
    settings_rect = pygame.Rect(0, 0, *BUTTON_SIZE)
    discord_rect = pygame.Rect(0, 0, *BUTTON_SIZE)
    store_rect = pygame.Rect(0, 0, *BUTTON_SIZE)

    total_width = 3 * BUTTON_SIZE[0] + 2 * BUTTON_MARGIN
    start_x = (screen_rect.width - total_width) / 2
    settings_rect.topleft = (start_x, button_y)
    discord_rect.topleft = (start_x + BUTTON_SIZE[0] + BUTTON_MARGIN, button_y)
    store_rect.topleft = (start_x + 2 * (BUTTON_SIZE[0] + BUTTON_MARGIN), button_y)

    return settings_rect, discord_rect, store_rect


settings_rect, discord_rect, store_rect = position_buttons(screen)

# Fade In/Out Functions
def fade_in(surface, screen, speed=FADE_SPEED):
    alpha = 0
    while alpha < 255:
        surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(surface, surface.get_rect(center=screen.get_rect().center))
        pygame.display.update()
        alpha += speed
        clock.tick(60)


def fade_out(surface, screen, speed=FADE_SPEED):
    alpha = 255
    while alpha > 0:
        surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(surface, surface.get_rect(center=screen.get_rect().center))
        pygame.display.update()
        alpha -= speed
        clock.tick(60)


def wait(seconds):
    start_ticks = pygame.time.get_ticks()
    while (pygame.time.get_ticks() - start_ticks) < seconds * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Main Game Loop
def main():
    global logo, click_image, logo_rect, click_image_rect, settings_rect, discord_rect, store_rect
    click_count, resolution = load_save_data()
    show_logo = True
    in_settings = False

    screen = pygame.display.set_mode(resolution)

    def set_resolution(value, res):
        nonlocal resolution
        resolution = res
        pygame.display.set_mode(resolution)
        resize_assets()
        save_data(click_count, resolution)

    def clear_save_data():
        nonlocal click_count
        click_count = 0
        save_data(click_count, resolution)

    def create_settings_menu():
        menu = pygame_menu.Menu('Settings', 400, 300, theme=pygame_menu.themes.THEME_DARK)

        resolution_options = [(f'{w}x{h}', (w, h)) for w, h in RESOLUTIONS]
        default_resolution_index = resolution_options.index((f'{resolution[0]}x{resolution[1]}', resolution))

        menu.add.selector('Resolution :', resolution_options, onchange=set_resolution, default=default_resolution_index)
        menu.add.button('Clear Save Data', clear_save_data)
        menu.add.button('Return to Game', lambda: menu.disable())
        return menu

    def resize_assets():
        global logo, click_image, logo_rect, click_image_rect, settings_rect, discord_rect, store_rect
        logo = resize_image(pygame.image.load(LOGO_PATH), LOGO_SIZE_RATIO, screen)
        click_image = resize_image(
            pygame.image.load(CLICK_IMAGE_PATH), CLICK_IMAGE_RATIO, screen
        )
        logo_rect = center_image(logo, screen)
        click_image_rect = center_image(click_image, screen)
        settings_rect, discord_rect, store_rect = position_buttons(screen)

    settings_menu = create_settings_menu()
    resize_assets()

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data(click_count, resolution)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if settings_menu.is_enabled():
                        settings_menu.disable()
                    else:
                        settings_menu.enable()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_logo:
                    fade_out(logo, screen)
                    show_logo = False
                else:
                    if click_image_rect.collidepoint(event.pos):
                        click_count += 1
                    elif settings_rect.collidepoint(event.pos):
                        settings_menu.enable()
                    elif discord_rect.collidepoint(event.pos):
                        webbrowser.open("https://discord.com/invite/2nHHHBWNDw")
                    elif store_rect.collidepoint(event.pos):
                        webbrowser.open("https://store.steampowered.com/")

        if show_logo:
            fade_in(logo, screen)
            wait(3)  # Wait for 3 seconds
            fade_out(logo, screen)
            show_logo = False
        elif settings_menu.is_enabled():
            settings_menu.mainloop(screen)
        else:
            screen.blit(click_image, click_image_rect)
            font = pygame.font.Font(None, 74)
            text = font.render(str(click_count), True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(screen.get_width() // 2, 50)))

            screen.blit(settings_icon, settings_rect)
            screen.blit(discord_icon, discord_rect)
            screen.blit(store_icon, store_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
