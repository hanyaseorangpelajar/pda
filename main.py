import os

start_input = ""  # kata yang akan dicek apakah diterima atau tidak
found = 0  # status apakah kata ditemukan
accepted_config = []  # menyimpan konfigurasi akhir yang diterima

# aturan produksi ("baca input", "pop stack", "push stack", "state berikutnya")
productions = {}

# simbol awal
start_symbol = ""

# simbol awal stack
stack_start = ""

# daftar state yang diterima
acceptable_states = []

# E - diterima jika stack kosong atau F - diterima di state tertentu
accept_with = ""


def generate(state, input, stack, config):
    """
    Secara rekursif menghasilkan semua kemungkinan jalur di automata untuk 
    memeriksa apakah input diterima.
    """
    global productions, found

    # Jika jalur valid sudah ditemukan, hentikan eksplorasi lebih lanjut
    if found:
        return 0

    # Periksa apakah konfigurasi saat ini diterima
    if is_found(state, input, stack):
        found = 1  # Tandai input sebagai diterima
        accepted_config.extend(config)
        return 1

    # Hasilkan semua kemungkinan pergerakan dari konfigurasi saat ini
    moves = get_moves(state, input, stack)
    if not moves:
        return 0  # Tidak ada pergerakan lebih lanjut; hentikan jalur ini

    # Eksplorasi semua pergerakan secara rekursif
    for move in moves:
        next_state, next_input, next_stack = move
        generate(next_state, next_input, next_stack, config + [(next_state, next_input, next_stack)])

    return found


def get_moves(state, input, stack):
    """
    Mendapatkan semua transisi valid dari state saat ini.
    """
    global productions
    moves = []

    for current_state, rules in productions.items():
        if current_state != state:
            continue

        for rule in rules:
            read_input, pop_stack, push_stack, next_state = rule

            # Tangani simbol input
            if read_input and (not input or input[0] != read_input):
                continue
            new_input = input[1:] if read_input else input

            # Tangani simbol stack
            if pop_stack and (not stack or stack[0] != pop_stack):
                continue
            new_stack = push_stack + stack[1:] if pop_stack else push_stack + stack

            moves.append((next_state, new_input, new_stack))

    return moves


def is_found(state, input, stack):
    """
    Periksa apakah konfigurasi saat ini mengarah ke penerimaan.
    """
    global accept_with, acceptable_states

    if input:  # Input belum selesai diproses
        return False

    if accept_with == "E" and not stack:  # Diterima jika stack kosong
        return True

    if accept_with == "F" and state in acceptable_states:  # Diterima jika di state akhir
        return True

    return False


def print_config(config):
    """
    Cetak konfigurasi yang mengarah ke penerimaan.
    """
    for state, input, stack in config:
        print(f"State: {state}, Input: {input}, Stack: {stack}")


def parse_file(filename):
    """
    Membaca file definisi automata dan mengisi struktur data yang diperlukan.
    """
    global productions, start_symbol, stack_start, acceptable_states, accept_with

    try:
        with open(filename, "r") as file:
            lines = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return False

    start_symbol = lines[3]
    stack_start = lines[4]
    acceptable_states = lines[5].split()
    accept_with = lines[6]

    for line in lines[7:]:
        parts = line.split()
        state = parts[0]
        read_input, pop_stack, next_state, push_stack = parts[1], parts[2], parts[3], parts[4]
        rule = (read_input if read_input != "e" else "",
                pop_stack if pop_stack != "e" else "",
                push_stack if push_stack != "e" else "",
                next_state)
        productions.setdefault(state, []).append(rule)

    return True


def done():
    """
    Menampilkan hasil akhir evaluasi automata.
    """
    if found:
        print(f"Berhasil! Kata \"{start_input}\" adalah bagian dari grammar.")
    else:
        print(f"Gagal! Kata \"{start_input}\" bukan bagian dari grammar.")


# Program exec
filename = input("Masukkan nama file automata Anda:\n")
while not parse_file(filename):
    print("File tidak ditemukan!")
    filename = input("Masukkan nama file automata lagi:\n")

print("Automata berhasil dibuat.")

start_input = input("Masukkan kata yang ingin dicek:\n")
print(f"Memeriksa kata \"{start_input}\" ...")

if generate(start_symbol, start_input, stack_start, [(start_symbol, start_input, stack_start)]):
    print_config(accepted_config)  # Tampilkan konfigurasi yang mengarah ke penerimaan
done()