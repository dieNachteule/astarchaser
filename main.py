import pygame
from chaser import Chaser
from target import Target
from bullet import Bullet
from shared import SharedIntel, obstacles
from grid_map import GridMap

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game state
intel = SharedIntel()
grid_map = GridMap(obstacles)
target = Target(400, 300)
chasers = [
    Chaser(100, 100, id=0, grid=grid_map),
    Chaser(700, 500, id=1, grid=grid_map),
    Chaser(400, 100, id=2, grid=grid_map),
]
bullets = []

running = True
while running:
    screen.fill((0, 0, 0))
    grid_map.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target.update()

    for chaser in chasers:
        chaser.chase(target, bullets, intel)
        chaser.draw_fov_wedge(screen)
        chaser.draw(screen)

    for bullet in bullets[:]:
        bullet.update(grid_map)
        if not bullet.alive or bullet.is_off_screen(WIDTH, HEIGHT):
            bullets.remove(bullet)
            continue

        if target.is_bullet_blocked(bullet):
            bullets.remove(bullet)
            continue

        bullet.draw(screen)

    target.draw(screen)
    pygame.display.flip()
    clock.tick(60)
