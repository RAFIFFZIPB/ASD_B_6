# ==============================================================
# Module: stack.py
# Deskripsi: Implementasi struktur data Stack (LIFO)
#            Digunakan untuk fitur Undo pada editor teks
# ==============================================================


class Stack:
    """Implementasi Stack menggunakan list Python (konsep LIFO)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Menambahkan item ke puncak stack."""
        self._items.append(item)

    def pop(self):
        """Menghapus dan mengembalikan item dari puncak stack.
        Mengembalikan None jika stack kosong."""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        """Melihat item di puncak stack tanpa menghapusnya.
        Mengembalikan None jika stack kosong."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        """Mengecek apakah stack kosong."""
        return len(self._items) == 0

    def size(self):
        """Mengembalikan jumlah item dalam stack."""
        return len(self._items)

    def clear(self):
        """Mengosongkan seluruh isi stack."""
        self._items.clear()

    def to_list(self):
        """Mengembalikan isi stack sebagai list (dari bawah ke atas)."""
        return list(self._items)

    def __str__(self):
        return f"Stack({self._items})"

    def __repr__(self):
        return self.__str__()
