import threading
from Crypto.Hash import SHA3_512

# Información del usuario
username, salt, pwd = ("rodeloi", "58c2ec00d53958b5057614ea6bffd9bf", "32a95dc817b65d395687ab703a0ab60c7e61907dc02745f858b0b2044558666716ff7e27c2b8da21126863d144ff52f6b26cd0b9a0715f85d201ed9d9caf3eb1")

# Lee las posibles contraseñas desde el archivo
def read_possible_passwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

possible_passwords = read_possible_passwords('password_database_ED2.csv')

# Función para calcular el hash
def calculate_hash(password, pepper, salt):
    hasher = SHA3_512.new()
    hasher.update(password)
    hasher.update(pepper)
    hasher.update(salt)
    return hasher.hexdigest()

# Convertir el salt de hexadecimal a bytes
salt_b = bytes.fromhex(salt)

# Variable para detener todos los hilos cuando se encuentre la contraseña
found = threading.Event()

# Función de trabajo para cada hilo
def worker(passwords):
    for password in passwords:
        if found.is_set():
            return
        password_b = bytes(password, "utf-8")
        for pepper in range(256):
            pepper_b = pepper.to_bytes(1, "big")
            pwd_h = calculate_hash(password_b, pepper_b, salt_b)
            if found.is_set():
                return
            if pwd == pwd_h:
                print(f'Contraseña encontrada: {password}, Pepper: {pepper}')
                found.set()
                return

# Dividir las contraseñas entre los hilos
def split_workload(passwords, num_threads):
    avg = len(passwords) // num_threads
    return [passwords[i*avg : (i+1)*avg] for i in range(num_threads)]

# Número de hilos
num_threads = 10
password_chunks = split_workload(possible_passwords, num_threads)

# Crear y lanzar los hilos
threads = []
for chunk in password_chunks:
    thread = threading.Thread(target=worker, args=(chunk,))
    threads.append(thread)
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

if not found.is_set():
    print('Contraseña no encontrada.')
