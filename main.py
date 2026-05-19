# ==============================================================
# APLIKASI EDITOR TEKS SEDERHANA (CLI)
# Kelompok 6 - Project Algoritma & Struktur Data
#
# Fitur Utama:
#   - CRUD dokumen lengkap
#   - Editor teks dengan Undo/Redo (Stack - LIFO)
#   - Penyimpanan data dokumen (Linked List)
#   - Sorting & Searching
#   - File Handling (CSV)
#   - Validasi input
#
# Struktur Data yang digunakan:
#   1. Stack   -> Undo/Redo history
#   2. Linked List -> Penyimpanan koleksi dokumen
# ==============================================================

from document import DocumentManager
from file_handler import save_documents, load_documents, export_document_to_txt
from search_sort import (
    search_by_title,
    search_by_content,
    sort_by_title,
    sort_by_date,
    sort_by_line_count,
)
from utils import (
    input_integer,
    input_non_empty,
    input_yes_no,
    clear_screen,
    print_header,
    print_separator,
    print_document_table,
    print_document_content,
    pause,
)


# ======================== GLOBAL ========================
manager = DocumentManager()


# ======================== MENU UTAMA ========================

# Fungsi: Tampilkan menu utama dalam layout 3 kolom yang dikelompokkan
def menu_utama():
    """Menampilkan menu utama aplikasi."""
    print_header("EDITOR TEKS SEDERHANA")

    W1, W2 = 22, 16
    rows = [
        ("  DOKUMEN",           "CARI & URUT",   "RIWAYAT"),
        ("  " + "-" * 14,       "-" * 11,        "-" * 7),
        ("  [1]  Buat Baru",    "[7]  Cari",     "[9]  Undo"),
        ("  [2]  Lihat Semua",  "[8]  Urutkan",  "[10] Redo"),
        ("  [3]  Buka & Edit",  "",              "[11] Riwayat"),
        ("  [4]  Ubah Judul",   "",              ""),
        ("  [5]  Hapus",        "",              ""),
        ("  [6]  Ekspor TXT",   "",              ""),
    ]
    for c1, c2, c3 in rows:
        print(f"{c1:<{W1}}{c2:<{W2}}{c3}")
    print_separator()
    print("  [12] Simpan & Keluar")
    print_separator("=")


# ======================== FITUR 1: BUAT DOKUMEN ========================

# Fungsi: Alur interaktif untuk membuat dokumen baru
def fitur_buat_dokumen():
    """Membuat dokumen baru (CREATE)."""
    print_header("BUAT DOKUMEN BARU")
    title = input_non_empty("  Masukkan judul dokumen: ")
    doc = manager.create_document(title)
    print(f"\n  [OK] Dokumen '{doc.title}' berhasil dibuat! (ID: {doc.doc_id})")

    if input_yes_no("  Ingin langsung menambahkan isi? (y/n): "):
        tambah_baris_interaktif(doc.doc_id)

    simpan_otomatis()


# ======================== FITUR 2: LIHAT SEMUA ========================

# Fungsi: Tampilkan semua dokumen dalam format tabel
def fitur_lihat_semua():
    """Menampilkan semua dokumen (READ ALL)."""
    print_header("DAFTAR SEMUA DOKUMEN")
    docs = manager.read_all_documents()
    print_document_table(docs)


# ======================== HELPER ========================

# Fungsi: Tampilkan tabel dokumen, minta ID dari user, kembalikan dokumen yang dipilih
def _pick_document(prompt="  Masukkan ID dokumen: "):
    """Tampilkan tabel dokumen, minta ID, validasi, kembalikan doc atau None."""
    docs = manager.read_all_documents()
    if not docs:
        print("  (Belum ada dokumen.)")
        return None
    print_document_table(docs)
    print()
    doc_id = input_integer(prompt, min_val=1)
    _, doc = manager.read_document(doc_id)
    if doc is None:
        print(f"  [!] Dokumen dengan ID {doc_id} tidak ditemukan.")
    return doc


# ======================== FITUR 3: BUKA & EDIT ========================

# Fungsi: Pilih dokumen lalu masuk ke mode editor
def fitur_buka_edit():
    """Membuka dokumen dan masuk ke mode editor."""
    print_header("BUKA & EDIT DOKUMEN")
    doc = _pick_document("  Masukkan ID dokumen yang ingin dibuka: ")
    if doc:
        mode_editor(doc)


