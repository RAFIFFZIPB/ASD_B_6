# ==============================================================
# Module: document.py
# Deskripsi: Kelas Dokumen dan Manager untuk mengelola dokumen
#            Mendukung operasi CRUD lengkap
# ==============================================================

from datetime import datetime
from stack import Stack
from linked_list import LinkedList


class Document:
    """Representasi satu dokumen teks."""

    _id_counter = 0

    def __init__(self, doc_id=None, title="", lines=None, created_at=None, updated_at=None):
        if doc_id is None:
            Document._id_counter += 1
            self.doc_id = Document._id_counter
        else:
            self.doc_id = doc_id
            if doc_id >= Document._id_counter:
                Document._id_counter = doc_id

        self.title = title
        self.lines = lines if lines is not None else []
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at if updated_at else self.created_at

    def add_line(self, text):
        """Menambahkan baris teks ke dokumen."""
        self.lines.append(text)
        self._update_timestamp()

    def remove_line(self, index):
        """Menghapus baris pada indeks tertentu."""
        if 0 <= index < len(self.lines):
            removed = self.lines.pop(index)
            self._update_timestamp()
            return removed
        return None

    def update_line(self, index, new_text):
        """Mengubah baris pada indeks tertentu."""
        if 0 <= index < len(self.lines):
            old_text = self.lines[index]
            self.lines[index] = new_text
            self._update_timestamp()
            return old_text
        return None

    def get_content(self):
        """Mengembalikan seluruh konten dokumen sebagai string."""
        return "\n".join(self.lines)

    def get_line_count(self):
        """Mengembalikan jumlah baris."""
        return len(self.lines)

    def _update_timestamp(self):
        """Memperbarui waktu terakhir diubah."""
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Mengubah dokumen menjadi dictionary untuk penyimpanan."""
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "lines": self.lines,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data):
        """Membuat objek Document dari dictionary."""
        return Document(
            doc_id=data["doc_id"],
            title=data["title"],
            lines=data["lines"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def __str__(self):
        return f"[ID:{self.doc_id}] {self.title} ({self.get_line_count()} baris)"

    def __repr__(self):
        return self.__str__()


class DocumentManager:
    """Mengelola koleksi dokumen menggunakan Linked List + Stack untuk undo."""

    def __init__(self):
        self.documents = LinkedList()  # Struktur data 1: Linked List
        self.undo_stack = Stack()      # Struktur data 2: Stack (untuk undo)
        self.redo_stack = Stack()      # Stack tambahan untuk redo

    # ======================== PRIVATE HELPERS ========================

    def _get_doc(self, doc_id):
        """Mendapatkan dokumen berdasarkan ID."""
        _, doc = self.documents.find(lambda d: d.doc_id == doc_id)
        return doc

    def _record(self, action):
        """Menyimpan aksi ke undo stack dan mengosongkan redo stack."""
        self.undo_stack.push(action)
        self.redo_stack.clear()

    # ======================== CRUD ========================

    def create_document(self, title):
        """Membuat dokumen baru (CREATE)."""
        doc = Document(title=title)
        self.documents.append(doc)
        self._record(("create", self.documents.size() - 1, doc.to_dict()))
        return doc

    def read_document(self, doc_id):
        """Membaca dokumen berdasarkan ID (READ)."""
        return self.documents.find(lambda d: d.doc_id == doc_id)

    def read_all_documents(self):
        """Membaca semua dokumen (READ ALL)."""
        return self.documents.to_list()

    def update_document_title(self, doc_id, new_title):
        """Memperbarui judul dokumen (UPDATE)."""
        doc = self._get_doc(doc_id)
        if doc is None:
            return False
        old_title = doc.title
        doc.title = new_title
        doc._update_timestamp()
        self._record(("update_title", doc_id, old_title, new_title))
        return True

    def delete_document(self, doc_id):
        """Menghapus dokumen berdasarkan ID (DELETE)."""
        index, doc = self.documents.find(lambda d: d.doc_id == doc_id)
        if doc is None:
            return False
        self._record(("delete", index, doc.to_dict()))
        self.documents.delete_at(index)
        return True

    # ======================== EDITOR ========================

    def add_line_to_doc(self, doc_id, text):
        """Menambahkan baris ke dokumen."""
        doc = self._get_doc(doc_id)
        if doc is None:
            return False
        doc.add_line(text)
        self._record(("add_line", doc_id, len(doc.lines) - 1, text))
        return True

    def edit_line_in_doc(self, doc_id, line_index, new_text):
        """Mengubah baris tertentu dalam dokumen."""
        doc = self._get_doc(doc_id)
        if doc is None:
            return False
        old_text = doc.update_line(line_index, new_text)
        if old_text is None:
            return False
        self._record(("edit_line", doc_id, line_index, old_text, new_text))
        return True

    def delete_line_in_doc(self, doc_id, line_index):
        """Menghapus baris tertentu dalam dokumen."""
        doc = self._get_doc(doc_id)
        if doc is None:
            return False
        removed = doc.remove_line(line_index)
        if removed is None:
            return False
        self._record(("delete_line", doc_id, line_index, removed))
        return True

    # ======================== UNDO / REDO ========================

    def _apply_action(self, action, forward):
        """Menerapkan aksi (forward=True untuk redo, False untuk undo)."""
        t = action[0]
        label = "Redo" if forward else "Undo"

        if t == "create":
            if forward:
                doc = Document.from_dict(action[2])
                self.documents.insert_at(action[1], doc)
                return f"Redo: Dokumen '{doc.title}' dibuat kembali."
            self.documents.delete_at(action[1])
            return "Undo: Pembuatan dokumen dibatalkan."

        if t == "delete":
            if forward:
                self.documents.delete_at(action[1])
                return "Redo: Dokumen dihapus kembali."
            doc = Document.from_dict(action[2])
            self.documents.insert_at(action[1], doc)
            return f"Undo: Dokumen '{doc.title}' dikembalikan."

        doc = self._get_doc(action[1])
        if doc is None:
            return f"{label}: Dokumen tidak ditemukan."

        if t == "update_title":
            doc.title = action[3] if forward else action[2]
            return f"{label}: Judul diubah ke '{doc.title}'."

        if t == "add_line":
            if forward:
                doc.add_line(action[3])
                return f"{label}: Baris ditambahkan kembali."
            doc.remove_line(action[2])
            return f"{label}: Baris terakhir dihapus."

        if t == "edit_line":
            doc.update_line(action[2], action[4] if forward else action[3])
            status = "diubah kembali" if forward else "dikembalikan"
            return f"{label}: Baris {action[2] + 1} {status}."

        if t == "delete_line":
            if forward:
                doc.remove_line(action[2])
                return f"{label}: Baris dihapus kembali."
            doc.lines.insert(action[2], action[3])
            return f"{label}: Baris '{action[3]}' dikembalikan."

        return ""

    def undo(self):
        """Membatalkan aksi terakhir menggunakan Stack (LIFO)."""
        if self.undo_stack.is_empty():
            return None, "Tidak ada aksi yang bisa di-undo."
        action = self.undo_stack.pop()
        msg = self._apply_action(action, forward=False)
        self.redo_stack.push(action)
        return action, msg

    def redo(self):
        """Mengulang aksi yang telah di-undo."""
        if self.redo_stack.is_empty():
            return None, "Tidak ada aksi yang bisa di-redo."
        action = self.redo_stack.pop()
        msg = self._apply_action(action, forward=True)
        self.undo_stack.push(action)
        return action, msg

    def get_undo_history(self):
        """Mengembalikan riwayat undo sebagai list."""
        return self.undo_stack.to_list()
