import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from main import AVLTree
import time


class TreeManager:
    def __init__(self):
        self.trees = {}
        self.current_id = 0

    def add_tree(self, tree):
        self.current_id += 1
        self.trees[self.current_id] = tree
        return self.current_id

    def remove_tree(self, tree_id):
        if tree_id in self.trees:
            del self.trees[tree_id]

    def get_tree_ids(self):
        return list(self.trees.keys())


class TreeVisualization:
    def __init__(self, master):
        self.master = master
        self.master.title("AVL Tree Manager")
        self.master.geometry("1400x900")

        self.tree_manager = TreeManager()
        self.current_frames = {}
        self.active_tree = None
        self.animation_speed = 500  # мСкорость аниации

        self.setup_ui()
        self.create_new_tree()

    def setup_ui(self):
        # Главная панелька
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Tree selection
        self.tree_combobox = ttk.Combobox(control_frame, state='readonly')
        self.tree_combobox.pack(side=tk.LEFT, padx=5)
        self.tree_combobox.bind('<<ComboboxSelected>>', self.on_tree_selected)

        # Кнопки для операций
        op_buttons = [
            ("Добавить", self.add_node),
            ("Удалить", self.delete_node),
            ("Поиск", self.search_node),
            ("Новое дерево", self.create_new_tree),
            ("Разделить", self.split_tree),
            ("Объединить", self.merge_trees),
            ("Прямой обход", self.preorder_traversal),
            ("Центральный обход", self.inorder_traversal),
            ("Обратный обход", self.postorder_traversal),
            ("Количество элементов", self.show_node_count)
        ]

        for text, cmd in op_buttons:
            btn = ttk.Button(control_frame, text=text, command=cmd)
            btn.pack(side=tk.LEFT, padx=2)

        # Ползунок для регулировки скорости анимации
        self.speed_scale = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="Скорость анимации (мс)")
        self.speed_scale.set(self.animation_speed)
        self.speed_scale.pack(side=tk.LEFT, padx=10)
        self.speed_scale.bind("<Motion>", self.update_animation_speed)

        # Место под дерево
        self.tree_container = ttk.Frame(self.master)
        self.tree_container.pack(fill=tk.BOTH, expand=True)

        # Сетка конфигурации
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(1, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(1, weight=1)

    def update_animation_speed(self, event):
        self.animation_speed = self.speed_scale.get()

    def create_new_tree(self, tree=None):
        new_tree = tree if tree else AVLTree()
        if not tree:
            new_tree.generate_random_tree(target_height=3)

        tree_id = self.tree_manager.add_tree(new_tree)
        self.add_tree_frame(tree_id)
        self.update_combobox()
        self.set_active_tree(tree_id)

    def add_tree_frame(self, tree_id):# Новый фраим под дерево
        frame = ttk.Frame(self.tree_container, relief=tk.SUNKEN, padding=5)

        header = ttk.Frame(frame)
        header.pack(fill=tk.X)

        ttk.Label(header, text=f"Дерево #{tree_id}",
                  font=('Arial', 10, 'bold')).pack(side=tk.LEFT)

        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="✖",
                   command=lambda: self.close_tree(tree_id),
                   width=3).pack(side=tk.LEFT)

        # Ну собственно интерфейс
        fig, ax = plt.subplots(figsize=(5, 4))
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.current_frames[tree_id] = {
            'frame': frame,
            'fig': fig,
            'ax': ax,
            'canvas': canvas,
            'header': header
        }

        # Position frame in grid
        row = len(self.current_frames) // 2
        col = len(self.current_frames) % 2
        frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        self.draw_tree(tree_id)

    def update_combobox(self):
        tree_ids = self.tree_manager.get_tree_ids()
        self.tree_combobox['values'] = tree_ids
        if tree_ids and self.active_tree not in tree_ids:
            self.set_active_tree(tree_ids[0])

    def set_active_tree(self, tree_id):
        self.active_tree = tree_id
        if tree_id:
            self.tree_combobox.set(tree_id)
            self.highlight_active_tree()

    def highlight_active_tree(self):
        for tid, frame_data in self.current_frames.items():
            color = '#e1e1e1' if tid == self.active_tree else '#f0f0f0'
            frame_data['frame'].configure(style='Active.TFrame' if tid == self.active_tree else 'TFrame')

    def on_tree_selected(self, event):
        selected_id = int(self.tree_combobox.get())
        self.set_active_tree(selected_id)

    def draw_tree(self, tree_id):
        tree = self.tree_manager.trees[tree_id]
        frame_data = self.current_frames[tree_id]
        ax = frame_data['ax']
        ax.clear()

        G = nx.DiGraph()
        pos = {}
        labels = {}

        def add_nodes(node, x=0, y=0, layer=1):
            if node:
                pos[node.uid] = (x, y)
                labels[node.uid] = str(node.val)
                G.add_node(node.uid)

                if node.left:
                    G.add_edge(node.uid, node.left.uid)
                    add_nodes(node.left, x - 1 / layer, y - 1, layer + 1)
                if node.right:
                    G.add_edge(node.uid, node.right.uid)
                    add_nodes(node.right, x + 1 / layer, y - 1, layer + 1)

        add_nodes(tree.root)

        if G.nodes:
            nx.draw(G, pos, ax=ax, labels=labels, with_labels=True,
                    node_size=800, node_color='#89CFF0',
                    font_size=9, font_weight='bold')

        frame_data['canvas'].draw()

    def close_tree(self, tree_id):
        if tree_id in self.current_frames:
            self.current_frames[tree_id]['frame'].destroy()
            del self.current_frames[tree_id]
            self.tree_manager.remove_tree(tree_id)
            self.update_combobox()
            self.rearrange_frames()

    def rearrange_frames(self):
        for widget in self.tree_container.winfo_children():
            widget.grid_forget()

        # Повторяю все кадры
        for i, (tid, frame_data) in enumerate(self.current_frames.items()):
            row = i // 2
            col = i % 2
            frame_data['frame'].grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

    def add_node(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return

        value = self.get_input("Введите значение для добавления:")
        if value is not None:
            self.tree_manager.trees[self.active_tree].insert(value)
            self.draw_tree(self.active_tree)

    def delete_node(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return

        value = self.get_input("Введите значение для удаления:")
        if value is not None:
            self.tree_manager.trees[self.active_tree].delete(value)
            self.draw_tree(self.active_tree)

    def search_node(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return

        value = self.get_input("Введите значение для поиска:")
        if value is not None:
            count = self.tree_manager.trees[self.active_tree].search_count(value)
            msg = f"Найдено {count} вхождений" if count > 0 else "Не найдено"
            messagebox.showinfo("Результат поиска", msg)

    def split_tree(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return

        value = self.get_input("Введите значение для разделения:")
        if value is None: return

        original_tree = self.tree_manager.trees[self.active_tree]
        left_tree, right_tree = original_tree.split(value)

        self.create_new_tree(left_tree)
        self.create_new_tree(right_tree)
        self.close_tree(self.active_tree)

    def merge_trees(self):
        trees = self.tree_manager.get_tree_ids()
        if len(trees) < 2:
            messagebox.showwarning("Ошибка", "Нужно минимум 2 дерева!")
            return

        merge_dialog = MergeDialog(self.master, trees)
        self.master.wait_window(merge_dialog.top)

        if merge_dialog.result:
            tree1_id, tree2_id = merge_dialog.result
            merged_tree = AVLTree.merge(
                self.tree_manager.trees[tree1_id],
                self.tree_manager.trees[tree2_id]
            )
            self.create_new_tree(merged_tree)
            self.close_tree(tree1_id)
            self.close_tree(tree2_id)

    def get_input(self, prompt):
        try:
            value = simpledialog.askinteger("Ввод значения", prompt)
            return int(value) if value else None
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат числа")
            return None

    def preorder_traversal(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return
        tree = self.tree_manager.trees[self.active_tree]
        nodes = tree.preorder_traversal()
        self.animate_traversal(nodes)

    def inorder_traversal(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return
        tree = self.tree_manager.trees[self.active_tree]
        nodes = tree.inorder_traversal()
        self.animate_traversal(nodes)

    def postorder_traversal(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return
        tree = self.tree_manager.trees[self.active_tree]
        nodes = tree.postorder_traversal()
        self.animate_traversal(nodes)

    def animate_traversal(self, nodes):
        for i, node in enumerate(nodes):
            self.highlight_node(node, nodes[:i + 1])  # Передаем только пройденные узлы
            self.master.update()
            time.sleep(self.animation_speed / 1000)
        self.draw_tree(self.active_tree)

    def highlight_node(self, node, visited_nodes):
        tree_id = self.active_tree
        frame_data = self.current_frames[tree_id]
        ax = frame_data['ax']
        ax.clear()

        G = nx.DiGraph()
        pos = {}
        labels = {}

        def add_nodes(current_node, x=0, y=0, layer=1):
            if current_node:
                pos[current_node.uid] = (x, y)
                labels[current_node.uid] = str(current_node.val)
                G.add_node(current_node.uid)

                if current_node.left:
                    G.add_edge(current_node.uid, current_node.left.uid)
                    add_nodes(current_node.left, x - 1 / layer, y - 1, layer + 1)
                if current_node.right:
                    G.add_edge(current_node.uid, current_node.right.uid)
                    add_nodes(current_node.right, x + 1 / layer, y - 1, layer + 1)

        add_nodes(self.tree_manager.trees[tree_id].root)

        if G.nodes:
            node_colors = []
            for n in G.nodes:
                if n == node.uid:
                    node_colors.append('#FF0000')  # Текущий узел - красный
                elif n in [vn.uid for vn in visited_nodes]:
                    node_colors.append('#FFAAAA')  # Пройденные узлы - светло-красный
                else:
                    node_colors.append('#89CFF0')  # Непройденные узлы

            nx.draw(G, pos, ax=ax, labels=labels, with_labels=True,
                    node_size=800, node_color=node_colors,
                    font_size=9, font_weight='bold')

        frame_data['canvas'].draw()

    def show_node_count(self):
        if not self.active_tree:
            messagebox.showwarning("Ошибка", "Выберите дерево!")
            return
        tree = self.tree_manager.trees[self.active_tree]
        count = len(tree.inorder_traversal())
        messagebox.showinfo("Количество элементов", f"В дереве {count} элементов")


class MergeDialog:
    def __init__(self, parent, tree_ids):
        self.top = tk.Toplevel(parent)
        self.result = None

        ttk.Label(self.top, text="Выберите два дерева для слияния:").pack(padx=10, pady=5)

        self.combo1 = ttk.Combobox(self.top, values=tree_ids, state='readonly')
        self.combo1.pack(padx=10, pady=2)

        self.combo2 = ttk.Combobox(self.top, values=tree_ids, state='readonly')
        self.combo2.pack(padx=10, pady=2)

        btn_frame = ttk.Frame(self.top)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.top.destroy).pack(side=tk.RIGHT, padx=5)

    def ok(self):
        try:
            tree1 = int(self.combo1.get())
            tree2 = int(self.combo2.get())
            if tree1 == tree2:
                messagebox.showerror("Ошибка", "Выберите разные деревья!")
                return
            self.result = (tree1, tree2)
            self.top.destroy()
        except:
            messagebox.showerror("Ошибка", "Некорректный выбор деревьев")
            return


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Active.TFrame', background='#e1e1e1')
    app = TreeVisualization(root)
    root.mainloop()