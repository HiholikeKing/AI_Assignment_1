import sys
import Node as n
import PriorityQueueFrontier as pq
from PIL import Image, ImageDraw

class Robot():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)                        
        self.width = max(len(line) for line in contents)   

        self.walls = []
        self.carpets = []
        self.furniture = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)                 
                        row.append("A")                   
                    elif contents[i][j] == "B":
                        self.goal = (i, j)                  
                        row.append("B")
                    elif contents[i][j] == "C":
                        self.carpets.append((i, j))                  
                        row.append("C")
                    elif contents[i][j] == "F":
                        self.furniture.append((i, j))                 
                        row.append("F")                   
                    elif contents[i][j] == " ":
                        row.append(" ")                  
                    else:
                        row.append("#")                   
                except IndexError:
                    row.append(" ")                       
            self.walls.append(row)

        self.solution = None                                

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col == "#":
                    print("█", end="")                    
                elif (i, j) == self.start:
                    print("A", end="")                    
                elif (i, j) == self.goal:
                    print("B", end="")
                elif col == "F":
                    print("F", end="")                 
                elif col == "C":
                    print("C", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")                    
                else:
                    print(" ", end="")                    
            print()
        print()

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])  

    def neighbors(self, state):
        row, col = state
        candidates = [("up", (row - 1, col)), ("down", (row + 1, col)), ("left", (row, col - 1)), ("right", (row, col + 1))]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:  # Check if (r, c) is within grid bounds
                if self.walls[r][c] not in ("#", "F"):  # Check if the cell is not a wall or furniture
                    cost = 1
                    if self.walls[r][c] == "C":
                        cost = 2  
                    result.append((action, (r, c), cost))
        return result

    def solve(self):
        start_node = n.Node(state=self.start, parent=None, action=None, cost=0, f_cost=0)  
        frontier = pq.PriorityQueueFrontier()                  
        frontier.add(start_node)
        self.explored = set()                              
        self.num_explored = 0                              

        while True:
            if frontier.empty():
                raise Exception("no solution")

            current_node = frontier.remove()
            self.num_explored += 1

            if current_node.state == self.goal:
                actions = []
                cells = []
                while current_node.parent is not None:
                    actions.append(current_node.action)
                    cells.append(current_node.state)
                    current_node = current_node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(current_node.state)

            for action, state, cost in self.neighbors(current_node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    new_cost = current_node.cost + cost
                    heuristic = self.heuristic(state)
                    f_cost = new_cost + heuristic
                    next_node = n.Node(state=state, parent=current_node, action=action, cost=new_cost, f_cost=f_cost)
                    frontier.add(next_node)

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col == "#":
                    fill = (40, 40, 40)  # Dark gray for walls
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Red for start
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)  # Green for goal
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Light yellow for solution path
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Light red for explored but not in solution path
                elif col == "F":
                    fill = (0, 0, 255)  # Blue for furniture
                elif col == "C":
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
print("Maze:")
r.print()
print("Solving...")
r.solve()
print("States Explored:", r.num_explored)
print("Solution:")
r.print()
r.output_image("maze.png", show_explored=True)

