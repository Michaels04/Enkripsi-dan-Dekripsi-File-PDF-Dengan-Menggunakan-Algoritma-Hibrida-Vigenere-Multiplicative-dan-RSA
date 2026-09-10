import os
import re
from tkinter import Tk, filedialog

def pilih_file_txt():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title="Pilih file TXT", filetypes=[("Text Files", "*.txt")])
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

def ambil_public_key(file_path):
    with open(file_path, "r") as f:
        for line in f:
            if "Public Key" in line:
                angka = re.findall(r'\d+', line)
                e, n = map(int, angka[:2])
                return (e, n)
    raise ValueError("Public Key tidak ditemukan!")

def rsa_enkripsi_bytes(data_bytes, pub, log_rsa_enc):
    e, n = pub
    enc = []
    with open(log_rsa_enc, "w") as log_file:
        log_file.write("===== PROSES ENKRIPSI RSA  =====\n")
        log_file.write("Rumus: C = P^e mod n\n")
        log_file.write(f"Public Key = {pub}\n\n")
        for b in data_bytes:
            c = pow(b, e, n)
            enc.append(c)
            log_file.write(f"{b}^{e} mod {n} = {c}\n")

    print("\n===== PROSES ENKRIPSI RSA =====")
    for i, b in enumerate(data_bytes):
        if i < 10:
            print(f"{b}^{e} mod {n} = {pow(b, e, n)}")
        elif i % (len(data_bytes)//10 + 1) == 0:
            persen = (i / len(data_bytes)) * 100
            print(f"Progress: {persen:.2f}%")
    print("Enkripsi selesai.")
    return enc

def main():
    print("===== ENKRIPSI ALGORITMA RSA  =====")
    print("Pilih file kunci simetris yang akan menjadi plainteks (.txt):")
    file_input = pilih_file_txt()
    with open(file_input, "rb") as f:
        data_bytes = f.read()

    print("\n===== PREVIEW PLAINTEXT =====")
    key_display = "".join(printable_byte(k) for k in data_bytes)
    print(key_display[:60] + ("..." if len(key_display) > 60 else ""))
    print("\n===== KONVERSI KE DESIMAL =====")
    print(", ".join(str(b) for b in data_bytes[:20]) + ("..." if len(data_bytes) > 20 else ""))

    print("\nPilih file kunci RSA:")
    rsa_file = pilih_file_txt()
    pub_key = ambil_public_key(rsa_file)
    print("Public Key:", pub_key)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_output = os.path.join(base_dir, "File Percobaan")
    folder_log = os.path.join(folder_output, "Progress enkripsi")
    os.makedirs(folder_output, exist_ok=True)
    os.makedirs(folder_log, exist_ok=True)

    nama_cipher = generate_nama_file(folder_output, "Cipherteks_RSA_", "txt")
    nama_log = generate_nama_file(folder_log, "Log_Enkripsi_RSA_", "txt")
    cipher_path = os.path.join(folder_output, nama_cipher)
    log_path = os.path.join(folder_log, nama_log)

    hasil = rsa_enkripsi_bytes(list(data_bytes), pub_key, log_path)
    print("\n===== CIPHERTEKS RSA (DESIMAL) =====")
    preview_rsa = ", ".join(str(c) for c in hasil[:10])
    if len(hasil) > 10:
        preview_rsa += ", ..."
    print(preview_rsa)

    cipher_hex = [format(c, "x") for c in hasil]
    print("\n===== CIPHERTEKS RSA (HEX) =====")
    preview = " ".join(cipher_hex[:10])
    if len(cipher_hex) > 10:
        preview += " ..."
    print(preview)

    with open(cipher_path, "w") as f:
        f.write(" ".join(cipher_hex))
    os.startfile(cipher_path)
    print("Cipherteks disimpan di dalam file :", os.path.basename(cipher_path))
    print("Log enkripsi disimpan di dalam file :", os.path.basename(log_path))

if __name__ == "__main__":
    main()
