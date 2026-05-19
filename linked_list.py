# ==============================================================
# Module: linked_list.py
# Deskripsi: Implementasi struktur data Linked List
#            Digunakan untuk menyimpan koleksi dokumen
# ==============================================================


class Node:
    """Node untuk Linked List, menyimpan data dan pointer ke node berikutnya."""

    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """Implementasi Singly Linked List untuk menyimpan data dokumen."""

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        """Menambahkan data di akhir linked list."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at(self, index, data):
        """Menyisipkan data pada posisi tertentu."""
        if index < 0 or index > self._size:
            return False
        new_node = Node(data)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1
        return True

    def delete_at(self, index):
        """Menghapus node pada posisi tertentu. Mengembalikan data yang dihapus."""
        if index < 0 or index >= self._size or self.head is None:
            return None
        if index == 0:
            removed = self.head.data
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            removed = current.next.data
            current.next = current.next.next
        self._size -= 1
        return removed

    def get_at(self, index):
        """Mengambil data pada posisi tertentu."""
        if index < 0 or index >= self._size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def update_at(self, index, data):
        """Memperbarui data pada posisi tertentu."""
        if index < 0 or index >= self._size:
            return False
        current = self.head
        for _ in range(index):
            current = current.next
        current.data = data
        return True

    def find(self, predicate):
        """Mencari node pertama yang memenuhi kondisi predicate.
        Mengembalikan tuple (index, data) atau (None, None)."""
        current = self.head
        index = 0
        while current is not None:
            if predicate(current.data):
                return index, current.data
            current = current.next
            index += 1
        return None, None

    def find_all(self, predicate):
        """Mencari semua node yang memenuhi kondisi predicate.
        Mengembalikan list of tuple (index, data)."""
        results = []
        current = self.head
        index = 0
        while current is not None:
            if predicate(current.data):
                results.append((index, current.data))
            current = current.next
            index += 1
        return results

    def to_list(self):
        """Mengubah linked list menjadi Python list."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def size(self):
        """Mengembalikan jumlah elemen dalam linked list."""
        return self._size

    def is_empty(self):
        """Mengecek apakah linked list kosong."""
        return self._size == 0

    def clear(self):
        """Mengosongkan seluruh linked list."""
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        items = self.to_list()
        return f"LinkedList({items})"

    def __repr__(self):
        return self.__str__()
