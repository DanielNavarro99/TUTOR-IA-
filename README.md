TUTOR-IA — Modelo Pedagógico Personalizado con LLMs
Tecnológico Superior de Jalisco, Campus Chapala — Ingeniería en Sistemas Computacionales

Un sistema de tutoría inteligente diseñado para la materia de Programación Orientada a Objetos (POO). Este sistema utiliza Grandes Modelos de Lenguaje (LLMs) para ofrecer un andamiaje pedagógico personalizado, guiando al alumno en lugar de proveer respuestas directas.

Arquitectura del Sistema
El proyecto sigue una sólida arquitectura cliente-servidor de tres capas:

Capa de Presentación (Frontend): Interfaces HTML/CSS/JS accesibles desde el navegador. Incluye el chat interactivo, el panel de administración docente y el sistema de autenticación.

Capa de Lógica de Negocio (Backend): Servidor Flask en Python que gestiona la API REST, valida sesiones, construye los prompts pedagógicos y orquesta la comunicación con la IA.

Capa de Datos: Base de datos local que registra alumnos y el historial de interacciones para minería de datos.

Stack Tecnológico
Backend & IA
Lenguaje: Python 3.x

Framework Web: Flask 3.0.3 y Flask-CORS 4.0.1

Base de Datos: SQLite 3.x

Inteligencia Artificial: Google Gemini API (Modelo 2.5 Flash) vía google-generativeai 0.8.3

Entorno de Producción: Gunicorn 22.0.0 y gestión de variables seguras con python-dotenv 1.0.1.

Frontend
Estructura y Estilos: HTML5, CSS3, JavaScript (ES6+)

Visualización de Datos: Chart.js 4.4.1

Procesamiento de Texto: Marked.js (Renderizado de Markdown) e Highlight.js 11.9.0 (Resaltado de sintaxis)

Tipografías: Plus Jakarta Sans y JetBrains Mono (Google Fonts)

Infraestructura y Despliegue
Servidor: VPS alojado en Neubox (México)

Sistema Operativo: Ubuntu 24 LTS

Control de Versiones: Git y GitHub

👨‍💻 Autores y Asesoría
Desarrolladores: Daniel Santos Navarro Mendoza, Fernando Raya Rodríguez

Asesora: Ing. Carmen Leticia Salcedo Quebedo

Año: 2026
