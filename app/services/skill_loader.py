"""Lee las skills de .github/skills/ y extrae sus metadatos (name, description).

Un SKILL.md empieza con un bloque entre '---' tipo:
    ---
    name: prompt-validator
    description: ...
    ---
Lo leemos a mano para no depender de librerías extra.
"""
from pathlib import Path

from app.config import SKILLS_DIR


def parse_skill(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
    return {
        "name": meta.get("name", path.parent.name),
        "description": meta.get("description", ""),
        "path": str(path.relative_to(SKILLS_DIR.parent.parent)),
    }


def list_skills() -> list[dict]:
    if not SKILLS_DIR.exists():
        return []
    return [parse_skill(p) for p in sorted(SKILLS_DIR.glob("*/SKILL.md"))]
