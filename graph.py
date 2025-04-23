import matplotlib.pyplot as plt
from node import *
from segment import Segment

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

    def AddNode(self, n: Node):
        if n not in self.nodes:
            self.nodes.append(n)

    def AddSegment(self, name, name_origin_node, name_destination_node):
        origin = None
        destination = None

        for node in self.nodes:
            if node.name == name_origin_node:
                origin = node
            if node.name == name_destination_node:
                destination = node

        if origin is None or destination is None:
            return False

        segment = Segment(name, origin, destination)
        self.segments.append(segment)
        addneighbor(origin,destination)
        return True

    def get_closest(self, x: float, y: float):
        closest = None
        min_distance = float('inf')

        for node in self.nodes:
            distance = ((node.x - x)**2 + (node.y - y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest = node

        return closest





    def plot(self):
        plt.figure(figsize=(10,8))
        for segment in self.segments:
            plt.plot([segment.origin.x, segment.destination.x],[segment.origin.y, segment.destination.y], 'b-', linewidth = 2)
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=9, color='black')

        for node in self.nodes:
            plt.scatter(node.x, node.y, color='red')
            plt.text(node.x, node.y, f" {node.name}", fontsize=12)

        plt.grid(True, color ='red', linestyle = 'dotted', alpha = 0.7)
        plt.tight_layout()

        plt.show()

    def plot_node(self, name_origin: str):
        origin = next((node for node in self.nodes if node.name == name_origin), None)
        if origin is None:
            return

        plt.figure(figsize=(10,8))

        for segment in self.segments:
            if segment.origin == origin:
                plt.arrow(origin.x, origin.y,
                          segment.destination.x - origin.x, segment.destination.y - origin.y,
                          head_width=0.5, head_length=0.7, fc='r', ec='r', length_includes_head=True)
            elif segment.destination == origin:
                plt.arrow(origin.x, origin.y,
                          segment.origin.x - origin.x, segment.origin.y - origin.y,
                          head_width=0.5, head_length=0.7, fc='r', ec='r', length_includes_head=True)

        for node in self.nodes:
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

    def cargar_fichero(self,fichero):
       fichero = open('text.txt', 'r')
       for linea in fichero:
           linea = linea.strip()
           if not linea:
               continue
           trozos = linea.split()
           if trozos[0] == 'NODO':
               name, x, y = trozos [1], float(trozos[2]), float(trozos[3])
               self.AddNode(Node(name,x,y))
           elif trozos[0] == 'SEGMENTO':
               name, origin, destination = trozos [1], trozos[2], trozos[3]
               self.AddSegment(name, origin, destination)

    def delete_node(self, node_name):
        self.nodes = [node for node in self.nodes if node.name != node_name]
        self.segments = [s for s in self.segments if s.origin.name != node_name and s.destination.name != node_name]

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for node in self.nodes:
                f.write(f"NODO {node.name} {node.x} {node.y}\n")
            for seg in self.segments:
                f.write(f"SEGMENTO {seg.name} {seg.origin.name} {seg.destination.name}\n")

