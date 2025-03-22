import pygame
import math
import pygame._sdl2.controller as sdl2_controller

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.shield_angle = 0
        self.last_move_dir = pygame.math.Vector2(1, 0)
        self.radius = 12
        self.controller = None
        self.aim_x = 0
        self.aim_y = 0

        # Initialize SDL2 controller system
        sdl2_controller.init()
        if sdl2_controller.get_count() > 0:
            self.controller = sdl2_controller.Controller(0)

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        # Controller input for movement and aiming
        if self.controller:
            try:
                move_x = self.controller.get_axis(0) / 32768.0
                move_y = self.controller.get_axis(1) / 32768.0
                aim_x = self.controller.get_axis(2) / 32768.0
                aim_y = self.controller.get_axis(3) / 32768.0

                if any(math.isnan(v) for v in (move_x, move_y, aim_x, aim_y)):
                    move_x = move_y = aim_x = aim_y = 0

                # Apply deadzone to movement
                if abs(move_x) < 0.05:
                    move_x = 0
                if abs(move_y) < 0.05:
                    move_y = 0

                move_vec = pygame.math.Vector2(move_x, move_y)
                if move_vec.length() > 1:
                    move_vec = move_vec.normalize()
                dx += move_vec.x * self.speed
                dy += move_vec.y * self.speed

                # Apply deadzone to aim
                if abs(aim_x) < 0.05:
                    aim_x = 0
                if abs(aim_y) < 0.05:
                    aim_y = 0

                self.aim_x = aim_x
                self.aim_y = aim_y

                if math.hypot(aim_x, aim_y) > 0.1:
                    self.shield_angle = math.atan2(-aim_y, aim_x)
            except Exception as e:
                print(f"Controller input error: {e}")

        if dx != 0 or dy != 0:
            self.x += dx
            self.y += dy
            self.last_move_dir = pygame.math.Vector2(dx, dy).normalize()

        # Clamp position to screen bounds
        screen_width, screen_height = 800, 600

        self.x = max(self.radius, min(self.x, screen_width - self.radius))
        self.y = max(self.radius, min(self.y, screen_height - self.radius))

        # Rotate shield with arrow keys
        if keys[pygame.K_RIGHT]:
            self.shield_angle += 0.1
        if keys[pygame.K_LEFT]:
            self.shield_angle -= 0.1

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
        return angle_diff < math.radians(60)

    def hit(self):
        print("Player was hit!")
import pygame
import math
import pygame._sdl2.controller as sdl2_controller

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.shield_angle = 0
        self.last_move_dir = pygame.math.Vector2(1, 0)
        self.radius = 12
        self.controller = None
        self.aim_x = 0
        self.aim_y = 0

        # Initialize SDL2 controller system
        sdl2_controller.init()
        if sdl2_controller.get_count() > 0:
            self.controller = sdl2_controller.Controller(0)

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        # Controller input for movement and aiming
        if self.controller:
            try:
                move_x = self.controller.get_axis(0) / 32768.0
                move_y = self.controller.get_axis(1) / 32768.0
                aim_x = self.controller.get_axis(2) / 32768.0
                aim_y = self.controller.get_axis(3) / 32768.0

                if any(math.isnan(v) for v in (move_x, move_y, aim_x, aim_y)):
                    move_x = move_y = aim_x = aim_y = 0

                # Apply deadzone to movement
                if abs(move_x) < 0.05:
                    move_x = 0
                if abs(move_y) < 0.05:
                    move_y = 0

                move_vec = pygame.math.Vector2(move_x, move_y)
                if move_vec.length() > 1:
                    move_vec = move_vec.normalize()
                dx += move_vec.x * self.speed
                dy += move_vec.y * self.speed

                # Apply deadzone to aim
                if abs(aim_x) < 0.05:
                    aim_x = 0
                if abs(aim_y) < 0.05:
                    aim_y = 0

                self.aim_x = aim_x
                self.aim_y = aim_y

                if math.hypot(aim_x, aim_y) > 0.1:
                    self.shield_angle = math.atan2(-aim_y, aim_x)
            except Exception as e:
                print(f"Controller input error: {e}")

        if dx != 0 or dy != 0:
            self.x += dx
            self.y += dy
            self.last_move_dir = pygame.math.Vector2(dx, dy).normalize()

        # Clamp position to screen bounds
        screen_width, screen_height = 800, 600

        self.x = max(self.radius, min(self.x, screen_width - self.radius))
        self.y = max(self.radius, min(self.y, screen_height - self.radius))

        # Rotate shield with arrow keys
        if keys[pygame.K_RIGHT]:
            self.shield_angle += 0.1
        if keys[pygame.K_LEFT]:
            self.shield_angle -= 0.1

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
        return angle_diff < math.radians(60)

    def hit(self):
        print("Player was hit!")
