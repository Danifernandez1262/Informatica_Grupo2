import math

class Node:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

def addneighbor(n1: Node, n2: Node):
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def distance(n1: Node, n2: Node):
    return math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)


