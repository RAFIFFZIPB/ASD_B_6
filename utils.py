# ==============================================================
# Module: utils.py
# Deskripsi: Modul utilitas untuk validasi input dan
#            fungsi-fungsi pembantu tampilan
# ==============================================================


def input_integer(prompt, min_val=None, max_val=None):
    """Meminta input integer dari user dengan validasi.

    Tidak akan crash jika user memasukkan input yang salah.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  [!] Nilai minimal adalah {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  [!] Nilai maksimal adalah {max_val}.")
                continue
            return value
        except ValueError:
            print("  [!] Input harus berupa angka. Coba lagi.")


def input_non_empty(prompt):
    """Meminta input string yang tidak boleh kosong."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] Input tidak boleh kosong. Coba lagi.")


def input_yes_no(prompt):
    """Meminta input ya/tidak (y/n)."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "ya", "yes"):
            return True
        elif value in ("n", "tidak", "no"):
            return False
        else:
            print("  [!] Masukkan 'y' untuk Ya atau 'n' untuk Tidak.")


def clear_screen():
    """Membersihkan layar terminal."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    """Mencetak header dengan format yang rapi."""
    width = 50
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_separator(char="-", width=50):
    """Mencetak garis pemisah."""
    print(char * width)


def print_document_table(documents):
    """Mencetak daftar dokumen dalam format tabel."""
    if not documents:
        print("  (Tidak ada dokumen)")
        return

    print(f"  {'ID':<5} {'Judul':<25} {'Baris':<7} {'Dibuat':<20}")
    print_separator()
    for doc in documents:
        title_display = doc.title[:23] + ".." if len(doc.title) > 25 else doc.title
        print(f"  {doc.doc_id:<5} {title_display:<25} {doc.get_line_count():<7} {doc.created_at:<20}")


def print_document_content(doc):
    """Mencetak isi dokumen dengan nomor baris."""
    print_header(f"Dokumen: {doc.title}")
    print(f"  ID       : {doc.doc_id}")
    print(f"  Dibuat   : {doc.created_at}")
    print(f"  Diubah   : {doc.updated_at}")
    print(f"  Jml Baris: {doc.get_line_count()}")
    print_separator()
    if doc.lines:
        for i, line in enumerate(doc.lines, 1):
            print(f"  {i:>3} | {line}")
    else:
        print("  (Dokumen kosong)")
    print_separator()


def pause():
    """Menunggu user menekan Enter untuk melanjutkan."""
    input("\n  Tekan Enter untuk melanjutkan...")
