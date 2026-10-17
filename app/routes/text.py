"""Endpoints de la API. Solo reciben la petición y delegan en los servicios."""
from fastapi import APIRouter

from app import config
from app.schemas import (ImproveResult, PromptInput, PromptValidation,
                         TextAnalysis, TextInput)
from app.services import analysis, llm, skill_loader

router = APIRouter()


@router.get("/health", summary="Estado de la API")
def health() -> dict:
    # No expone la clave: solo dice si hay IA configurada o no.
    return {"status": "ok",
            "ai_mode": "ia" if config.openai_configured() else "reglas"}


@router.post("/analyze-text", response_model=TextAnalysis,
             summary="Analiza un texto (palabras, oraciones, frecuentes)")
def analyze_text(body: TextInput):
    return analysis.analyze_text(body.text)


@router.post("/validate-prompt", response_model=PromptValidation,
             summary="Valida la calidad de un prompt")
def validate_prompt(body: PromptInput):
    return analysis.validate_prompt(body.prompt)


@router.post("/improve-prompt", response_model=ImproveResult,
             summary="Mejora un prompt (OpenAI si hay clave; reglas si no)")
def improve_prompt(body: PromptInput):
    return llm.improve(body.prompt)


@router.get("/skills", summary="Lista las skills cargadas desde .github/skills/")
def skills() -> list[dict]:
    return skill_loader.list_skills()
