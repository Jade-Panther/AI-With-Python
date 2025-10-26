import sys


class Frontier():
    def __init__(self, type='stack'):
        self.frontier = []
        self.type = type

    def empty(self):
        return len(self.frontier) <= 0
    
    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        if self.type == 'stack':
            return self.frontier.pop()
        else:
            return self.frontier.pop(0)
    
    def hasState(self, state):
        return any(node.state == state for node in self.frontier)
    
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.grid = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                if j < len(contents[i]):
                    char = contents[i][j]
                    if char == 'A':
                        self.start = (i, j)
                        row.append(0)
                    elif char == 'B':
                        self.end = (i, j)
                        row.append(0)
                    elif char == ' ':
                        row.append(0)
                    else:
                        row.append(1)
                else:
                    row.append(1)
            self.grid.append(row)
        

    def getNeighbors(self, state):
        row, col = state
        possible = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        neighbors = []
        for (r, c) in possible:
            if 0 <= r < self.height and 0 <= c < self.width and self.grid[r][c] == 0:
                neighbors.append((r, c))

        return neighbors

    def solve(self):
        self.frontier = Frontier('queue')
        self.visited = set()
        
        self.frontier.add(Node(state=self.start, parent=None, action=None))
        

        while True:
            if self.frontier.empty():
                raise Exception("no solution")
            
            currNode = self.frontier.remove()
            
            if currNode.state == self.end:
                path = []
                while currNode.parent != None:
                    path.append(currNode.state)
                    currNode = currNode.parent
                path.reverse()
                self.solution = path
                return

            self.visited.add(currNode.state)
            
            for state in self.getNeighbors(currNode.state):
                if not self.frontier.hasState(state) and state not in self.visited:
                    self.frontier.add(Node(state=state, parent=currNode, action=None))
      
    def print(self):
        for i, row in enumerate(self.grid):
            str = ''
            for j, col in enumerate(row):
                if col == 1:
                    str += '█'
                elif (i, j) == self.start:
                    str += 'A'
                elif (i, j) == self.end:
                    str += 'B'
                elif (i, j) in self.solution:
                    str += '*'
                else:
                    str += ' '
            print(str)

    def outputImage(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):

                # Walls
                if col == 1:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.end:
                    fill = (0, 171, 28)

                # Solution
                elif self.solution is not None and show_solution and (i, j) in self.solution:
                    fill = (220, 235, 113)

                # Explored
                elif self.solution is not None and show_explored and (i, j) in self.visited:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

maze = Maze('/workspaces/AI-With-Python/Projects1/maze/maze3.txt')
maze.solve()
maze.print()
maze.outputImage('/workspaces/AI-With-Python/Projects1/maze/maze.png')