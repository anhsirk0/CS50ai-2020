from PIL import Image, ImageDraw, ImageFont
import util
import sys

class Maze():
    def __init__(self, filename):

        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze should have exactly one starting point")

        if contents.count("B") != 1:
            raise Exception("maze should have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.name = filename.split(".")[0]
        self.width = max([len(line) for line in contents])

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)


    def neighbors(self, state):
        y, x = state
        
        neighbors = [
            ("up", (y - 1, x)),
            ("down", (y + 1, x)),
            ("left", (y, x  - 1)),
            ("right", (y, x + 1)),
        ]

        result = []
        for action , (y, x) in neighbors:
            try:
                if not self.walls[y][x]:
                    result.append((action, (y, x)))
            except IndexError:
                continue
        return result


    def print(self):
        print()
        for i in range(self.height):
            for j in range(len(self.walls[i])):
                if (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif self.walls[i][j]:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def create_image(self, show_solution=False):
        solution_cells = [i.state for i in self.solution[1]]
        size = 100
        # inverted image
        total_width = self.height * size
        total_height = self.width * size
        img = Image.new('RGB', (total_height, total_width))
        draw = ImageDraw.Draw(img)
        for i in range(self.height):
            for j in range(len(self.walls[i])):
                y = i*size
                x = j*size
                location = [x, y, x + size, y + size]
                if (i, j) == self.start:
                    img.paste((50, 50, 250), location)
                elif (i, j) == self.goal:
                    img.paste((250, 200, 20), location)
                elif self.walls[i][j]:
                    img.paste((105,105, 105), location)
                elif (i, j) in solution_cells and show_solution:
                    img.paste((5, 200, 5), location)
                else:
                    img.paste((10, 10, 10), location)

        for i in range(self.height):
            draw.line([0, i*size, total_height, i*size])
        for j in range(self.width):
            draw.line([j*size, 0, j*size, total_width])
        img.save(f"{self.name}.png")


    def solve(self):
        self.num_explored = 0
        start = util.Node(
            state=self.start, parent=None, action=None, goal=self.goal
        )
        frontier = util.AstarFrontier()
        frontier.add(start)

        self.explored = set()

        # find solution
        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove(self.goal)
            self.num_explored += 1
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.parent)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if (not frontier.contains_state(state) and
                        state not in self.explored):
                    child = util.Node(state=state,
                                      parent=node,
                                      action=action,
                                      goal=self.goal)
                    frontier.add(child)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: main.py maze.txt")
    maze = Maze(sys.argv[1])
    maze.print()
    maze.solve()
    maze.create_image(True)
    # print(maze.solution[0])
    print(maze.num_explored)
    
if __name__ == "__main__":
    main()
