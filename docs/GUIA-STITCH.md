# Guía de Stitch: de las pantallas al código

Las vistas que trae el proyecto (`views/`) ya funcionan: son una base hecha a mano. Esta guía explica cómo
reemplazarlas por tus diseños de Stitch (guía 22) sin romper la conexión con la API.

## 1. Diseñar en Stitch (tú, con tu cuenta de Google)
1. Abre https://stitch.withgoogle.com, elige **Web** y pega los prompts de `docs/prompts-stitch.md`.
2. Pon al proyecto el nombre del repositorio.

## 2. Conectar Stitch a OpenCode
1. En Stitch: foto de perfil → **Stitch settings** → **API key** → **Create key**. Cópiala.
2. Guárdala como variable de entorno. Nunca en un archivo del repo, ni en el chat, ni en una captura:
   ```powershell
   # Windows PowerShell: permanente (luego abre una terminal NUEVA)
   setx STITCH_API_KEY "pega-aqui-tu-clave"
   # Comprobar sin mostrarla; debe responder True
   [bool]$env:STITCH_API_KEY
   ```
3. En la carpeta del proyecto, en la terminal nueva: `opencode mcp list` (debe salir `stitch connected`).
   Esto solo prueba que cargó la configuración (`opencode.json` ya viene en el repo y no contiene la clave).
4. Abre `opencode` y escribe: `Usa el MCP de Stitch y lista mis proyectos.` Esa es la prueba real de la clave.

> OpenCode no lee archivos `.env`: la clave tiene que ser una variable del sistema o de la sesión.

## 3. Importar las pantallas (modo plan primero, luego build)
En OpenCode pulsa Tab para el modo plan y pega:
```
Usa el MCP de Stitch para listar las pantallas del proyecto "NOMBRE-DE-TU-PROYECTO".
Propón qué archivo de views/ corresponde a cada una. No escribas nada todavía.
```
Luego Tab para volver a build y pega:
```
Usa el MCP de Stitch:
1. Para cada pantalla del proyecto, usa get_screen y descarga su HTML (no inventes el HTML).
2. Guárdalas como views/escribir.html, views/evaluacion.html y views/mejorado.html.
3. En cada una conserva el contrato de docs/GUIA-STITCH.md: los ids de la sección 4, el atributo
   data-page en <body>, la etiqueta <script src="/static/app.js"></script> y un pequeño bloque <style>
   para las clases dinámicas (ok, fail, high, mid, low).
4. Abre docs/DESIGN.md (ya existe: es la dirección visual) y completa su sección 9 con la paleta (códigos hex),
   tipografías y componentes que Stitch realmente generó. No borres el resto del archivo.
Reglas: no cambies static/app.js, app/, AGENTS.md ni opencode.json; no instales dependencias; no hagas commits.
Al final, muéstrame la lista de archivos creados.
```
Aprueba cada llamada a herramientas. Para probar, corre `uvicorn app.main:app --reload` y abre
http://127.0.0.1:8000 (no abras los HTML con doble clic: necesitan la API en el mismo servidor).

## 4. Contrato de ids (lo que `static/app.js` necesita)
| Vista | `<body data-page=...>` | Ids obligatorios |
|---|---|---|
| `escribir.html` | `escribir` | `prompt-input` (textarea), `counter`, `btn-evaluar`, `status`, `mode-badge` |
| `evaluacion.html` | `evaluacion` | `verdict`, `score`, `checks` (ul), `suggestions` (ul), `prompt-echo`, `btn-mejorar`, `status`, `mode-badge` |
| `mejorado.html` | `mejorado` | `mode`, `original`, `improved`, `score-before`, `score-after`, `score-delta`, `changes` (ul), `btn-copiar`, `btn-nuevo`, `status`, `mode-badge` |

Clases que escribe el JavaScript y que tu CSS debe estilizar: `score high|mid|low` (círculo de puntaje),
`ok` y `fail` (filas de chequeo), `error` (en `status`).

## 5. Plan B si el MCP no conecta
En Stitch exporta o copia el código de cada pantalla, pégalo en `views/` y pídele al agente solo los pasos
3 y 4. Anótalo en el README: la guía 22 lo acepta con puntaje parcial.

## 6. Probar OpenAI sin gastar saldo
```powershell
# Terminal 1
python tools/mock_openai.py
# Terminal 2
$env:OPENAI_BASE_URL = "http://127.0.0.1:8765/v1"
$env:OPENAI_API_KEY  = "clave-falsa"
$env:OPENAI_MODEL    = "modelo-demo-1"
uvicorn app.main:app --reload
```
Al terminar: `Remove-Item Env:OPENAI_BASE_URL` para volver a la API real.

## 7. Con la API real de OpenAI
1. Crea una clave solo para esta actividad en https://platform.openai.com/api-keys y pon un límite de gasto en Billing.
2. Elige el modelo en la página de modelos de OpenAI (cambian cada pocos meses).
3. Copia `.env.example` como `.env` y completa `OPENAI_API_KEY` y `OPENAI_MODEL`. `.env` está en `.gitignore`.
4. Reinicia uvicorn. La insignia de la esquina debe decir "IA activa".
