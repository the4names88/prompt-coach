"""Lógica de negocio: análisis de texto y validación de prompts.

Aquí NO hay nada de FastAPI. Son funciones normales de Python,
así se pueden probar y reutilizar fácilmente.
"""
import re
from collections import Counter

from app.config import MIN_PROMPT_LENGTH

# Palabras comunes que no aportan al conteo de "palabras frecuentes"
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "de", "del", "y", "o", "en", "a",
    "que", "es", "por", "con", "para", "se", "su", "al", "lo", "como", "the",
    "and", "of", "to", "in", "is", "for", "on",
}

# Verbos de acción que indican una tarea clara en un prompt
ACTION_VERBS = (
    "analiza", "resume", "explica", "genera", "crea", "escribe", "traduce",
    "compara", "lista", "clasifica", "redacta", "describe",
    "analyze", "summarize", "explain", "generate", "create", "write",
    "translate", "compare", "list", "classify", "describe", "dame", "haz",
    "diseña", "prepara", "elabora", "propón", "ayúdame",
)

CONTEXT_MARKERS = ("contexto", "para un", "para una", "eres", "actúa", "como un",
                   "audience", "context", "you are", "act as")
FORMAT_MARKERS = ("formato", "tabla", "lista", "en json", "máximo", "maximo",
                  "palabras", "viñetas", "format", "bullet", "table", "words")

# Nombre legible de cada chequeo (se usa en la API, el frontend y la skill)
CHECK_LABELS = {
    "longitud_minima": "Longitud mínima",
    "tarea_clara": "Tarea clara (verbo de acción)",
    "tiene_contexto": "Contexto o rol",
    "indica_formato": "Formato de salida",
}


def _words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def analyze_text(text: str) -> dict:
    words = _words(text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    avg_len = round(sum(len(w) for w in words) / len(words), 2) if words else 0.0
    frequent = Counter(w for w in words if w not in STOPWORDS and len(w) > 2)
    return {
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences),
        "average_word_length": avg_len,
        # Lectura promedio: ~200 palabras por minuto
        "reading_time_seconds": round(len(words) / 200 * 60),
        "top_words": [w for w, _ in frequent.most_common(5)],
    }


def validate_prompt(prompt: str) -> dict:
    low = prompt.lower()
    checks = {
        "longitud_minima": len(prompt.strip()) >= MIN_PROMPT_LENGTH,
        "tarea_clara": any(v in low for v in ACTION_VERBS),
        "tiene_contexto": any(m in low for m in CONTEXT_MARKERS),
        "indica_formato": any(m in low for m in FORMAT_MARKERS),
    }
    suggestions = []
    if not checks["longitud_minima"]:
        suggestions.append("El prompt es muy corto: agrega más detalle.")
    if not checks["tarea_clara"]:
        suggestions.append("Empieza con un verbo de acción (analiza, resume, genera...).")
    if not checks["tiene_contexto"]:
        suggestions.append("Agrega contexto: rol, audiencia o situación.")
    if not checks["indica_formato"]:
        suggestions.append("Indica el formato de salida (lista, tabla, máximo de palabras).")

    score = round(sum(checks.values()) / len(checks) * 100)
    # Es válido si cumple lo mínimo: longitud y tarea clara
    is_valid = checks["longitud_minima"] and checks["tarea_clara"]
    return {"score": score, "is_valid": is_valid, "checks": checks,
            "suggestions": suggestions}
