import sys

# Alfabetul oficial al limbii române (31 litere)
ROMANIAN_ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

# Pentru matricea Playfair de 6x5 (30 celule), înlocuim 'J' cu 'I' (conform specficațiilor din laborator)
PLAYFAIR_ALPHABET = "AĂÂBCDEFGHIÎKLMNOPQRSȘTȚUVWXYZ"
GRID_ROWS = 6
GRID_COLS = 5

def normalize_text(text):
    """
    Transformă textul în majuscule, standardizează diacriticele și elimină spațiile.
    """
    # Toate operațiile cifrului folosesc aceeași reprezentare a literelor.
    text = text.upper()
    text = text.replace('Ş', 'Ș').replace('Ţ', 'Ț')
    text = text.replace(' ', '')
    # Litera J nu apare în alfabetul Playfair de 30 de caractere și este
    # tratată ca I pentru a putea construi matricea de 6 x 5.
    text = text.replace('J', 'I')
    return text

def validate_text(text):
    """
    Verifică dacă textul conține doar litere din alfabetul românesc.
    """
    normalized = normalize_text(text)
    for char in normalized:
        if char not in PLAYFAIR_ALPHABET:
            return False, char
    return True, ""

def validate_key(key):
    """
    Verifică dacă cheia are minim 7 caractere și conține doar litere valide.
    """
    normalized = normalize_text(key)
    if len(normalized) < 7:
        return False, "Lungimea cheii trebuie să fie de cel puțin 7 caractere."
    
    is_valid, bad_char = validate_text(key)
    if not is_valid:
        return False, f"Caracter invalid în cheie: '{bad_char}'. Permise doar litere A-Z și diacritice."
    return True, normalized

def build_matrix(key):
    """
    Construiește matricea Playfair de 6x5 pe baza cheii furnizate.
    """
    normalized_key = normalize_text(key)
    matrix_chars = []
    
    # Cheia apare prima în matrice, dar fiecare literă este introdusă o singură dată.
    for char in normalized_key:
        if char not in matrix_chars:
            matrix_chars.append(char)
            
    # Completăm cu literele alfabetului care nu au apărut deja în cheie.
    for char in PLAYFAIR_ALPHABET:
        if char not in matrix_chars:
            matrix_chars.append(char)
            
    # Cele 30 de caractere sunt împărțite pe 6 rânduri și 5 coloane.
    matrix = []
    for r in range(GRID_ROWS):
        row = matrix_chars[r * GRID_COLS : (r + 1) * GRID_COLS]
        matrix.append(row)
        
    return matrix

def display_matrix(matrix):
    """
    Afișează matricea Playfair într-un format lizibil.
    """
    print("\n--- Matricea de Criptare Playfair (6x5) ---")
    for row in matrix:
        print("  ".join(row))
    print("-------------------------------------------\n")

def find_position(matrix, char):
    """
    Găsește coordonatele (linie, coloană) ale unui caracter în matrice.
    """
    # Coordonatele sunt necesare pentru aplicarea regulilor Playfair.
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if matrix[r][c] == char:
                return r, c
    return None

def prepare_text_for_encryption(text):
    """
    Împarte textul în digrafe (perechi de 2 litere), inserând 'X' dacă literele sunt identice
    și 'X' la final dacă numărul total de litere este impar.
    """
    normalized = normalize_text(text)
    pairs = []
    i = 0
    while i < len(normalized):
        char1 = normalized[i]
        if i + 1 < len(normalized):
            char2 = normalized[i + 1]
            if char1 == char2:
                # Un digraf nu poate conține două litere identice; inserăm un filler.
                filler = 'Z' if char1 == 'X' else 'X'
                pairs.append((char1, filler))
                i += 1
            else:
                pairs.append((char1, char2))
                i += 2
        else:
            # Un text cu lungime impară primește un filler în ultima pereche.
            filler = 'Z' if char1 == 'X' else 'X'
            pairs.append((char1, filler))
            i += 1
    return pairs