# Fungsi: Loop interaktif untuk mengedit isi dokumen, termasuk undo dan redo
def mode_editor(doc):
    """Mode editor interaktif untuk satu dokumen."""
    while True:
        clear_screen()
        print_document_content(doc)
        print("\n  --- Menu Editor ---")
        print("  [1] Tambah Baris")
        print("  [2] Edit Baris")
        print("  [3] Hapus Baris")
        print("  [4] Undo")
        print("  [5] Redo")
        print("  [0] Kembali ke Menu Utama")
        print_separator()

        pilihan = input_integer("  Pilih: ", min_val=0, max_val=5)

        if pilihan == 0:
            simpan_otomatis()
            break
        elif pilihan == 1:
            tambah_baris_interaktif(doc.doc_id)
        elif pilihan == 2:
            edit_baris_interaktif(doc)
        elif pilihan == 3:
            hapus_baris_interaktif(doc)
        elif pilihan == 4:
            _, msg = manager.undo()
            print(f"\n  {msg}")
            # Refresh referensi dokumen setelah undo
            _, doc_refresh = manager.read_document(doc.doc_id)
            if doc_refresh is None:
                print("  [!] Dokumen sudah dihapus oleh undo.")
                pause()
                break
            doc = doc_refresh
            pause()
        elif pilihan == 5:
            _, msg = manager.redo()
            print(f"\n  {msg}")
            _, doc_refresh = manager.read_document(doc.doc_id)
            if doc_refresh is None:
                print("  [!] Dokumen sudah dihapus oleh redo.")
                pause()
                break
            doc = doc_refresh
            pause()


# Fungsi: Tambah baris satu per satu ke dokumen sampai user ketik "selesai"
def tambah_baris_interaktif(doc_id):
    """Menambahkan baris secara interaktif. Ketik 'selesai' untuk berhenti."""
    print("\n  Ketik baris teks (ketik 'selesai' untuk berhenti):")
    while True:
        text = input("  > ")
        if text.strip().lower() == "selesai":
            break
        if text.strip() == "":
            print("  [!] Baris kosong dilewati.")
            continue
        manager.add_line_to_doc(doc_id, text)
        print("  [+] Baris ditambahkan.")


# Fungsi: Minta nomor baris dan teks baru, lalu ubah isi baris tersebut
def edit_baris_interaktif(doc):
    """Mengedit baris tertentu dalam dokumen."""
    if doc.get_line_count() == 0:
        print("\n  [!] Dokumen kosong. Tidak ada baris untuk diedit.")
        pause()
        return
    nomor = input_integer(
        f"  Masukkan nomor baris yang ingin diedit (1-{doc.get_line_count()}): ",
        min_val=1,
        max_val=doc.get_line_count(),
    )
    print(f"  Baris saat ini: {doc.lines[nomor - 1]}")
    teks_baru = input_non_empty("  Masukkan teks baru: ")
    if manager.edit_line_in_doc(doc.doc_id, nomor - 1, teks_baru):
        print("  [OK] Baris berhasil diubah.")
    else:
        print("  [!] Gagal mengubah baris.")
    pause()


# Fungsi: Minta nomor baris, konfirmasi, lalu hapus baris tersebut
def hapus_baris_interaktif(doc):
    """Menghapus baris tertentu dalam dokumen."""
    if doc.get_line_count() == 0:
        print("\n  [!] Dokumen kosong. Tidak ada baris untuk dihapus.")
        pause()
        return
    nomor = input_integer(
        f"  Masukkan nomor baris yang ingin dihapus (1-{doc.get_line_count()}): ",
        min_val=1,
        max_val=doc.get_line_count(),
    )
    if input_yes_no(f"  Yakin hapus baris {nomor}? (y/n): "):
        if manager.delete_line_in_doc(doc.doc_id, nomor - 1):
            print("  [OK] Baris berhasil dihapus.")
        else:
            print("  [!] Gagal menghapus baris.")
    pause()


# ======================== FITUR 4: UBAH JUDUL ========================

# Fungsi: Pilih dokumen lalu ubah judulnya
def fitur_ubah_judul():
    """Mengubah judul dokumen (UPDATE)."""
    print_header("UBAH JUDUL DOKUMEN")
    doc = _pick_document("  Masukkan ID dokumen: ")
    if doc is None:
        return
    print(f"  Judul saat ini: {doc.title}")
    new_title = input_non_empty("  Masukkan judul baru: ")
    if manager.update_document_title(doc.doc_id, new_title):
        print(f"  [OK] Judul berhasil diubah menjadi '{new_title}'.")
        simpan_otomatis()
    else:
        print("  [!] Gagal mengubah judul.")


