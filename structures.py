from search import direct_search


class _AVLNode:
    __slots__ = ("key", "data", "left", "right", "height")

    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def clear(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _balance(self, node):
        self._update_height(node)
        factor = self._balance_factor(node)

        if factor > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if factor < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key, data):
        def add(node):
            if node is None:
                return _AVLNode(key, data), True

            if key < node.key:
                node.left, inserted = add(node.left)
            elif key > node.key:
                node.right, inserted = add(node.right)
            else:
                return node, False

            return self._balance(node), inserted

        self.root, inserted = add(self.root)
        return inserted

    def delete(self, key):
        def min_node(node):
            while node.left:
                node = node.left
            return node

        def remove(node):
            if node is None:
                return None, False

            if key < node.key:
                node.left, deleted = remove(node.left)
            elif key > node.key:
                node.right, deleted = remove(node.right)
            else:
                if node.left is None:
                    return node.right, True
                if node.right is None:
                    return node.left, True

                replacement = min_node(node.right)
                node.key = replacement.key
                node.data = replacement.data
                node.right, _ = remove_duplicate(node.right, replacement.key)
                return self._balance(node), True

            return self._balance(node), deleted

        def remove_duplicate(node, duplicate_key):
            if duplicate_key < node.key:
                node.left, deleted = remove_duplicate(node.left, duplicate_key)
            elif duplicate_key > node.key:
                node.right, deleted = remove_duplicate(node.right, duplicate_key)
            else:
                if node.left is None:
                    return node.right, True
                if node.right is None:
                    return node.left, True

            return self._balance(node), deleted

        self.root, deleted = remove(self.root)
        return deleted

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.data
            node = node.left if key < node.key else node.right
        return None

    def preorder(self):
        result = []

        def walk(node):
            if node is None:
                return
            result.append(node.data)
            walk(node.left)
            walk(node.right)

        walk(self.root)
        return result

    def find_clients_by_fragment(self, fragment):
        result = []

        def walk(node):
            if node is None:
                return

            client = node.data
            if (
                direct_search(client.full_name, fragment)
                or direct_search(client.address, fragment)
            ):
                result.append(client)

            walk(node.left)
            walk(node.right)

        walk(self.root)
        return result


_DELETED = object()


class HashTableSIM:
    def __init__(self, size=17):
        self.initial_size = size
        self.size = size
        self.table = [None] * size
        self.count = 0

    def clear(self):
        self.size = self.initial_size
        self.table = [None] * self.size
        self.count = 0

    def _hash_one(self, key):
        total = 0
        for index, char in enumerate(key):
            total += ord(char) * 31**index
        return total % self.size

    def _hash_two(self, key):
        total = 0
        for index, char in enumerate(key):
            total += ord(char) * 37**index
        return total % (self.size - 2) + 1

    def _index(self, key, attempt):
        return (self._hash_one(key) + attempt * self._hash_two(key)) % self.size

    def _next_prime(self, start):
        candidate = start if start % 2 else start + 1
        while True:
            for divisor in range(3, int(candidate**0.5) + 1, 2):
                if candidate % divisor == 0:
                    break
            else:
                return candidate
            candidate += 2

    def _rehash(self):
        old_items = self.get_all()
        self.size = self._next_prime(self.size * 2 + 1)
        self.table = [None] * self.size
        self.count = 0

        for sim in old_items:
            self.insert(sim)

    def insert(self, sim):
        if self.count / self.size > 0.7:
            self._rehash()

        first_deleted = None
        for attempt in range(self.size):
            index = self._index(sim.number, attempt)
            slot = self.table[index]

            if slot is None:
                target = first_deleted if first_deleted is not None else index
                self.table[target] = sim
                self.count += 1
                return True

            if slot is _DELETED and first_deleted is None:
                first_deleted = index
            elif slot is not _DELETED and slot.number == sim.number:
                return False

        return False

    def delete(self, sim_number):
        for attempt in range(self.size):
            index = self._index(sim_number, attempt)
            slot = self.table[index]

            if slot is None:
                return False
            if slot is not _DELETED and slot.number == sim_number:
                self.table[index] = _DELETED
                self.count -= 1
                return True

        return False

    def search(self, sim_number):
        for attempt in range(self.size):
            index = self._index(sim_number, attempt)
            slot = self.table[index]

            if slot is None:
                return None
            if slot is not _DELETED and slot.number == sim_number:
                return slot

        return None

    def search_by_tariff(self, tariff):
        target = tariff.lower()
        return [sim for sim in self.get_all() if sim.tariff.lower() == target]

    def get_all(self):
        return [sim for sim in self.table if sim is not None and sim is not _DELETED]


class _ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class IssueList:
    def __init__(self):
        self.head = None

    def insert_sorted(self, record):
        node = _ListNode(record)

        if self.head is None or record.sim_number <= self.head.data.sim_number:
            node.next = self.head
            self.head = node
            return

        current = self.head
        while current.next and current.next.data.sim_number < record.sim_number:
            current = current.next

        node.next = current.next
        current.next = node

    def delete(self, passport, sim_number):
        if self.head is None:
            return False

        if self._matches(self.head.data, passport, sim_number):
            self.head = self.head.next
            return True

        current = self.head
        while current.next:
            if self._matches(current.next.data, passport, sim_number):
                current.next = current.next.next
                return True
            current = current.next

        return False

    def find_by_sim(self, sim_number):
        return [record for record in self.get_all() if record.sim_number == sim_number]

    def find_by_passport(self, passport):
        return [record for record in self.get_all() if record.passport == passport]

    def get_all(self):
        records = []
        current = self.head
        while current:
            records.append(current.data)
            current = current.next
        return records

    def _matches(self, record, passport, sim_number):
        return record.passport == passport and record.sim_number == sim_number
