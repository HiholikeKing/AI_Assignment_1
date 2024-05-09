import sys
import Node as n
import PriorityQueueFrontier as pq
from PIL import Image, ImageDraw


class Robot():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        # Parses the file contents to identify walls (#),
        # start position (A), dirt locations (+), carpet (X), and empty spaces ().
        # Stores the maze dimensions (height and width).
        # Initializes attributes like walls (2D list representing the maze),
        # dirt (list of dirt locations), start (starting position),
        # and solution (stores path and explored cells after solving).

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        self.wall = []
        self.dirt = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append("A")
                    elif contents[i][j] == "#":
                        row.append("#")
                        self.wall.append((i, j))
                    elif contents[i][j] == "X":
                        row.append("X")
                    elif contents[i][j] == "+":
                        row.append("+")
                        self.dirt.append((i, j))
                    elif contents[i][j] == " ":
                        row.append(" ")
                    else:
                        row.append("#")
                except IndexError:
                    row.append(" ")
            self.walls.append(row)

        self.solution = None
        self.total_cost = 0

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col == "#":
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif col == "X":
                    print("X", end="")
                elif col == "+":
                    print("+", end="")
                elif col == " ":
                    print(" ", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def complex_heuristic(self, state):
        """
        tried dijiskstra algorithm failed to implement

        Calculates a heuristic score for a given robot state.

        Args:
            state: A tuple representing the robot's current coordinates (x, y).

        Returns:
            A float representing the heuristic score. Higher score indicates less desirable location.
        """

        def adjusted_distance_to_obstacle(state):
            """
            Calculates the squared distance to the nearest obstacle.

            Args:
              state: A tuple representing the robot's current coordinates (x, y).

            Distance to nearest obstacle: It calculates the squared distance to the closest wall using adjusted_distance_to_obstacle.
            Squaring the distance emphasizes avoiding obstacles more significantly.
            """
            distances = [abs(state[0] - obstacle[0]) + abs(state[1] - obstacle[1]) for obstacle in self.wall]
            return min(distances, default=0) ** 2

        def distance_to_dirt(state):
            """
            Calculates the Manhattan distance to the nearest dirt location.

            Args:
              state: A tuple representing the robot's current coordinates (x, y).

            Distance to nearest dirt: It calculates the Manhattan distance to the closest dirt location using distance_to_dirt.

            """
            distances = [abs(state[0] - dirt[0]) + abs(state[1] - dirt[1]) for dirt in self.dirt]
            return min(distances, default=0)

        # These weights control the relative importance of avoiding obstacles and reaching dirt locations.
        # By default, obstacles have a higher weight (0.7) to prioritize staying clear of walls.
        # Weight for obstacle influence (0 to 1)
        obstacle_weight = 0.7

        # Weight for dirt proximity (1 - obstacle_weight)
        dirt_weight = 1 - obstacle_weight

        # Combine weighted distances with penalties
        return obstacle_weight * adjusted_distance_to_obstacle(state) + dirt_weight * distance_to_dirt(state)

    def neighbors(self, state):
        row, col = state
        candidates = [("up", (row - 1, col)), ("down", (row + 1, col)), ("left", (row, col - 1)),
                      ("right", (row, col + 1))]
        # Given the current state (robot's position),
        # this method identifies all valid neighboring locations (up, down, left, right)
        # that are within the maze boundaries and not blocked by walls.
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:
                if self.walls[r][c] != "#":
                    cost = 1
                    # 1 for moving to an empty space.
                    if (r, c) in self.dirt:
                        cost = 3  # Increase cost for cleaning dirt
                    elif self.walls[r][c] == "X":
                        cost = 5  # Increase cost for obstacles
                    result.append((action, (r, c), cost))
        return result

    def solve(self):
        start_node = n.Node(state=self.start, parent=None, action=None, cost=0, f_cost=0)
        frontier = pq.PriorityQueueFrontier()
        frontier.add(start_node)
        self.explored = set()
        self.num_explored = 0
        remaining_dirt = set(self.dirt)

        while True:
            if frontier.empty():
                raise Exception("no solution")

            current_node = frontier.remove()
            self.num_explored += 1

            if current_node.state in remaining_dirt:
                # If the current state is a dirty location, it's marked as cleaned in remaining_dirt
                remaining_dirt.remove(current_node.state)
                if not remaining_dirt:
                    actions = []
                    cells = []
                    total_cost = 0
                    while current_node.parent is not None:
                        actions.append(current_node.action)
                        cells.append(current_node.state)
                        total_cost += current_node.cost
                        current_node = current_node.parent
                    actions.reverse()
                    cells.reverse()
                    self.solution = (actions, cells)
                    self.total_cost = total_cost
                    return

            self.explored.add(current_node.state)

            for action, state, cost in self.neighbors(current_node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    new_cost = current_node.cost + cost
                    heuristic = self.complex_heuristic(state)
                    f_cost = new_cost + heuristic
                    next_node = n.Node(state=state, parent=current_node, action=action, cost=new_cost, f_cost=f_cost)
                    frontier.add(next_node)

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 30
        cell_border = 2

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        explored_dict = {state: index for index, state in enumerate(self.explored)}

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col == "#":
                    fill = (40, 40, 40)  # Dark gray for walls
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Red for start
                elif show_explored and (i, j) in self.explored and self.walls[i][j] == "+":
                    fill = (255, 165, 0)  # Orange for explored cells containing "+"
                    draw.text((j * cell_size + 5, i * cell_size + 5), str(explored_dict[(i, j)]),
                              fill="black")  # Add number to explored cells
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Light yellow for solution path
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Light red for explored but not in solution path
                elif col == "X":
                    fill = (128, 0, 128)  # Purple for carpet
                else:
                    fill = (237, 240, 252)  # Default light gray for empty space

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

r = Robot(sys.argv[1])
r.solve()
print("States Explored:", r.num_explored)
print("Total Cost:", r.total_cost)  # Print total cost
r.output_image("maze(CH).png", show_explored=True)
