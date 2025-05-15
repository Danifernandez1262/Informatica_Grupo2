from graph import *
from node import *
from path import Path

def TestAirspace_Catalunya():
    print("\nTesting Airspace integration - Catalunya...")
    G = Graph()
    G.load_from_airspace("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
    plot(G)

    path = FindShortestPath(G, "SID1.D", "STAR1.A")
    if path:
        print("Found path:")
        for node in path.path:
            print(node.name, end=" -> ")
        print()
    else:
        print("No path found")

def TestAirspace_Spain():
    print("\nTesting Airspace integration - Spain...")
    G = Graph()
    G.load_from_airspace("Spain_nav.txt", "Spain_seg.txt", "Spain_aer.txt")
    plot(G)

    path = FindShortestPath(G, "SID1.D", "STAR1.A")
    if path:
        print("Found path:")
        for node in path.path:
            print(node.name, end=" -> ")
        print()
    else:
        print("No path found")


TestAirspace_Catalunya()
TestAirspace_Spain()
