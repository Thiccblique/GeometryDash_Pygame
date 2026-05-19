# STEP 7: Score + Classes
# We refactor the player and obstacles into classes so each object manages itself.
# Classes are great when an object has its own data AND its own behavior.

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Geometry Dash - Step 7")
clock = pygame.time.Clock()

GRAVITY = 0.6
JUMP_FORCE = -12
GROUND_Y = 310
PLAYER_SIZE = 40
SCROLL_SPEED = 5

font_big = pygame.font.SysFont(None, 64)
font_small = pygame.font.SysFont(None, 36)


class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_Y
        self.size = PLAYER_SIZE
        self.vel_y = 0
        self.on_ground = True
        self.alive = True

    def jump(self):
        if self.on_ground and self.alive:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

    def update(self):
        if not self.alive:
            return
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        color = (255, 50, 50) if not self.alive else (255, 200, 0)
        pygame.draw.rect(surface, color, self.get_rect())
        # Draw an X detail on the square
        if self.alive:
            pygame.draw.rect(surface, (200, 150, 0),
                             (self.x + 5, self.y + 5, self.size - 10, self.size - 10), 2)


class Obstacle:
    def __init__(self):
        self.height = random.choice([40, 60, 80])
        self.rect = pygame.Rect(820, GROUND_Y + PLAYER_SIZE - self.height, 30, self.height)

    def update(self):
        self.rect.x -= SCROLL_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 50, 50), self.rect)
        pygame.draw.rect(surface, (200, 20, 20), self.rect, 2)   # darker border


# ---- Game state ----
player = Player()
obstacles = []
spawn_timer = 0
score = 0
high_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.alive:
                    player.jump()
                else:
                    # Restart
                    high_score = max(high_score, score)
                    player = Player()
                    obstacles = []
                    spawn_timer = 0
                    score = 0

    # --- UPDATE ---
    player.update()

    if player.alive:
        spawn_timer += 1
        if spawn_timer >= 90:
            spawn_timer = 0
            obstacles.append(Obstacle())

        for obs in obstacles:
            obs.update()

        obstacles = [o for o in obstacles if o.rect.right > 0]

        # Collision
        for obs in obstacles:
            if player.get_rect().colliderect(obs.rect):
                player.alive = False

        # Score goes up every frame the player survives
        score += 1

    # --- DRAW ---
    screen.fill((50, 50, 80))

    ground_top = GROUND_Y + PLAYER_SIZE
    pygame.draw.rect(screen, (100, 180, 100), (0, ground_top, 800, 400 - ground_top))
    pygame.draw.line(screen, (200, 200, 200), (0, ground_top), (800, ground_top), 3)

    for obs in obstacles:
        obs.draw(screen)

    player.draw(screen)

    # Score display
    score_text = font_small.render(f"Score: {score // 10}", True, (255, 255, 255))
    best_text = font_small.render(f"Best: {high_score // 10}", True, (180, 180, 180))
    screen.blit(score_text, (10, 10))
    screen.blit(best_text, (10, 40))

    if not player.alive:
        msg = font_big.render("GAME OVER", True, (255, 255, 255))
        sub = font_small.render("Press SPACE to restart", True, (200, 200, 200))
        screen.blit(msg, (800 // 2 - msg.get_width() // 2, 150))
        screen.blit(sub, (800 // 2 - sub.get_width() // 2, 220))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
