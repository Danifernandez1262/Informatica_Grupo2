import tkinter as tk
from tkinter import filedialog, messagebox
from graph import Graph, Node
from test_graph import CreateGraph_1  # Assuming this returns a Graph

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Viewer")
        self.graph = None


        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Show Example Graph", command=self.show_example_graph).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Load Graph from File", command=self.load_from_file).grid(row=0, column=1, padx=5)


        self.node_var = tk.StringVar(root)
        self.node_menu = tk.OptionMenu(root, self.node_var, "")
        self.node_menu.config(width=30)
        self.node_menu.pack(pady=10)

        tk.Button(root, text="Show Neighbors", command=self.show_neighbors).pack(pady=5)

    def show_example_graph(self):
        self.graph = CreateGraph_1()
        self.graph.plot()
        self.update_node_menu()
        messagebox.showinfo("Graph Loaded", "Example graph loaded and shown.")

    def load_from_file(self):
        filepath = filedialog.askopenfilename(title="Select Graph File", filetypes=[("Text Files", "*.txt")])
        if not filepath:
            return

        self.graph = Graph()
        try:
            self.graph.cargar_fichero(filepath)
            self.graph.plot()
            self.update_node_menu()
            messagebox.showinfo("Graph Loaded", f"Graph loaded from {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph: {e}")

    def update_node_menu(self):
        menu = self.node_menu["menu"]
        menu.delete(0, "end")
        if self.graph:
            for node in self.graph.nodes:
                menu.add_command(label=node.name, command=lambda name=node.name: self.node_var.set(name))
            if self.graph.nodes:
                self.node_var.set(self.graph.nodes[0].name)

    def show_neighbors(self):
        if not self.graph:
            messagebox.showwarning("No Graph", "Please load or create a graph first.")
            return
        selected = self.node_var.get()
        if not selected:
            messagebox.showwarning("No Node Selected", "Please select a node.")
            return
        self.graph.plot_node(selected)


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
