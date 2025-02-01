class MyDict:
    def __init__(self, initial_size=8):
        self.size = initial_size
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        self.load_factor = 0.7

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        if self.count / self.size >= self.load_factor:
            self.resize()
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return v
        raise KeyError(f"Key {key} not found")

    def contains(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return True
        return False

    def resize(self):
        new_size = self.size * 2
        new_buckets = [[] for _ in range(new_size)]
        for bucket in self.buckets:
            for key, value in bucket:
                index = hash(key) % new_size
                new_buckets[index].append((key, value))
        self.size = new_size
        self.buckets = new_buckets


class MyDictUI:
    def __init__(self):
        self.my_dict = MyDict()

    def start(self):
        while True:
            print("\n1. Добавить элемент")
            print("2. Получить элемент")
            print("3. Удалить элемент")
            print("4. Проверить наличие элемента")
            print("5. Выйти")
            choice = input("Выберите действие: ")

            if choice == '1':
                key = input("Введите ключ: ")
                value = input("Введите значение: ")
                self.my_dict.put(key, value)
                print(f"Элемент {key}: {value} добавлен.")
            elif choice == '2':
                key = input("Введите ключ: ")
                try:
                    value = self.my_dict.get(key)
                    print(f"Значение для ключа {key}: {value}")
                except KeyError as e:
                    print(e)
            elif choice == '3':
                key = input("Введите ключ: ")
                try:
                    value = self.my_dict.delete(key)
                    print(f"Элемент {key}: {value} удален.")
                except KeyError as e:
                    print(e)
            elif choice == '4':
                key = input("Введите ключ: ")
                if self.my_dict.contains(key):
                    print(f"Ключ {key} присутствует в словаре.")
                else:
                    print(f"Ключ {key} отсутствует в словаре.")
            elif choice == '5':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите действие от 1 до 5.")

