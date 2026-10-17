"""Modelos de entrada y salida. FastAPI los usa para validar y documentar."""
from typing import Literal

from pydantic import BaseModel, Field

from app.config import MAX_TEXT_LENGTH


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT_LENGTH,
                      description="Texto a analizar")


class PromptInput(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=MAX_TEXT_LENGTH,
                        description="Prompt que se quiere validar o mejorar")


class TextAnalysis(BaseModel):
    characters: int
    words: int
    sentences: int
    average_word_length: float
    reading_time_seconds: int
    top_words: list[str]


class PromptValidation(BaseModel):
    score: int = Field(..., description="Puntaje de 0 a 100")
    is_valid: bool
    checks: dict[str, bool]
    suggestions: list[str]


class ImprovedPrompt(BaseModel):
    """Lo que debe devolver el modelo (también valida su salida)."""
    improved_prompt: str = Field(..., min_length=1)
    changes: list[str]


class ImproveResult(BaseModel):
    original_prompt: str
    improved_prompt: str
    changes: list[str]
    mode: Literal["ia", "reglas"] = Field(
        ..., description="'ia' si respondió OpenAI, 'reglas' si no hay clave configurada")
    model: str | None = None
    original_score: int
    improved_score: int
