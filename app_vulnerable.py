import sqlite3
import sys

DB_NAME = 'tienda.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def login_vulnerable():
    print("\n--- 🔓 LOGIN VULNERABLE ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # ❌ VULNERABILIDAD AQUÍ: Concatenación directa de strings
    # Esto permite que lo que escriba el usuario modifique la lógica SQL
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    
    print(f"\n[DEBUG SQL] Ejecutando: {query}") # Para que veas qué está pasando
    
    try:
        cursor.execute(query) # Ejecuta la consulta concatenada
        user = cursor.fetchone()
        
        if user:
            print(f"✅ ¡Bienvenido de nuevo, {user[1]}!")
            print(f"   (Tus datos: {user})")
            return True
        else:
            print("❌ Credenciales incorrectas.")
            return False
    except sqlite3.Error as e:
        print(f"⚠️ Error SQL: {e}")
        return False
    finally:
        conn.close()

def buscar_producto_vulnerable():
    print("\n--- 🔍 BÚSQUEDA VULNERABLE ---")
    filtro = input("Buscar producto por nombre: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # ❌ VULNERABILIDAD AQUÍ: Otra inyección posible (útil para UNION attacks)
    query = f"SELECT * FROM productos WHERE nombre LIKE '%{filtro}%'"
    
    print(f"\n[DEBUG SQL] Ejecutando: {query}")
    
    try:
        cursor.execute(query)
        productos = cursor.fetchall()
        
        if productos:
            print(f"\n📦 Se encontraron {len(productos)} productos:")
            for p in productos:
                print(f" - {p[1]}: {p[2]} ({p[3]}€)")
        else:
            print("❌ No se encontraron productos.")
    except sqlite3.Error as e:
        print(f"⚠️ Error SQL: {e}")
    finally:
        conn.close()

def menu():
    while True:
        print("\n=== 🛒 TIENDA VULNERABLE (Práctica SQLi) ===")
        print("1. Iniciar Sesión (Login)")
        print("2. Buscar Productos")
        print("3. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == '1':
            login_vulnerable()
        elif opcion == '2':
            buscar_producto_vulnerable()
        elif opcion == '3':
            print("👋 ¡Hasta luego!")
            sys.exit()
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    menu()