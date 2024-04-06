import heapq

class GridWorld:
    def __init__(self, width, height, obstacles):
        self.width = width
        self.height = height
        self.obstacles = obstacles

    def is_valid_move(self, x, y):

    def get_neighbors(self, x, y):
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]  # Right, Left, Down, Up
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if self.is_valid_move(nx, ny)]
        return valid_neighbors

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star(grid, start, goal):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            break

        for next_node in grid.get_neighbors(*current_node):
            new_cost = cost_so_far[current_node] + 1  # Cost of moving to next node is 1

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + manhattan_distance(goal, next_node)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current_node

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Example usage:
width = 10
height = 10
obstacles = [(2, 2), (3, 3), (4, 4)]  # Define obstacle coordinates
start = (0, 0)
goal = (9, 9)

grid = GridWorld(width, height, obstacles)
path = a_star(grid, start, goal)
print("Optimal Path:", path)



if __name__ == 'goal':
    Environment = [
        ["0", "0", "0", "1", "1", "1", "1", "0", "0", "0"],
        ["0", "0", "0", "1", "1", "1", "1", "0", "0", "0"],
        ["0", "0", "2", "2", "2", "2", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "2", "2", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "1", "1", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "1", "1", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "1", "1", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "1", "1", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "1", "1", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "1", "1", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "2", "2", "2", "2", "0", "0"],
        ["0", "0", "2", "2", "2", "2", "2", "2", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    ]
