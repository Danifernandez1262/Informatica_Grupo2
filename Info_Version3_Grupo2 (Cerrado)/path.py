import math
import matplotlib.pyplot as plt
from node import Node
from segment import Segment

class Path:
    def __init__(self, node):
        self.path = [node]
        self.cost = 0
        self.origin = node
def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

def AddOriginNode(path, node, name_origin_node):
    if node == name_origin_node and node not in path.path:
        path.origin = node
        path.path.append(node)

def AddNodeToPath(path, node, segment_cost):
    if node not in path.path:
        path.path.append(node)
        path.cost += segment_cost

def ContainsNode(path, node):
    if node in path.path:
        return True
    else:
        return False

def CostToNode(path, node, origin):
    if node not in path.path:
        return -1

    total_cost = 0
    for i in range(1, len(path.path)):
        origin = path.path[i - 1]
        current_node = path.path[i]
        segment_cost = ((current_node.x - origin.x) ** 2 + (current_node.y - origin.y) ** 2) ** 0.5
        total_cost += segment_cost
        if current_node == node:
            return total_cost

    if path.path[0] == node:
        return 0

    return total_cost

def LastNode(path):
    return path.path[-1]

def EstimatedCost(path, destination):
    last_node = LastNode(path)
    final_cost = ((last_node.x - destination.x)**2 + (last_node.y - destination.y)**2)**0.5
    return path.cost + final_cost

def RemovePath(path_container, destination):
    lowest_path = None
    min_cost = 100

    for path in path_container.path:
        current_cost = EstimatedCost(path, destination)
        if current_cost < min_cost:
            min_cost = current_cost
            lowest_path = path

    if lowest_path:
        path_container.path.remove(lowest_path)
        copied_path = Path(lowest_path.origin)
        copied_path.path = lowest_path.path.copy()
        copied_path.cost = lowest_path.cost
        return copied_path


def PlotPath(graph, path):
    plt.figure(figsize=(10, 8))


    for node in graph.nodes:
        plt.plot(node.x, node.y, 'bo')
        plt.text(node.x, node.y, node.name, fontsize=12)


    for segment in graph.segments:
        x_vals = [segment.origin.x, segment.destination.x]
        y_vals = [segment.origin.y, segment.origin.y]
        plt.plot(x_vals, y_vals, 'gray', linestyle='--', alpha=0.5)


    if path and len(path.path) > 1:
        x_vals = [node.x for node in path.path]
        y_vals = [node.y for node in path.path]
        plt.plot(x_vals, y_vals, 'r-', linewidth=2, marker='o', markersize=8)


        for i in range(len(path.path) - 1):
            x_mid = (path.path[i].x + path.path[i + 1].x) / 2
            y_mid = (path.path[i].y + path.path[i + 1].y) / 2
            dx = path.path[i + 1].x - path.path[i].x
            dy = path.path[i + 1].y - path.path[i].y
            segment_cost = (dx ** 2 + dy ** 2) ** 0.5
            plt.text(x_mid, y_mid, f"{segment_cost:.1f}", backgroundcolor='white', fontsize=10)

    plt.title("Graph with Path Highlighted")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()


def reachable_nodes(graph, origin):
    reachable = []
    to_visit = [origin]
    visited = set()

    while to_visit:
        node = to_visit.pop()
        if node not in visited:
            visited.add(node)
            reachable.append(node)

            for segment in graph.segments:
                if segment.origin == node and segment.destination not in visited:
                    to_visit.append(segment.destination)

    return reachable


def shortest_path(graph, origin, destination):
    current_paths = [{'path': [origin], 'cost': 0, 'estimated_cost': distance(origin, destination)}]

    while current_paths:
        best_index = 0
        best_value = current_paths[0]['cost'] + current_paths[0]['estimated_cost']

        for i in range(1, len(current_paths)):
            total_cost = current_paths[i]['cost'] + current_paths[i]['estimated_cost']
            if total_cost < best_value:
                best_value = total_cost
                best_index = i


        current_path = current_paths.pop(best_index)
        last_node = current_path['path'][-1]

        if last_node == destination:
            return current_path['path']


        for segment in graph.segments:
            if segment.origin == last_node and segment.destination not in current_path['path']:
                new_cost = current_path['cost'] + segment.cost
                new_path = current_path['path'] + [segment.destination]
                estimated_cost = distance(segment.destination, destination)
                current_paths.append({'path': new_path, 'cost': new_cost, 'estimated_cost': estimated_cost})

    return None

