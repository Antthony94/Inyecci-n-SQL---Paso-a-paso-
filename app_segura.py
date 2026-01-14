import sqlite3
import sys

DB_NAME = 'tienda.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def login_seguro():
    print("\n--- 🛡️ LOGIN SEGURO ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # ✅ SOLUCIÓN: Usamos ? como marcadores de posición
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    
    # Los datos van SEPARADOS en una tupla (username, password)
    # Así la base de datos sabe que son datos, no órdenes.
    print(f"\n[DEBUG SQL] Query: {query}")
    print(f"[DEBUG SQL] Datos: {(username, password)}")
    
    try:
        cursor.execute(query, (username, password)) 
        user = cursor.fetchone()
        
        if user:
            print(f"✅ ¡Bienvenido de nuevo, {user[1]}!")
            return True
        else:
            print("❌ Credenciales incorrectas.")
            return False
    except sqlite3.Error as e:
        print(f"⚠️ Error SQL: {e}")
        return False
    finally:
        conn.close()

def buscar_producto_seguro():
    print("\n--- 🛡️ BÚSQUEDA SEGURA ---")
    filtro = input("Buscar producto por nombre: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # ✅ SOLUCIÓN: Incluso para búsquedas parciales (LIKE), usamos parámetros.
    # Nota cómo añadimos los % en la variable python, no en la query SQL directa.
    query = "SELECT * FROM productos WHERE nombre LIKE ?"
    filtro_con_wildcards = f"%{filtro}%"
    
    print(f"\n[DEBUG SQL] Query: {query}")
    print(f"[DEBUG SQL] Datos: {(filtro_con_wildcards,)}")
    
    try:
        cursor.execute(query, (filtro_con_wildcards,))
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
        print("\n=== 🏰 TIENDA BLINDADA (Versión Segura) ===")
        print("1. Iniciar Sesión (Login Seguro)")
        print("2. Buscar Productos (Búsqueda Segura)")
        print("3. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == '1':
            login_seguro()
        elif opcion == '2':
            buscar_producto_seguro()
        elif opcion == '3':
            print("👋 ¡Hasta luego!")
            sys.exit()
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    menu()