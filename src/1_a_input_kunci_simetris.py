import math
import random
import os

# ================= FUNGSI MENGHITUNG INVERS MODULO ================= #
def mod_inverse(a, m=256):
    if math.gcd(a, m) != 1:
        return None
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# ================= FUNGSI GENERATE NAMA FILE ================= #
def generate_nama_file(folder, base_name, ext):
    i = 1
    while True:
        nama = f"{base_name}_{i}.{ext}"
        path = os.path.join(folder, nama)
        if not os.path.exists(path):
            return nama
        i += 1

# ================= FORMAT BYTE REPRESENTATIF ================= #
def printable_character(k):
    if 32 <= k <= 126:
        return chr(k)
    else:
        return f"\\x{k:02x}"

def format_key_display(text, width=60):
    return [text[i:i+width] for i in range(0, len(text), width)]

# ================= GENERATE KUNCI ================= #
def generate_kunci():
    print("\n===== GENERATOR KUNCI SIMETRIS =====")

    while True:
        try:
            len_key = int(input("Masukkan panjang kunci simetris yang diinginkan : "))
            if len_key <= 0:
                print("Panjang kunci harus lebih dari 0.")
                continue
            break
        except ValueError:
            print("Input tidak valid.")

    syarat_kunci = [i for i in range(1, 256) if math.gcd(i, 256) == 1]
    pilihan_kunci = []

    print("\n===== MEMILIH KUNCI SIMETRIS =====")

    for i in range(5):
        key = [random.choice(syarat_kunci) for _ in range(len_key)]
        pilihan_kunci.append(key)

        char_key = "".join(printable_character(k) for k in key)
        lines = format_key_display(char_key, 60)

        print(f"Pilihan {i+1}:")
        for line in lines:
            print(f"   {line}")

    while True:
        try:
            pilihan = int(input("\nPilih kunci simetris yang akan digunakan (1-5): "))
            if 1 <= pilihan <= 5:
                return pilihan_kunci[pilihan - 1]
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Input tidak valid.")

# ================= INPUT KUNCI ================= #
def input_kunci():
    print("===== INPUT KUNCI SIMETRIS =====")

    teks_kunci = input("Masukkan kunci simetris : ")

    key = [ord(c) for c in teks_kunci]

    total = len(key)
    valid_count = sum(1 for k in key if mod_inverse(k, 256) is not None)

    print("\n===== VALIDASI KUNCI SIMETRIS =====")
    print(f"Jumlah byte valid: {valid_count}/{total}")

    if valid_count == total:
        print("Kunci Valid")
        return key

    print("Kunci Tidak Valid")

    while True:
        print("\n1. Masukkan ulang kunci")
        print("2. Generate kunci otomatis")

        pilihan = input("Pilih opsi (1/2): ")

        if pilihan == "1":
            return input_kunci()
        elif pilihan == "2":
            return generate_kunci()
        else:
            print("Pilihan tidak valid.")

# ================= PROGRAM UTAMA ================= #
def main():
    key = input_kunci()

    char_key = "".join(printable_character(k) for k in key)

    print("\n===== KUNCI SIMETRIS TERPILIH (REPRESENTATIF) =====")
    print(char_key[:60] + ("..." if len(char_key) > 60 else ""))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_output = os.path.join(base_dir, "File Percobaan", "Kunci")

    os.makedirs(folder_output, exist_ok=True)

    nama_file = generate_nama_file(folder_output, "Kunci_Simetris", "txt")
    path_file = os.path.join(folder_output, nama_file)

    with open(path_file, "wb") as f:
        f.write(bytes(key))

    print(f"\nKunci simetris (berbentuk byte asli) disimpan di file: {os.path.basename(path_file)}")

if __name__ == "__main__":
    main()
