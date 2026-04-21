import sqlite3
from datetime import datetime

DB_NAME = "tutor.db"

# -------------------------------
# CREAR BASE DE DATOS
# -------------------------------
def crear_bd():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Tabla de interacciones (con alumno_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interacciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pregunta TEXT,
        tema TEXT,
        fecha TEXT,
        alumno_id INTEGER
    )
    """)

    # Tabla de alumnos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        numero_control INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        grupo TEXT NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()


# -------------------------------
# GUARDAR PREGUNTA
# -------------------------------
def guardar_pregunta(pregunta, tema, alumno_id=None):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO interacciones (pregunta, tema, fecha, alumno_id)
        VALUES (?, ?, ?, ?)
    """, (pregunta, tema, fecha, alumno_id))

    conexion.commit()
    conexion.close()


# -------------------------------
# OBTENER ESTADÍSTICAS GLOBALES
# -------------------------------
def obtener_estadisticas():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT tema, COUNT(*)
        FROM interacciones
        GROUP BY tema
    """)

    datos = cursor.fetchall()
    conexion.close()
    return datos


# -------------------------------
# LOGIN ALUMNO
# -------------------------------
def login_alumno(numero_control, contrasena):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT numero_control, nombre, grupo
        FROM alumnos
        WHERE numero_control = ? AND contrasena = ?
    """, (numero_control, contrasena))

    alumno = cursor.fetchone()
    conexion.close()

    if alumno:
        return {"numero_control": alumno[0], "nombre": alumno[1], "grupo": alumno[2]}
    return None


# -------------------------------
# OBTENER TODOS LOS ALUMNOS
# -------------------------------
def obtener_alumnos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT a.numero_control, a.nombre, a.grupo,
               COUNT(i.id) as total_preguntas
        FROM alumnos a
        LEFT JOIN interacciones i ON a.numero_control = i.alumno_id
        GROUP BY a.numero_control
        ORDER BY a.nombre
    """)

    datos = cursor.fetchall()
    conexion.close()

    return [{"numero_control": r[0], "nombre": r[1], "grupo": r[2], "total_preguntas": r[3]} for r in datos]


# -------------------------------
# OBTENER PREGUNTAS DE UN ALUMNO
# -------------------------------
def obtener_preguntas_alumno(numero_control):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT pregunta, tema, fecha
        FROM interacciones
        WHERE alumno_id = ?
        ORDER BY id DESC
    """, (numero_control,))

    datos = cursor.fetchall()
    conexion.close()

    return [{"pregunta": r[0], "tema": r[1], "fecha": r[2]} for r in datos]


# -------------------------------
# TEMAS DIFÍCILES DE UN ALUMNO
# -------------------------------
def temas_dificiles_alumno(numero_control):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT tema, COUNT(*) as veces
        FROM interacciones
        WHERE alumno_id = ?
        GROUP BY tema
        ORDER BY veces DESC
    """, (numero_control,))

    datos = cursor.fetchall()
    conexion.close()

    return [{"tema": r[0], "veces": r[1]} for r in datos]


# -------------------------------
# REGISTRAR ALUMNO NUEVO
# -------------------------------
def registrar_alumno(numero_control, nombre, grupo, contrasena):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO alumnos (numero_control, nombre, grupo, contrasena)
            VALUES (?, ?, ?, ?)
        """, (numero_control, nombre, grupo, contrasena))

        conexion.commit()
        conexion.close()
        return True
    except sqlite3.IntegrityError:
        return False  # numero_control ya existe
