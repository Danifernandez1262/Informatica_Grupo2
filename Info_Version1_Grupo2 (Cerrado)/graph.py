import matplotlib.pyplot as plt
from node import *
from segment import Segment

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

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
    addneighbor(origin,destination)
    return True

def get_closest(G, x, y):
    closest = None
    min_distance = 100

    for node in G.nodes:
        distance = ((node.x - x)**2 + (node.y - y)**2)**0.5
        if distance < min_distance:
            min_distance = distance
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
        if node == origin:
            color= 'gray'
            size= 150
        elif node in origin.neighbors:
            color= 'blue'
            size= 100
        else:
            color = 'blue'
            size = 100
        plt.scatter(node.x, node.y, color=color, s=size)
        plt.text(node.x, node.y, f" {node.name}", fontsize=12)

    plt.tight_layout()
    plt.grid(True, color = 'red', linestyle='dotted', alpha=0.7)

    plt.show()

def cargar_fichero(G,fichero):
   fichero = open('text.txt', 'r')
   for linea in fichero:
       linea = linea.strip()
       if not linea:
           continue
       trozos = linea.split()
       if trozos[0] == 'NODO':
           name, x, y = trozos [1], float(trozos[2]), float(trozos[3])
           AddNode(G, Node(name,x,y))
       elif trozos[0] == 'SEGMENTO':
           name, origin, destination = trozos [1], trozos[2], trozos[3]
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




