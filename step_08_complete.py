# STEP 8: Complete Geometry Dash Clone
# Pulls everything together and adds polish:
#   - Scrolling background stripes
#   - Player rotation while jumping
#   - Particles on death
#   - Double jump
#   - Speed increases over time
#   - Start screen

import pygame
import random
import math

pygame.init()

SCREEN_W, SCREEN_H = 800, 400
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock()

# ── Constants ──────────────────────────────────────────────────────────────────
GRAVITY       = 0.65
JUMP_FORCE    = -13
GROUND_Y      = 300        # top of the ground surface
PLAYER_SIZE   = 36
BASE_SPEED    = 5

font_big   = pygame.font.SysFont(None, 72)
font_mid   = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 30)

# ── Colors ─────────────────────────────────────────────────────────────────────
SKY_TOP    = (30,  30,  60)
SKY_BOT    = (60,  60, 110)
GROUND_COL = (80, 160,  80)
STRIPE_COL = (40,  40,  80)


# ── Helper: draw text centered on x ───────────────────────────────────────────
def draw_centered(surface, font, text, color, cx, y):
    surf = font.render(text, True, color)
    surface.blit(surf, (cx - surf.get_width() // 2, y))


# ── Background ─────────────────────────────────────────────────────────────────
class Background:
    def __init__(self):
        self.offset = 0            # horizontal scroll position

    def update(self, speed):
        self.offset = (self.offset + speed * 0.4) % 80   # stripes repeat every 80px

    def draw(self, surface):
        # Gradient sky (drawn as two rects for simplicity)
        surface.fill(SKY_TOP)
        pygame.draw.rect(surface, SKY_BOT, (0, SCREEN_H // 2, SCREEN_W, SCREEN_H // 2))

        # Diagonal stripes
        for x in range(-80, SCREEN_W + 80, 80):
            pts = [
                (x - self.offset,          0),
                (x - self.offset + 40,     0),
                (x - self.offset + 40 - 60, GROUND_Y),
                (x - self.offset      - 60, GROUND_Y),
            ]
            pygame.draw.polygon(surface, STRIPE_COL, pts)

        # Ground
        pygame.draw.rect(surface, GROUND_COL, (0, GROUND_Y, SCREEN_W, SCREEN_H - GROUND_Y))
        pygame.draw.rect(surface, (60, 130, 60), (0, GROUND_Y, SCREEN_W, 6))


# ── Particle ───────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 7)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 3
        self.life = random.randint(20, 40)
        self.color = random.choice([(255, 200, 0), (255, 100, 50), (255, 255, 100)])
        self.size = random.randint(3, 7)

    def update(self):
        self.vy += 0.3
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        alpha = max(0, self.life * 6)
        pygame.draw.rect(surface, self.color,
                         (int(self.x), int(self.y), self.size, self.size))


# ── Player ─────────────────────────────────────────────────────────────────────
class Player:
    MAX_JUMPS = 2          # allow one double-jump

    def __init__(self):
        self.x = 120
        self.y = float(GROUND_Y - PLAYER_SIZE)
        self.vel_y = 0.0
        self.jumps_left = self.MAX_JUMPS
        self.alive = True
        self.angle = 0.0          # rotation in degrees

    def jump(self):
        if self.jumps_left > 0 and self.alive:
            self.vel_y = JUMP_FORCE
            self.jumps_left -= 1

    def update(self):
        if not self.alive:
            self.angle += 8           # spin when dead
            return

        self.vel_y += GRAVITY
        self.y += self.vel_y

        # Rotate while in the air, snap to nearest 90° on ground
        if self.y < GROUND_Y - PLAYER_SIZE:
            self.angle += 6
        else:
            self.y = float(GROUND_Y - PLAYER_SIZE)
            self.vel_y = 0
            self.jumps_left = self.MAX_JUMPS
            # Snap angle to the nearest multiple of 90
            self.angle = round(self.angle / 90) * 90

    def get_rect(self):
        # Slightly shrink the hitbox so grazing edges doesn't feel unfair
        pad = 4
        return pygame.Rect(self.x + pad, self.y + pad,
                           PLAYER_SIZE - pad * 2, PLAYER_SIZE - pad * 2)

    def draw(self, surface):
        # Rotate the square surface and blit it
        size = PLAYER_SIZE
        sq = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (255, 200, 0) if self.alive else (255, 80, 80)
        pygame.draw.rect(sq, color, (0, 0, size, size))
        pygame.draw.rect(sq, (200, 140, 0), (4, 4, size - 8, size - 8), 2)
        pygame.draw.line(sq, (200, 140, 0), (4, 4), (size - 4, size - 4), 2)
        pygame.draw.line(sq, (200, 140, 0), (size - 4, 4), (4, size - 4), 2)

        rotated = pygame.transform.rotate(sq, -self.angle)
        offset_x = rotated.get_width()  // 2 - size // 2
        offset_y = rotated.get_height() // 2 - size // 2
        surface.blit(rotated, (self.x - offset_x, self.y - offset_y))


# ── Obstacle ───────────────────────────────────────────────────────────────────
class Obstacle:
    HEIGHTS = [36, 54, 72]

    def __init__(self, speed):
        self.h = random.choice(self.HEIGHTS)
        self.rect = pygame.Rect(SCREEN_W + 10,
                                GROUND_Y - self.h,
                                28, self.h)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        # Main body
        pygame.draw.rect(surface, (220, 50, 50), self.rect)
        # Shading
        pygame.draw.rect(surface, (170, 30, 30), self.rect, 3)
        # Triangle spike on top
        tip   = (self.rect.centerx, self.rect.top - 10)
        left  = (self.rect.left,  self.rect.top)
        right = (self.rect.right, self.rect.top)
        pygame.draw.polygon(surface, (255, 80, 80), [tip, left, right])


# ── Game ───────────────────────────────────────────────────────────────────────
class Game:
    STATE_START   = "start"
    STATE_PLAYING = "playing"
    STATE_DEAD    = "dead"

    def __init__(self):
        self.bg = Background()
        self.high_score = 0
        self.reset()
        self.state = self.STATE_START

    def reset(self):
        self.player    = Player()
        self.obstacles = []
        self.particles = []
        self.score     = 0
        self.speed     = BASE_SPEED
        self.spawn_timer = 0
        self.spawn_interval = 100

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
            if self.state == self.STATE_START:
                self.state = self.STATE_PLAYING
            elif self.state == self.STATE_PLAYING:
                self.player.jump()
            elif self.state == self.STATE_DEAD:
                self.high_score = max(self.high_score, self.score // 10)
                self.reset()
                self.state = self.STATE_PLAYING

    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        self.bg.update(self.speed)
        self.player.update()

        # Speed and spawn rate increase with score
        self.speed = BASE_SPEED + (self.score // 600) * 0.5
        self.spawn_interval = max(55, 100 - (self.score // 300) * 5)

        # Spawn obstacles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.obstacles.append(Obstacle(self.speed))

        for obs in self.obstacles:
            obs.update()
        self.obstacles = [o for o in self.obstacles if o.rect.right > 0]

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

        # Collision
        if self.player.alive:
            for obs in self.obstacles:
                if self.player.get_rect().colliderect(obs.rect):
                    self.player.alive = False
                    # Burst of particles at death
                    cx = self.player.x + PLAYER_SIZE // 2
                    cy = self.player.y + PLAYER_SIZE // 2
                    self.particles = [Particle(cx, cy) for _ in range(30)]
                    self.state = self.STATE_DEAD
                    break

        self.score += 1

    def draw(self, surface):
        self.bg.draw(surface)

        for obs in self.obstacles:
            obs.draw(surface)

        self.player.draw(surface)

        for p in self.particles:
            p.draw(surface)

        # HUD
        s = self.score // 10
        score_surf = font_small.render(f"Score: {s}", True, (255, 255, 255))
        best_surf  = font_small.render(f"Best:  {self.high_score}", True, (180, 220, 180))
        surface.blit(score_surf, (10, 10))
        surface.blit(best_surf,  (10, 36))

        # Speed indicator
        spd_surf = font_small.render(f"Speed: {self.speed:.1f}x", True, (180, 180, 255))
        surface.blit(spd_surf, (SCREEN_W - spd_surf.get_width() - 10, 10))

        # Overlays
        if self.state == self.STATE_START:
            draw_centered(surface, font_big,   "GEOMETRY DASH",       (255, 220, 50),  SCREEN_W // 2, 120)
            draw_centered(surface, font_mid,   "Press SPACE to start", (255, 255, 255), SCREEN_W // 2, 200)
            draw_centered(surface, font_small, "SPACE / UP = jump  |  double-jump allowed",
                          (180, 180, 180), SCREEN_W // 2, 250)

        elif self.state == self.STATE_DEAD:
            draw_centered(surface, font_big,   "YOU DIED",             (255,  80,  80), SCREEN_W // 2, 130)
            draw_centered(surface, font_mid,   f"Score: {s}",          (255, 255, 255), SCREEN_W // 2, 200)
            draw_centered(surface, font_small, "Press SPACE to retry", (200, 200, 200), SCREEN_W // 2, 255)


# ── Main loop ──────────────────────────────────────────────────────────────────
game = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    game.update()
    game.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
