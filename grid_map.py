import pygame
import heapq

TILE_SIZE = 20
GRID_WIDTH = 800 // TILE_SIZE
GRID_HEIGHT = 600 // TILE_SIZE

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

class GridMap:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.grid = [[True for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        self._build_grid()

    def _build_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                for obstacle in self.obstacles:
                    if rect.colliderect(obstacle):
                        self.grid[x][y] = False
                        break

    def is_walkable(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.grid[x][y]

    def find_path(self, start, goal):
        start = (start[0] // TILE_SIZE, start[1] // TILE_SIZE)
        goal = (goal[0] // TILE_SIZE, goal[1] // TILE_SIZE)

        if not self.is_walkable(*start) or not self.is_walkable(*goal):
            return []

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                next_node = (current[0] + dx, current[1] + dy)
                if not self.is_walkable(*next_node):
                    continue

                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        path = []
        current = goal
        while current in came_from and current != start:
            path.append((current[0] * TILE_SIZE + TILE_SIZE // 2, current[1] * TILE_SIZE + TILE_SIZE // 2))
            current = came_from[current]
        path.reverse()
        return path
