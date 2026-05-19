# ==============================================================
# Module: search_sort.py
# Deskripsi: Modul untuk fitur pencarian (Searching) dan
#            pengurutan (Sorting) data dokumen
# ==============================================================


# ======================== SEARCHING ========================

# Fungsi: Cari dokumen yang judulnya mengandung kata kunci (tidak peka huruf besar/kecil)
def search_by_title(documents_list, keyword):
    """Mencari dokumen berdasarkan judul (case-insensitive).

    Mengembalikan list dokumen yang judulnya mengandung keyword.
    """
    keyword_lower = keyword.lower()
    results = []
    for doc in documents_list:
        if keyword_lower in doc.title.lower():
            results.append(doc)
    return results


# Fungsi: Cari dokumen yang isinya mengandung kata kunci, kembalikan baris yang cocok
def search_by_content(documents_list, keyword):
    """Mencari dokumen yang kontennya mengandung keyword (case-insensitive).

    Mengembalikan list of tuple (doc, [nomor_baris_yang_cocok]).
    """
    keyword_lower = keyword.lower()
    results = []
    for doc in documents_list:
        matching_lines = []
        for i, line in enumerate(doc.lines):
            if keyword_lower in line.lower():
                matching_lines.append(i)
        if matching_lines:
            results.append((doc, matching_lines))
    return results


# Fungsi: Cari dokumen berdasarkan ID secara langsung
def search_by_id(documents_list, doc_id):
    """Mencari dokumen berdasarkan ID."""
    for doc in documents_list:
        if doc.doc_id == doc_id:
            return doc
    return None


# ======================== SORTING ========================

# Fungsi: Urutkan dokumen berdasarkan judul menggunakan Bubble Sort
def sort_by_title(documents_list, ascending=True):
    """Mengurutkan dokumen berdasarkan judul (A-Z atau Z-A).

    Menggunakan algoritma Bubble Sort.
    """
    docs = list(documents_list)
    n = len(docs)
    for i in range(n - 1):
        swapped = False
        # Setiap pass: elemen terbesar/terkecil "menggelembung" ke posisi akhir
        for j in range(n - 1 - i):  # rentang berkurang tiap pass karena ujungnya sudah urut
            if ascending:
                if docs[j].title.lower() > docs[j + 1].title.lower():
                    docs[j], docs[j + 1] = docs[j + 1], docs[j]
                    swapped = True
            else:
                if docs[j].title.lower() < docs[j + 1].title.lower():
                    docs[j], docs[j + 1] = docs[j + 1], docs[j]
                    swapped = True
        if not swapped:
            break  # tidak ada pertukaran = sudah urut, hentikan lebih awal
    return docs


# Fungsi: Urutkan dokumen berdasarkan tanggal menggunakan Selection Sort
def sort_by_date(documents_list, ascending=True, by="created"):
    """Mengurutkan dokumen berdasarkan tanggal (terlama/terbaru).

    Menggunakan algoritma Selection Sort.
    Parameter by: 'created' atau 'updated'.
    """
    docs = list(documents_list)
    n = len(docs)
    for i in range(n - 1):
        target_idx = i  # asumsikan posisi i adalah yang terkecil/terbesar sementara
        # Cari elemen terkecil/terbesar di sisa list
        for j in range(i + 1, n):
            date_j = docs[j].created_at if by == "created" else docs[j].updated_at
            date_target = docs[target_idx].created_at if by == "created" else docs[target_idx].updated_at
            if ascending:
                if date_j < date_target:
                    target_idx = j
            else:
                if date_j > date_target:
                    target_idx = j
        # Tukar elemen yang ditemukan ke posisi i
        if target_idx != i:
            docs[i], docs[target_idx] = docs[target_idx], docs[i]
    return docs


# Fungsi: Urutkan dokumen berdasarkan jumlah baris menggunakan Insertion Sort
def sort_by_line_count(documents_list, ascending=True):
    """Mengurutkan dokumen berdasarkan jumlah baris.

    Menggunakan algoritma Insertion Sort.
    """
    docs = list(documents_list)
    n = len(docs)
    for i in range(1, n):
        key = docs[i]           # elemen yang akan disisipkan ke posisi yang tepat
        key_count = key.get_line_count()
        j = i - 1
        # Geser elemen yang lebih besar/kecil ke kanan untuk membuka ruang
        if ascending:
            while j >= 0 and docs[j].get_line_count() > key_count:
                docs[j + 1] = docs[j]
                j -= 1
        else:
            while j >= 0 and docs[j].get_line_count() < key_count:
                docs[j + 1] = docs[j]
                j -= 1
        docs[j + 1] = key       # sisipkan di posisi yang benar
    return docs
