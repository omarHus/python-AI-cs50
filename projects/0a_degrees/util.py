class Node():
    def __init__(self, state, parent, action, heuristic, cost):
        self.state     = state
        self.parent    = parent
        self.action    = action
        self.heuristic = heuristic
        self.cost      = cost

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

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

class GreedyBestFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # find the lowest age gap Node
            minHeuristic = 100000
            minNode = None
            index = -1
            for node in self.frontier:
                index += 1
                if node.heuristic < minHeuristic:
                    minNode = node
                    minHeuristic  = node.heuristic

            self.frontier.remove(minNode)
            return minNode

class AFrontier(StackFrontier):
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # find the lowest age gap Node
            minHeuristic = 100000
            minNode = None
            index = -1
            for node in self.frontier:
                index += 1
                if node.heuristic + node.cost < minHeuristic:
                    minNode = node
                    minHeuristic  = node.heuristic + node.cost

            self.frontier.remove(minNode)
            return minNode
