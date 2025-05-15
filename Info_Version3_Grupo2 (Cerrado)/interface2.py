import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graph import *
from path import *


class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - Airspace Navigation")
        self.graph = Graph()

        self.current_path = None
        self.add_node_mode = False

        self.setup_ui()
        self.draw_graph()


        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        plt.close('all')
        self.root.destroy()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        graph_frame = tk.Frame(main_frame)
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(main_frame, padx=10, pady=10)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_click)

        tk.Button(button_frame, text="Nuevo Grafo", command=self.new_graph, width=20).pack(pady=5)
        tk.Button(button_frame, text="Cargar Airspace", command=self.load_airspace, width=20).pack(pady=5)
        tk.Button(button_frame, text="Cargar Grafo", command=self.load_graph, width=20).pack(pady=5)
        tk.Button(button_frame, text="Guardar Grafo", command=self.save_graph, width=20).pack(pady=5)

        tk.Label(button_frame, text="").pack(pady=5)
        tk.Button(button_frame, text="Añadir Nodo", command=self.enable_add_node, width=20).pack(pady=5)
        tk.Button(button_frame, text="Añadir Segmento", command=self.prompt_segment, width=20).pack(pady=5)
        tk.Button(button_frame, text="Eliminar Nodo", command=self.prompt_delete, width=20).pack(pady=5)

        tk.Label(button_frame, text="").pack(pady=5)
        tk.Button(button_frame, text="Nodos Alcanzables", command=self.show_reachable_nodes, width=20).pack(pady=5)
        tk.Button(button_frame, text="Camino Más Corto", command=self.find_shortest_path, width=20).pack(pady=5)
        tk.Button(button_frame, text="Mostrar SIDs/STARs", command=self.show_airport_points, width=20).pack(pady=5)

    def draw_graph(self):
        self.ax.clear()

        for segment in self.graph.segments:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            self.ax.plot(x, y, 'b-')
            mid_x = (x[0] + x[1]) / 2
            mid_y = (y[0] + y[1]) / 2
            self.ax.text(mid_x, mid_y, f"{segment.cost:.1f}", fontsize=8, color='black')

        for node in self.graph.nodes:
            self.ax.plot(node.x, node.y, 'ro')
            self.ax.text(node.x, node.y, f" {node.name}", fontsize=10)

        if self.current_path and len(self.current_path.path) > 1:
            x_vals = [node.x for node in self.current_path.path]
            y_vals = [node.y for node in self.current_path.path]
            self.ax.plot(x_vals, y_vals, 'r-', linewidth=2, marker='o', markersize=8)

        self.ax.set_title("Editor de Grafos - Airspace")
        self.ax.grid(True)
        self.canvas.draw()

    def enable_add_node(self):
        self.add_node_mode = True
        messagebox.showinfo("Añadir Nodo", "Haz clic en el gráfico para añadir un nodo.")

    def on_click(self, event):
        if event.inaxes != self.ax or not self.add_node_mode:
            return

        name = simpledialog.askstring("Nuevo Nodo", "Nombre del nodo:")
        if name:
            AddNode(self.graph, Node(name, event.xdata, event.ydata))
            self.draw_graph()
        self.add_node_mode = False

    def prompt_segment(self):
        if len(self.graph.nodes) < 2:
            messagebox.showerror("Error", "Debe haber al menos 2 nodos.")
            return

        origin = simpledialog.askstring("Segmento", "Nombre del nodo origen:")
        destination = simpledialog.askstring("Segmento", "Nombre del nodo destino:")

        if origin and destination:
            success = AddSegment(self.graph, f"{origin}-{destination}", origin, destination)
            if not success:
                messagebox.showerror("Error", "Nodo no encontrado.")
            self.draw_graph()

    def prompt_delete(self):
        name = simpledialog.askstring("Eliminar Nodo", "Nombre del nodo a eliminar:")
        if name:
            delete_node(self.graph, name)
            self.draw_graph()

    def load_graph(self):
        filename = filedialog.askopenfilename(title="Cargar Grafo", filetypes=[("TXT Files", "*.txt")])
        if filename:
            cargar_fichero(self.graph, filename)
            self.draw_graph()

    def save_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar Grafo",
                                                filetypes=[("TXT Files", "*.txt")])
        if filename:
            save_to_file(self.graph, filename)
            messagebox.showinfo("Guardado", "Grafo guardado correctamente.")

    def load_airspace(self):
        nav_file = filedialog.askopenfilename(title="NavPoints", filetypes=[("TXT Files", "*.txt")])
        seg_file = filedialog.askopenfilename(title="NavSegments", filetypes=[("TXT Files", "*.txt")])
        aer_file = filedialog.askopenfilename(title="Airports", filetypes=[("TXT Files", "*.txt")])

        if nav_file and seg_file and aer_file:
            self.graph.load_from_airspace(nav_file, seg_file, aer_file)
            self.draw_graph()

    def new_graph(self):
        self.graph = Graph()
        self.current_path = None
        self.draw_graph()

    def show_reachable_nodes(self):
        origin = simpledialog.askstring("Nodos Alcanzables", "Nodo de origen:")
        if not origin:
            return

        node = self.graph.get_node_by_name(origin)
        if node:
            nodes = reachable_nodes(self.graph, node)
            names = ', '.join(n.name for n in nodes)
            messagebox.showinfo("Nodos Alcanzables", f"Nodos alcanzables desde {origin}:\n{names}")
        else:
            messagebox.showerror("Error", "Nodo no encontrado.")

    def find_shortest_path(self):
        origin = simpledialog.askstring("Camino más corto", "Nodo de origen:")
        destination = simpledialog.askstring("Camino más corto", "Nodo de destino:")

        if origin and destination:
            path = FindShortestPath(self.graph, origin, destination)
            if path:
                self.current_path = path
                cost = path.cost
                messagebox.showinfo("Camino más corto",
                                    f"Costo: {cost:.2f}\nRuta: {' -> '.join(n.name for n in path.path)}")
                self.draw_graph()
            else:
                messagebox.showerror("Error", "No se encontró camino.")

    def show_airport_points(self):
        if not self.graph.airspace or not self.graph.airspace.navairports:
            messagebox.showerror("Error", "Primero cargue los datos del airspace.")
            return

        airport_name = simpledialog.askstring("Aeropuerto", "Nombre del aeropuerto:")
        airport = self.graph.airspace.get_airport_by_name(airport_name)

        if airport:
            sids = ', '.join(p.name for p in airport.sids)
            stars = ', '.join(p.name for p in airport.stars)
            messagebox.showinfo("SID/STAR", f"Aeropuerto: {airport.name}\n\nSIDs:\n{sids}\n\nSTARs:\n{stars}")
        else:
            messagebox.showerror("Error", "Aeropuerto no encontrado.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()