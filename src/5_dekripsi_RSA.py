import os
import re
from tkinter import Tk, filedialog

def pilih_file_txt():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title="Pilih file TXT", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    root.destroy()
    return file_path

def generate_nama_file(folder, base_name, ext):
    i = 1
    while True:
        nama = f"{base_name}{i}.{ext}"
        path = os.path.join(folder, nama)
        if not os.path.exists(path):
            return nama
        i += 1

def printable_byte(k):
    if 32 <= k <= 126:
        return chr(k)
    return f"\\x{k:02x}"

def ambil_private_key(file_path):
    with open(file_path, "r") as f:
        for line in f:
            if "Private Key" in line:
                angka = re.findall(r'\d+', line)
                d, n = map(int, angka[:2])
                return (d, n)
    raise ValueError("Private Key tidak ditemukan!")

def rsa_dekripsi_bytes(enc_list, priv, log_rsa_dec):
    d, n = priv
    hasil_bytes = []
    with open(log_rsa_dec, "w") as log_file:
        log_file.write("===== PROSES DEKRIPSI RSA  =====\n")
        log_file.write("Rumus: P = C^d mod n\n")
        log_file.write(f"Private Key = {priv}\n\n")
        for c in enc_list:
            if c >= n:
                raise ValueError(f"Cipher lebih besar dari n: {c}")
            p = pow(c, d, n)
            if p > 255:
                raise ValueError(f"Byte tidak valid hasil dekripsi: {p}")
            hasil_bytes.append(p)
            log_file.write(f"{c}^{d} mod {n} = {p}\n")

    print("\n===== PROSES DEKRIPSI RSA =====")
    for i, c in enumerate(enc_list):
        if i < 10:
            print(f"{c}^{d} mod {n} = {pow(c, d, n)}")
        elif i % (len(enc_list)//10 + 1) == 0:
            persen = (i/len(enc_list))*100
            print(f"Progress: {persen:.2f}%")
    print("Dekripsi selesai.")
    return bytes(hasil_bytes)

def main():
    print("===== DEKRIPSI ALGORITMA RSA =====")
    print("Pilih file cipherteks RSA (.txt):")
    file_cipherteks = pilih_file_txt()
    with open(file_cipherteks, "r") as f:
        teks = f.read()
    if not teks:
        print("Gagal membaca file.")
        return

    print("\n===== PREVIEW CIPHERTEKS =====")
    print(teks[:60] + ("..." if len(teks) > 60 else ""))
    teks = teks.replace("\n", " ").replace("\r", " ")
    hex_list = teks.split()
    if len(hex_list) == 0:
        print("Cipher kosong!")
        return

    try:
        enc_list = [int(h, 16) for h in hex_list]
    except:
        raise ValueError("Format HEX rusak (kemungkinan PDF corrupt)")

    print("\n===== KONVERSI KE DESIMAL =====")
    print(", ".join(str(b) for b in enc_list[:20]) + ("..." if len(enc_list) > 20 else ""))
    print("\nPilih file kunci RSA (.txt):")
    rsa_file = pilih_file_txt()
    priv_key = ambil_private_key(rsa_file)
    print("Private Key:", priv_key)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.join(base_dir, "File Percobaan")
    folder_output = os.path.join(root_folder, "Kunci")
    folder_log = os.path.join(root_folder, "Progress dekripsi")
    os.makedirs(folder_output, exist_ok=True)
    os.makedirs(folder_log, exist_ok=True)

    nama_plain = generate_nama_file(folder_output, "Hasil_Dekripsi_Kunci_Simetris_", "txt")
    nama_log = generate_nama_file(folder_log, "Log_Dekripsi_RSA_", "txt")
    plain_path = os.path.join(folder_output, nama_plain)
    log_path = os.path.join(folder_log, nama_log)

    hasil = rsa_dekripsi_bytes(enc_list, priv_key, log_path)
    print("\n===== HASIL DEKRIPSI RSA (DESIMAL) =====")
    preview = ", ".join(str(p) for p in hasil[:20])
    if len(hasil) > 20:
        preview += ", ..."
    print(preview)

    with open(plain_path, "wb") as f:
        f.write(hasil)

    print("\n===== HASIL =====")
    hasil_display = "".join(printable_byte(b) for b in hasil)
    print(hasil_display[:60] + ("..." if len(hasil_display) > 60 else ""))
    print("File hasil:", os.path.basename(plain_path))
    print("Log dekripsi disimpan di dalam file :", os.path.basename(log_path))

if __name__ == "__main__":
    main()
