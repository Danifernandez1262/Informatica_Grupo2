from path import *
from node import *
from segment import *
from graph import *
import matplotlib.pyplot as plt
from NavPoints import NavPoint


def test_path_creation():
    print("\nTest 1: Creación de Path ")
    n1 = Node("A", 0, 0)
    path = Path(n1)

    print(f"Camino creado con nodo origen: {path.origin.name}")
    print(f"Nodos en el camino: {[n.name for n in path.path]}")
    print(f"Costo inicial: {path.cost}")

    if path.origin == n1:
        print("El nodo origen es correcto.")
    else:
        print("El nodo origen no es correcto.")

    if len(path.path) == 1:
        print("El camino contiene 1 nodo.")
    else:
        print(f"El camino contiene {len(path.path)} nodos, no 1")

    print("Test 1 pasado")

def test_navpoint_path():
    print("\nTest 1b: Creación de Path con NavPoint")
    np1 = NavPoint(1, "NAV1", 40.0, -3.0)
    path = Path(np1)

    print(f"Camino creado con nodo origen: {path.origin.name}")
    print(f"Coordenadas: ({path.origin.x}, {path.origin.y})")

    if isinstance(path.origin, NavPoint):
        print("El origen es un NavPoint")
        print(f"Lat/Lon: ({path.origin.lat}, {path.origin.lon})")
    else:
        print("El origen no es un NavPoint")

    print("Test 1b pasado")


def test_add_nodes_to_path():
    print("\nTest 2: Añadir nodos al camino")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 4)
    n3 = Node("C", 6, 8)

    path = Path(n1)
    AddOriginNode(path, n1, n1)
    AddNodeToPath(path, n2, 5.0)
    AddNodeToPath(path, n3, 5.0)

    print(f"Camino actual: {[n.name for n in path.path]}")
    print(f"Costo acumulado: {path.cost}")

    if len(path.path) == 3:
        print("El camino contiene 3 nodos.")
    else:
        print(f"El camino contiene {len(path.path)} nodos, no 3.")

    if path.cost == 10.0:
        print("El costo acumulado es correcto.")
    else:
        print(f"El costo acumulado es {path.cost}, no 10.0.")

    print("Test 2 pasado")


def test_contains_node():
    print("\nTest 3: Verificar nodos en el camino")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 4)
    n3 = Node("C", 6, 8)
    n4 = Node("D", 9, 12)

    path = Path(n1)
    AddOriginNode(path, n1, n1)
    AddNodeToPath(path, n2, 5.0)
    AddNodeToPath(path, n3, 5.0)

    contains_n1 = ContainsNode(path, n1)
    contains_n2 = ContainsNode(path, n2)
    contains_n4 = ContainsNode(path, n4)

    print(f"¿Contiene A? {ContainsNode(path, n1)}")
    print(f"¿Contiene B? {ContainsNode(path, n2)}")
    print(f"¿Contiene D? {ContainsNode(path, n4)}")

    if contains_n1 is True:
        print("El camino contiene a A.")
    else:
        print("El camino no contiene a A.")

    if contains_n2 is True:
        print("El camino contiene a B.")
    else:
        print("El camino no contiene a B.")

    if contains_n4 is False:
        print("El camino no contiene a D.")
    else:
        print("El camino contiene a D.")

    print("Test 3 pasado")


def test_cost_to_node():
    print("\nTest 4: Calcular costo hasta nodo")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 0)
    n3 = Node("C", 3, 4)

    path = Path(n1)
    AddOriginNode(path, n1, n1)
    AddNodeToPath(path, n2, 3.0)
    AddNodeToPath(path, n3, 4.0)

    cost_a = CostToNode(path, n1, n1)
    cost_b = CostToNode(path, n2, n1)
    cost_c = CostToNode(path, n3, n1)
    cost_d = CostToNode(path, Node("D", 0, 0), n1)

    print(f"Costo hasta A: {cost_a}")
    print(f"Costo hasta B: {cost_b}")
    print(f"Costo hasta C: {cost_c}")
    print(f"Costo hasta D: {cost_d}")

    if abs(cost_a - 0) < 0.001:
        print("El costo hasta A es correcto.")
    else:
        print(f"El costo hasta A es incorrecto. Esperado: 0, Obtenido: {cost_a}")

    if abs(cost_b - 3.0) < 0.001:
        print("El costo hasta B es correcto.")
    else:
        print(f"El costo hasta B es incorrecto. Esperado: 3.0, Obtenido: {cost_b}")

    if abs(cost_c - 7.0) < 0.001:
        print("El costo hasta C es correcto.")
    else:
        print(f"El costo hasta C es incorrecto. Esperado: 7.0, Obtenido: {cost_c}")

    if cost_d == -1:
        print("El costo hasta D es correcto (no existe el nodo).")
    else:
        print(f"El costo hasta D es incorrecto. Esperado: -1, Obtenido: {cost_d}")

    print("Test 4 pasado")

