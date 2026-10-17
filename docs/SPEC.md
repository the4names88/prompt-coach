# Spec: Prompt Coach MVP

Escrita antes de programar, siguiendo el método Spec-Driven Development del curso (guías 13 a 15):
requisitos con notación EARS (`WHEN ... THE SYSTEM SHALL ...`), casos borde decididos de antemano y una
Definición de Terminado por historia.

**Objetivo del epic:** que una persona escriba un prompt, vea qué le falta y obtenga una versión mejor,
con la IA solo cuando aporta valor.

| Historia | Título | Tipo |
|---|---|---|
| PC-101 | Vista 1: escribir el prompt | Frontend |
| PC-102 | Vista 2: evaluación del prompt | Frontend |
| PC-103 | Vista 3: prompt mejorado | Frontend |
| PC-104 | `POST /validate-prompt` | Backend |
| PC-105 | `POST /improve-prompt` (OpenAI + respaldo) | Backend |

---

## PC-104 · Backend: validar un prompt
**Requisitos**
- WHEN llega un prompt de 1 a 5000 caracteres, THE SYSTEM SHALL responder 200 con `score` (0 a 100), `is_valid`, `checks` y `suggestions`.
- WHEN el prompt está vacío o supera 5000 caracteres, THE SYSTEM SHALL responder 422.
- THE SYSTEM SHALL calcular el puntaje como el porcentaje de 4 chequeos cumplidos: longitud mínima (20 caracteres), tarea clara, contexto y formato.
- THE SYSTEM SHALL marcar `is_valid: true` solo si cumple longitud mínima y tarea clara.

**Casos borde decididos**
- Mayúsculas y minúsculas no importan (se compara en minúsculas).
- Un prompt de solo espacios cuenta como corto.

## PC-105 · Backend: mejorar un prompt
**Requisitos**
- WHEN hay `OPENAI_API_KEY` y `OPENAI_MODEL` configurados, THE SYSTEM SHALL pedir la mejora a OpenAI con la Responses API y salida JSON de esquema estricto, y responder `mode: "ia"`.
- WHEN falta la clave o el modelo, THE SYSTEM SHALL responder igual con una plantilla de reglas y `mode: "reglas"`, sin llamar a OpenAI.
- THE SYSTEM SHALL poner el texto del usuario solo en el rol `user` de OpenAI, nunca dentro de las instrucciones `developer`.
- WHEN OpenAI falla, THE SYSTEM SHALL responder con el formato `{"error": {"code", "message"}}`: 502 para clave inválida, modelo inexistente o error general; 503 para límite de uso o falta de conexión.
- THE SYSTEM SHALL devolver `original_score` e `improved_score` calculados con la misma función de validación.

**Casos borde decididos**
- La clave y el modelo nunca aparecen en el código, en los logs ni en las respuestas (`/health` solo dice `ia` o `reglas`).
- Si el modelo devuelve algo que no cumple el esquema, se responde `OPENAI_BAD_OUTPUT` en vez de un error 500 genérico.
- No se fija `temperature`: los modelos de razonamiento actuales la rechazan (guía 19).
- Si el prompt ya tiene 100 puntos, el frontend ofrece mejorar de todos modos, pero la skill indica no gastar IA en ese caso.

## PC-101 · Vista 1: escribir
- WHEN la persona escribe, THE SYSTEM SHALL mostrar el contador de caracteres (`n / 5000`).
- WHEN pulsa "Evaluar prompt" con el campo vacío, THE SYSTEM SHALL mostrar un mensaje de error sin llamar a la API.
- WHEN la API responde, THE SYSTEM SHALL ir a la vista 2.
- WHEN la API no responde, THE SYSTEM SHALL mostrar "No se pudo conectar con la API" y reactivar el botón.

## PC-102 · Vista 2: evaluación
- THE SYSTEM SHALL mostrar el puntaje con color: verde desde 75, ámbar desde 50, rojo por debajo.
- THE SYSTEM SHALL listar los 4 chequeos con ✔ o ✖ y las sugerencias.
- WHEN se abre la vista sin un prompt guardado, THE SYSTEM SHALL volver a la vista 1.
- WHEN pulsa "Mejorar mi prompt", THE SYSTEM SHALL llamar a `/improve-prompt`, mostrar "Mejorando..." y desactivar el botón mientras espera.

## PC-103 · Vista 3: mejorado
- THE SYSTEM SHALL mostrar el prompt original y el mejorado lado a lado, con sus puntajes y la diferencia.
- THE SYSTEM SHALL indicar si se mejoró con IA (y qué modelo) o con reglas.
- WHEN pulsa "Copiar", THE SYSTEM SHALL copiar el prompt mejorado; si el navegador lo impide, SHALL explicar cómo copiarlo a mano.
- En móvil las dos columnas se apilan.

---

## Definición de Terminado
- [x] Las 3 vistas funcionan con la API real y con el servidor simulado de OpenAI.
- [x] `pytest` pasa (13 pruebas), incluida la que busca claves en los archivos.
- [x] Cada caso borde de arriba está resuelto en el código o probado.
- [x] Ninguna clave en el repositorio (`.env` está en `.gitignore`).
- [ ] Las vistas coinciden con el diseño de Stitch (se completa al importar las pantallas, ver `docs/GUIA-STITCH.md`).
