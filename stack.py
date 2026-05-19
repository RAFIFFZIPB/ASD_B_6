# ==============================================================
# Module: stack.py
# Deskripsi: Implementasi struktur data Stack (LIFO)
#            Digunakan untuk fitur Undo pada editor teks
# ==============================================================


class Stack:
    """Implementasi Stack menggunakan list Python (konsep LIFO)."""

    # Fungsi: Inisialisasi stack dengan list kosong
    def __init__(self):
        self._items = []

    # Fungsi: Tambahkan item ke puncak stack
    def push(self, item):
        """Menambahkan item ke puncak stack."""
        self._items.append(item)

    # Fungsi: Ambil dan hapus item di puncak stack (prinsip LIFO)
    def pop(self):
        """Menghapus dan mengembalikan item dari puncak stack.
        Mengembalikan None jika stack kosong."""
        if self.is_empty():
            return None
        return self._items.pop()

    # Fungsi: Lihat item di puncak tanpa menghapusnya
    def peek(self):
        """Melihat item di puncak stack tanpa menghapusnya.
        Mengembalikan None jika stack kosong."""
        if self.is_empty():
            return None
        return self._items[-1]

    # Fungsi: Cek apakah stack tidak memiliki item
    def is_empty(self):
        """Mengecek apakah stack kosong."""
        return len(self._items) == 0

    # Fungsi: Kembalikan jumlah item dalam stack
    def size(self):
        """Mengembalikan jumlah item dalam stack."""
        return len(self._items)

    # Fungsi: Hapus semua item dari stack
    def clear(self):
        """Mengosongkan seluruh isi stack."""
        self._items.clear()

    # Fungsi: Konversi isi stack ke Python list (urutan bawah ke atas)
    def to_list(self):
        """Mengembalikan isi stack sebagai list (dari bawah ke atas)."""
        return list(self._items)

    # Fungsi: Tampilkan isi stack sebagai string
    def __str__(self):
        return f"Stack({self._items})"

    # Fungsi: Alias untuk __str__
    def __repr__(self):
        return self.__str__()
