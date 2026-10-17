# Guía de commits (el coach va a revisar el historial)

## Qué se evalúa
Que el historial muestre **tu proceso**: varios commits pequeños, con formato Conventional Commits, repartidos
mientras avanzas, y sin ninguna clave dentro.

## Antes del primer commit
```bash
git init
git config user.name "Tu Nombre"
git config user.email "tu-correo@ejemplo.com"
git config core.hooksPath .githooks      # activa los hooks (ver docs/HOOKS.md)
git status                                # comprueba que NO aparece .env
```

## Formato
`tipo(alcance opcional): descripción corta en imperativo`, sin punto final y de menos de 72 caracteres.

| Tipo | Cuándo | Ejemplo |
|---|---|---|
| `feat` | Algo nuevo | `feat(api): agrega endpoint para mejorar prompts` |
| `fix` | Corrige un error | `fix(home): corrige enlace roto de volver al inicio` |
| `docs` | Documentación | `docs: guarda prompts usados en stitch` |
| `style` | Formato o estilo sin cambiar el comportamiento | `style(menu): ajusta padding del botón` |
| `refactor` | Reorganiza sin cambiar lo que hace | `refactor(views): renombra archivos a kebab-case` |
| `test` | Pruebas | `test: agrega prueba de errores de openai` |
| `chore` | Mantenimiento | `chore: ignora la carpeta .venv` |

Evita mensajes como `cambios`, `update` o `listo`: los hooks los rechazan.

## Orden sugerido (un commit por cada paso real, cuando lo hagas tú)
1. `chore: agrega gitignore y archivos de configuración` → `.gitignore`, `.env.example`, `requirements.txt`, `pytest.ini`
2. `feat(api): agrega api con validación de prompts` → `app/`
3. `feat(llm): agrega mejora de prompts con openai y modo de reglas` → si lo separas del paso anterior
4. `feat(skill): agrega skill prompt-validator y reglas del agente` → `.github/skills/`, `AGENTS.md`
5. `test: agrega pruebas y servidor simulado de openai` → `tests/`, `tools/`
6. `docs: agrega spec y guías del proyecto` → `docs/`
7. `feat(ui): agrega las tres vistas base` → `views/`, `static/`
8. `docs: guarda prompts usados en stitch` → cuando diseñes en Stitch
9. `feat(escribir): importa vista desde stitch con el mcp` (y una por cada vista) → cuando el agente las importe
10. Un commit por cada ajuste propio (`fix`, `style`, `refactor`)
11. `docs: completa evidencia de uso de ia en el readme` → al final

Haz commit de cada paso cuando lo termines, no todos juntos al final.

## Antes de cada commit
```bash
git status        # ¿aparece .env? entonces NO hagas commit
git diff --cached # revisa lo que vas a subir
```

## Subir a GitHub
```bash
gh repo create prompt-coach --public --source=. --remote=origin
git push -u origin main
```
(Sin GitHub CLI: crea el repo vacío en github.com/new y sigue las dos líneas que te muestra GitHub.)

## Si se te escapa una clave
Revócala primero en la plataforma (OpenAI o Stitch) y crea otra. Borrar el archivo no basta: la clave queda
en el historial. Avisa al coach.

## Revisar antes de entregar
```bash
git log --oneline
```
