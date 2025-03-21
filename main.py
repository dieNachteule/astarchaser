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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target.update()

    for chaser in chasers:
        chaser.chase(target, bullets, intel)
        chaser.draw_fov_wedge(screen)
        chaser.draw(screen)

    for bullet in bullets[:]:
        bullet.update()

        if bullet.is_off_screen():
            bullets.remove(bullet)
            continue

        if target.is_bullet_blocked(bullet):
            bullet.reflect_from_shield(target.shield_angle)
            bullet.source = None
            continue

        if bullet.collides_with(target):
            target.hit()
            bullets.remove(bullet)
            continue

        for chaser in chasers[:]:
            if bullet.collides_with(chaser) and bullet.source != chaser:
                chaser.take_damage()
                bullets.remove(bullet)
                if chaser.hp <= 0:
                    chasers.remove(chaser)
                break
        else:
            bullet.draw(screen)

    for obstacle in obstacles:
        pygame.draw.rect(screen, (100, 100, 100), obstacle)

    target.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
