import sqlite3
from faker import Faker
import random

# Configuración
DB_NAME = 'tienda.db'
fake = Faker('es_ES') # Datos en español

def crear_bd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Crear Tablas (Usuarios y Productos)
    # Tabla de Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        direccion TEXT
    )
    ''')
    
    # Tabla de Productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL
    )
    ''')

    # 2. Insertar un admin 
    try:
        cursor.execute("INSERT INTO usuarios (username, password, email, direccion) VALUES (?, ?, ?, ?)",
                       ('admin', '123456', 'admin@tienda.com', 'Calle Falsa 123'))
        print("✅ Usuario 'admin' creado (pass: 123456)")
    except sqlite3.IntegrityError:
        print("ℹ️ El usuario 'admin' ya existe.")

    # 3. Generar datos aleatorios con Faker
    print("🔄 Generando usuarios y productos aleatorios...")
    
    # Crear 10 usuarios extra
    for _ in range(10):
        user = fake.user_name()
        pwd = fake.password()
        email = fake.email()
        addr = fake.address()
        cursor.execute("INSERT INTO usuarios (username, password, email, direccion) VALUES (?, ?, ?, ?)",
                       (user, pwd, email, addr))
        
    # Crear 10 productos
    for _ in range(10):
        prod = fake.word().capitalize()
        desc = fake.sentence()
        price = round(random.uniform(10.0, 100.0), 2)
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)",
                       (prod, desc, price))

    conn.commit()
    conn.close()
    print(f"🚀 Base de datos '{DB_NAME}' lista.")

if __name__ == '__main__':
    crear_bd()