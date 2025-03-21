import pygame
import math
import random
from shared import obstacles
from bullet import Bullet

class Chaser:
    group_target = None  # Class-level shared target for group convergence

    def __init__(self, x, y, id=0, grid=None):
        self.x = x
        self.y = y
        self.id = id
        self.hp = 2
        self.hit_flash = 0
        self.speed = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_seen = None
        self.last_seen_dir = pygame.math.Vector2(1, 0)
        self.exploring = True
        self.path = []
        self.search_timer = 180
        self.shoot_cooldown = 0
        self.facing_angle = 0
        self.grid = grid
        self.stare_timer = 15
        self.corner_checks = []

    def take_damage(self):
        self.hp -= 1
        self.hit_flash = 10

    def _lerp_angle(self, a, b, t):
        diff = (b - a + math.pi) % (2 * math.pi) - math.pi
        return a + diff * t

    def has_line_of_sight(self, tx, ty, fov_degrees=60):
        dx = tx - self.x
        dy = ty - self.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return True

        dir_to_target = pygame.math.Vector2(dx, dy).normalize()
        facing_dir = pygame.math.Vector2(math.cos(self.facing_angle), math.sin(self.facing_angle))
        dot_product = facing_dir.dot(dir_to_target)
        clamped_dot = max(-1.0, min(1.0, dot_product))
        angle_between = math.acos(clamped_dot)

        if angle_between > math.radians(fov_degrees / 2):
            return False

        for obstacle in obstacles:
            if obstacle.clipline((self.x, self.y), (tx, ty)):
                return False

        return True

    def chase(self, target, bullets, intel):
        if self.hp <= 0:
            return

        saw_target = self.has_line_of_sight(target.x, target.y)
        if saw_target:
            self.last_seen = (int(target.x), int(target.y))
            self.last_seen_dir = target.last_move_dir
            intel.last_seen_pos = self.last_seen
            intel.last_seen_dir = self.last_seen_dir
            self.exploring = False
            self.corner_checks = []
            Chaser.group_target = self.last_seen  # Set group target for convergence
            self.path = self.grid.find_path((int(self.x), int(self.y)), self.last_seen)
            self.stare_timer = 15
            if self.shoot_cooldown <= 0:
                bullets.append(Bullet(self.x, self.y, target.x, target.y, source=self))
                self.shoot_cooldown = 60

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if not saw_target and self.stare_timer > 0:
            self.stare_timer -= 1
            return

        if not self.path:
            if Chaser.group_target:
                self.path = self.grid.find_path((int(self.x), int(self.y)), Chaser.group_target)
                return
            if self.corner_checks:
                next_corner = self.corner_checks.pop(0)
                self.path = self.grid.find_path((int(self.x), int(self.y)), (int(next_corner[0]), int(next_corner[1])))
            elif self.last_seen:
                lx, ly = self.last_seen
                dir = self.last_seen_dir
                full_checks = [
                    (lx + dir.x * 40 + dx * 40, ly + dir.y * 40 + dy * 40)
                    for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                    if not (dx == 0 and dy == 0)
                ]
                offset = self.id % len(full_checks)
                full_checks = full_checks[offset:] + full_checks[:offset]
                self.corner_checks = full_checks
            elif self.exploring and self.search_timer <= 0:
                target_pos = (
                    int(self.x) + random.choice([-1, 0, 1]) * 100,
                    int(self.y) + random.choice([-1, 0, 1]) * 100
                )
                self.path = self.grid.find_path((int(self.x), int(self.y)), (int(target_pos[0]), int(target_pos[1])))
                self.search_timer = 180
            elif self.exploring:
                self.search_timer -= 1

        if self.path:
            tx, ty = self.path[0]
            dx = tx - self.x
            dy = ty - self.y
            distance = math.hypot(dx, dy)

            if distance < 5:
                self.x, self.y = tx, ty
                self.path.pop(0)
                return

            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
            self.x += self.velocity_x
            self.y += self.velocity_y

            if abs(self.velocity_x) > 0.5 or abs(self.velocity_y) > 0.5:
                target_angle = math.atan2(self.velocity_y, self.velocity_x)
                self.facing_angle = self._lerp_angle(self.facing_angle, target_angle, 0.3)

    def draw(self, screen):
        if self.hp <= 0:
            return
        color = (255, 0, 0) if self.hit_flash == 0 else (255, 128, 128)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 10)
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def draw_fov_wedge(self, screen):
        if self.hp <= 0:
            return
        radius = 80
        angle = math.radians(60)
        base_angle = self.facing_angle
        num_points = 15
        points = [(self.x, self.y)]
        for i in range(num_points + 1):
            theta = base_angle - angle / 2 + (angle * i / num_points)
            px = self.x + radius * math.cos(theta)
            py = self.y + radius * math.sin(theta)
            points.append((px, py))
        surface = pygame.Surface((800, 600), pygame.SRCALPHA)
        pygame.draw.polygon(surface, (255, 0, 0, 64), points)
        screen.blit(surface, (0, 0))
