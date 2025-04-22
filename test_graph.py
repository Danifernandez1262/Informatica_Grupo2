from graph import *

def CreateGraph_1():
    G = Graph()
    G.AddNode(Node("A",1,20))
    G.AddNode(Node("B",8,17))
    G.AddNode(Node("C",15,20))
    G.AddNode(Node("D",18,15))
    G.AddNode(Node("E",2,4))
    G.AddNode(Node("F",6,5))
    G.AddNode(Node("G",12,12))
    G.AddNode(Node("H",10,3))
    G.AddNode(Node("I",19,1))
    G.AddNode(Node("J",13,5))
    G.AddNode(Node("K",3,15))
    G.AddNode(Node("L",4,10))

    G.AddSegment("AB","A","B")
    G.AddSegment("AE","A","E")
    G.AddSegment("AK","A","K")
    G.AddSegment("BA","B","A")
    G.AddSegment("BC","B","C")
    G.AddSegment("BF","B","F")
    G.AddSegment("BK","B","K")
    G.AddSegment("BG","B","G")
    G.AddSegment("CD","C","D")
    G.AddSegment("CG","C","G")
    G.AddSegment("DG","D","G")
    G.AddSegment("DH","D","H")
    G.AddSegment("DI","D","I")
    G.AddSegment("EF","E","F")
    G.AddSegment("FL","F","L")
    G.AddSegment("GB","G","B")
    G.AddSegment("GF","G","F")
    G.AddSegment("GH","G","H")
    G.AddSegment("ID","I","D")
    G.AddSegment("IJ","I","J")
    G.AddSegment("JI","J","I")
    G.AddSegment("KA","K","A")
    G.AddSegment("KL","K","L")
    G.AddSegment("LK","L","K")
    G.AddSegment("LF","L","F")
    return G

# Uso del grafo
print("Probando el grafo...")
G = CreateGraph_1()
G.plot()
G.plot_node("C")

n = G.get_closest(15,5)
print(n.name) # La respuesta debe ser J

n = G.get_closest(8,19)
print(n.name) # La respuesta debe ser B

# Segundo grafo desde archivo
G2 = Graph()
G2.cargar_fichero('text.txt')
G2.plot()

print("Nodos cargados desde archivo:")
for node in G2.nodes:
    print(f"- {node.name} ({node.x}, {node.y})")

print("Segmentos cargados desde archivo:")
for seg in G2.segments:
    print(f"- {seg.name}: {seg.origin.name} -> {seg.destination.name}")

n = G2.get_closest(1.1, 2.1)
print("Nodo más cercano a (1.1, 2.1):", n.name)
