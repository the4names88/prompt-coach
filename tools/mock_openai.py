"""Servidor simulado de OpenAI para probar SIN clave y SIN gastar saldo.

Idea tomada de la guía 19 (sección 14): el SDK acepta OPENAI_BASE_URL, así que
apuntamos a este servidor local. Solo usa la librería estándar de Python.

Uso (dos terminales):
  Terminal 1:  python tools/mock_openai.py
  Terminal 2:  $env:OPENAI_BASE_URL = "http://127.0.0.1:8765/v1"
               $env:OPENAI_API_KEY  = "clave-falsa"
               $env:OPENAI_MODEL    = "modelo-demo-1"
               uvicorn app.main:app --reload

Si OPENAI_MODEL vale "no-existe", responde 404; si la clave es "bad", 401.
"""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def response_object(text: str, model: str) -> dict:
    return {
        "id": "resp_mock", "object": "response", "created_at": int(time.time()),
        "status": "completed", "model": model,
        "output": [{"type": "message", "id": "msg_1", "status": "completed",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": text, "annotations": []}]}],
        "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15,
                  "input_tokens_details": {"cached_tokens": 0},
                  "output_tokens_details": {"reasoning_tokens": 0}},
        "parallel_tool_calls": True, "tool_choice": "auto", "tools": [],
        "error": None, "incomplete_details": None, "instructions": None,
        "metadata": {}, "temperature": None, "top_p": None,
    }


FAKE_RESULT = {
    "improved_prompt": (
        "Contexto: soy estudiante principiante de programación.\n"
        "Tarea: Genera un plan de estudio de Python para 4 semanas.\n"
        "Restricciones: máximo 1 hora por día, sin temas avanzados.\n"
        "Formato de salida: tabla con semana, tema y ejercicio.\n"
        "Criterio de éxito: puedo seguir el plan sin buscar otros recursos."
    ),
    "changes": ["Agregué contexto y nivel.", "Definí restricciones de tiempo.",
                "Pedí formato de tabla.", "Agregué un criterio de éxito."],
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # silencia el log
        pass

    def _json(self, status: int, body: dict) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(length) or b"{}")
        if self.headers.get("Authorization", "") == "Bearer bad":
            return self._json(401, {"error": {"message": "Incorrect API key provided",
                                              "type": "invalid_request_error",
                                              "code": "invalid_api_key"}})
        model = req.get("model")
        if model == "no-existe":
            return self._json(404, {"error": {"message": "The model does not exist",
                                              "type": "invalid_request_error",
                                              "code": "model_not_found"}})
        # Guarda lo último que recibió, útil para inspeccionar en pruebas
        Handler.last_request = req
        self._json(200, response_object(json.dumps(FAKE_RESULT, ensure_ascii=False), model))


if __name__ == "__main__":
    print("Mock de OpenAI en http://127.0.0.1:8765  (Ctrl+C para salir)")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
