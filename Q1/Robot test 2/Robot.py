import sys
import Node as n  # Importing the Node class for representing nodes in search algorithms
import PriorityQueueFrontier as pq  # Importing the PriorityQueueFrontier for managing nodes in A* search
from PIL import Image, ImageDraw  # Importing PIL modules for image processing

class Robot():
    def __init__(self, filename):
        # Read the environment from the file
        with open(filename) as f:
            contents = f.read()

        # Split the contents into lines
        contents = contents.splitlines()

        # Determine height and width of the environment
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Initialize lists for walls and dirt locations
        self.walls = []
        self.dirt = []

        # Parse each character in the file and create the environment grid
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        # Set start position
                        self.start = (i, j)
                        row.append("A")
                    elif contents[i][j] == "#":
                        # Add walls
                        row.append("#")
                    elif contents[i][j] == "X":
                        # Add obstacles
                        row.append("X")
                    elif contents[i][j] == "+":
                        # Add dirt locations
                        row.append("+")
                        self.dirt.append((i, j))
                    elif contents[i][j] == " ":
                        # Empty space
                        row.append(" ")
                    else:
                        # Default to wall
                        row.append("#")
                except IndexError:
                    # Handle incomplete rows
                    row.append(" ")
            # Add the row to the walls grid
            self.walls.append(row)

        # Initialize solution and total_cost attributes
        self.solution = None
        self.total_cost = 0

    def print(self):
        # Print the environment grid with specific characters representing the robot, walls, dirt, and solution path
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col == "#":
                    print("█", end="")  # Wall
                elif (i, j) == self.start:
                    print("A", end="")  # Robot start position
                elif col == "X":
                    print("X", end="")  # Obstacle
                elif col == "+":
                    print("+", end="")  # Dirt
                elif col == " ":
                    print(" ", end="")  # Empty space
                elif solution is not None and (i, j) in solution:
                    print("*", end="")  # Solution path
                else:
                    print(" ", end="")
            print()
        print()

    def heuristic(self, state):
        # Calculate the Manhattan distance between the current state and the nearest dirt location
        distances = [abs(state[0] - dirt[0]) + abs(state[1] - dirt[1]) for dirt in self.dirt]
        return min(distances, default=0)

    def neighbors(self, state):
        # Generate neighboring states/actions that the robot can take from the current state
        row, col = state
        candidates = [("up", (row - 1, col)), ("down", (row + 1, col)), ("left", (row, col - 1)), ("right", (row, col + 1))]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:
                if self.walls[r][c] != "#":
                    cost = 1
                    if (r, c) in self.dirt:
                        cost = 3  # Increase cost for cleaning dirt
                    elif self.walls[r][c] == "X":
                        cost = 5  # Increase cost for obstacles
                    result.append((action, (r, c), cost))
        return result

    def solve(self):
        # Implement the A* search algorithm to find the optimal path
        start_node = n.Node(state=self.start, parent=None, action=None, cost=0, f_cost=0)  # Create the start node
        frontier = pq.PriorityQueueFrontier()  # Create the frontier using a priority queue
        frontier.add(start_node)  # Add the start node to the frontier
        self.explored = set()  # Initialize the set of explored states
        self.num_explored = 0  # Initialize the number of states explored
        remaining_dirt = set(self.dirt)  # Initialize the set of remaining dirt locations

        while True:
            if frontier.empty():
                # If the frontier is empty and no solution is found, raise an exception
                raise Exception("no solution")

            current_node = frontier.remove()  # Get the next node from the frontier
            self.num_explored += 1  # Increment the number of states explored

            if current_node.state in remaining_dirt:
                # If the current node is on a dirt location, clean it
                remaining_dirt.remove(current_node.state)
                if not remaining_dirt:
                    # If all dirt locations are cleaned, construct the solution path
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

            self.explored.add(current_node.state)  # Add the current node to the set of explored states

            for action, state, cost in self.neighbors(current_node.state):
                # Iterate over neighboring states
                if not frontier.contains_state(state) and state not in self.explored:
                    # If the state is neither in the frontier nor explored, add it to the frontier
                    new_cost = current_node.cost + cost
                    heuristic = self.heuristic(state)
                    f_cost = new_cost + heuristic
                    next_node = n.Node(state=state, parent=current_node, action=action, cost=new_cost, f_cost=f_cost)
                    frontier.add(next_node)

    def output_image(self, filename, show_solution=True, show_explored=False):
        # Generate an image representation of the environment
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
                    draw.text((j * cell_size + 5, i * cell_size + 5), str(explored_dict[(i, j)]), fill="black")  # Add number to explored cells
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Light yellow for solution path
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Light red for explored but not in solution path
                elif col == "X":
                    fill = (128, 0, 128)  # Purple for obstacles
                else:
                    fill = (237, 240, 252)  # Default light gray for empty space

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)  # Save the generated image to a file


if len(sys.argv) != 2:
    sys.exit("Usage: python Robot.py h1.txt")  # Exit if the script is not called with the correct arguments

r = Robot(sys.argv[1])  # Create a Robot instance with the filename provided as a command-line argument
r.solve()  # Solve the environment
print("States Explored:", r.num_explored)  # Print the number of states explored
print("Total Cost:", r.total_cost)  # Print the total cost of the solution
r.output_image("maze.png", show_explored=True)  # Generate an image representing the environment


