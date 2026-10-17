# Prompts para Stitch

Usa la plantilla de 3 capas de la guía 22: **estructura + vibe + contenido**.
En Stitch elige **Web**, deja el modelo recomendado y pon al proyecto el nombre del repositorio.
Pega la vista 1, espera a que termine (puede tardar uno o dos minutos) y pide las otras dos en el
chat lateral del mismo proyecto, para que mantengan el mismo estilo.

## Vista 1: escribir el prompt
```
[ESTRUCTURA] Pantalla web "Escribir el prompt" de una app llamada Prompt Coach. Header con el logo
"Prompt Coach" y una pequeña etiqueta a la derecha que dice "IA activa". Debajo, un indicador de 3 pasos:
"1 · Escribir" (activo), "2 · Evaluar", "3 · Mejorar". Título grande, una frase de apoyo, una tarjeta con
un área de texto grande con placeholder, contador de caracteres "0 / 5000" alineado a la derecha y un
botón principal "Evaluar prompt".
[VIBE] Estilo limpio, moderno y amable, mucho espacio en blanco, esquinas redondeadas, paleta índigo con
fondo gris muy claro, tipografía sans-serif legible. Debe verse bien en móvil.
[CONTENIDO] Título: "Escribe el prompt que quieres mejorar". Frase: "Lo evaluamos con 4 criterios y, si
quieres, lo reescribimos mejor." Placeholder: "Ejemplo: dame un plan de estudio de Python".
```

## Vista 2: evaluación
```
Con el mismo estilo, paleta, tipografía y header que la pantalla 1, crea la pantalla "Evaluación del
prompt". El paso activo del indicador es "2 · Evaluar". Una tarjeta con un círculo grande de puntaje
("25/100") con borde rojo a la izquierda y, a la derecha, 4 filas de chequeo: "Longitud mínima" (✔ verde),
"Tarea clara (verbo de acción)", "Contexto o rol" y "Formato de salida" (✖ rojo). Debajo, una tarjeta
"Qué mejorar" con 3 sugerencias en lista, y otra tarjeta con el prompt original en un recuadro, un botón
principal "Mejorar mi prompt" y un botón secundario "Editar".
```

## Vista 3: prompt mejorado
```
Con el mismo estilo, paleta, tipografía y header que la pantalla 1, crea la pantalla "Prompt mejorado".
El paso activo es "3 · Mejorar". Título "Tu prompt mejorado" y una línea que dice "Mejorado con IA". Una
tarjeta "Antes y después" con dos columnas: "Original · 25/100" con el texto original, y "Mejorado · 100/100
+75 puntos" con un recuadro de borde índigo que contiene un prompt de 5 líneas (Contexto, Tarea,
Restricciones, Formato de salida, Criterio de éxito). Debajo, botones "Copiar prompt mejorado" (principal)
y "Probar otro prompt". Al final, una tarjeta "Qué cambió" con 4 viñetas. En móvil las columnas se apilan.
```

## Ajustes útiles (frases cortas en el chat de Stitch)
- "Usa exactamente la misma paleta, tipografía y header que la pantalla 1."
- "Botones más grandes."
- "Agrega una versión en modo oscuro."

Guarda aquí los prompts que realmente uses, si los cambias: la guía 22 pide que queden en este archivo.
