# [cite_start] TUTOR-IA — Modelo Pedagógico Personalizado con LLMs [cite: 3, 4]

[cite_start]**Tecnológico Superior de Jalisco, Campus Chapala — Ingeniería en Sistemas Computacionales** [cite: 1, 2]

[cite_start]Un sistema de tutoría inteligente diseñado para la materia de Programación Orientada a Objetos (POO)[cite: 10]. [cite_start]Este sistema utiliza Grandes Modelos de Lenguaje (LLMs) para ofrecer un andamiaje pedagógico personalizado, guiando al alumno en lugar de proveer respuestas directas[cite: 10].

## [cite_start] Arquitectura del Sistema [cite: 30]
[cite_start]El proyecto sigue una sólida arquitectura cliente-servidor de tres capas:

* **Capa de Presentación (Frontend):** Interfaces HTML/CSS/JS accesibles desde el navegador. [cite_start]Incluye el chat interactivo, el panel de administración docente y el sistema de autenticación[cite: 32, 33].
* [cite_start]**Capa de Lógica de Negocio (Backend):** Servidor Flask en Python que gestiona la API REST, valida sesiones, construye los prompts pedagógicos y orquesta la comunicación con la IA[cite: 34].
* [cite_start]**Capa de Datos:** Base de datos local que registra alumnos y el historial de interacciones para minería de datos[cite: 35].

## [cite_start] Stack Tecnológico [cite: 9]

### [cite_start]Backend & IA [cite: 15, 18]
* [cite_start]**Lenguaje:** Python 3.x [cite: 17]
* [cite_start]**Framework Web:** Flask 3.0.3 y Flask-CORS 4.0.1 [cite: 17]
* [cite_start]**Base de Datos:** SQLite 3.x [cite: 17]
* [cite_start]**Inteligencia Artificial:** Google Gemini API (Modelo 2.5 Flash) vía `google-generativeai` 0.8.3 [cite: 20]
* [cite_start]**Entorno de Producción:** Gunicorn 22.0.0 [cite: 17] [cite_start]y gestión de variables seguras con `python-dotenv` 1.0.1[cite: 17].

### [cite_start]Frontend [cite: 21]
* [cite_start]**Estructura y Estilos:** HTML5, CSS3, JavaScript (ES6+) [cite: 23]
* [cite_start]**Visualización de Datos:** Chart.js 4.4.1 [cite: 23]
* [cite_start]**Procesamiento de Texto:** Marked.js (Renderizado de Markdown) e Highlight.js 11.9.0 (Resaltado de sintaxis) [cite: 23]
* [cite_start]**Tipografías:** Plus Jakarta Sans y JetBrains Mono (Google Fonts) [cite: 23]

### [cite_start]Infraestructura y Despliegue [cite: 24]
* [cite_start]**Servidor:** VPS alojado en Neubox (México) [cite: 26]
* [cite_start]**Sistema Operativo:** Ubuntu 24 LTS [cite: 26]
* [cite_start]**Control de Versiones:** Git y GitHub [cite: 26]

## 👨‍💻 Autores y Asesoría
* [cite_start]**Desarrolladores:** Daniel Santos Navarro Mendoza, Fernando Raya Rodríguez [cite: 6]
* **Asesora:** Ing. [cite_start]Carmen Leticia Salcedo Quebedo 
* [cite_start]**Año:** 2026 [cite: 8]