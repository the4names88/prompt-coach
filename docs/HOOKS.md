# Hooks de Git: guardarraíles del repositorio

Un hook es un script que Git ejecuta solo, en un momento fijo, y que puede **bloquear** la acción. Aquí hay dos,
en `.githooks/`. Están adaptados de la guía 22 (hook `commit-msg` de la plantilla) y de la guía 27 (política de
secretos), en versión simple y sin Node.

| Regla | Hook | ¿Bloquea? | Qué pasa |
|---|---|---|---|
| El mensaje sigue Conventional Commits | `commit-msg` | Sí | Rechaza `cambios`, `update: algo` o un mensaje con punto final |
| No subir archivos `.env` | `pre-commit` | Sí | Rechaza el commit si `.env` está en lo que vas a subir (`.env.example` sí se permite) |
| No subir claves en el código | `pre-commit` | Sí | Rechaza líneas que parecen una API key de OpenAI, Google o AWS, o una llave privada |

## Cómo activarlos (una vez por clon)
```bash
git config core.hooksPath .githooks
```
Git no activa los hooks solo: sin este comando existen pero no corren.

## Cómo comprobar que funcionan
```bash
git add README.md
git commit -m "cambios"                      # debe rechazarlo
git commit -m "docs: actualiza el readme"    # debe pasar
```
Guarda una captura del rechazo y del commit correcto como evidencia para el README.

## Limitaciones (para decirlas con honestidad)
- Detectan formatos conocidos de claves, no todas las posibles. Siguen siendo una red de seguridad, no un sustituto de guardar la clave en una variable de entorno.
- Se pueden saltar con `git commit --no-verify`. Por eso el `AGENTS.md` le prohíbe ese flag al agente.
- Solo protegen el repo local. Verificarlo también en el servidor (por ejemplo con GitHub Actions) sería el siguiente paso.
- La guía 27 muestra además hooks para el agente (un plugin de OpenCode). No se incluyeron aquí.
