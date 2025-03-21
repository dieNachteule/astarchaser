import pygame
import math

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.shield_angle = 0
        self.last_move_dir = pygame.math.Vector2(1, 0)
        self.radius = 12
        self.shield_rotate_speed = 0.1  # radians per frame
        self.joystick = None

        # Initialize joystick if available
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        # Controller input for movement
        if self.joystick:
            dx += self.joystick.get_axis(0) * self.speed
            dy += self.joystick.get_axis(1) * self.speed

        if dx != 0 or dy != 0:
            self.x += dx
            self.y += dy
            self.last_move_dir = pygame.math.Vector2(dx, dy).normalize()

        # Rotate shield with arrow keys
        if keys[pygame.K_RIGHT]:
            self.shield_angle += self.shield_rotate_speed
        if keys[pygame.K_LEFT]:
            self.shield_angle -= self.shield_rotate_speed

        # Controller input for shield aim
        if self.joystick:
            aim_x = self.joystick.get_axis(2)
            aim_y = self.joystick.get_axis(3)
            if abs(aim_x) > 0.2 or abs(aim_y) > 0.2:
                self.shield_angle = math.atan2(aim_y, aim_x)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.radius)

        # Draw shield arc
        shield_radius = self.radius + 10
        arc_angle = math.radians(60)
        start_angle = self.shield_angle - arc_angle / 2
        end_angle = self.shield_angle + arc_angle / 2
        rect = pygame.Rect(self.x - shield_radius, self.y - shield_radius, shield_radius * 2, shield_radius * 2)
        pygame.draw.arc(screen, (0, 200, 255), rect, start_angle, end_angle, 4)

    def is_bullet_blocked(self, bullet):
        dx = bullet.x - self.x
        dy = bullet.y - self.y
        distance = math.hypot(dx, dy)
        if distance > self.radius + 14:
            return False

        angle_to_bullet = math.atan2(dy, dx)
        angle_diff = abs((angle_to_bullet - self.shield_angle + math.pi) % (2 * math.pi) - math.pi)
        return angle_diff < math.radians(30)

    def hit(self):
        print("Player was hit!")