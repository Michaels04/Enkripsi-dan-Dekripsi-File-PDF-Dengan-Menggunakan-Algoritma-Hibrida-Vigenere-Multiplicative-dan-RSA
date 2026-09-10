# Enkripsi dan Dekripsi File PDF dengan Algoritma Hibrida Vigenere Multiplicative dan RSA

Project ini merupakan implementasi sistem **enkripsi dan dekripsi file PDF** menggunakan pendekatan kriptografi hibrida. Data PDF dienkripsi menggunakan **Multiplicative Vigenere Cipher**, sedangkan kunci simetris diamankan menggunakan **RSA**.

## 🔐 Konsep

Sistem menggunakan dua jenis algoritma:

- **Multiplicative Vigenere Cipher** — digunakan untuk mengenkripsi byte dari file PDF.
- **RSA** — digunakan untuk mengenkripsi kunci simetris sehingga kunci dapat diamankan secara terpisah.

### Rumus utama

Enkripsi byte:

`C[i] = (P[i] × K[i]) mod 256`

Dekripsi byte menggunakan invers modulo:

`P[i] = (C[i] × K⁻¹[i]) mod 256`

Setiap nilai kunci harus memiliki invers modulo 256 agar proses dekripsi dapat dilakukan.

## ✨ Fitur

- Generate kunci simetris.
- Input kunci simetris secara manual.
- Enkripsi file PDF menggunakan Multiplicative Vigenere.
- Generate pasangan kunci RSA.
- Enkripsi kunci simetris menggunakan RSA.
- Dekripsi kunci RSA.
- Dekripsi kembali file PDF menggunakan kunci simetris.
- Pemilihan file menggunakan file picker Tkinter.

## 📂 Struktur Program

```text
.
├── 1_a_input_kunci_simetris.py
├── 1_generate_kunci_simetris.py
├── 2_enkripsi_vigenere.py
├── 3_generate_kunci_RSA.py
├── 4_enkripsi_RSA.py
├── 5_dekripsi_RSA.py
├── 6_dekripsi_vigenere.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Requirements

Python 3.x dan library berikut:

```bash
pip install reportlab pdfplumber
```

`tkinter`, `math`, `random`, `os`, `re`, dan `logging` merupakan bagian dari standard library Python (Tkinter pada beberapa sistem perlu dipasang melalui paket OS).

## 🚀 Cara Menjalankan

Jalankan program sesuai urutan proses yang diperlukan:

1. Buat/input kunci simetris.
2. Jalankan enkripsi Multiplicative Vigenere terhadap PDF.
3. Generate kunci RSA.
4. Enkripsi kunci simetris menggunakan RSA.
5. Saat proses dekripsi, lakukan dekripsi kunci RSA.
6. Gunakan kunci hasil dekripsi untuk mengembalikan PDF ke bentuk semula.

Contoh menjalankan program:

```bash
python 1_generate_kunci_simetris.py
```

Kemudian lanjutkan ke file Python berikutnya sesuai alur program.

## 🧩 Alur Sistem

```text
             File PDF Asli
                   │
                   ▼
       Multiplicative Vigenere
                   │
                   ▼
          PDF Terenkripsi

     Kunci Simetris ──────────┐
                              ▼
                         RSA Encryption
                              │
                              ▼
                    Kunci RSA Terenkripsi

          Proses Dekripsi dilakukan
          secara terbalik untuk
          mendapatkan PDF asli.
```

## ⚠️ Catatan

Project ini dibuat untuk **pembelajaran dan penelitian/skripsi di bidang kriptografi**. Implementasi algoritma dibuat secara manual untuk memahami proses kerja algoritma dan tidak dimaksudkan sebagai pengganti library kriptografi yang telah diaudit untuk sistem produksi.

## 👨‍💻 Author

**Michaels04**

GitHub: https://github.com/Michaels04
