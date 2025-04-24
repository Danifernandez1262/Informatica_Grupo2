import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graph import *
from path import *
import sys


class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Graph Editor")
        self.graph = Graph()

        # Configuración del layout principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para el gráfico
        graph_frame = tk.Frame(main_frame)
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para los botones (columna derecha)
        button_frame = tk.Frame(main_frame, padx=10, pady=10)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuración del gráfico matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Botones de operaciones básicas
        tk.Button(button_frame, text="Nuevo Grafo", command=self.new_graph, width=15).pack(pady=5, fill=tk.X)
        tk.Button(button_frame, text="Añadir Nodo", command=self.enable_add_node, width=15).pack(pady=5, fill=tk.X)
        tk.Button(button_frame, text="Añadir Segmento", command=self.prompt_segment, width=15).pack(pady=5, fill=tk.X)
        tk.Button(button_frame, text="Eliminar Nodo", command=self.prompt_delete, width=15).pack(pady=5, fill=tk.X)

        # Separador
        tk.Frame(button_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # Botones de archivo
        tk.Button(button_frame, text="Cargar Grafo", command=self.load_graph, width=15).pack(pady=5, fill=tk.X)
        tk.Button(button_frame, text="Guardar Grafo", command=self.save_graph, width=15).pack(pady=5, fill=tk.X)
        tk.Button(button_frame, text="Grafo de Prueba", command=self.load_test_graph, width=15).pack(pady=5, fill=tk.X)

        # Separador
        tk.Frame(button_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # Botones de análisis
        tk.Button(button_frame, text="Nodos Alcanzables", command=self.show_reachable_nodes, width=15).pack(pady=5,
                                                                                                            fill=tk.X)
        tk.Button(button_frame, text="Camino Más Corto", command=self.find_shortest_path, width=15).pack(pady=5,
                                                                                                         fill=tk.X)
        tk.Button(button_frame, text="Mostrar Camino", command=self.plot_path, width=15).pack(pady=5, fill=tk.X)

        # Variables de estado
        self.current_path = None
        self.add_node_mode = False

        # Dibujar el grafo vacío inicial
        self.draw_graph()

    def enable_add_node(self):
        self.add_node_mode = True
        messagebox.showinfo("Añadir Nodo", "Haga clic en el gráfico para añadir un nuevo nodo")

    def on_click(self, event):
        if event.inaxes != self.ax or not self.add_node_mode:
            return

        name = simpledialog.askstring("Nombre del Nodo", "Ingrese el nombre para el nuevo nodo:")
        if name:
            AddNode(self.graph, Node(name, event.xdata, event.ydata))
            self.draw_graph()
        self.add_node_mode = False

    def draw_graph(self):
        self.ax.clear()

        # Dibujar segmentos
        for segment in self.graph.segments:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            self.ax.plot(x, y, 'b-')
            mid_x = (x[0] + x[1]) / 2
            mid_y = (y[0] + y[1]) / 2
            self.ax.text(mid_x, mid_y, f"{segment.cost:.1f}", fontsize=8, color='black')

        # Dibujar nodos
        for node in self.graph.nodes:
            self.ax.plot(node.x, node.y, 'ro')
            self.ax.text(node.x, node.y, f" {node.name}", fontsize=10)

        # Resaltar camino actual si existe
        if self.current_path and len(self.current_path.path) > 1:
            x_vals = [node.x for node in self.current_path.path]
            y_vals = [node.y for node in self.current_path.path]
            self.ax.plot(x_vals, y_vals, 'r-', linewidth=2, marker='o', markersize=8)

        self.ax.set_title("Editor de Grafos")
        self.ax.grid(True)
        self.canvas.draw()

    def prompt_segment(self):
        if len(self.graph.nodes) < 2:
            messagebox.showinfo("Información", "Se necesitan al menos 2 nodos.")
            return

        options = [node.name for node in self.graph.nodes]
        origin = simpledialog.askstring("Segmento", f"Nodo origen ({', '.join(options)}):")
        destination = simpledialog.askstring("Segmento", f"Nodo destino ({', '.join(options)}):")

        if origin and destination:
            if AddSegment(self.graph, f"{origin}-{destination}", origin, destination):
                self.draw_graph()
            else:
                messagebox.showerror("Error", "No se pudo crear el segmento. Verifique los nombres.")

    def prompt_delete(self):
        name = simpledialog.askstring("Eliminar Nodo", "Ingrese el nombre del nodo a eliminar:")
        if name:
            delete_node(self.graph, name)
            self.draw_graph()

    def new_graph(self):
        self.graph = Graph()
        self.current_path = None
        self.draw_graph()

    def save_graph(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            save_to_file(self.graph, path)
            messagebox.showinfo("Guardado", f"Grafo guardado en {path}")

    def load_graph(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            self.graph = Graph()
            cargar_fichero(self.graph, path)
            self.current_path = None
            self.draw_graph()

    def load_test_graph(self):
        from test_graph import CreateGraph_1
        self.graph = CreateGraph_1()
        self.current_path = None
        self.draw_graph()
        messagebox.showinfo("Grafo de Prueba", "Grafo de prueba cargado correctamente")

    def show_reachable_nodes(self):
        if not self.graph.nodes:
            messagebox.showinfo("Información", "El grafo está vacío.")
            return

        options = [node.name for node in self.graph.nodes]
        origin = simpledialog.askstring("Nodos Alcanzables", f"Seleccione nodo origen ({', '.join(options)}):")
        if not origin:
            return

        origin_node = next((node for node in self.graph.nodes if node.name == origin), None)
        if not origin_node:
            messagebox.showerror("Error", f"Nodo {origin} no encontrado.")
            return

        reachable = reachable_nodes(self.graph, origin_node)
        reachable_names = [node.name for node in reachable]

        # Resaltar nodos alcanzables
        self.ax.clear()
        for segment in self.graph.segments:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            self.ax.plot(x, y, 'b-')

        for node in self.graph.nodes:
            color = 'green' if node in reachable else 'blue'
            size = 100 if node == origin_node else 80
            self.ax.plot(node.x, node.y, 'o', color=color, markersize=size)
            self.ax.text(node.x, node.y, f" {node.name}", fontsize=10)

        self.ax.set_title(f"Nodos alcanzables desde {origin}")
        self.canvas.draw()

        messagebox.showinfo("Nodos Alcanzables", f"Desde {origin} se puede llegar a: {', '.join(reachable_names)}")

    def find_shortest_path(self):
        if not self.graph.nodes:
            messagebox.showinfo("Información", "El grafo está vacío.")
            return

        options = [node.name for node in self.graph.nodes]
        origin = simpledialog.askstring("Camino Más Corto", f"Nodo origen ({', '.join(options)}):")
        if not origin:
            return

        destination = simpledialog.askstring("Camino Más Corto", f"Nodo destino ({', '.join(options)}):")
        if not destination:
            return

        path = FindShortestPath(self.graph, origin, destination)
        if path:
            self.current_path = path
            path_str = " -> ".join([node.name for node in path.path])
            messagebox.showinfo("Camino Más Corto",
                                f"Camino encontrado!\nNodos: {path_str}\nCosto total: {path.cost:.2f}")
            self.draw_graph()
        else:
            messagebox.showinfo("Camino Más Corto", f"No hay camino entre {origin} y {destination}")

    def plot_path(self):
        if self.current_path:
            PlotPath(self.graph, self.current_path)
        else:
            messagebox.showinfo("Información", "No hay camino para mostrar. Encuentre un camino primero.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit()))
    root.mainloop()