import os
import math
from tkinter import Tk, filedialog
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

def pilih_file_pdf():
    root = Tk(); root.withdraw(); root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title="Pilih file PDF", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
    root.destroy(); return file_path

def pilih_file_txt():
    root = Tk(); root.withdraw(); root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title="Pilih file TXT", filetypes=[("Text Files", "*.txt")])
    root.destroy(); return file_path

def mod_inverse(a, m=256):
    if math.gcd(a, m) != 1: return None
    for i in range(1, m):
        if (a * i) % m == 1: return i
    return None

def generate_nama_file(folder, base_name, ext):
    i = 1
    while True:
        nama = f"{base_name}{i}.{ext}"; path = os.path.join(folder, nama)
        if not os.path.exists(path): return nama
        i += 1

def build_pdf_canvas(output_path, hex_data):
    c = canvas.Canvas(output_path, pagesize=letter); width, height = letter
    margin = 40; y = height - margin; font_name = "Courier"; font_size = 7; line_height = 9
    c.setFont(font_name, font_size); max_width = width - 2 * margin
    char_width = c.stringWidth("A", font_name, font_size); chars_per_line = int(max_width // char_width)
    for i in range(0, len(hex_data), chars_per_line):
        if y <= margin: c.showPage(); c.setFont(font_name, font_size); y = height - margin
        c.drawString(margin, y, hex_data[i:i+chars_per_line]); y -= line_height
    c.save()

def printable_byte(k):
    if 32 <= k <= 126: return chr(k)
    return f"\\x{k:02x}"

def vigenere_dekripsi_bytes(data, key, log_vig_dec):
    hasil = bytearray()
    with open(log_vig_dec, "w") as log_file:
        log_file.write("===== PROSES DEKRIPSI VIGENERE MULTIPLICATIVE CIPHER =====\n")
        log_file.write("Rumus: P[i] = (C[i] * k_inv[i]) mod 256\n")
        log_file.write("Index | Data Byte | Key Byte | Invers Key | Hasil Dekripsi (P[i])\n")
        log_file.write("-" * 70 + "\n")
        for i in range(len(data)):
            k = key[i % len(key)]; inv_k = mod_inverse(k, 256); p = (data[i] * inv_k) % 256; hasil.append(p)
            log_file.write(f"{i:5} | {data[i]:9} | {k:8} | {inv_k:10} | {p:28}\n")
    print("\n===== PROSES DEKRIPSI VIGENERE MULTIPLICATIVE CIPHER =====")
    print("Rumus: P[i] = (C[i] * k_inv[i]) mod 256")
    for i in range(len(data)):
        k = key[i % len(key)]; inv_k = mod_inverse(k, 256); p = (data[i] * inv_k) % 256
        if i < 10: print(f"{i:5} | {data[i]:9} | {k:8} | {inv_k:10} | {p:28}")
        if i != 0 and i % (len(data)//10 + 1) == 0: print(f"Progress Dekripsi Vigenere Multiplicative Cipher: {(i/len(data))*100:.2f}% selesai")
    return hasil

def main():
    print("===== DEKRIPSI VIGENERE MULTIPLICATIVE CIPHER =====")
    print("Pilih file cipherteks (.PDF):"); file_path = pilih_file_pdf()
    teks = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t: teks += t + " "
    if not teks: print("Gagal membaca PDF."); return
    print("\n===== PREVIEW CIPHERTEKS ====="); print(teks[:60] + ("..." if len(teks) > 60 else ""))
    cipher_bytes = bytes.fromhex(teks)
    print("\n===== BYTE DESIMAL ====="); print(", ".join(str(b) for b in cipher_bytes[:20]) + ("..." if len(cipher_bytes) > 20 else ""))
    print("\nMasukkan file kunci simetris (.txt):"); key_file = pilih_file_txt()
    with open(key_file, "rb") as f: key = list(f.read())
    key_display = "".join(printable_byte(k) for k in key)
    print("\n===== KUNCI SIMETRIS(REPRESENTATIF) ====="); print(key_display[:60] + ("..." if len(key_display) > 60 else ""))
    print("\n===== KONVERSI KE DESIMAL ====="); print(", ".join(str(k) for k in key[:20]) + ("..." if len(key) > 20 else ""))
    base_dir = os.path.dirname(os.path.abspath(__file__)); folder_output = os.path.join(base_dir, "File Percobaan"); folder_log = os.path.join(folder_output, "Progress dekripsi")
    os.makedirs(folder_output, exist_ok=True); os.makedirs(folder_log, exist_ok=True)
    plain_path = os.path.join(folder_output, generate_nama_file(folder_output, "Hasil_Dekripsi_Vigenere_", "pdf")); log_path = os.path.join(folder_log, generate_nama_file(folder_log, "Log_Dekripsi_Vigenere_", "txt"))
    hasil = vigenere_dekripsi_bytes(cipher_bytes, key, log_path)
    print("\n===== HASIL DEKRIPSI (DESIMAL - PREVIEW) ====="); print(", ".join(str(b) for b in hasil[:20]) + ("..." if len(hasil) > 20 else ""))
    plain_bytes = bytes(hasil)
    print("\n===== PREVIEW HEADER PDF ====="); print(plain_bytes[:120].decode(errors="ignore"))
    with open(plain_path, "wb") as f: f.write(plain_bytes)
    print(f"\nFile hasil dekripsi: {os.path.basename(plain_path)}"); print(f"Log dekripsi disimpan dalam: {os.path.basename(log_path)}")
    os.startfile(plain_path)

if __name__ == "__main__": main()
