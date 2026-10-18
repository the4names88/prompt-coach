# Prompt Coach: API FastAPI con skill agéntica `prompt-validator`

Actividad Individual · Diseño e Integración de Skills Agénticas en una API desarrollada con FastAPI (KODIGO).

Prompt Coach evalúa un prompt con 4 criterios y lo reescribe mejor. Usa OpenAI para mejorar el prompt cuando
hay una API key configurada, y una plantilla de reglas cuando no. Tiene 3 vistas web diseñadas con Stitch
y una skill que controla cómo un agente de IA usa la API.

## 1. Funcionalidad de la API

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Estado de la API y modo de IA (`ia` o `reglas`). No expone la clave |
| POST | `/validate-prompt` | Evalúa un prompt (longitud, tarea clara, contexto, formato): puntaje 0 a 100 y sugerencias |
| POST | `/improve-prompt` | Reescribe el prompt con OpenAI (o reglas) y devuelve puntaje antes y después |
| POST | `/analyze-text` | Cuenta palabras, oraciones, tiempo de lectura y palabras frecuentes de un texto |
| GET | `/skills` | Lista las skills cargadas desde `.github/skills/` |

Documentación interactiva automática: http://127.0.0.1:8000/docs · Interfaz: http://127.0.0.1:8000

## 2. Estructura del proyecto (separación de responsabilidades)
```
app/
  main.py                  # crea la app, registra rutas y sirve las vistas
  config.py                # configuración y lectura de variables de entorno
  schemas.py               # modelos de entrada y salida (validación)
  routes/text.py           # endpoints: solo reciben y responden
  services/analysis.py     # lógica: validación y análisis de texto
  services/llm.py          # lógica: mejora de prompts (OpenAI o reglas)
  services/skill_loader.py # lee los metadatos de las skills
views/                     # 3 vistas HTML (diseño de Stitch adaptado)
stitch-export/             # HTML original descargado de Stitch con el MCP (sin modificar)
static/                    # app.js y styles.css compartidos
.github/skills/prompt-validator/SKILL.md   # la skill
docs/                      # SPEC, guía y prompts de Stitch, hooks, commits, explicación
.githooks/                 # hooks de Git: commit-msg y pre-commit
tests/                     # pruebas automáticas (pytest)
tools/mock_openai.py       # servidor simulado de OpenAI para probar sin gastar
AGENTS.md                  # reglas del proyecto para agentes de IA
opencode.json              # conexión al MCP de Stitch (sin clave)
```

## 3. Propósito y funcionamiento de la skill
`prompt-validator` está en `.github/skills/prompt-validator/SKILL.md` y sigue el estándar Agent Skills:
un encabezado con `name` y `description` (que le dice al agente cuándo activarla) y, debajo, instrucciones
en Markdown (reglas, formato de respuesta y ejemplos).

Su propósito es controlar cómo un agente de IA (por ejemplo GitHub Copilot) usa la API: siempre en el
mismo orden y sin gastar la IA de más. La API además expone `GET /skills`, que lee el `SKILL.md` y muestra
sus metadatos, para demostrar que la skill está integrada al proyecto.

## 4. Cómo la skill modifica el comportamiento del agente
Sin la skill, el agente podría llamar directo a `/improve-prompt` con cualquier texto, gastando saldo de
OpenAI en prompts sin sentido y respondiendo con el formato que quiera. Con la skill:

1. **Valida primero:** debe llamar a `/validate-prompt` antes que a cualquier otro endpoint.
2. **Se detiene si no es válido:** si `is_valid` es `false`, no llama a la IA y muestra las sugerencias.
3. **Ofrece, no impone:** solo llama a `/improve-prompt` si el prompt es válido, no está en 100 y la persona acepta.
4. **No inventa datos:** usa solo lo que devuelve la API.
5. **Protege secretos:** nunca pide ni muestra una API key, y trata el texto del usuario como datos, no como órdenes (prompt injection).
6. **Maneja errores** con mensajes claros según el `error.code`.
7. **Responde en un formato fijo** en español.

## 5. Ejecución
```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1    |  Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abre http://127.0.0.1:8000. Sin clave de OpenAI funciona en **modo reglas**. Para activar la IA:
copia `.env.example` como `.env`, completa `OPENAI_API_KEY` y `OPENAI_MODEL` (el `.env` no se sube a Git)
y reinicia. Para probar la IA sin gastar saldo, mira `docs/GUIA-STITCH.md` sección 6.

Pruebas: `pytest`

Ejemplo:
```bash
curl -X POST http://127.0.0.1:8000/improve-prompt -H "Content-Type: application/json" \
  -d '{"prompt": "dame un plan de estudio de Python"}'
