import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed=5, source=None):
        self.x = x
        self.y = y
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        self.velocity_x = (dx / dist) * speed
        self.velocity_y = (dy / dist) * speed
        self.radius = 4
        self.source = source

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self, screen_width=800, screen_height=600):
        return self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height

    def collides_with(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y
        return math.hypot(dx, dy) < self.radius + getattr(obj, 'radius', 10)

    def reflect_from_shield(self, shield_angle):
        incoming = pygame.math.Vector2(self.velocity_x, self.velocity_y)
        normal = pygame.math.Vector2(math.cos(shield_angle), math.sin(shield_angle))
        reflected = incoming - 2 * incoming.dot(normal) * normal
        self.velocity_x = reflected.x
        self.velocity_y = reflected.y
