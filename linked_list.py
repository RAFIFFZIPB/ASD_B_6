# ==============================================================
# Module: linked_list.py
# Deskripsi: Implementasi struktur data Linked List
#            Digunakan untuk menyimpan koleksi dokumen
# ==============================================================


class Node:
    """Node untuk Linked List, menyimpan data dan pointer ke node berikutnya."""

    # Fungsi: Buat node baru dengan data dan set pointer next ke None
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """Implementasi Singly Linked List untuk menyimpan data dokumen."""

    # Fungsi: Inisialisasi linked list kosong (head kosong, ukuran 0)
    def __init__(self):
        self.head = None
        self._size = 0

    # Fungsi: Tambahkan data baru di bagian akhir linked list
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

    # Fungsi: Sisipkan data di posisi tertentu (menggeser node sesudahnya)
    def insert_at(self, index, data):
        """Menyisipkan data pada posisi tertentu."""
        if index < 0 or index > self._size:
            return False
        new_node = Node(data)
        if index == 0:
            # Sisipkan di depan: node baru menunjuk ke head lama
            new_node.next = self.head
            self.head = new_node
        else:
            # Jalan sampai node sebelum posisi target
            current = self.head
            for _ in range(index - 1):
                current = current.next
            # Sambungkan: baru → lama, sebelumnya → baru
            new_node.next = current.next
            current.next = new_node
        self._size += 1
        return True

    # Fungsi: Hapus node di posisi tertentu dan kembalikan datanya
    def delete_at(self, index):
        """Menghapus node pada posisi tertentu. Mengembalikan data yang dihapus."""
        if index < 0 or index >= self._size or self.head is None:
            return None
        if index == 0:
            # Hapus head: geser head ke node berikutnya
            removed = self.head.data
            self.head = self.head.next
        else:
            # Jalan ke node sebelum target
            current = self.head
            for _ in range(index - 1):
                current = current.next
            removed = current.next.data
            current.next = current.next.next  # lompati node yang dihapus
        self._size -= 1
        return removed

    # Fungsi: Ambil data di posisi tertentu tanpa menghapusnya
    def get_at(self, index):
        """Mengambil data pada posisi tertentu."""
        if index < 0 or index >= self._size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    # Fungsi: Ganti data di posisi tertentu dengan data baru
    def update_at(self, index, data):
        """Memperbarui data pada posisi tertentu."""
        if index < 0 or index >= self._size:
            return False
        current = self.head
        for _ in range(index):
            current = current.next
        current.data = data
        return True

    # Fungsi: Cari node pertama yang memenuhi kondisi tertentu (pakai lambda)
    def find(self, predicate):
        """Mencari node pertama yang memenuhi kondisi predicate.
        Mengembalikan tuple (index, data) atau (None, None).
        Contoh predicate: lambda d: d.doc_id == 5
        """
        current = self.head
        index = 0
        while current is not None:
            if predicate(current.data):  # cek apakah node ini memenuhi syarat
                return index, current.data
            current = current.next
            index += 1
        return None, None

    # Fungsi: Cari semua node yang memenuhi kondisi tertentu
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

    # Fungsi: Ubah linked list menjadi Python list biasa
    def to_list(self):
        """Mengubah linked list menjadi Python list."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    # Fungsi: Kembalikan jumlah node dalam linked list
    def size(self):
        """Mengembalikan jumlah elemen dalam linked list."""
        return self._size

    # Fungsi: Cek apakah linked list tidak memiliki elemen
    def is_empty(self):
        """Mengecek apakah linked list kosong."""
        return self._size == 0

    # Fungsi: Hapus semua node, reset linked list ke kondisi awal
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
