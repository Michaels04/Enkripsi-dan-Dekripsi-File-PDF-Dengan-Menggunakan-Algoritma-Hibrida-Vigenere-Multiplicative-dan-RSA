import random
import os

def generate_nama_file(folder, base_name, ext):
    i = 1
    while True:
        nama = f"{base_name}_{i}.{ext}"
        path = os.path.join(folder, nama)
        if not os.path.exists(path):
            return nama
        i += 1

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def generate_rsa():
    primes = [i for i in range(1000, 10000)
              if all(i % j != 0 for j in range(2, int(i**0.5)+1))]

    p = random.choice(primes)
    q = random.choice(primes)
    while q == p:
        q = random.choice(primes)

    print("\n===== PARAMETER RSA =====")
    print("\n===== LANGKAH 1: Pilih Bilangan Prima p dan q secara acak =====")
    print("p =", p)
    print("q =", q)

    print("\n===== LANGKAH 2: Hitung n dan φ(n) =====")
    print("Rumus n = p * q")
    n = p * q
    print("n =", n)

    print("\nRumus φ(n) = (p-1) * (q-1)")
    phi = (p-1) * (q-1)
    print("φ(n) =", phi)

    print("\n===== LANGKAH 3: Pilih e yang relatif prima dengan φ(n) =====")
    while True:
        e = random.randint(3, phi-1)
        if gcd(e, phi) == 1:
            break

    print("Dipilih e =", e)
    print("gcd(e, φ(n)) =", gcd(e, phi), "→ e relatif prima dengan φ(n)")

    print("\n===== LANGKAH 4: Hitung d =====")
    print("Rumus d = (1+k*φ(n)) / e, untuk k = 1, 2, ...")

    k = 1
    while True:
        numerator = 1 + k * phi
        if numerator % e == 0:
            d = numerator // e
            break
        k += 1

    print("Nilai k yang memenuhi =", k)
    print("d =", d)
    print("\nDidapatkan Pasangan Kunci Publik dan Privat RSA, yaitu:")
    print("Public Key  =", (e, n))
    print("Private Key =", (d, n))
    return (e, n), (d, n)

def simpan_kunci_rsa(public_key, private_key):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_output = os.path.join(base_dir, "File Percobaan", "Kunci")
    os.makedirs(folder_output, exist_ok=True)
    nama_file = generate_nama_file(folder_output, "Kunci_RSA", "txt")
    path_file = os.path.join(folder_output, nama_file)
    with open(path_file, "w") as f:
        f.write("===== KUNCI RSA =====\n")
        f.write(f"Public Key  = {public_key}\n")
        f.write(f"Private Key = {private_key}\n")
    print(f"\nKunci RSA disimpan di file: {path_file}")

if __name__ == "__main__":
    public_key, private_key = generate_rsa()
    simpan_kunci_rsa(public_key, private_key)
