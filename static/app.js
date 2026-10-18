/* Lógica de las 3 vistas. Cada <body data-page="..."> activa su función.
   Contrato con el HTML: los ids están documentados en docs/GUIA-STITCH.md.
   Si reemplazas el HTML con el de Stitch, conserva esos ids y todo sigue funcionando. */

// Estado compartido entre vistas (sessionStorage; si falla, la vista lo pide de nuevo).
const store = {
  get(key) { try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; } },
  set(key, value) { try { sessionStorage.setItem(key, JSON.stringify(value)); } catch { /* sin storage */ } },
};

const $ = (id) => document.getElementById(id);

const CHECK_LABELS = {
  longitud_minima: "Longitud mínima",
  tarea_clara: "Tarea clara (verbo de acción)",
  tiene_contexto: "Contexto o rol",
  indica_formato: "Formato de salida",
};

// Llama a la API del mismo servidor. Si falla, lanza un Error con mensaje legible.
async function post(path, body) {
  let res;
  try {
    res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    throw new Error("No se pudo conectar con la API. ¿Está corriendo uvicorn?");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data?.error?.message ||
      (res.status === 422 ? "El prompt está vacío o supera los 5000 caracteres." : `Error ${res.status}`);
    throw new Error(msg);
  }
  return data;
}

function setStatus(text, isError = false) {
  const el = $("status");
  if (!el) return;
  el.textContent = text;
  el.classList.toggle("error", isError);
}

function scoreClass(score) { return score >= 75 ? "high" : score >= 50 ? "mid" : "low"; }

// Badge que dice si la API está usando IA o el modo de reglas.
async function showMode() {
  const el = $("mode-badge");
  if (!el) return;
  try {
    const data = await (await fetch("/health")).json();
    el.textContent = data.ai_mode === "ia" ? "IA activa" : "Modo reglas (sin API key)";
  } catch { el.textContent = "API sin conexión"; }
}

/* ---------- Vista 1: escribir ---------- */
function pageEscribir() {
  const input = $("prompt-input");
  const counter = $("counter");
  const btn = $("btn-evaluar");
  input.value = store.get("prompt") || "";
  const update = () => { counter.textContent = `${input.value.length} / 5000`; };
  input.addEventListener("input", update);
  update();

  btn.addEventListener("click", async () => {
    const prompt = input.value.trim();
    if (!prompt) { setStatus("Escribe un prompt primero.", true); return; }
    btn.disabled = true;
    setStatus("Evaluando...");
    try {
      const validation = await post("/validate-prompt", { prompt });
      store.set("prompt", prompt);
      store.set("validation", validation);
      store.set("improved", null);
      window.location.href = "/views/evaluacion.html";
    } catch (e) {
      setStatus(e.message, true);
      btn.disabled = false;
    }
  });
}

/* ---------- Vista 2: evaluación ---------- */
function pageEvaluacion() {
  const prompt = store.get("prompt");
  const v = store.get("validation");
  if (!prompt || !v) { window.location.href = "/views/escribir.html"; return; }

  $("prompt-echo").textContent = prompt;
  const score = $("score");
  score.className = `score ${scoreClass(v.score)}`;
  score.style.setProperty("--pct", v.score); // el anillo se llena según el puntaje
  score.innerHTML = `${v.score}<small>/100</small>`;
  $("verdict").textContent = v.is_valid ? "El prompt cumple lo mínimo." : "Al prompt le falta lo mínimo: tarea clara o más detalle.";

  const checks = $("checks");
  checks.innerHTML = "";
  for (const [key, ok] of Object.entries(v.checks)) {
    const li = document.createElement("li");
    li.className = ok ? "ok" : "fail";
    const mark = document.createElement("span");
    mark.className = "mark";
    mark.textContent = ok ? "✓" : "✕";
    const name = document.createElement("span");
    name.textContent = CHECK_LABELS[key] || key;
    li.append(mark, name);
    checks.appendChild(li);
  }

  const sug = $("suggestions");
  sug.innerHTML = "";
  if (v.suggestions.length === 0) {
    const li = document.createElement("li");
    li.textContent = "Sin sugerencias: el prompt tiene las piezas clave.";
    sug.appendChild(li);
  }
  for (const s of v.suggestions) {
    const li = document.createElement("li");
    li.textContent = s;
    sug.appendChild(li);
  }

  const btn = $("btn-mejorar");
  btn.addEventListener("click", async () => {
    btn.disabled = true;
    setStatus("Mejorando el prompt...");
    try {
      const result = await post("/improve-prompt", { prompt });
      store.set("improved", result);
      window.location.href = "/views/mejorado.html";
    } catch (e) {
      setStatus(e.message, true);
      btn.disabled = false;
    }
  });
}

/* ---------- Vista 3: prompt mejorado ---------- */
function pageMejorado() {
  const r = store.get("improved");
  if (!r) { window.location.href = "/views/escribir.html"; return; }

  $("original").textContent = r.original_prompt;
  $("improved").textContent = r.improved_prompt;
  $("mode").textContent = r.mode === "ia" ? `Mejorado con IA (${r.model})` : "Mejorado con reglas (sin IA)";
  $("score-before").textContent = r.original_score;
  $("score-after").textContent = r.improved_score;
  const diff = r.improved_score - r.original_score;
  $("score-delta").textContent = diff > 0 ? `+${diff} puntos` : diff === 0 ? "sin cambio" : `${diff} puntos`;

  const list = $("changes");
  list.innerHTML = "";
  for (const c of r.changes) {
    const li = document.createElement("li");
    li.textContent = c;
    list.appendChild(li);
  }

  $("btn-copiar").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(r.improved_prompt);
      setStatus("Copiado al portapapeles.");
    } catch { setStatus("No se pudo copiar: selecciona el texto y usa Ctrl+C.", true); }
  });
  $("btn-nuevo").addEventListener("click", () => {
    store.set("prompt", null); store.set("validation", null); store.set("improved", null);
    window.location.href = "/views/escribir.html";
  });
}

const PAGES = { escribir: pageEscribir, evaluacion: pageEvaluacion, mejorado: pageMejorado };
document.addEventListener("DOMContentLoaded", () => {
  showMode();
  PAGES[document.body.dataset.page]?.();
});
