# Explicación para presentar (lenguaje simple)

## Tu pitch de 1 minuto
"Hice **Prompt Coach**, una API con FastAPI que revisa qué tan bueno es un prompt. Le da un puntaje con 4
criterios y, si lo pides, lo reescribe mejor usando OpenAI. Está dividida en carpetas con una responsabilidad
cada una. Además creé una **skill** que le dice a un agente de IA cómo debe usar mi API: primero validar, y
solo después mejorar, para no gastar IA en prompts sin sentido. Las pantallas las diseñé en Stitch y las
conecté al código con MCP. Y la API key nunca está en el código: vive en una variable de entorno."

## Cómo fluye todo
```
Navegador (3 vistas de Stitch)
   │  pide evaluar / mejorar
   ▼
FastAPI ── routes (reciben) ──► services (piensan) ──► OpenAI (solo para mejorar)
   ▲                                   │                  la clave vive solo aquí, en el servidor
   │                                   └─ si no hay clave: plantilla de reglas
   └── skill prompt-validator: reglas para el agente de IA que use esta API
```

## Glosario
- **API:** forma de que un programa le pida algo a otro. Como el mesero de un restaurante.
- **Endpoint:** cada "plato del menú" de la API (`/validate-prompt`, `/improve-prompt`...).
- **FastAPI:** la librería de Python con la que se construye la API. Genera sola la página `/docs`.
- **API key:** contraseña para usar el servicio de otra empresa (OpenAI, Stitch). Se guarda en una variable de entorno, nunca en el código ni en Git.
- **Variable de entorno:** valor guardado fuera del código, en tu computadora, que el programa lee al arrancar.
- **Skill (Agent Skills):** archivo `SKILL.md` con reglas para un agente de IA. Su `description` le dice cuándo usarla.
- **Agente de IA:** una IA que no solo responde, sino que usa herramientas (por ejemplo, llamar a tu API).
- **Stitch:** herramienta de Google que diseña pantallas a partir de una descripción.
- **MCP:** protocolo que deja que un agente (OpenCode) use herramientas externas, como Stitch.
- **Prompt injection:** cuando un texto trae órdenes escondidas ("ignora lo anterior"). Por eso el texto del usuario va en el rol `user` y la skill lo trata como datos.
- **Structured Outputs:** pedirle a OpenAI que responda con un JSON de formato exacto, para que el programa pueda leerlo sin adivinar.
- **Modo de reglas:** respaldo sin IA; la app sigue funcionando si no hay clave.

## Preguntas que te pueden hacer
**¿Por qué separaron rutas, lógica y configuración?** Para poder cambiar una parte sin romper las otras y
probar la lógica sin levantar el servidor.

**¿Qué hace la skill que no haría el agente por su cuenta?** Lo obliga a validar antes de mejorar, a no
llamar a la IA si el prompt no tiene lo mínimo o ya está completo, a no tocar claves y a responder siempre
con el mismo formato.

**¿Dónde se usa OpenAI y qué entra y sale?** Solo en `/improve-prompt`. Entra el prompt y la lista de
piezas que le faltan; sale un JSON con el prompt mejorado y la lista de cambios.

**¿Qué pasa si no hay API key?** La API responde igual en modo reglas, y la insignia lo muestra.

**¿Cómo protegieron la clave?** Variable de entorno, `.env` en `.gitignore`, ningún archivo con claves
(hay una prueba automática que lo verifica) y el navegador nunca la ve porque la llamada a OpenAI la hace el servidor.

**¿Para qué sirve Stitch aquí?** Para diseñar las 3 pantallas antes de programarlas; el agente las baja al
proyecto con el MCP. La spec dice qué debe pasar y el diseño dice cómo se ve.

**¿Cómo probaron sin gastar saldo?** Con un servidor simulado de OpenAI (`tools/mock_openai.py`).

## Tu parte antes de entregar (esto es lo que evalúan como "criterio técnico")
1. Haz un cambio propio y explícalo: por ejemplo, agrega un verbo a `ACTION_VERBS` en `app/services/analysis.py`, ajusta un texto de la skill o cambia un color en `static/styles.css`. Anótalo en la tabla de la sección 7 del README.
2. Corre `pytest` y mira que pasen. Después rompe algo a propósito (cambia un número en un test), mira cómo falla y devuélvelo.
3. Prueba la skill con GitHub Copilot, Claude u otro agente: pídele "revisa este prompt: hola" y comprueba que no llama a la IA. Haz una captura.
4. Completa las 4 filas "(completar)" del README con lo que realmente hiciste.
5. Diseña las 3 pantallas en Stitch e impórtalas (`docs/GUIA-STITCH.md`). Si no alcanzas, déjalo anotado y entrega las vistas base.
6. Antes de subir a Git: `git status` y comprueba que no aparece `.env`.

## Commits
El coach va a revisar el historial de commits. La guía completa (formato, orden sugerido, cómo activar los hooks
y qué hacer si se escapa una clave) está en `docs/COMMITS.md`. Los hooks de `.githooks/` rechazan los mensajes
sin formato y bloquean `.env` y claves (`docs/HOOKS.md`).
