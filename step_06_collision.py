# STEP 6: Collision Detection + Game Over
# pygame.Rect has a .colliderect() method that returns True if two rects overlap.
# We also introduce a simple "game state" variable to track playing vs. dead.

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 6")
clock = pygame.time.Clock()

GRAVITY = 0.6
JUMP_FORCE = -12
GROUND_Y = 310
PLAYER_SIZE = 40
SCROLL_SPEED = 5
SPAWN_INTERVAL = 90

# Font for text
font = pygame.font.SysFont(None, 64)   # None = default system font, 64 = size

def reset_game():
    """Return fresh starting values for all game variables."""
    return {
        "player_y": GROUND_Y,
        "velocity_y": 0,
        "on_ground": True,
        "obstacles": [],
        "spawn_timer": 0,
        "alive": True,
    }

state = reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state["alive"] and state["on_ground"]:
                    state["velocity_y"] = JUMP_FORCE
                    state["on_ground"] = False
                elif not state["alive"]:
                    # Restart the game
                    state = reset_game()

    # --- UPDATE (only when alive) ---
    if state["alive"]:
        state["velocity_y"] += GRAVITY
        state["player_y"] += state["velocity_y"]
        if state["player_y"] >= GROUND_Y:
            state["player_y"] = GROUND_Y
            state["velocity_y"] = 0
            state["on_ground"] = True

        # Spawn obstacles
        state["spawn_timer"] += 1
        if state["spawn_timer"] >= SPAWN_INTERVAL:
            state["spawn_timer"] = 0
            height = random.choice([40, 60, 80])
            obs = pygame.Rect(820, GROUND_Y + PLAYER_SIZE - height, 30, height)
            state["obstacles"].append(obs)

        for obs in state["obstacles"]:
            obs.x -= SCROLL_SPEED
        state["obstacles"] = [o for o in state["obstacles"] if o.right > 0]

        # Collision detection
        player_rect = pygame.Rect(100, state["player_y"], PLAYER_SIZE, PLAYER_SIZE)
        for obs in state["obstacles"]:
            if player_rect.colliderect(obs):   # <-- the magic method!
                state["alive"] = False

    # --- DRAW ---
    screen.fill((50, 50, 80))

    ground_top = GROUND_Y + PLAYER_SIZE
    pygame.draw.rect(screen, (100, 180, 100), (0, ground_top, 800, 400 - ground_top))
    pygame.draw.line(screen, (200, 200, 200), (0, ground_top), (800, ground_top), 3)

    for obs in state["obstacles"]:
        pygame.draw.rect(screen, (255, 50, 50), obs)

    # Player: flash red when dead
    color = (255, 50, 50) if not state["alive"] else (255, 200, 0)
    pygame.draw.rect(screen, color, (100, state["player_y"], PLAYER_SIZE, PLAYER_SIZE))

    # Game over message
    if not state["alive"]:
        text = font.render("GAME OVER  (SPACE to restart)", True, (255, 255, 255))
        screen.blit(text, (800 // 2 - text.get_width() // 2, 160))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