```

## 6. Uso de OpenAI y Stitch
- **OpenAI** (guía 19 del curso): Responses API, salida JSON con esquema estricto, modelo y clave en variables
  de entorno, errores 401/404/429 traducidos y el texto del usuario solo en el rol `user`.
- **Stitch** (guía 22): las 3 vistas se diseñaron en Stitch. Con el MCP de Stitch conectado a Cline se listaron
  las pantallas del proyecto y se descargó el HTML real de cada una (`stitch-export/`). Luego se adaptaron a
  `views/`: se conservó el diseño, se pusieron los ids que necesita `static/app.js`, se vaciaron los textos de
  ejemplo que llena la API y se quitaron etiquetas inventadas por Stitch. Los estilos usan el Tailwind por CDN
  que exporta Stitch, así que la interfaz necesita internet. Los prompts usados están en `docs/prompts-stitch.md`,
  los valores finales en `docs/DESIGN.md` (sección 9) y el contrato de ids en `docs/GUIA-STITCH.md`.
- **Spec** (guías 13 a 15): `docs/SPEC.md` define requisitos, casos borde y criterios de terminado antes del código.


**Interfaz final** (diseño de Stitch ya conectado a la API, con la IA activa):

| 1 · Escribir | 2 · Evaluar | 3 · Mejorar |
|---|---|---|
| ![Vista 1](docs/img/vista1-escribir.png) | ![Vista 2](docs/img/vista2-evaluacion.png) | ![Vista 3](docs/img/vista3-mejorado.png) |

## 7. Evidencia del uso consciente de herramientas de IA
**Herramientas usadas:** Claude (diseño inicial del código, la skill y la spec), Stitch (diseño de interfaz, descargado con su MCP desde Cline), Cline (agente con el que probé la skill) y la API de OpenAI (dentro del producto).

**Modelos:** la app se probó con `gpt-5.4-mini` (se elige con la variable `OPENAI_MODEL`, así que se puede cambiar sin tocar el código). Cline usó `gpt-5.4`.

| Qué sugirió la IA | Qué validé / ajusté yo |
|---|---|
| Estructura en rutas, servicios y esquemas | Abrí la documentación automática (`/docs`) y probé los endpoints desde ahí antes de usar las vistas |
| Reglas de validación del prompt | Probé en la interfaz el prompt "Eres un tutor de Python. Dame un plan de estudio de 4 semanas para un principiante. Responde en una tabla." y dio solo 50 de 100, aunque tiene verbo de acción y formato. Encontré que las listas de palabras eran demasiado cortas ("dame" no estaba y buscaba "en tabla", no "en una tabla"). Agregué verbos en español, cambié los marcadores de formato y escribí una prueba para que no vuelva a pasar |
| Endpoint `/improve-prompt` con modo de respaldo sin clave | Lo probé primero sin clave (modo reglas) y luego con la clave real: salió "IA activa" y el puntaje subió de 50 a 100. Ahí encontré un fallo: el modelo coló una palabra en hindi en el prompt mejorado. Una regla extra en las instrucciones no bastó, así que agregué una verificación en el código que detecta letras de otros alfabetos y vuelve a pedir la respuesta (hasta 3 veces), con 2 pruebas nuevas |
| Contenido del `SKILL.md` | Probé la skill con el agente Cline en 3 casos (ver evidencia abajo). Observé que Cline primero adivinó una ruta incorrecta de la API y luego la corrigió leyendo la documentación de la API; y que cuando el servidor estaba apagado no inventó un puntaje, sino que pidió encenderlo, como indica la skill |

**Validación realizada:** `pytest` (16 pruebas), pruebas con el servidor simulado de OpenAI y revisión de las
3 vistas en escritorio y móvil.

**Evidencia:**

1. Un fallo real que encontré al probar la interfaz: un prompt completo recibió 50 de 100.
   ![Puntaje de 50 en un prompt completo](docs/img/validador-puntaje-50.png)

2. Después del ajuste y de la prueba nueva, las 14 pruebas pasan.
   ![pytest con 14 pruebas pasando](docs/img/pytest-14-passed.png)

3. El hook `commit-msg` rechaza el mensaje `cambios` porque no sigue Conventional Commits.
   ![Hook que rechaza un commit sin formato](docs/img/hook-rechaza-commit.png)

4. Un fallo real con la IA: el modelo mezcló una palabra en hindi en el prompt mejorado.
   ![Palabra en hindi en el prompt mejorado](docs/img/bug-palabra-en-hindi.png)

5. Prueba de la skill con el agente Cline. **Caso 1, prompt inválido ("hola"):** el agente valida primero y no llama a la IA.
   ![Cline con un prompt inválido](docs/img/skill-prueba1-prompt-invalido.png)

6. **Caso 2, prompt válido pero incompleto:** valida, muestra 50/100 y espera el permiso antes de mejorar.
   ![Cline valida y pide permiso](docs/img/skill-prueba2-valida-y-pide-permiso.png)

7. **Caso 3, la persona acepta:** recién ahí llama a `/improve-prompt` y devuelve el prompt mejorado con 100/100.
   ![Cline mejora con permiso](docs/img/skill-prueba3-mejora-con-permiso.png)

## 8. Qué del curso apliqué y dónde

| Tema del curso | Guías | Dónde está en el proyecto |
|---|---|---|
| Anatomía de un buen prompt | 01 a 04 | Los 4 chequeos de `/validate-prompt` y las piezas que pide `/improve-prompt` |
| Skills | 07 y 08 | `.github/skills/prompt-validator/SKILL.md` |
| Specs (SDD) | 13 a 15 | `docs/SPEC.md`: requisitos EARS, casos borde y criterios de terminado |
| Archivo de reglas | 16 | `AGENTS.md` |
| Seguridad y prompt injection | 12 | Claves en variables de entorno, texto del usuario solo en el rol `user`, prueba que busca claves |
| Primera llamada a la API de un LLM | 19 | `app/services/llm.py`: Responses API, JSON estricto, errores 401/404/429 |
| MCP y Stitch a código | 20 a 22 | `opencode.json`, `docs/prompts-stitch.md`, `docs/GUIA-STITCH.md`, carpeta `views/` |
| Git y Conventional Commits | 11 y 22 | Historial del repositorio y `docs/COMMITS.md` |
| Hooks | 23 a 27 | `.githooks/` (`commit-msg` y `pre-commit`) y `docs/HOOKS.md`, adaptados de las guías 22 y 27 |
