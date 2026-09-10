import math
import os
from tkinter import Tk, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def pilih_file_pdf():
    root = Tk(); root.withdraw(); root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title="Pilih file PDF", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
    root.destroy(); return file_path

def pilih_file_txt():
    root = Tk(); root.withdraw(); root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title="Pilih file TXT", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
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

def vigenere_enkripsi_bytes(data, key, log_vig_enc):
    hasil = bytearray()
    with open(log_vig_enc, "w") as log_file:
        log_file.write("===== PROSES ENKRIPSI VIGENERE MULTIPLICATIVE CIPHER =====\n")
        log_file.write("Rumus: C[i] = (P[i] * k[i]) mod 256\n")
        log_file.write("Index | Data Byte | Key Byte | Hasil Enkripsi (C[i])\n")
        log_file.write("-" * 55 + "\n")
        for i in range(len(data)):
            k = key[i % len(key)]; c = (data[i] * k) % 256; hasil.append(c)
            log_file.write(f"{i:5} | {data[i]:9} | {k:8} | {c:28}\n")
    print("\n===== PROSES ENKRIPSI VIGENERE MULTIPLICATIVE CIPHER =====")
    print("Rumus: C[i] = (P[i] * k[i]) mod 256")
    for i in range(len(data)):
        k = key[i % len(key)]; c = (data[i] * k) % 256
        if i < 10: print(f"{i:5} | {data[i]:9} | {k:8} | {c:28}")
        if i != 0 and i % (len(data)//10 + 1) == 0: print(f"Progress Enkripsi Vigenere Multiplicative Cipher: {(i/len(data))*100:.2f}% selesai")
    print(f"\nEnkripsi Vigenere Multiplicative Cipher selesai. Progress disimpan dalam '{os.path.basename(log_vig_enc)}'.")
    return hasil

def main():
    print("===== ENKRIPSI VIGENERE MULTIPLICATIVE CIPHER =====")
    print("\nPilih file PDF yang akan dienkripsi:"); pdf_file = pilih_file_pdf()
    with open(pdf_file, "rb") as f: data = f.read()
    print("===== PREVIEW HEADER PDF ====="); print(data[:120].decode(errors="ignore")); print(f"File '{os.path.basename(pdf_file)}' berhasil dibaca. Ukuran: {len(data)} bytes")
    print("\nMasukkan kunci simetris:"); key_file = pilih_file_txt()
    with open(key_file, "rb") as f: key = list(f.read())
    print("===== KUNCI SIMETRIS (REPRESENTATIF) ====="); print("".join(printable_byte(k) for k in key)[:60])
    base_dir = os.path.dirname(os.path.abspath(__file__)); folder_output = os.path.join(base_dir, "File Percobaan"); folder_log = os.path.join(folder_output, "Progress enkripsi")
    os.makedirs(folder_output, exist_ok=True); os.makedirs(folder_log, exist_ok=True)
    output_pdf = os.path.join(folder_output, generate_nama_file(folder_output, "Cipherteks_Vigenere_", "pdf")); log_vig = os.path.join(folder_log, generate_nama_file(folder_log, "Log_Enkripsi_Vigenere_", "txt"))
    print("\n===== BYTE PDF (DESIMAL - PREVIEW) ====="); print(list(data[:20])); print("\n===== KUNCI SIMETRIS (DESIMAL - PREVIEW) ====="); print(key[:20])
    cipher = vigenere_enkripsi_bytes(data, key, log_vig); hex_data = cipher.hex()
    print("\n===== DATA ENKRIPSI HEX ====="); print(hex_data[:120]); build_pdf_canvas(output_pdf, hex_data)
    print("\nFile hasil enkripsi:", os.path.basename(output_pdf)); os.startfile(output_pdf)

if __name__ == "__main__": main()
