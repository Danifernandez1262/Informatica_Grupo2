import math
import matplotlib.pyplot as plt
from node import *
from segment import Segment
from path import *
from AirSpace import AirSpace

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []
        self.airspace = None

    def get_node_by_name(self, name):
        return next((n for n in self.nodes if n.name == name), None)

    def load_from_airspace(self, nav_file, seg_file, aer_file):
        self.airspace = AirSpace()
        self.airspace.load_all(nav_file, seg_file, aer_file)


        for navpoint in self.airspace.navpoints:
            node = Node(navpoint.name, navpoint.x, navpoint.y)
            self.nodes.append(node)


        for navsegment in self.airspace.navsegments:

            origin_nav = self.airspace.get_navpoint_by_number(navsegment.origin_number)
            dest_nav = self.airspace.get_navpoint_by_number(navsegment.destination_number)

            if not origin_nav or not dest_nav:
                print(
                    f"Warning: Missing navpoint for segment {navsegment.origin_number}-{navsegment.destination_number}")
                continue


            origin = self.get_node_by_name(origin_nav.name)
            destination = self.get_node_by_name(dest_nav.name)

            if origin and destination:
                segment = Segment(f"{origin.name}-{destination.name}", origin, destination)
                segment.cost = navsegment.distance
                self.segments.append(segment)
                addneighbor(origin, destination)
            else:
                print(f"Warning: Could not find nodes for segment {origin_nav.name}-{dest_nav.name}")
def AddNode(G, n):
    if n not in G.nodes:
        G.nodes.append(n)

def AddSegment(G, name, name_origin_node, name_destination_node):
    origin = None
    destination = None

    for node in G.nodes:
        if node.name == name_origin_node:
            origin = node
        if node.name == name_destination_node:
            destination = node

    if origin is None or destination is None:
        return False

    segment = Segment(name, origin, destination)
    G.segments.append(segment)
    addneighbor(origin, destination)
    return True

def get_closest(G, x, y):
    closest = None
    min_distance = 100

    for node in G.nodes:
        dist = ((node.x - x)**2 + (node.y - y)**2)**0.5
        if dist < min_distance:
            min_distance = dist
            closest = node

    return closest

def plot(G):
    plt.figure(figsize=(10,8))
    for segment in G.segments:
        plt.plot([segment.origin.x, segment.destination.x],[segment.origin.y, segment.destination.y], 'b-', linewidth = 2)
        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=9, color='black')

    for node in G.nodes:
        plt.scatter(node.x, node.y, color='red')
        plt.text(node.x, node.y, f" {node.name}", fontsize=12)

    plt.grid(True, color ='red', linestyle = 'dotted', alpha = 0.7)
    plt.tight_layout()
    plt.show()

def plot_node(G, name_origin):
    origin = next((node for node in G.nodes if node.name == name_origin), None)
    if origin is None:
        return

    plt.figure(figsize=(10,8))

    for segment in G.segments:
        if segment.origin == origin:
            plt.arrow(origin.x, origin.y,
                      segment.destination.x - origin.x, segment.destination.y - origin.y,
                      head_width=0.5, head_length=0.7, fc='r', ec='r', length_includes_head=True)
        elif segment.destination == origin:
            plt.arrow(origin.x, origin.y,
                      segment.origin.x - origin.x, segment.origin.y - origin.y,
                      head_width=0.5, head_length=0.7, fc='r', ec='r', length_includes_head=True)

    for node in G.nodes:
        color = 'gray' if node == origin else 'blue'
        size = 150 if node == origin else 100
        plt.scatter(node.x, node.y, color=color, s=size)
        plt.text(node.x, node.y, f" {node.name}", fontsize=12)

    plt.tight_layout()
    plt.grid(True, color = 'red', linestyle='dotted', alpha=0.7)
    plt.show()

def cargar_fichero(G, fichero):
    with open(fichero, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            trozos = linea.split()
            if trozos[0] == 'NODO':
                name, x, y = trozos[1], float(trozos[2]), float(trozos[3])
                AddNode(G, Node(name, x, y))
            elif trozos[0] == 'SEGMENTO':
                name, origin, destination = trozos[1], trozos[2], trozos[3]
                AddSegment(G, name, origin, destination)

def delete_node(G, node_name):
    G.nodes = [node for node in G.nodes if node.name != node_name]
    G.segments = [s for s in G.segments if s.origin.name != node_name and s.destination.name != node_name]

def save_to_file(G, filename):
    with open(filename, 'w') as f:
        for node in G.nodes:
            f.write(f"NODO {node.name} {node.x} {node.y}\n")
        for seg in G.segments:
            f.write(f"SEGMENTO {seg.name} {seg.origin.name} {seg.destination.name}\n")

def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

def find_best_path(paths, destination):
    best_index = 0
    best_cost = paths[0].cost + distance(paths[0].path[-1], destination)
    i = 1
    while i < len(paths):
        total_cost = paths[i].cost + distance(paths[i].path[-1], destination)
        if total_cost < best_cost:
            best_index = i
            best_cost = total_cost
        i += 1
    return best_index

def FindShortestPath(G, origin_name, destination_name):
    origin = next((n for n in G.nodes if n.name == origin_name), None)
    destination = next((n for n in G.nodes if n.name == destination_name), None)

    if not origin or not destination:
        return None

    current_paths = [Path(origin)]
    visited = set()

    while current_paths:
        best_index = find_best_path(current_paths, destination)
        current_path = current_paths.pop(best_index)

        last_node = current_path.path[-1]

        if last_node == destination:
            return current_path

        if last_node.name in visited:
            continue

        visited.add(last_node.name)

        for segment in G.segments:
            if segment.origin == last_node and segment.destination.name not in visited:
                new_path = Path(last_node)
                new_path.path = current_path.path + [segment.destination]
                new_path.cost = current_path.cost + segment.cost
                current_paths.append(new_path)

    return None