def test_last_node():
    print("\nTest 5: Obtener último nodo del camino")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 1, 1)

    path = Path(n1)
    AddOriginNode(path, n1, n1)
    AddNodeToPath(path, n2, 1.41)

    last = LastNode(path)
    print(f"Último nodo: {last.name}")
    if last == n2:
        print("El último nodo es correcto (es B).")
    else:
        print(f"El último nodo es incorrecto. Esperado: B, Obtenido: {last.name}")

    print("Test 5 pasado")


def test_estimated_cost():
    print("\nTest 6: Costo estimado hasta destino")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 4)

    path = Path(n1)
    AddOriginNode(path, n1, n1)
    AddNodeToPath(path, n2, 5.0)

    destination = Node("C", 6, 8)
    estimated = EstimatedCost(path, destination)
    print(f"Costo estimado hasta C: {estimated}")
    if abs(estimated - 10.0) < 0.1:
        print("El costo estimado es correcto.")
    else:
        print(f"El costo estimado es incorrecto. Esperado: 10.0, Obtenido: {estimated}")

    print("Test 6 pasado")


def test_remove_path():
    print("\nTest 7: Eliminar camino con menor costo estimado")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 1, 1)
    n3 = Node("C", 2, 2)

    p1 = Path(n1)
    AddOriginNode(p1, n1, n1)
    AddNodeToPath(p1, n2, 1.4)

    p2 = Path(n1)
    AddOriginNode(p2, n1, n1)
    AddNodeToPath(p2, n3, 2.8)

    lista = Path(None)
    lista.path = [p1, p2]

    destino = Node("D", 3, 3)
    seleccionado = RemovePath(lista, destino)

    print(f"Camino seleccionado: {[n.name for n in seleccionado.path]}")
    if len(seleccionado.path) > 1:
        selected_node = seleccionado.path[1]
        if selected_node.name == n2.name and selected_node.x == n2.x and selected_node.y == n2.y:
            print("El nodo en la posición 1 es el esperado.")
        else:
            print(f"El nodo en la posición 1 es {selected_node.name}, no {n2.name}")
    else:
        print("El camino seleccionado no tiene suficientes nodos.")

    print("Test 7 completado")

def test_plot_path():
    print("\nTest 8: Mostrar gráfico del camino")
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 4)
    n3 = Node("C", 6, 8)

    g = Graph()
    g.nodes = [n1, n2, n3]
    g.segments = [Segment("Segmento n1-n2",n1, n2), Segment("Segmento n2-n3",n2, n3)]

    p = Path(n1)
    AddOriginNode(p, n1, n1)
    AddNodeToPath(p, n2, 5.0)
    AddNodeToPath(p, n3, 5.0)

    print("Mostrando gráfico (cerrar ventana para continuar)...")
    PlotPath(g, p)
    print("Test 8 pasado")



def test_airspace_path():
    print("\nTest 9: Camino con datos de AirSpace")

    airspace = AirSpace()


    airspace.navpoints = [
        NavPoint(1, "NAV1", 40.0, -3.0),
        NavPoint(2, "NAV2", 40.1, -3.1),
        NavPoint(3, "NAV3", 40.2, -3.2)
    ]


    g = Graph()
    g.nodes = airspace.navpoints
    g.segments = [
        Segment("S1", g.nodes[0], g.nodes[1]),
        Segment("S2", g.nodes[1], g.nodes[2])
    ]


    p = Path(g.nodes[0])
    AddNodeToPath(p, g.nodes[1], distance(g.nodes[0], g.nodes[1]))
    AddNodeToPath(p, g.nodes[2], distance(g.nodes[1], g.nodes[2]))

    print(f"Camino creado: {[n.name for n in p.path]}")
    print(f"Costo total: {p.cost}")


    print("Mostrando gráfico de ruta aérea...")
    PlotPath(g, p)
    print("Test 9 pasado")


if __name__ == "__main__":
    test_path_creation()
    test_navpoint_path()
    test_add_nodes_to_path()
    test_contains_node()
    test_cost_to_node()
    test_last_node()
    test_estimated_cost()
    test_remove_path()
    test_plot_path()
    test_airspace_path()

    print("\nTodos los tests completados correctamente.")
