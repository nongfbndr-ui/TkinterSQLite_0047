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

        