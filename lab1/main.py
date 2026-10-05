import sys

# Alfabetul oficial românesc (n=31) conform tabelului 2
ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
N = len(ALPHABET)

def normalize_text(text):
    # Convertire la majuscule
    text = text.upper()
    # Înlocuirea literelor cu sedilă cu cele cu virgulă (conform Implementation tip)
    text = text.replace('Ş', 'Ș').replace('Ţ', 'Ț')
    # Eliminarea spațiilor
    text = text.replace(' ', '')
    return text

def validate_text(text):
    for char in text:
        if char not in ALPHABET:
            return False, char
    return True, ""

def validate_key1(k):
    if not str(k).isdigit(): return False
    k = int(k)
    return 1 <= k <= 30

def validate_key2(keyword):
    keyword = normalize_text(keyword)
    if len(keyword) < 7:
        return False, "Cuvântul cheie trebuie să aibă cel puțin 7 caractere."
    is_valid, bad_char = validate_text(keyword)
    if not is_valid:
        return False, f"Caracter invalid în cuvântul cheie: {bad_char}"
    return True, keyword

# Task 1.1: Caesar clasic
def caesar_cipher(text, k, encrypt=True):
    result = ""
    for char in text:
        x = ALPHABET.index(char)
        if encrypt:
            new_pos = (x + k) % N
        else:
            new_pos = (x - k) % N
        result += ALPHABET[new_pos]
    return result

# Task 1.2: Caesar cu permutare
def build_permuted_alphabet(keyword):
    permuted = ""
    # Adăugăm literele din cheie fără duplicate
    for char in keyword:
        if char not in permuted:
            permuted += char
    # Adăugăm restul alfabetului
    for char in ALPHABET:
        if char not in permuted:
            permuted += char
    return permuted

def caesar_permuted_cipher(text, permuted_alphabet, k, encrypt=True):
    result = ""
    for char in text:
        x = permuted_alphabet.index(char)
        if encrypt:
            new_pos = (x + k) % N
        else:
            new_pos = (x - k) % N
        result += permuted_alphabet[new_pos]
    return result

# Meniul interactiv
def main():
    print("=== Cifrul Caesar - Alfabetul Românesc ===")
    task = input("Alegeți Task-ul (1 pentru clasic, 2 pentru permutare): ")
    
    op = input("Alegeți operația (E pentru criptare, D pentru decriptare): ").upper()
    if op not in ['E', 'D']:
        print("Operație invalidă!")
        return

    encrypt = (op == 'E')
    text = input("Introduceți textul: ")
    text = normalize_text(text)
    
    is_valid, bad_char = validate_text(text)
    if not is_valid:
        print(f"Eroare: Textul conține un caracter invalid '{bad_char}'. Permis doar A-Z și diacritice.")
        return

    k1_str = input("Introduceți cheia numerică k (1-30): ")
    if not validate_key1(k1_str):
        print("Eroare: Cheia k trebuie să fie un număr întreg între 1 și 30 inclusiv.")
        return
    k1 = int(k1_str)

    if task == '1':
        # Task 1.1
        result = caesar_cipher(text, k1, encrypt)
        print(f"\nRezultat Task 1.1: {result}")

    elif task == '2':
        # Task 1.2
        keyword_str = input("Introduceți cuvântul cheie k2 (min 7 litere): ")
        is_valid_k2, msg = validate_key2(keyword_str)
        if not is_valid_k2:
            print(f"Eroare: {msg}")
            return
        
        # Generare și afișare alfabet permutat
        permuted_alpha = build_permuted_alphabet(msg)
        print(f"\nAlfabetul standard: {ALPHABET}")
        print(f"Alfabetul permutat: {permuted_alpha}")
        
        result = caesar_permuted_cipher(text, permuted_alpha, k1, encrypt)
        print(f"Rezultat Task 1.2: {result}")
    else:
        print("Task invalid.")

if __name__ == "__main__":
    main()