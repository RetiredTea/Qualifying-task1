import random


class Node:
    def __init__(self, val, left=None, right=None, uid=None):
        self.val = val
        self.left = left
        self.right = right
        self.height = 1
        self.uid = uid


class AVLTree:
    def __init__(self):
        self.node_id_counter = 0
        self.root = None

    def get_height(self, node: Node) -> int:
        return node.height if node else 0

    def update_height(self, node: Node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node: Node) -> int:
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y: Node) -> Node:
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x: Node) -> Node:
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)
        return y

    def rebalance(self, node: Node) -> Node:
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) <= 0:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def insert(self, val: int) -> None:
        def _insert(node: Node) -> Node:
            if not node:
                self.node_id_counter += 1
                return Node(val, uid=self.node_id_counter)
            if val < node.val:
                node.left = _insert(node.left)
            else:
                node.right = _insert(node.right)

            self.update_height(node)
            return self.rebalance(node)

        self.root = _insert(self.root)

    def delete(self, val: int) -> None:
        def _delete(node: Node) -> Node:
            if not node:
                return node
            if val < node.val:
                node.left = _delete(node.left)
            elif val > node.val:
                node.right = _delete(node.right)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                temp = self._find_min(node.right)
                node.val = temp.val
                node.right = _delete(node.right)

            self.update_height(node)
            return self.rebalance(node)

        self.root = _delete(self.root)

    def _find_min(self, node: Node) -> Node:
        while node.left:
            node = node.left
        return node

    def search_count(self, value):
        def _search(node):
            if not node:
                return 0
            return (1 if node.val == value else 0) + _search(node.left) + _search(node.right)

        return _search(self.root)

    # Обходы дерева
    def preorder_traversal(self):
        result = []

        def _preorder(node):
            if node:
                result.append(node)
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def inorder_traversal(self):
        result = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def postorder_traversal(self):
        result = []

        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node)

        _postorder(self.root)
        return result

    # Новые методы для разделения и слияния
    def split(self, value):
        left_tree = AVLTree()
        right_tree = AVLTree()

        def _split(node):
            if not node:
                return
            if node.val < value:
                left_tree.insert(node.val)
            else:
                right_tree.insert(node.val)
            _split(node.left)
            _split(node.right)

        _split(self.root)
        return left_tree, right_tree

    @staticmethod #для определения статического метода в классе
    def merge(tree1, tree2):
        merged = AVLTree()

        def _add_nodes(node):
            if node:
                merged.insert(node.val)
                _add_nodes(node.left)
                _add_nodes(node.right)

        _add_nodes(tree1.root)
        _add_nodes(tree2.root)
        return merged

    #генератор деревье
    def generate_random_tree(self, target_height=5):
        values = set()
        while self.get_height(self.root) < target_height:
            val = random.randint(1, 100)
            if val not in values:
                self.insert(val)
                values.add(val)
    #Функиця проверки
    def validate(self):
        def _validate(node):
            if not node:
                return True
            balance = self.get_balance(node)
            left = _validate(node.left)
            right = _validate(node.right)
            return abs(balance) <= 1 and left and right

        return _validate(self.root)