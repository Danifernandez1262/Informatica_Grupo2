# interface2.py
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import datetime

from graph import *
from path import *
from kml_export import *

AIRCRAFT_SPEEDS = { #lista de aviones sus velocidades medias.
    "A320": 828,
    "B737": 842,
    "Eurofighter Typhoon": 2495,
    "Falcon 900": 950,
    "Cessna 172": 226}


class GraphGUI: #La clase de la interfaz.
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - Airspace Navigation")
        self.graph = Graph()

        self.current_path = None
        self.add_node_mode = False
        self.path_line_color = 'red'

        self.setup_ui()
        self.draw_graph()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self): #Cerrar
        plt.close('all')
        self.root.destroy()

    def setup_ui(self): #Función con todos los botones de la interfaz y sus usos
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

        # Botones principales
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

        tk.Label(button_frame, text="").pack(pady=5)
        tk.Button(button_frame, text="Exportar a KML", command=self.export_to_kml, width=20).pack(pady=5)
        tk.Button(button_frame, text="Animar avión (KML)", command=self.export_animated_track, width=20).pack(pady=5)
        tk.Button(button_frame, text="Cambiar color línea", command=self.change_path_color, width=20).pack(pady=5)
        tk.Button(button_frame, text="Mostrar Imagen", command=self.show_image, width=20).pack(pady=5)



        # Avión y hora
        tk.Label(button_frame, text="Avión:").pack(pady=2)
        self.aircraft_var = tk.StringVar(value="A320")
        aircraft_menu = tk.OptionMenu(button_frame, self.aircraft_var, *AIRCRAFT_SPEEDS.keys())
        aircraft_menu.config(width=20)
        aircraft_menu.pack(pady=2)

        tk.Label(button_frame, text="Fecha y hora salida:").pack(pady=2)
        self.departure_entry = tk.Entry(button_frame, width=22)
        self.departure_entry.insert(0, "2025-01-01 12:00")
        self.departure_entry.pack(pady=2)

        tk.Button(button_frame, text="Funcionalidades extra", command=self.funcionalidades_extra, width=20).pack(
            pady=5)

    def draw_graph(self): #Ejecuta el grafico.
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
            self.ax.plot(x_vals, y_vals, color=self.path_line_color, linewidth=2, marker='o', markersize=8)

        self.ax.set_title("Editor de Grafos - Airspace")
        self.ax.grid(True)
        self.canvas.draw()

    def enable_add_node(self): #Permite añadir nodos.
        self.add_node_mode = True
        messagebox.showinfo("Añadir Nodo", "Haz clic en el gráfico para añadir un nodo.")

    def on_click(self, event): #Toma como input el cursor y el click.
        if event.inaxes != self.ax or not self.add_node_mode:
            return

        name = simpledialog.askstring("Nuevo Nodo", "Nombre del nodo:")
        if name:
            AddNode(self.graph, Node(name, event.xdata, event.ydata))
            self.draw_graph()
        self.add_node_mode = False

    def prompt_segment(self): #Hace aparecer segmento.
        origin = simpledialog.askstring("Segmento", "Nombre del nodo origen:")
        destination = simpledialog.askstring("Segmento", "Nombre del nodo destino:")
        if origin and destination:
            success = AddSegment(self.graph, f"{origin}-{destination}", origin, destination)
            if not success:
                messagebox.showerror("Error", "Nodo no encontrado.")
            self.draw_graph()

    def prompt_delete(self): #Elimina el nodo elegido por el usuario.
        name = simpledialog.askstring("Eliminar Nodo", "Nombre del nodo a eliminar:")
        if name:
            delete_node(self.graph, name)
            self.draw_graph()

    def load_graph(self): #Carga el graph.
        filename = filedialog.askopenfilename(title="Cargar Grafo", filetypes=[("TXT Files", "*.txt")])
        if filename:
            cargar_fichero(self.graph, filename)
            self.draw_graph()

    def save_graph(self): #Guarda el graph.
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar Grafo",
                                                filetypes=[("TXT Files", "*.txt")])
        if filename:
            save_to_file(self.graph, filename)
            messagebox.showinfo("Guardado", "Grafo guardado correctamente.")

    def load_airspace(self): #Carga el Airspace sobre el graph.
        nav_file = filedialog.askopenfilename(title="NavPoints", filetypes=[("TXT Files", "*.txt")])
        seg_file = filedialog.askopenfilename(title="NavSegments", filetypes=[("TXT Files", "*.txt")])
        aer_file = filedialog.askopenfilename(title="Airports", filetypes=[("TXT Files", "*.txt")])
        if nav_file and seg_file and aer_file:
            self.graph.load_from_airspace(nav_file, seg_file, aer_file)
            self.draw_graph()

    def new_graph(self): #Permite crear un nuevo graph.
        self.graph = Graph()
        self.current_path = None
        self.draw_graph()

    def show_reachable_nodes(self): #Muestra todos los nodos alcanzables de un nodo escogido.
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

    def find_shortest_path(self): #Encuentra camino más corto.
        origin = simpledialog.askstring("Camino más corto", "Nodo de origen:")
        destination = simpledialog.askstring("Camino más corto", "Nodo de destino:")
        if origin and destination:
            path = FindShortestPath(self.graph, origin, destination)
            if path:
                self.current_path = path
                cost_km = path.cost
                aircraft = self.aircraft_var.get()
                speed = AIRCRAFT_SPEEDS.get(aircraft, 800)
                duration_hours = cost_km / speed
                duration = datetime.timedelta(hours=duration_hours)

                try:
                    departure_str = self.departure_entry.get()
                    departure_time = datetime.datetime.strptime(departure_str, "%Y-%m-%d %H:%M")
                    arrival_time = departure_time + duration
                    hora_llegada = arrival_time.strftime("%Y-%m-%d %H:%M")
                except:
                    hora_llegada = "Formato inválido"

                ruta = " -> ".join(n.name for n in path.path)
                messagebox.showinfo(
                    "Camino más corto",
                    f"Avión: {aircraft}\nDistancia: {cost_km:.2f} km\n"
                    f"Velocidad: {speed} km/h\nHora llegada: {hora_llegada}\n\nRuta:\n{ruta}"
                )
                self.draw_graph()
            else:
                messagebox.showerror("Error", "No se encontró camino.")

    def show_airport_points(self): #Muestra los SID y Star de los aeropuertos.
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

    def export_to_kml(self): #Exporta el graph en formato kml para usarlo en Google Earth y permite escoger la manera de marcar los nodos.
        if not self.current_path:
            messagebox.showerror("Error", "Primero debes calcular un camino.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".kml", title="Guardar archivo KML",
                                                 filetypes=[("KML Files", "*.kml")])
        if filename:
            try:
                kml_color = self.convert_color_to_kml(self.path_line_color)
                icon_options = {
                    1: ("Chincheta", "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"),
                    2: ("Avioncito", "http://maps.google.com/mapfiles/kml/shapes/airports.png"),
                    3: ("Ubicación", "http://maps.google.com/mapfiles/kml/pal4/icon54.png"),
                }
                options_str = "\n".join([f"{k}: {v[0]}" for k, v in icon_options.items()])
                choice = simpledialog.askinteger("Icono", f"Elige ícono:\n{options_str}", minvalue=1, maxvalue=3)
                icon_url = icon_options.get(choice, icon_options[1])[1]

                export_to_kml(self.graph, self.current_path.path, filename,
                              color=kml_color, node_icon_url=icon_url)
                messagebox.showinfo("Éxito", f"KML guardado:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    def convert_color_to_kml(self, color): #Permite cambiar el color del camino en Google Earth.
        import matplotlib.colors as mcolors
        try:
            rgba = mcolors.to_rgba(color)
        except ValueError:
            rgba = (1, 0, 0, 1)
        r, g, b, a = [int(x * 255) for x in rgba]
        return f"{a:02x}{b:02x}{g:02x}{r:02x}"

    def change_path_color(self): #Permite cambiar el color del camino.
        if not self.current_path:
            messagebox.showinfo("Sin ruta", "No hay ruta que colorear.")
            return
        color = simpledialog.askstring("Color", "Nombre o código del color:")
        if color:
            import matplotlib.colors as mcolors
            try:
                mcolors.to_rgba(color)
                self.path_line_color = color
                self.draw_graph()
            except ValueError:
                messagebox.showerror("Color inválido", "Color no reconocido.")

    def export_animated_track(self): #Muestra una animación del vuelo a tiempo real (estimaciones).
        if not self.current_path:
            messagebox.showerror("Error", "Primero calcula un camino.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".kml", title="Guardar animación KML",
                                                filetypes=[("KML Files", "*.kml")])
        if filename:
            try:
                aircraft = self.aircraft_var.get()
                speed = AIRCRAFT_SPEEDS.get(aircraft, 800)
                distance_km = self.current_path.cost
                duration_hours = distance_km / speed
                duration_seconds = int(duration_hours * 3600)

                departure_str = self.departure_entry.get()
                start_time = datetime.datetime.strptime(departure_str, "%Y-%m-%d %H:%M")
                iso_start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

                export_track_kml(self.current_path, filename, start_time=iso_start, duration_seconds=duration_seconds)
                messagebox.showinfo("Éxito", f"KML animado guardado:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def show_image(self): #Muestra la foto del grupo
        top = tk.Toplevel(self.root)
        top.title("Imagen")
        img = tk.PhotoImage(file="GRUPO 2.png")
        img = img.subsample(2, 2)
        lbl = tk.Label(top, image=img)
        lbl.image = img
        lbl.pack(padx=10, pady=10)
        top.geometry(f"{img.width()}x{img.height()}")

    def funcionalidades_extra(self): #Añade botón que muestra las funcionalidades extra.
        top = tk.Toplevel(self.root)
        top.title("Mensaje Personalizado")

        tk.Label(top, text="1. Poder cambiar el color del camino más corto.\n 2. Poder elegir los simbolos de los navpoints al exportar a Google Earth. \n "
                           "3.Poder ver una animación de la ruta que seguirá el avión. \n 4. Poder elegir entre diferentes modelos de avión. \n"
                           "5. Poder elegir la fecha y hora de salida", font=("Arial", 12)).pack(padx=20, pady=20)
        tk.Button(top, text="Cerrar", command=top.destroy).pack(pady=10)




if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
