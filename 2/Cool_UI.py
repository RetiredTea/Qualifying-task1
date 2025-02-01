import tkinter as tk
from tkinter import messagebox
from Associative_array import MyDict
import random
import string


class MyDictUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MyDict Interface")
        self.my_dict = MyDict()

        # Создаем фрейм для кнопок
        self.button_frame = tk.Frame(root, width=200, bg="lightgray")
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.display_frame = tk.Frame(root, bg="white")
        self.display_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Кнопки
        self.add_button = tk.Button(self.button_frame, text="Добавить элемент", command=self.add_item)
        self.add_button.pack(pady=10, padx=10, fill=tk.X)

        self.get_button = tk.Button(self.button_frame, text="Получить элемент", command=self.get_item)
        self.get_button.pack(pady=10, padx=10, fill=tk.X)

        self.delete_button = tk.Button(self.button_frame, text="Удалить элемент", command=self.delete_item)
        self.delete_button.pack(pady=10, padx=10, fill=tk.X)

        self.contains_button = tk.Button(self.button_frame, text="Проверить наличие", command=self.contains_item)
        self.contains_button.pack(pady=10, padx=10, fill=tk.X)

        # Кнопка для добавления 5 случайных элементов
        self.add_random_button = tk.Button(self.button_frame, text="Добавить 5 случайных элементов", command=lambda: self.generate_random_items(5))
        self.add_random_button.pack(pady=10, padx=10, fill=tk.X)

        self.display_text = tk.Text(self.display_frame, wrap=tk.NONE, state=tk.DISABLED)
        self.display_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.update_display()

    def add_item(self):

        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить элемент")

        tk.Label(add_window, text="Ключ:").grid(row=0, column=0, padx=10, pady=10)
        key_entry = tk.Entry(add_window)
        key_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Значение:").grid(row=1, column=0, padx=10, pady=10)
        value_entry = tk.Entry(add_window)
        value_entry.grid(row=1, column=1, padx=10, pady=10)

        def submit():
            key = key_entry.get()
            value = value_entry.get()
            if key and value:
                self.my_dict.put(key, value)
                self.update_display()
                add_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Ключ и значение не могут быть пустыми!")

        tk.Button(add_window, text="Добавить", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

    def get_item(self):
        get_window = tk.Toplevel(self.root)
        get_window.title("Получить элемент")

        tk.Label(get_window, text="Ключ:").grid(row=0, column=0, padx=10, pady=10)
        key_entry = tk.Entry(get_window)
        key_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit():
            key = key_entry.get()
            if key:
                try:
                    value = self.my_dict.get(key)
                    messagebox.showinfo("Результат", f"Значение для ключа '{key}': {value}")
                except KeyError:
                    messagebox.showwarning("Ошибка", f"Ключ '{key}' не найден!")
            else:
                messagebox.showwarning("Ошибка", "Ключ не может быть пустым!")
            get_window.destroy()

        tk.Button(get_window, text="Получить", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_item(self):# Окно для ввода ключа
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Удалить элемент")

        tk.Label(delete_window, text="Ключ:").grid(row=0, column=0, padx=10, pady=10)
        key_entry = tk.Entry(delete_window)
        key_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit():
            key = key_entry.get()
            if key:
                try:
                    value = self.my_dict.delete(key)
                    self.update_display()
                    messagebox.showinfo("Результат", f"Элемент '{key}': {value} удален.")
                except KeyError:
                    messagebox.showwarning("Ошибка", f"Ключ '{key}' не найден!")
            else:
                messagebox.showwarning("Ошибка", "Ключ не может быть пустым!")
            delete_window.destroy()

        tk.Button(delete_window, text="Удалить", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

    def contains_item(self):# Окно для ввода ключа
        contains_window = tk.Toplevel(self.root)
        contains_window.title("Проверить наличие")

        tk.Label(contains_window, text="Ключ:").grid(row=0, column=0, padx=10, pady=10)
        key_entry = tk.Entry(contains_window)
        key_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit():
            key = key_entry.get()
            if key:
                if self.my_dict.contains(key):
                    messagebox.showinfo("Результат", f"Ключ '{key}' присутствует в словаре.")
                else:
                    messagebox.showinfo("Результат", f"Ключ '{key}' отсутствует в словаре.")
            else:
                messagebox.showwarning("Ошибка", "Ключ не может быть пустым!")
            contains_window.destroy()

        tk.Button(contains_window, text="Проверить", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

    def generate_random_items(self, num_items=5):
        # Генерация случайных элементов
        for _ in range(num_items):
            key = ''.join(random.choices(string.ascii_letters, k=5))
            value = random.randint(1, 100)
            self.my_dict.put(key, value)
        self.update_display()
        messagebox.showinfo("Успех", f"Добавлено {num_items} случайных элементов.")

    def update_display(self):
        self.display_text.config(state=tk.NORMAL)
        self.display_text.delete(1.0, tk.END)
        for bucket in self.my_dict.buckets:
            for key, value in bucket:
                self.display_text.insert(tk.END, f"{key}: {value}\n")
        self.display_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyDictUI(root)
    root.mainloop()