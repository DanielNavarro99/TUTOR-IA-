# Tutor-IA 🤖🎓
**Tecnológico Superior de Jalisco, Campus Chapala — Ingeniería en Sistemas Computacionales**

Un sistema de tutoría inteligente diseñado para la materia de Programación Orientada a Objetos (POO). Utiliza Grandes Modelos de Lenguaje (LLMs) para ofrecer un andamiaje pedagógico personalizado, guiando al alumno en la Zona de Desarrollo Próximo (ZDP) en lugar de darle respuestas directas.

## Estructura del proyecto

```text
tutor-ia/
  app.py                      ← Backend Flask (API, Prompts, Lógica)
  requirements.txt            ← Dependencias de Python
  .env                        ← Variables seguras (API Keys - IGNORADO EN GIT)
  database/
    tutor.db                  ← Base de datos SQLite (alumnos e historial)
  static/
    css/
      style.css               ← Interfaz de usuario
    js/
      chat.js                 ← Lógica del cliente, Markdown e Highlight.js
      dashboard.js            ← Minería de datos y gráficas con Chart.js
  templates/
    index.html                ← Interfaz principal del chat
    admin.html                ← Panel de administración docente
```

## Stack Tecnológico 🛠️

**Backend & IA**
- Python 3.x con **Flask 3.0.3** y Flask-CORS
- Base de datos: **SQLite 3.x**
- IA: **Google Gemini API** (2.5 Flash) mediante `google-generativeai`
- Producción: **Gunicorn 22.0.0**

**Frontend**
- HTML5, CSS3, JS (ES6+)
- Visualización: **Chart.js 4.4.1**
- Procesamiento: **Marked.js** (Markdown) y **Highlight.js** (Sintaxis)
- Tipografías: *Plus Jakarta Sans* y *JetBrains Mono*

## Instalación desde cero

### 1. Requisitos
- Python 3.x instalado en el sistema
- Una clave de API de Google Gemini Studio

### 2. Setup del Entorno
Clona el repositorio y configura el entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate
# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Variables de Entorno (`.env`)
Crea un archivo llamado `.env` en la raíz del proyecto (este archivo está protegido por el `.gitignore` para no filtrarse en GitHub). Formato:

```env
GEMINI_API_KEY="tu_clave_de_api_aqui"
FLASK_ENV="development"
```

### 4. Ejecutar localmente
```bash
python app.py
# El servidor iniciará en http://localhost:5000
```

## Infraestructura en Producción 🚀
El despliegue está configurado para un **VPS en Neubox (México)** corriendo sobre **Ubuntu 24 LTS**, utilizando Gunicorn para levantar la aplicación Flask de forma estable.

## Funcionalidades

- ✅ Andamiaje pedagógico (No da el código, te enseña a pensarlo)
- ✅ Integración nativa con Gemini 2.5 Flash
- ✅ Interfaz de chat accesible desde el navegador
- ✅ Renderizado en tiempo real de Markdown y bloques de código
- ✅ Base de datos local para rastrear el progreso de los alumnos
- ✅ Panel de administración para docentes con métricas visuales (Chart.js)
- ✅ Arquitectura segura separando credenciales con `python-dotenv`

## 👨‍💻 Autores y Asesoría

- **Desarrollador:** Daniel Santos Navarro Mendoza
- **Asesora:** Ing. Carmen Leticia Salcedo Quebedo
- **Año:** 2026