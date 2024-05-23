import threading
import csv
from Crypto.Hash import SHA3_512

# Función para calcular el hash según el esquema descrito
def calculate_hash(password, pepper, salt):
    H = SHA3_512.new()
    password_b = bytes(password, "utf-8")
    H.update(password_b)
    
    pepper_b = pepper.to_bytes(1, "big")
    H.update(pepper_b)
    
    salt_b = bytes.fromhex(salt)
    H.update(salt_b)
    
    return H.hexdigest()

# Función para verificar contraseñas posibles
def check_password(possible_passwords, salt, target_pwd, result, stop_event, thread_id):
    print(f"Iniciando hilo {thread_id}...")
    for password in possible_passwords:
        if stop_event.is_set():
            print(f"Hilo {thread_id} deteniéndose debido a que se encontró la contraseña en otro hilo.")
            return
        for pepper in range(256):
            pwd_h = calculate_hash(password, pepper, salt)
            if pwd_h == target_pwd:
                result['password'] = password
                print(f"Contraseña encontrada por el hilo {thread_id}: {password}")
                stop_event.set()  # Indica a todos los hilos que se ha encontrado la contraseña
                return
    print(f"Hilo {thread_id} completado.")

# Carga de contraseñas desde el archivo rockyou.txt
def load_passwords(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        return [line.strip() for line in file]

# Carga de datos de la base de datos desde un archivo CSV
def load_database(file_path):
    database = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                username, salt, pwd = row
                database.append((username, salt, pwd))
    return database

# Función principal
def main():
    print("Iniciando búsqueda de contraseñas...")
    possible_passwords = load_passwords('Laboratorios-Estructura-de-Datos-2/Laboratorio 3/rockyou.txt')
    database = load_database('Laboratorios-Estructura-de-Datos-2/Laboratorio 3/password_database_ED2.csv')  

    username = "rodeloi"  
    target_salt, target_pwd = None, None

    for user, salt, pwd in database:
        if user == username:
            target_salt, target_pwd = salt, pwd
            print(f"Usuario {username} encontrado, su pwd: {target_pwd} y su salt es {target_salt} ")
            break

    # target_salt, target_pwd= "f6cdd77c86adde155a0cd15a0be87054", "2914d209dde8c5985708cfcc46c0af818a17bdacc127840bb8d27f1aa884e9c8e0100043ecf704e84ce11c6377f2b8f1637704444d862f338122e9e8fdc4eca9"
    
    if target_salt is None or target_pwd is None:
        print(f"Usuario {username} no encontrado en la base de datos")
        return

    num_threads = 16
    passwords_per_thread = len(possible_passwords) // num_threads
    threads = []
    result = {}
    stop_event = threading.Event()

    for i in range(num_threads):
        start = i * passwords_per_thread
        end = (i + 1) * passwords_per_thread if i != num_threads - 1 else len(possible_passwords)
        thread = threading.Thread(target=check_password, args=(possible_passwords[start:end], target_salt, target_pwd, result, stop_event, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if 'password' in result:
        print(f"Contraseña encontrada: {result['password']}")
    else:
        print("Contraseña no encontrada")

# Ejecución del programa principal
if __name__== "__main__":
    main()
