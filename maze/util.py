class Node():
    def __init__(self, state, parent, action, goal=(0,0)):
        self.state = state
        self.parent = parent
        self.action = action
        if self.parent is None:
            self.cost = 0
        else:
            self.cost = self.parent.cost + 1
        self.distance = abs(state[0] + state[1]
                            - goal[0] - goal[1]) + self.cost

    def __gt__(self, other):
        return True if self.distance > other.distance else False

    def __lt__(self, other):
        return True if self.distance < other.distance else False

    def __eq__(self, other):
        return True if self.distance == other.distance else False

    def __repr__(self):
        return f"{self.state} {self.cost}"


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class AstarFrontier(StackFrontier):

    def remove(self, goal):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # max = cost + goal
            self.frontier.sort()
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
    def __repr__(self):

        nodes = [n.state for n in self.frontier]
        return str(nodes)
