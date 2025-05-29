from node import *
from segment import *

n1 = Node('A', 0, 0)
n2 = Node('B', 3, 4)
n3 = Node('C', 6, 8)


s1 = Segment('S1', n1, n2)
s2 = Segment('S2', n2, n3)


print("Nodes:")
for n in [n1, n2, n3]:
    print(f"Name: {n.name}, Coordinates: ({n.x}, {n.y})")


print("\nSegments:")
for s in [s1, s2]:
    print(f"Segment {s.name}: {s.origin.name} -> {s.destination.name}, Cost: {s.cost}")