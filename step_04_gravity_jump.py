# STEP 4: Gravity and Jumping
# Real physics uses velocity - a speed with a direction.
# Each frame: velocity changes by gravity, then position changes by velocity.
# This creates the arc shape of a jump.

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 4")
clock = pygame.time.Clock()

# Physics constants
GRAVITY = 0.6          # how fast the player speeds up when falling
JUMP_FORCE = -12       # negative = upward (y goes DOWN in pygame)
GROUND_Y = 310         # y position of the ground surface

# Player
player_x = 100
player_y = GROUND_Y
player_size = 40

# Velocity - how many pixels to move each frame
velocity_y = 0
on_ground = True       # is the player currently standing on the ground?

running = True
while running:

    # --- EVENTS (one-time keypresses, not held) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # KEYDOWN fires once when the key is first pressed
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = JUMP_FORCE   # launch upward
                on_ground = False

    # --- UPDATE ---
    # Apply gravity: pull the player downward every frame
    velocity_y += GRAVITY

    # Move the player by its velocity
    player_y += velocity_y

    # Land on the ground
    if player_y >= GROUND_Y:
        player_y = GROUND_Y
        velocity_y = 0
        on_ground = True

    # --- DRAW ---
    screen.fill((50, 50, 80))

    # Ground
    pygame.draw.rect(screen, (100, 180, 100), (0, GROUND_Y + player_size, 800, 400))
    pygame.draw.line(screen, (200, 200, 200), (0, GROUND_Y + player_size), (800, GROUND_Y + player_size), 3)

    # Player
    pygame.draw.rect(screen, (255, 200, 0), (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
