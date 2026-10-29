import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Koneksi ke Database SQLite
conn = sqlite3.connect("prediksi_diabetes.db")
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT,
    usia INTEGER,
    gula_darah REAL,
    bmi REAL,
    riwayat_ortu TEXT,
    hasil_prediksi TEXT
)
""")
conn.commit()


def prediksi():
    try:
        nama = nama_entry.get().strip()
        usia = int(usia_entry.get())
        gula = float(gula_entry.get())
        bmi = float(bmi_entry.get())
        riwayat = ortu_box.get()

        if not nama or not riwayat:
            raise ValueError

        if usia < 1 or usia > 120 or gula <= 0 or bmi <= 0:
            messagebox.showerror("Error", "Data tidak valid! Masukkan angka yang sesuai.")
            return

        # Logika Prediksi Risiko Diabetes
        if gula >= 200:
            hasil = "Sangat Tinggi" if bmi >= 30 or riwayat == "Ya" else "Tinggi"
        elif gula >= 140:
            hasil = "Tinggi" if bmi >= 30 and riwayat == "Ya" else "Sedang"
        elif bmi >= 30:
            hasil = "Sedang" if riwayat == "Ya" else "Waspada"
        elif riwayat == "Ya":
            hasil = "Waspada"
        else:
            hasil = "Rendah"

        # Simpan ke Database SQLite
        cursor.execute("""
        INSERT INTO pasien 
        (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (nama, usia, gula, bmi, riwayat, hasil))
        conn.commit()

        # Warna teks hasil prediksi
        warna = {
            "Rendah": "green",
            "Waspada": "blue",
            "Sedang": "orange",
            "Tinggi": "red",
            "Sangat Tinggi": "darkred"
        }
        hasil_label.config(text="Hasil: " + hasil, fg=warna[hasil])
        
        messagebox.showinfo("Sukses", "Data berhasil disimpan dan diprediksi!")

    except ValueError:
        messagebox.showerror("Error", "Periksa kembali semua input! Pastikan semua kolom terisi dan usia, gula darah, serta BMI berupa angka.")


def lihat_data():
    # Membuat jendela baru (Toplevel)
    jendela_data = tk.Toplevel(root)
    jendela_data.title("Data Riwayat Pasien")
    jendela_data.geometry("680x350")

    # Membuat Treeview (Tabel)
    columns = ("ID", "Nama", "Usia", "Gula Darah", "BMI", "Riwayat", "Hasil")
    tree = ttk.Treeview(jendela_data, columns=columns, show="headings")

    # Mengatur judul dan lebar kolom
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=90, anchor="center")
    
    tree.column("Nama", width=120, anchor="w")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Mengambil seluruh data dari database pasien
    cursor.execute("SELECT * FROM pasien")
    rows = cursor.fetchall()

    # Memasukkan data ke dalam tabel GUI
    for row in rows:
        tree.insert("", "end", values=row)


