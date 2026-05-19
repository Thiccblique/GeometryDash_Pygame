# STEP 3: Moving the Player
# We store the player's position in variables and change them with keyboard input.
# pygame.key.get_pressed() checks which keys are held down RIGHT NOW.

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 3")
clock = pygame.time.Clock()

# Player position (top-left corner of the square)
player_x = 100
player_y = 300
player_size = 40
player_speed = 5          # pixels per frame

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- UPDATE ---
    # get_pressed() returns a list of True/False for every key
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Keep the player inside the window
    player_x = max(0, min(player_x, 800 - player_size))
    player_y = max(0, min(player_y, 400 - player_size))

    # --- DRAW ---
    screen.fill((50, 50, 80))
    pygame.draw.line(screen, (200, 200, 200), (0, 350), (800, 350), 3)

    # Draw the player using its current x, y
    pygame.draw.rect(screen, (255, 200, 0), (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
