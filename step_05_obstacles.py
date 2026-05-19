# STEP 5: Scrolling Obstacles
# In Geometry Dash the player stays in place and obstacles move LEFT toward them.
# We use a list to hold multiple obstacles so we can add and remove them easily.

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 5")
clock = pygame.time.Clock()

GRAVITY = 0.6
JUMP_FORCE = -12
GROUND_Y = 310
PLAYER_SIZE = 40
SCROLL_SPEED = 5       # how fast obstacles move left

# Player
player_x = 100
player_y = GROUND_Y
velocity_y = 0
on_ground = True

# Obstacles - each one is a pygame.Rect (x, y, width, height)
obstacles = []
spawn_timer = 0        # counts frames; spawn a new obstacle every N frames
SPAWN_INTERVAL = 90   # frames between spawns (~1.5 seconds at 60fps)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = JUMP_FORCE
                on_ground = False

    # --- UPDATE ---
    velocity_y += GRAVITY
    player_y += velocity_y
    if player_y >= GROUND_Y:
        player_y = GROUND_Y
        velocity_y = 0
        on_ground = True

    # Spawn a new obstacle off the right edge of the screen
    spawn_timer += 1
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0
        height = random.choice([40, 60, 80])      # vary obstacle heights
        obs = pygame.Rect(820, GROUND_Y + PLAYER_SIZE - height, 30, height)
        obstacles.append(obs)

    # Move every obstacle to the left
    for obs in obstacles:
        obs.x -= SCROLL_SPEED

    # Remove obstacles that have scrolled off the left edge (keep list small)
    obstacles = [obs for obs in obstacles if obs.right > 0]

    # --- DRAW ---
    screen.fill((50, 50, 80))

    # Ground
    ground_top = GROUND_Y + PLAYER_SIZE
    pygame.draw.rect(screen, (100, 180, 100), (0, ground_top, 800, 400 - ground_top))
    pygame.draw.line(screen, (200, 200, 200), (0, ground_top), (800, ground_top), 3)

    # Obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 50, 50), obs)

    # Player
    pygame.draw.rect(screen, (255, 200, 0), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
