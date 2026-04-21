from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
import google.generativeai as genai
import sqlite3
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

from database import (guardar_pregunta, crear_bd, obtener_estadisticas,
                      login_alumno, obtener_alumnos, obtener_preguntas_alumno,
                      temas_dificiles_alumno, registrar_alumno)

# -------------------------------
# CONFIGURACIÓN
# -------------------------------
crear_bd()

app = Flask(__name__, static_folder='.')
app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto_cambiar')
CORS(app)

# Contraseña del administrador (viene del .env)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'docente2026')

# -------------------------------
# CONFIGURACIÓN GEMINI
# -------------------------------
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    print("⚠️  ADVERTENCIA: No se encontró GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# -------------------------------
# CARGAR MATERIAL POO
# -------------------------------
try:
    with open("material_poo.txt", "r", encoding="utf-8") as f:
        CONTENIDO_MATERIA = f.read()
except:
    CONTENIDO_MATERIA = "No se encontró el archivo material_poo.txt"

# -------------------------------
# MODELO PEDAGÓGICO
# -------------------------------
SYSTEM_PROMPT = f"""
Eres un Tutor Inteligente especializado en Programación Orientada a Objetos (POO).

BASE DE CONOCIMIENTO:
{CONTENIDO_MATERIA}

ROL PEDAGÓGICO (MÉTODO SOCRÁTICO):
Tu objetivo principal NO es dar respuestas directas, sino guiar al estudiante para que él mismo construya el conocimiento. Eres un facilitador del aprendizaje.

REGLAS ESTRICTAS:
1. DOMINIO EXCLUSIVO: SOLO responde preguntas relacionadas con Programación Orientada a Objetos. Si la pregunta no es sobre la materia, responde cortésmente: "Este tutor está enfocado exclusivamente en apoyarte con la materia de Programación Orientada a Objetos."
2. PROHIBIDO DAR LA RESPUESTA FINAL: Si el alumno te hace una pregunta conceptual (ej. "¿Qué es el polimorfismo?"), no le des la definición de Wikipedia. Dale una analogía sencilla y hazle una pregunta de vuelta para ver qué entiende él.
3. MANEJO DE CÓDIGO (MUY IMPORTANTE): Si el estudiante te pide que le escribas código o le resuelvas un ejercicio:
   - NUNCA le des el código completo de la solución.
   - Explícale la lógica o el algoritmo que debe seguir.
   - Proporciona un ejemplo en Java de un problema SIMILAR, pero no el que te está preguntando.
   - Pídele que intente escribir una parte del código y te la muestre para revisarla.
4. TONO: Debes ser empático, paciente, motivador y profesional.
"""

# -------------------------------
# DETECTAR TEMA
# -------------------------------
def detectar_tema(pregunta):
    p = pregunta.lower()
    if "clase" in p or "class" in p:
        return "Clases"
    elif "objeto" in p or "instancia" in p or "new " in p:
        return "Objetos"
    elif "metodo" in p or "método" in p or "void" in p or "return" in p or "funcion" in p:
        return "Métodos"
    elif "herencia" in p or "extends" in p or "super" in p:
        return "Herencia"
    elif "encapsul" in p or "private" in p or "public" in p or "getter" in p or "setter" in p:
        return "Encapsulamiento"
    elif "polimorf" in p or "override" in p or "sobrescri" in p:
        return "Polimorfismo"
    elif "atributo" in p or "variable" in p or "campo" in p:
        return "Atributos"
    elif "constructor" in p:
        return "Constructores"
    elif "abstrac" in p or "interfaz" in p or "interface" in p:
        return "Abstracción"
    else:
        return "POO General"


# ================================
# RUTAS DE AUTENTICACIÓN
# ================================

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    numero_control = data.get('numero_control')
    contrasena = data.get('contrasena')

    alumno = login_alumno(numero_control, contrasena)

    if alumno:
        session['alumno'] = alumno
        return jsonify({"ok": True, "nombre": alumno['nombre']})
    else:
        return jsonify({"ok": False, "error": "Número de control o contraseña incorrectos."})


@app.route('/registro', methods=['POST'])
def registro_publico():
    data = request.json
    numero_control = data.get('numero_control')
    nombre = data.get('nombre', '').strip()
    grupo = data.get('grupo', '').strip()
    contrasena = data.get('contrasena', '').strip()

    if not all([numero_control, nombre, grupo, contrasena]):
        return jsonify({"ok": False, "error": "Todos los campos son obligatorios."})

    if len(contrasena) < 4:
        return jsonify({"ok": False, "error": "La contraseña debe tener al menos 4 caracteres."})

    ok = registrar_alumno(numero_control, nombre, grupo, contrasena)

    if ok:
        # Iniciar sesión automáticamente después del registro
        alumno = login_alumno(numero_control, contrasena)
        if alumno:
            session['alumno'] = alumno
        return jsonify({"ok": True})
    else:
        return jsonify({"ok": False, "error": "Ese número de control ya está registrado."})


@app.route('/login-admin', methods=['POST'])
def login_admin():
    data = request.json
    contrasena = data.get('contrasena')

    if contrasena == ADMIN_PASSWORD:
        session['admin'] = True
        return jsonify({"ok": True})
    else:
        return jsonify({"ok": False, "error": "Contraseña incorrecta."})


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login.html')


@app.route('/sesion-actual')
def sesion_actual():
    if 'alumno' in session:
        return jsonify({"tipo": "alumno", "datos": session['alumno']})
    elif 'admin' in session:
        return jsonify({"tipo": "admin"})
    else:
        return jsonify({"tipo": None})


# ================================
# RUTAS PRINCIPALES
# ================================

@app.route('/')
def index():
    # Si no hay sesión, redirige al login
    if 'alumno' not in session:
        return redirect('/login.html')
    return send_from_directory('.', 'index.html')


@app.route('/login.html')
def login_page():
    return send_from_directory('.', 'login.html')


@app.route('/admin')
def admin_page():
    if 'admin' not in session:
        return redirect('/login.html')
    return send_from_directory('.', 'admin.html')


# ================================
# CHAT DEL TUTOR
# ================================

@app.route('/chat', methods=['POST'])
def chat():
    # Verificar sesión
    if 'alumno' not in session:
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    mensaje_usuario = data.get('mensaje', '')
    alumno_id = session['alumno']['numero_control']

    prompt_final = f"""
INSTRUCCIÓN PARA EL TUTOR:
{SYSTEM_PROMPT}

PREGUNTA DEL ALUMNO:
{mensaje_usuario}
"""

    try:
        response = model.generate_content(prompt_final)
        respuesta_modelo = response.text
        tema = detectar_tema(mensaje_usuario)
        guardar_pregunta(mensaje_usuario, tema, alumno_id)
        return jsonify({"respuesta": respuesta_modelo})
    except Exception as e:
        return jsonify({"respuesta": f"Error de conexión: {str(e)}"})



# ================================
# HISTORIAL DEL ALUMNO
# ================================

@app.route('/historial.html')
def historial_page():
    if 'alumno' not in session:
        return redirect('/login.html')
    return send_from_directory('.', 'historial.html')


@app.route('/api/mi-historial')
def mi_historial():
    if 'alumno' not in session:
        return jsonify({"error": "No autorizado"}), 401

    nc = session['alumno']['numero_control']
    preguntas = obtener_preguntas_alumno(nc)
    temas     = temas_dificiles_alumno(nc)

    return jsonify({
        "alumno": session['alumno'],
        "preguntas": preguntas,
        "temas": temas
    })


# ================================
# RUTAS DEL ADMINISTRADOR
# ================================

@app.route('/api/alumnos')
def api_alumnos():
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401
    return jsonify(obtener_alumnos())


@app.route('/api/alumno/<int:numero_control>')
def api_alumno_detalle(numero_control):
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401

    preguntas = obtener_preguntas_alumno(numero_control)
    temas = temas_dificiles_alumno(numero_control)

    return jsonify({
        "preguntas": preguntas,
        "temas_dificiles": temas
    })


@app.route('/api/registrar-alumno', methods=['POST'])
def api_registrar_alumno():
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    ok = registrar_alumno(
        data.get('numero_control'),
        data.get('nombre'),
        data.get('grupo'),
        data.get('contrasena')
    )

    if ok:
        return jsonify({"ok": True})
    else:
        return jsonify({"ok": False, "error": "El número de control ya existe."})


@app.route('/api/estadisticas')
def api_estadisticas():
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401

    datos = obtener_estadisticas()
    return jsonify([{"tema": t, "cantidad": c} for t, c in datos])


# Compatibilidad con dashboard.html anterior
@app.route('/estadisticas')
def estadisticas_legacy():
    datos = obtener_estadisticas()
    return jsonify([{"tema": t, "cantidad": c} for t, c in datos])


@app.route('/preguntas')
def preguntas_legacy():
    conexion = sqlite3.connect("tutor.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT i.id, i.pregunta, i.tema, i.fecha, i.alumno_id, a.nombre
        FROM interacciones i
        LEFT JOIN alumnos a ON i.alumno_id = a.numero_control
        ORDER BY i.id DESC
    """)
    datos = cursor.fetchall()
    lista = [{"id": r[0], "pregunta": r[1], "tema": r[2], "fecha": r[3],
              "alumno_id": r[4], "nombre": r[5] or "—"} for r in datos]
    conexion.close()
    return jsonify(lista)


# -------------------------------
# INICIAR SERVIDOR
# -------------------------------
if __name__ == '__main__':
    print("------------------------------------------------")
    print("🎓 SERVIDOR TUTOR POO ENCENDIDO 🎓")
    print("👉 Login:   http://localhost:5000/login.html")
    print("👉 Tutor:   http://localhost:5000")
    print("👉 Admin:   http://localhost:5000/admin")
    print(f"🔑 Clave admin: {ADMIN_PASSWORD}")
    print("------------------------------------------------")
    app.run(port=5000, debug=False)