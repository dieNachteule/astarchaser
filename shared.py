import pygame

# Shared intel class to coordinate chasers
class SharedIntel:
    def __init__(self):
        self.last_seen_pos = None
        self.last_seen_dir = pygame.math.Vector2(1, 0)

# Define map obstacles
obstacles = [
    pygame.Rect(200, 150, 100, 200),
    pygame.Rect(500, 100, 50, 300),
    pygame.Rect(300, 400, 200, 30)
]
