# ==============================================================
# Module: file_handler.py
# Deskripsi: Modul untuk menyimpan dan memuat data dari file CSV
#            Memastikan data tersimpan secara permanen
# ==============================================================

import csv
import os
from document import Document

# Nama file penyimpanan default
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.csv")


# Fungsi: Simpan semua dokumen ke file CSV
def save_documents(documents_list):
    """Menyimpan daftar dokumen ke file CSV.

    Format CSV:
    doc_id | title | lines (dipisah '|||') | created_at | updated_at
    """
    try:
        with open(DOCUMENTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(["doc_id", "title", "lines", "created_at", "updated_at"])
            for doc in documents_list:
                # Gabungkan baris dengan separator khusus agar bisa disimpan di 1 cell CSV
                lines_str = "|||".join(doc.lines)
                writer.writerow([
                    doc.doc_id,
                    doc.title,
                    lines_str,
                    doc.created_at,
                    doc.updated_at,
                ])
        return True, f"Data berhasil disimpan ke {DOCUMENTS_FILE}"
    except Exception as e:
        return False, f"Gagal menyimpan data: {e}"


# Fungsi: Muat dokumen dari file CSV saat program pertama kali dibuka
def load_documents():
    """Memuat daftar dokumen dari file CSV.

    Mengembalikan list of Document objects.
    """
    documents = []
    if not os.path.exists(DOCUMENTS_FILE):
        return documents, "File data belum ada. Memulai dengan data kosong."

    try:
        with open(DOCUMENTS_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header
            if header is None:
                return documents, "File data kosong."

            for row in reader:
                if len(row) < 5:
                    continue
                doc_id = int(row[0])
                title = row[1]
                lines_str = row[2]
                lines = lines_str.split("|||") if lines_str else []
                created_at = row[3]
                updated_at = row[4]

                doc = Document(
                    doc_id=doc_id,
                    title=title,
                    lines=lines,
                    created_at=created_at,
                    updated_at=updated_at,
                )
                documents.append(doc)

        return documents, f"{len(documents)} dokumen berhasil dimuat."
    except Exception as e:
        return [], f"Gagal memuat data: {e}"


# Fungsi: Ekspor isi satu dokumen ke file TXT
def export_document_to_txt(doc, filepath=None):
    """Mengekspor satu dokumen ke file TXT."""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, f"{doc.title}.txt")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Judul: {doc.title}\n")
            f.write(f"Dibuat: {doc.created_at}\n")
            f.write(f"Diubah: {doc.updated_at}\n")
            f.write("=" * 40 + "\n")
            for i, line in enumerate(doc.lines, 1):
                f.write(f"{line}\n")
        return True, f"Dokumen diekspor ke {filepath}"
    except Exception as e:
        return False, f"Gagal mengekspor: {e}"
