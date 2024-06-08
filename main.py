import os
import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Clicker Game")

# Load assets
assets_dir = "assets"
startup_dir = os.path.join(assets_dir, "startup")
icons_dir = os.path.join(assets_dir, "icons")
clicker_dir = os.path.join(assets_dir, "clicker")

logo = pygame.image.load(os.path.join(startup_dir, "logo.svg"))
settings_icon = pygame.transform.scale(pygame.image.load(os.path.join(icons_dir, "Settings.png")), (75, 75))
discord_icon = pygame.transform.scale(pygame.image.load(os.path.join(icons_dir, "Discord.png")), (75, 75))
store_icon = pygame.transform.scale(pygame.image.load(os.path.join(icons_dir, "Store.png")), (75, 75))
clicker_image = pygame.image.load(os.path.join(clicker_dir, "clicker_image.png"))

# Game state
click_count = 0
is_fullscreen = False
save_data_path = "save_data.txt"

# Load or create save data
if os.path.exists(save_data_path):
    with open(save_data_path, "r") as file:
        click_count = int(file.read())

# Button properties
button_size = (75, 75)
button_padding = 20

# Settings menu
settings_menu_open = False
available_resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
resolution_index = available_resolutions.index((WINDOW_WIDTH, WINDOW_HEIGHT))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                clicker_rect = clicker_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                if clicker_rect.collidepoint(mouse_pos):
                    click_count += 1
                elif not settings_menu_open:
                    button_positions = [
                        (WINDOW_WIDTH // 2 - button_size[0] - button_padding, WINDOW_HEIGHT - button_size[1] - button_padding),
                        (WINDOW_WIDTH // 2, WINDOW_HEIGHT - button_size[1] - button_padding),
                        (WINDOW_WIDTH // 2 + button_size[0] + button_padding, WINDOW_HEIGHT - button_size[1] - button_padding),
                    ]
                    for i, button_pos in enumerate(button_positions):
                        button_rect = pygame.Rect(button_pos, button_size)
                        if button_rect.collidepoint(mouse_pos):
                            if i == 0:
                                settings_menu_open = True
                            elif i == 1:
                                print("Discord button clicked")
                            else:
                                print("Store button clicked")
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.size
            window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

    # Clear the screen
    window.fill((255, 255, 255))

    # Draw the clicker image
    clicker_rect = clicker_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(clicker_image, clicker_rect)

    # Draw the click counter
    font = pygame.font.Font(None, 48)
    text = font.render(f"Clicks: {click_count}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    window.blit(text, text_rect)

    # Draw the buttons
    button_positions = [
        (WINDOW_WIDTH // 2 - button_size[0] - button_padding, WINDOW_HEIGHT - button_size[1] - button_padding),
        (WINDOW_WIDTH // 2, WINDOW_HEIGHT - button_size[1] - button_padding),
        (WINDOW_WIDTH // 2 + button_size[0] + button_padding, WINDOW_HEIGHT - button_size[1] - button_padding),
    ]

    for i, button_pos in enumerate(button_positions):
        button_rect = pygame.Rect(button_pos, button_size)
        if i == 0:
            window.blit(settings_icon, button_rect)
        elif i == 1:
            window.blit(discord_icon, button_rect)
        else:
            window.blit(store_icon, button_rect)

    # Draw the settings menu
    if settings_menu_open:
        settings_menu_rect = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        pygame.draw.rect(window, (200, 200, 200), settings_menu_rect)

        # Draw resolution options
        font = pygame.font.Font(None, 24)
        y = settings_menu_rect.top + 20
        for i, resolution in enumerate(available_resolutions):
            text = font.render(f"{resolution[0]}x{resolution[1]}", True, (0, 0, 0))
            text_rect = text.get_rect(topleft=(settings_menu_rect.left + 20, y))
            window.blit(text, text_rect)
            if i == resolution_index:
                pygame.draw.rect(window, (255, 0, 0), text_rect, 2)
            y += 30

        # Draw fullscreen toggle
        fullscreen_text = font.render("Fullscreen", True, (0, 0, 0))
        fullscreen_text_rect = fullscreen_text.get_rect(topleft=(settings_menu_rect.left + 20, y))
        window.blit(fullscreen_text, fullscreen_text_rect)
        if is_fullscreen:
            pygame.draw.rect(window, (0, 255, 0), fullscreen_text_rect, 2)
        else:
            pygame.draw.rect(window, (255, 0, 0), fullscreen_text_rect, 2)

    # Update the display
    pygame.display.flip()

# Save click count
with open(save_data_path, "w") as file:
    file.write(str(click_count))

# Quit Pygame
pygame.quit()