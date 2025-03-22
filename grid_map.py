import pygame
TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15

class GridMap:
    def __init__(self, obstacles):
        self.grid = [[True for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        self.obstacles = obstacles
        for rect in obstacles:
            if isinstance(rect, pygame.Rect):
                for x in range(rect.left, rect.right, TILE_SIZE):
                    for y in range(rect.top, rect.bottom, TILE_SIZE):
                        gx = x // TILE_SIZE
                        gy = y // TILE_SIZE
                        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                            self.grid[gx][gy] = False
            else:
                print(f"⚠️ Invalid obstacle format: {rect}")

    def is_walkable(self, x, y):
        gx = int(x) // TILE_SIZE
        gy = int(y) // TILE_SIZE
        return 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT and self.grid[gx][gy]

    def neighbors(self, x, y):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and self.grid[nx][ny]:
                yield nx, ny

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        import heapq
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.neighbors(*current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

        return []

    def draw(self, screen):
        for rect in self.obstacles:
            if isinstance(rect, pygame.Rect):
                pygame.draw.rect(screen, (100, 100, 100), rect)
