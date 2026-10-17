# AGENTS.md: reglas del proyecto Prompt Coach

## Qué es este proyecto
API en FastAPI que valida y mejora prompts, con una interfaz de 3 vistas HTML.
Usa OpenAI para mejorar prompts cuando hay clave configurada y reglas simples cuando no.

## Cómo ejecutarlo
- Instalar: `pip install -r requirements.txt` (dentro de un entorno virtual `.venv`)
- Servidor: `uvicorn app.main:app --reload` y abrir http://127.0.0.1:8000
- Pruebas: `pytest` (deben pasar todas antes de terminar cualquier tarea)
- Probar sin gastar saldo: `python tools/mock_openai.py` y las variables de `docs/GUIA-STITCH.md`

## Estructura (separación de responsabilidades)
- `app/routes/`: solo reciben la petición y responden. Nada de lógica.
- `app/services/`: la lógica (validación, llamada a OpenAI, lectura de skills).
- `app/schemas.py`: modelos de entrada y salida.
- `app/config.py`: configuración. Lee variables de entorno.
- `views/` y `static/`: frontend. `docs/` tiene el diseño de Stitch; no lo edites a mano.
- `.github/skills/prompt-validator/SKILL.md`: la skill que controla al agente.

## Convenciones
- Python 3.10+, funciones cortas, tipos en las firmas.
- Comentarios y textos de la interfaz en español.
- Los errores de la API usan el formato `{"error": {"code": "...", "message": "..."}}`.
- Las vistas conservan los ids documentados en `docs/GUIA-STITCH.md`.

## Seguridad (obligatorio)
- Nunca leas, edites ni crees `.env`. Las variables nuevas se agregan a `.env.example`.
- Nunca escribas claves en el código, en Markdown ni en capturas. Se leen con `os.environ`.
- El modelo de OpenAI sale de `OPENAI_MODEL`; no lo escribas fijo en el código.
- El texto del usuario va en el rol `user` de OpenAI, nunca dentro de las instrucciones `developer`.
- No ejecutes `rm -rf`, `git push --force` ni `--no-verify`.

## Git
- Conventional Commits: `tipo(alcance): descripción corta en minúsculas e imperativo`
  (feat, fix, docs, style, refactor, test, chore).
- Un commit = un cambio lógico. Nunca hagas `git push` sin que te lo pidan.
- Los hooks de `.githooks/` validan el mensaje y buscan claves: se activan con `git config core.hooksPath .githooks`. Nunca uses `--no-verify`.
