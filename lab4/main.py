import random

# Definirea celor 8 cutii de substituție (S-Boxes) standard DES
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

def generate_random_48bit():
    """Generează un șir binar aleatoriu de 48 biți."""
    return "".join(random.choice(['0', '1']) for _ in range(48))

def print_sbox_table(j, s_box):
    """Afișează matricea S-Box curentă într-un format lizibil."""
    print(f"\n--- Matricea S-Box S{j} ---")
    print("Linie/Col | " + " ".join(f"{c:2d}" for c in range(16)))
    print("-" * 62)
    for row_idx, row in enumerate(s_box):
        row_str = " ".join(f"{val:2d}" for val in row)
        print(f"   L{row_idx}     | {row_str}")
    print("-" * 62 + "\n")

def process_des_sbox_task(bits_48, j):
    """Procesează șirul de 48 biți și aplică S-Box j."""
    if len(bits_48) != 48 or not all(c in '01' for c in bits_48):
        raise ValueError("Șirul furnizat trebuie să aibă exact 48 de biți (0 și 1).")
    
    if not (1 <= j <= 8):
        raise ValueError("Indicele j trebuie să fie între 1 și 8.")

    print(f"\n[1] Șirul de 48 biți K_i (+) E(R_{{i-1}}):")
    print(f"    {bits_48}")

    # Împărțirea în 8 blocuri de câte 6 biți
    blocks = [bits_48[i*6:(i+1)*6] for i in range(8)]
    
    print("\n[2] Împărțirea pe cele 8 blocuri (B1 .. B8):")
    for idx, b in enumerate(blocks, start=1):
        mark = " <-- Bloc selectat (Bj)" if idx == j else ""
        print(f"    B{idx}: {b}{mark}")

    # Preluarea blocului Bj
    b_j = blocks[j - 1]
    
    # Calcularea liniei și coloanei
    row_bin = b_j[0] + b_j[5]
    col_bin = b_j[1:5]
    
    row_val = int(row_bin, 2)
    col_val = int(col_bin, 2)

    # Preluarea S-Box-ului corespunzător (indexat de la 0 la 7)
    s_box = S_BOXES[j - 1]
    
    print_sbox_table(j, s_box)

    output_val = s_box[row_val][col_val]
    output_bin = f"{output_val:04b}"

    print(f"[3] Analiza detaliată pentru B{j} = '{b_j}':")
    print(f"    - Primul și ultimul bit (b1, b6): '{row_bin}' -> Linia {row_val}")
    print(f"    - Biții din mijloc (b2..b5)    : '{col_bin}' -> Coloana {col_val}")
    print(f"    - Căutare în S{j}[Linia {row_val}][Coloana {col_val}] -> Valoarea decimală: {output_val}")
    print(f"    - Conversia în 4 biți: {output_bin}")
    print("\n" + "="*50)
    print(f" REZULTAT FINAL: S_{j}(B_{j}) = {output_bin} (hex: {hex(output_val)[2:].upper()})")
    print("="*50 + "\n")

    # Afișarea tuturor valorilor S1..S8 pentru o imagine completă
    print("[Opțional] Calculul aplicării tuturor celor 8 S-Boxes S1(B1)..S8(B8):")
    all_outputs = []
    for idx, b in enumerate(blocks):
        r_bin = b[0] + b[5]
        c_bin = b[1:5]
        r = int(r_bin, 2)
        c = int(c_bin, 2)
        out_v = S_BOXES[idx][r][c]
        out_b = f"{out_v:04b}"
        all_outputs.append(out_b)
        print(f"    S{idx+1}(B{idx+1}) = S{idx+1}[{r}][{c}] = {out_b}")
    
    full_32bit = "".join(all_outputs)
    print(f"\n Rezultat total (32 biți după S-Boxes): {full_32bit}")

def main():
    print("==================================================")
    print("   DES Laboratory Work 4 - Sarcina 2.9 (S-Boxes)  ")
    print("==================================================")
    
    print("Alegeți modalitatea de introducere a datelor:")
    print("1 - Generare aleatorie a șirului de 48 biți")
    print("2 - Introducere manuală (șir de 48 biți binari)")
    print("3 - Introducere manuală în format Hexazecimal (12 caractere HEX)")
    
    choice = input("Opțiunea dvs. (1/2/3): ").strip()
    
    bits_48 = ""
    if choice == '1':
        bits_48 = generate_random_48bit()
    elif choice == '2':
        bits_48 = input("Introduceți șirul de 48 biți (0 și 1): ").strip()
    elif choice == '3':
        hex_in = input("Introduceți 12 caractere HEX (ex: 1F4A0B9C2D3E): ").strip()
        try:
            bits_48 = bin(int(hex_in, 16))[2:].zfill(48)
        except ValueError:
            print("Eroare: Format hexazecimal invalid!")
            return
    else:
        print("Opțiune invalidă.")
        return

    try:
        j_input = int(input("Introduceți indicele j pentru S_j (1 - 8): ").strip())
        process_des_sbox_task(bits_48, j_input)
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    main()