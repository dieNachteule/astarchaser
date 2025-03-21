import pygame
import math

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_pos = (x, y)
        self.last_move_dir = pygame.math.Vector2(1, 0)
        self.shield_angle = 0
        self.shield_fov = math.radians(60)
        self.shield_radius = 25
        self.hit_timer = 0

    def update(self):
        mx, my = pygame.mouse.get_pos()

        # Calculate movement before updating position
        dx = mx - self.x
        dy = my - self.y

        if dx != 0 or dy != 0:
            self.shield_angle = math.atan2(dy, dx)
            self.last_move_dir = pygame.math.Vector2(dx, dy).normalize()

        self.prev_pos = (self.x, self.y)
        self.x, self.y = mx, my

        if self.hit_timer > 0:
            self.hit_timer -= 1

    def draw(self, screen):
        self.draw_shield(screen)
        color = (0, 255, 0) if self.hit_timer == 0 else (255, 255, 255)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 10)

    def draw_shield(self, screen):
        arc_radius = self.shield_radius
        arc_angle = self.shield_fov
        start_angle = self.shield_angle - arc_angle / 2
        num_segments = 10

        points = [(self.x, self.y)]
        for i in range(num_segments + 1):
            theta = start_angle + (i / num_segments) * arc_angle
            px = self.x + arc_radius * math.cos(theta)
            py = self.y + arc_radius * math.sin(theta)
            points.append((px, py))

        pygame.draw.polygon(screen, (0, 200, 255), points)

    def is_bullet_blocked(self, bullet):
        dx = bullet.x - self.x
        dy = bullet.y - self.y
        distance = math.hypot(dx, dy)
        if distance > self.shield_radius + bullet.radius:
            return False

        angle_to_bullet = math.atan2(dy, dx)
        angle_diff = (angle_to_bullet - self.shield_angle + math.pi) % (2 * math.pi) - math.pi
        return abs(angle_diff) <= self.shield_fov / 2

    def hit(self):
        self.hit_timer = 10