# ======================== FITUR 5: HAPUS DOKUMEN ========================

# Fungsi: Pilih dokumen, minta konfirmasi, lalu hapus secara permanen
def fitur_hapus_dokumen():
    """Menghapus dokumen (DELETE)."""
    print_header("HAPUS DOKUMEN")
    doc = _pick_document("  Masukkan ID dokumen yang ingin dihapus: ")
    if doc is None:
        return
    print(f"  Dokumen: {doc.title} ({doc.get_line_count()} baris)")
    if input_yes_no("  Yakin ingin menghapus? (y/n): "):
        if manager.delete_document(doc.doc_id):
            print("  [OK] Dokumen berhasil dihapus.")
            simpan_otomatis()
        else:
            print("  [!] Gagal menghapus dokumen.")


# ======================== FITUR 6: CARI DOKUMEN ========================

# Fungsi: Cari dokumen berdasarkan judul atau isi konten
def fitur_cari_dokumen():
    """Fitur pencarian dokumen (SEARCHING)."""
    print_header("CARI DOKUMEN")
    print("  [1] Cari berdasarkan Judul")
    print("  [2] Cari berdasarkan Isi/Konten")
    print("  [0] Kembali")
    print_separator()

    pilihan = input_integer("  Pilih: ", min_val=0, max_val=2)
    if pilihan == 0:
        return

    keyword = input_non_empty("  Masukkan kata kunci: ")
    docs = manager.read_all_documents()

    if pilihan == 1:
        results = search_by_title(docs, keyword)
        if results:
            print(f"\n  Ditemukan {len(results)} dokumen:")
            print_document_table(results)
        else:
            print(f"\n  Tidak ada dokumen dengan judul mengandung '{keyword}'.")

    elif pilihan == 2:
        results = search_by_content(docs, keyword)
        if results:
            print(f"\n  Ditemukan di {len(results)} dokumen:")
            for doc, line_indices in results:
                print(f"\n  [{doc.doc_id}] {doc.title}:")
                for idx in line_indices:
                    print(f"    Baris {idx + 1}: {doc.lines[idx]}")
        else:
            print(f"\n  Tidak ada konten yang mengandung '{keyword}'.")


# ======================== FITUR 7: URUTKAN DOKUMEN ========================

_SORT_OPTIONS = [
    ("Judul (A-Z)",                   sort_by_title,      {"ascending": True}),
    ("Judul (Z-A)",                   sort_by_title,      {"ascending": False}),
    ("Tanggal Dibuat (Terlama)",      sort_by_date,       {"ascending": True}),
    ("Tanggal Dibuat (Terbaru)",      sort_by_date,       {"ascending": False}),
    ("Jumlah Baris (Sedikit-Banyak)", sort_by_line_count, {"ascending": True}),
    ("Jumlah Baris (Banyak-Sedikit)", sort_by_line_count, {"ascending": False}),
]


# Fungsi: Tampilkan opsi urutan, minta pilihan, lalu tampilkan hasil pengurutan
def fitur_urutkan_dokumen():
    """Fitur pengurutan dokumen (SORTING)."""
    print_header("URUTKAN DOKUMEN")
    docs = manager.read_all_documents()
    if not docs:
        print("  (Belum ada dokumen.)")
        return
    for i, (label, _, _) in enumerate(_SORT_OPTIONS, 1):
        print(f"  [{i}] Urutkan berdasarkan {label}")
    print("  [0] Kembali")
    print_separator()
    pilihan = input_integer("  Pilih: ", min_val=0, max_val=len(_SORT_OPTIONS))
    if pilihan == 0:
        return
    label, fn, kwargs = _SORT_OPTIONS[pilihan - 1]
    sorted_docs = fn(docs, **kwargs)
    print(f"\n  Hasil pengurutan ({label}):")
    print_document_table(sorted_docs)


# ======================== FITUR 8 & 9: UNDO / REDO ========================

# Fungsi: Panggil undo dari manager, tampilkan pesan, lalu simpan otomatis
def fitur_undo():
    """Membatalkan aksi terakhir."""
    action, msg = manager.undo()
    print(f"\n  {msg}")
    if action:
        simpan_otomatis()


