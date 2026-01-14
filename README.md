# Inyección-SQL: Paso a paso
Para esta práctica se ha desarrollado un prototipo de Tienda Online utilizando Python junto con una base de datos SQLite. El objetivo es demostrar de forma práctica y comprensible qué es una Inyección SQL (SQLi) y por qué supone un problema grave de seguridad.
# 🛡️ Práctica Final: Inyección SQL (SQLi)

## 🎯 Tienda Online: Aplicación Vulnerable vs. Aplicación Segura

**Asignatura:** Ciberseguridad
**Equipo:** Anthony - Luis- Jonathan - Miguel - Rossel
**Profesor:** Jordi Lopez Amat

---

## 1. 🏗️ Escenario de la Práctica

Para esta práctica se ha desarrollado un **prototipo de Tienda Online** utilizando **Python** junto con una base de datos **SQLite**.
El objetivo es **demostrar de forma práctica y comprensible qué es una Inyección SQL (SQLi)** y por qué supone un problema grave de seguridad.

Se han creado **dos versiones de la aplicación**:

* 🔴 **`app_vulnerable.py`** → Contiene errores comunes de programación insegura.
* 🟢 **`app_segura.py`** → Implementa buenas prácticas de seguridad recomendadas por OWASP.

Ambas aplicaciones realizan las mismas funciones (login y búsqueda de productos), pero **la forma de acceder a la base de datos es diferente**.

---

## 2. ❌ El Problema: Concatenación Directa de SQL

En la versión vulnerable, la consulta SQL se construye **concatenando directamente el texto introducido por el usuario** dentro de la sentencia SQL.

### ☠️ Código Vulnerable (Python)

```python
query = f"SELECT * FROM usuarios WHERE username = '{usuario}'"
```

### 🗣️ Explicación sencilla

* El programa **mezcla el código SQL con el texto del usuario**.
* La base de datos **no sabe distinguir** qué parte es código y qué parte es un dato.
* Si el usuario introduce código SQL en lugar de texto normal, **ese código se ejecuta**.

Esto abre la puerta a ataques de **Inyección SQL**.

---

## 3. ⚔️ DEMOSTRACIÓN RED TEAM (Ataques)

A continuación se muestran ataques reales realizados contra `app_vulnerable.py`.

---

### 🅰️ Ataque 1: Bypass de Autenticación

**Objetivo:** Entrar en la aplicación como administrador **sin conocer la contraseña**.

**Pasos:**

1. Ejecutar la aplicación:

   ```bash
   python app_vulnerable.py
   ```
2. Elegir **Opción 1 (Login)**.
3. Introducir los siguientes datos:

**Usuario:**

```sql
admin' OR '1'='1
```

**Contraseña:**

```text
123 (o cualquier valor)
```

### ❓ ¿Por qué funciona?

La consulta que llega a la base de datos es:

```sql
SELECT * FROM usuarios WHERE username = 'admin' OR '1'='1'
```

* `'1'='1'` siempre es **verdadero**.
* La condición completa se cumple.
* La base de datos devuelve resultados y **permite el acceso sin validar la contraseña**.

🗣️ *Se ha roto completamente el sistema de autenticación.*

---

### 🅱️ Ataque 2: Robo de Datos con UNION

**Objetivo:** Obtener los usuarios, contraseñas y correos usando el buscador de productos.

**Pasos:**

1. En el menú, elegir **Opción 2 (Buscar productos)**.
2. Introducir en el buscador:

```sql
%' UNION SELECT id, username, password, email FROM usuarios --
```

### ❓ ¿Qué ocurre?

* El atacante usa `UNION` para **unir otra consulta SQL**.
* La aplicación cree que muestra productos.
* En realidad está mostrando **datos de la tabla de usuarios**.

🗣️ **Impacto:**

> Se ha producido una brecha de seguridad crítica. Toda la base de datos ha sido expuesta.

---

## 4. 🛡️ La Solución: Consultas Parametrizadas

En `app_segura.py` se utiliza **parametrización**, separando claramente:

* 📌 El **código SQL**
* 📌 Los **datos del usuario**

---

### ✅ Código Seguro (Python)

```python
query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
cursor.execute(query, (usuario, password))
```

### 🗣️ Explicación sencilla

* El símbolo `?` indica a la base de datos que ahí va un **dato**, no código.
* El motor SQL **nunca ejecuta el contenido del usuario**.
* Todo input se trata como texto literal.

Esto **elimina por completo la Inyección SQL**.

---

## 5. 🧪 DEMOSTRACIÓN BLUE TEAM (Defensa)

Se prueban los **mismos ataques anteriores** contra `app_segura.py`.

### Prueba de ataque

**Usuario:**

```sql
admin' OR '1'='1
```

### Resultado

* La aplicación busca literalmente un usuario con ese nombre.
* No existe.
* Devuelve:

```text
❌ Credenciales incorrectas
```

🗣️ *El ataque ha sido neutralizado. El código malicioso ahora es solo texto inofensivo.*

---

## 6. 📝 Conclusiones Finales

* 🚫 **Nunca confiar en el input del usuario**: todo dato externo es potencialmente peligroso.
* ⚙️ **Usar siempre consultas parametrizadas**: es la defensa más eficaz contra SQLi.
* 🔒 **Seguridad desde el diseño**: programar seguro desde el principio ahorra errores graves.

---

**Gracias por su atención.** 👨‍💻👩‍💻
