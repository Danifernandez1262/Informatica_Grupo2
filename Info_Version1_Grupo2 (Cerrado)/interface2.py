import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graph import *
import sys

class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Graph Editor")
        self.graph = Graph()


        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()


        self.canvas.mpl_connect("button_press_event", self.on_click)


        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="New Graph", command=self.new_graph).grid(row=0, column=0, padx=3)
        tk.Button(frame, text="Add Segment", command=self.prompt_segment).grid(row=0, column=1, padx=3)
        tk.Button(frame, text="Delete Node", command=self.prompt_delete).grid(row=0, column=2, padx= 3)
        tk.Button(frame, text="Save Graph", command=self.save_graph).grid(row=0, column=3, padx = 3)
        tk.Button(frame, text="Load Graph", command=self.load_graph).grid(row=0, column=4, padx=3)

        self.selected_nodes = []

        self.draw_graph()

    def on_click(self, event) -> None:
        if event.inaxes != self.ax:
            return
        name = simpledialog.askstring("Node Name", "Enter name for the new node:")
        if name:
            AddNode(self.graph, Node(name, event.xdata, event.ydata))
            self.draw_graph()


    def draw_graph(self):
        self.ax.clear()
        for segment in self.graph.segments:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            self.ax.plot(x, y, 'b-')
            mid_x = (x[0] + x[1]) / 2
            mid_y = (y[0] + y[1]) / 2
            self.ax.text(mid_x, mid_y, segment.name, fontsize=8, color='black')

        for node in self.graph.nodes:
            self.ax.plot(node.x, node.y, 'ro')
            self.ax.text(node.x, node.y, f" {node.name}", fontsize=10)

        self.ax.set_title("Click to Add Nodes")
        self.ax.grid(True)
        self.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        name = simpledialog.askstring("Node Name", "Enter name for the new node:")
        if name:
            AddNode(self.graph,Node(name, event.xdata, event.ydata))
            self.draw_graph()

    def prompt_segment(self):
        if len(self.graph.nodes) < 2:
            messagebox.showinfo("Info", "Need at least 2 nodes.")
            return
        options = [node.name for node in self.graph.nodes]
        origin = simpledialog.askstring("Segment", f"Origin node ({', '.join(options)}):")
        destination = simpledialog.askstring("Segment", f"Destination node ({', '.join(options)}):")
        name = simpledialog.askstring("Segment", "Segment name:")
        if origin and destination and name:
            AddSegment(self.graph,name, origin, destination)
            self.draw_graph()

    def prompt_delete(self):
        name = simpledialog.askstring("Delete Node", "Enter node name to delete:")
        if name:
            delete_node(self.graph,name)
            self.draw_graph()

    def new_graph(self):
        self.graph = Graph()
        self.draw_graph()

    def save_graph(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            save_to_file(self.graph,path)
            messagebox.showinfo("Saved", f"Graph saved to {path}")

    def load_graph(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.graph = Graph()
            cargar_fichero(self.graph,path)
            self.draw_graph()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit()))
    root.mainloop()
