# STEP 1: Opening a Window
# This is the minimum code needed to get a pygame window on screen.
# Every pygame program follows this same basic structure.

import pygame

# 1. Initialize pygame (always do this first)
pygame.init()

# 2. Create a window: width=800, height=400
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 1")

# 3. Create a clock to control how fast the loop runs
clock = pygame.time.Clock()

# 4. The game loop - runs forever until the player closes the window
running = True
while running:

    # 5. Handle events (things the user does)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # clicked the X button
            running = False

    # 6. Draw everything
    screen.fill((50, 50, 80))           # fill the screen with a dark blue color
                                        # colors are (Red, Green, Blue), 0-255

    # 7. Show what we drew (flip the hidden buffer to the screen)
    pygame.display.flip()

    # 8. Limit to 60 frames per second
    clock.tick(60)

# 9. Clean up when the loop ends
pygame.quit()
