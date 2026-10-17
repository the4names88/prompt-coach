"""Punto de entrada. Ejecutar con:  uvicorn app.main:app --reload"""
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR, VIEWS_DIR
from app.routes import text
from app.services.llm import LLMError

app = FastAPI(
    title="Prompt Coach API",
    description="Valida y mejora prompts. Integra la skill agéntica prompt-validator.",
    version="2.0.0",
)


@app.exception_handler(LLMError)
async def llm_error_handler(request, exc: LLMError):
    """Formato de error estándar (igual al de la guía 15): {"error": {code, message}}."""
    return JSONResponse(status_code=exc.status,
                        content={"error": {"code": exc.code, "message": exc.message}})


app.include_router(text.router)


@app.get("/", include_in_schema=False)
def home():
    """La vista 1 (escribir el prompt) es la portada."""
    return FileResponse(VIEWS_DIR / "escribir.html")


# Vistas HTML (las que salen de Stitch) y archivos estáticos (css/js).
app.mount("/views", StaticFiles(directory=VIEWS_DIR, html=True), name="views")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