# Fungsi: Panggil redo dari manager, tampilkan pesan, lalu simpan otomatis
def fitur_redo():
    """Mengulang aksi yang telah di-undo."""
    action, msg = manager.redo()
    print(f"\n  {msg}")
    if action:
        simpan_otomatis()


# ======================== FITUR 10: RIWAYAT ========================

# Fungsi: Tampilkan seluruh riwayat aksi yang tersimpan di stack undo
def fitur_riwayat():
    """Menampilkan riwayat aksi (isi Stack)."""
    print_header("RIWAYAT AKSI (STACK)")
    history = manager.get_undo_history()
    if not history:
        print("  (Riwayat kosong)")
        return

    label_aksi = {
        "create": "Buat dokumen",
        "delete": "Hapus dokumen",
        "update_title": "Ubah judul",
        "add_line": "Tambah baris",
        "edit_line": "Edit baris",
        "delete_line": "Hapus baris",
    }

    print(f"  {'No':<5} {'Aksi':<20} {'Detail':<30}")
    print_separator()
    for i, action in enumerate(reversed(history), 1):
        aksi = label_aksi.get(action[0], action[0])
        if action[0] == "create":
            detail = f"ID dokumen pada index {action[1]}"
        elif action[0] == "delete":
            detail = f"Dokumen '{action[2].get('title', '?')}'"
        elif action[0] == "update_title":
            detail = f"'{action[2]}' -> '{action[3]}'"
        elif action[0] == "add_line":
            detail = f"Doc ID {action[1]}, baris {action[2] + 1}"
        elif action[0] == "edit_line":
            detail = f"Doc ID {action[1]}, baris {action[2] + 1}"
        elif action[0] == "delete_line":
            detail = f"Doc ID {action[1]}, '{action[3][:20]}'"
        else:
            detail = str(action[1:])

        print(f"  {i:<5} {aksi:<20} {detail:<30}")

    print(f"\n  Total aksi tersimpan: {len(history)}")


# ======================== FITUR 11: EKSPOR TXT ========================

# Fungsi: Pilih dokumen lalu ekspor seluruh isinya ke file TXT
def fitur_ekspor_txt():
    """Mengekspor dokumen ke file TXT."""
    print_header("EKSPOR DOKUMEN KE TXT")
    doc = _pick_document("  Masukkan ID dokumen yang ingin diekspor: ")
    if doc is None:
        return
    success, msg = export_document_to_txt(doc)
    print(f"  {'[OK]' if success else '[!]'} {msg}")


# ======================== UTILITAS ========================

# Fungsi: Simpan semua dokumen ke CSV tanpa interaksi user
def simpan_otomatis():
    """Menyimpan data secara otomatis ke file CSV."""
    docs = manager.read_all_documents()
    save_documents(docs)


# Fungsi: Muat data dari CSV ke linked list saat program pertama kali dibuka
def muat_data_awal():
    """Memuat data dari file CSV saat aplikasi dimulai."""
    docs, msg = load_documents()
    print(f"  {msg}")
    for doc in docs:
        manager.documents.append(doc)


# ======================== MAIN LOOP ========================

_MENU_ACTIONS = {
    1: fitur_buat_dokumen,
    2: fitur_lihat_semua,
    3: fitur_buka_edit,
    4: fitur_ubah_judul,
    5: fitur_hapus_dokumen,
    6: fitur_ekspor_txt,
    7: fitur_cari_dokumen,
    8: fitur_urutkan_dokumen,
    9: fitur_undo,
    10: fitur_redo,
    11: fitur_riwayat,
}


# Fungsi: Titik masuk utama program, tampilkan sambutan lalu jalankan loop menu
def main():
    """Fungsi utama aplikasi."""
    clear_screen()
    print_header("SELAMAT DATANG")
    print("  Aplikasi Editor Teks Sederhana")
    print("  Kelompok 6 - Project Algoritma")
    print_separator("=")
    print()
    muat_data_awal()
    pause()

    while True:
        clear_screen()
        menu_utama()
        pilihan = input_integer("  Pilih menu: ", min_val=1, max_val=12)
        if pilihan == 12:
            simpan_otomatis()
            print_header("TERIMA KASIH")
            print("  Data telah disimpan. Sampai jumpa!")
            print_separator("=")
            break
        _MENU_ACTIONS[pilihan]()
        if pilihan != 3:  # editor punya pause sendiri
            pause()


if __name__ == "__main__":
    main()