def prepare_text_for_decryption(text):
    """
    Împarte criptograma în perechi de câte 2 litere.
    """
    normalized = normalize_text(text)
    pairs = []
    for i in range(0, len(normalized), 2):
        if i + 1 < len(normalized):
            pairs.append((normalized[i], normalized[i+1]))
    return pairs

def encrypt_pair(matrix, p1, p2):
    r1, c1 = find_position(matrix, p1)
    r2, c2 = find_position(matrix, p2)
    
    # Regula depinde de poziția celor două litere în matrice.
    if r1 == r2:
        # Regula 1: Aceeași linie -> deplasare la dreapta
        return matrix[r1][(c1 + 1) % GRID_COLS] + matrix[r2][(c2 + 1) % GRID_COLS]
    elif c1 == c2:
        # Regula 2: Aceeași coloană -> deplasare în jos
        return matrix[(r1 + 1) % GRID_ROWS][c1] + matrix[(r2 + 1) % GRID_ROWS][c2]
    else:
        # Regula 3: Dreptunghi -> schimbăm coloanele între ele
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(matrix, p1, p2):
    r1, c1 = find_position(matrix, p1)
    r2, c2 = find_position(matrix, p2)
    
    # La decriptare se aplică regulile inverse celor folosite la criptare.
    if r1 == r2:
        # Regula 1: Aceeași linie -> deplasare la stânga
        return matrix[r1][(c1 - 1) % GRID_COLS] + matrix[r2][(c2 - 1) % GRID_COLS]
    elif c1 == c2:
        # Regula 2: Aceeași coloană -> deplasare în sus
        return matrix[(r1 - 1) % GRID_ROWS][c1] + matrix[(r2 - 1) % GRID_ROWS][c2]
    else:
        # Regula 3: Dreptunghi -> schimbăm coloanele între ele
        return matrix[r1][c2] + matrix[r2][c1]

def main():
    print("==================================================")
    print("   Cifrul Playfair (Sarcina 3.1 - Limba Română)   ")
    print("==================================================")
    
    op = input("Alegeți operația (E - Criptare, D - Decriptare): ").strip().upper()
    if op not in ['E', 'D']:
        print("Eroare: Operație invalidă! Alegeți 'E' sau 'D'.")
        return

    # Introducere și validare cheie
    key_input = input("Introduceți cheia (lungime minimă 7 caractere): ")
    is_key_valid, key_msg = validate_key(key_input)
    if not is_key_valid:
        print(f"Eroare cheie: {key_msg}")
        return

    # Introducere și validare text
    text_input = input("Introduceți textul: ")
    is_text_valid, bad_char = validate_text(text_input)
    if not is_text_valid:
        print(f"Eroare text: Caracterul '{bad_char}' nu este permis! Folosiți doar litere din alfabetul românesc.")
        return

    # Construire și afișare matrice
    matrix = build_matrix(key_input)
    display_matrix(matrix)

    if op == 'E':
        pairs = prepare_text_for_encryption(text_input)
        ciphertext = ""
        # Criptăm fiecare digraf și concatenăm rezultatele într-o singură criptogramă.
        for p1, p2 in pairs:
            ciphertext += encrypt_pair(matrix, p1, p2)
        
        print("Digrafe pregătite:", " ".join([p1 + p2 for p1, p2 in pairs]))
        print(f"Text Criptat: {ciphertext}")
    else:
        pairs = prepare_text_for_decryption(text_input)
        plaintext = ""
        # Decriptăm perechile fără a elimina automat caracterul filler de la final.
        for p1, p2 in pairs:
            plaintext += decrypt_pair(matrix, p1, p2)
        
        print("Digrafe decriptate:", " ".join([p1 + p2 for p1, p2 in pairs]))
        print(f"Text Decriptat (fără spațiere): {plaintext}")

if __name__ == "__main__":
    main()