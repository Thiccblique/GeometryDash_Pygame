# STEP 2: Drawing Shapes
# pygame.draw lets us draw rectangles, circles, lines, and more.
# A pygame.Rect stores (x, y, width, height) - the top-left corner + size.

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 2")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- DRAW ---
    screen.fill((50, 50, 80))

    # pygame.draw.rect(surface, color, rect)
    # rect = (x, y, width, height)  -- x,y is the TOP-LEFT corner
    pygame.draw.rect(screen, (255, 200, 0), (100, 300, 40, 40))   # yellow player square
    pygame.draw.rect(screen, (255, 50, 50),  (500, 280, 30, 60))  # red obstacle

    # pygame.draw.circle(surface, color, center, radius)
    pygame.draw.circle(screen, (100, 200, 255), (400, 200), 25)   # blue circle

    # pygame.draw.line(surface, color, start_pos, end_pos, width)
    pygame.draw.line(screen, (200, 200, 200), (0, 350), (800, 350), 3)  # ground line

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
