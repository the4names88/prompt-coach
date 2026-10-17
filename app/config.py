"""Configuración central de la API (un solo lugar para los valores ajustables).

La API key de OpenAI y el nombre del modelo NUNCA se escriben aquí:
se leen de variables de entorno (guía 19 del curso).
"""
import os
from pathlib import Path

# Raíz del proyecto: la carpeta que contiene "app" y ".github"
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde viven las skills del agente (estándar Agent Skills)
SKILLS_DIR = BASE_DIR / ".github" / "skills"

# Carpetas del frontend (las vistas de Stitch viven en views/)
VIEWS_DIR = BASE_DIR / "views"
STATIC_DIR = BASE_DIR / "static"

# Límites de validación
MAX_TEXT_LENGTH = 5000
MIN_PROMPT_LENGTH = 20


def _load_env_file(path: Path) -> None:
    """Lee un archivo .env sencillo (CLAVE=valor) sin librerías extra.

    No pisa variables que ya existen en el entorno. El archivo .env está en
    .gitignore, así que nunca se sube a Git.
    """
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(BASE_DIR / ".env")


def openai_model() -> str:
    """Modelo elegido. Cambiar de modelo = cambiar la variable, no el código."""
    return os.environ.get("OPENAI_MODEL", "").strip()


def openai_configured() -> bool:
    """True si hay clave y modelo; si no, la API usa el modo de reglas."""
    return bool(os.environ.get("OPENAI_API_KEY", "").strip()) and bool(openai_model())
