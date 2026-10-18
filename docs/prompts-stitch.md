# Prompts para Stitch

Usa la plantilla de 3 capas de la guía 22: **estructura + vibe + contenido**, más una regla final.
En Stitch elige **Web**, deja el modelo recomendado y pon al proyecto el nombre del repositorio.
Pega la vista 1, espera a que termine (puede tardar uno o dos minutos) y pide las otras dos en el
chat lateral del mismo proyecto, para que mantengan el mismo estilo.
La dirección visual completa está en `docs/DESIGN.md`.

## Decisión de diseño
1. La primera versión pedía paleta índigo. La cambié porque el índigo y el violeta son el color por defecto
   de casi todo lo que genera una IA y se ve genérico.
2. La segunda versión quitó tantos elementos que quedó un formulario pelado y sin carácter. Lo descarté.
3. La versión actual usa la guía de la skill `soft-skill` (taste-skill): estructuralismo suave, contenedores
   de doble marco, píldoras flotantes y una división editorial, con un ejemplo de prompt resaltado como con
   marcador. Mantiene la paleta verde azulada y no inventa menús ni afirmaciones.

## Vista 1: escribir el prompt
```
Rediseña la Pantalla 1 con un acabado premium, de estudio de diseño. Conserva el contenido descrito y mejora por completo la forma.

[DIRECCIÓN VISUAL] Estructuralismo suave: fondo gris plata verdoso muy claro (#EEF1EC) con superficies blancas que flotan, sombras largas y muy difusas teñidas de verde (nada de bordes grises duros de 1 px ni sombras negras), esquinas muy redondeadas (28 px). Los contenedores importantes tienen doble marco: una bandeja exterior translúcida con borde fino y 6 px de relleno, y dentro un núcleo blanco con esquinas concéntricas y un brillo interior sutil. Títulos en Bricolage Grotesque, grandes y de peso fuerte, con espaciado ajustado. Texto en Plus Jakarta Sans. Lo que escribe el usuario en JetBrains Mono. Texto en azul tinta (#14213D) y secundario en #5B6577. Único color de acento: verde azulado profundo (#0F5C5A). Amarillo marcador (#FFE45C) solo para resaltar texto. Iconos de línea ultrafina. Mucho espacio en blanco. Sin morado, índigo, neón, Inter, emojis ni negro puro.

[LAYOUT] Escritorio con división editorial: columna izquierda de ~55% y columna derecha de ~45%. Header como una píldora flotante, separada del borde superior (no pegada), con el logo "Prompt Coach" a la izquierda y la etiqueta "IA activa" a la derecha. Debajo, un indicador de 3 pasos en otra píldora flotante: "1 · Escribir" (activo, relleno verde azulado), "2 · Evaluar", "3 · Mejorar".
Columna izquierda: título grande "Escribe el prompt que quieres mejorar" (máximo 3 líneas), la frase "Lo evaluamos con 4 criterios y, si quieres, lo reescribimos mejor.", y el área de texto dentro de un contenedor de doble marco, con placeholder "Ejemplo: dame un plan de estudio de Python" y contador "0 / 5000" a la derecha. Botón principal en píldora completa "Evaluar prompt", con un pequeño círculo con una flecha dentro del propio botón, a la derecha.
Columna derecha: una tarjeta de doble marco titulada "Así se ve un buen prompt". Dentro, este ejemplo en JetBrains Mono: "Eres un tutor de Python. Dame un plan de estudio de 4 semanas para un principiante. Responde en una tabla." Resalta con marcador amarillo estos fragmentos: "Eres un tutor de Python" (etiqueta pequeña "Rol"), "Dame un plan de estudio" ("Tarea"), "de 4 semanas para un principiante" ("Contexto") y "Responde en una tabla" ("Formato"). Debajo, una línea: "Evaluamos cuatro cosas: longitud, tarea clara, contexto y formato."
Móvil: una sola columna, la tarjeta del ejemplo debajo del área de texto, botones de al menos 44 px de alto.

[REGLA] Usa solo lo descrito. Sin menús de navegación, sin enlaces, sin pie de página, sin estadísticas, sin imágenes y sin afirmaciones inventadas.
```

## Vista 2: evaluación
El primer intento (dos columnas con mucho contenido) salió apretado: el texto se partía en columnas muy angostas.
Este es el prompt que funcionó, pegado en el chat con la Vista 2 seleccionada:
```
Rehaz esta pantalla con un layout más simple y ancho. Usa una sola columna del mismo ancho que la columna principal de la Vista 1, con las secciones apiladas una debajo de otra y mucho espacio entre ellas. Mantén exactamente el mismo estilo, header, paleta y tipografías de la Vista 1 (doble marco, píldoras flotantes).

Orden de arriba a abajo:
1. Header flotante e indicador de pasos, con "2 · Evaluar" activo.
2. Una tarjeta de doble marco con el círculo de puntaje "25/100" (anillo rojo lápiz) a la izquierda y, a su derecha, las 4 filas de chequeo en una lista vertical bien legible: "Longitud mínima" (✓ verde), "Tarea clara (verbo de acción)", "Contexto o rol" y "Formato de salida" (✕ rojo), cada una con borde izquierdo de 3 px, el símbolo y el texto completo en una sola línea.
3. Una tarjeta "Qué mejorar" con 3 sugerencias en lista, con texto a ancho completo.
4. Una tarjeta con el prompt original en JetBrains Mono.
5. Los botones: "Mejorar mi prompt" (píldora principal con círculo con flecha) y "Editar" (borde fino), uno al lado del otro.

Ningún texto debe partirse en columnas angostas. Sin menús, enlaces, pie de página ni afirmaciones inventadas.
```

## Vista 3: prompt mejorado
Con lo aprendido en la Vista 2, se pidió desde el inicio una sola columna con las secciones apiladas.
Se pegó en el chat sin ninguna pantalla seleccionada:
```
Con el mismo estilo, paleta, tipografías, header y reglas que la Vista 1 y la Vista 2 (doble marco, píldoras flotantes, estructuralismo suave), crea una nueva pantalla llamada "Vista 3" con el título "Prompt mejorado". Usa una sola columna del mismo ancho que la Vista 2, con las secciones apiladas una debajo de otra y mucho espacio entre ellas. Ningún texto debe partirse en columnas angostas.

Orden de arriba a abajo:
1. Header flotante e indicador de pasos, con "3 · Mejorar" activo.
2. Título "Tu prompt mejorado" y una línea que dice "Mejorado con IA".
3. Una tarjeta de doble marco "Antes y después": primero una fila compacta "Original · 25/100" con el texto "dame un plan de estudio de Python", y debajo una fila "Mejorado · 100/100 · +75 puntos" con un prompt de 5 líneas (Contexto, Tarea, Restricciones, Formato de salida, Criterio de éxito) en JetBrains Mono, sobre fondo amarillo marcador (#FFE45C al 40%).
4. Una tarjeta "Qué cambió" con 4 viñetas, con texto a ancho completo.
5. Los botones, uno al lado del otro: "Copiar prompt mejorado" (píldora principal con círculo con flecha) y "Probar otro prompt" (borde fino).

Sin menús, enlaces, pie de página, estadísticas ni afirmaciones inventadas.
```

## Lecciones del diseño
- Una sola columna con secciones apiladas funciona mejor en Stitch que dos columnas con mucho texto.
- Pedir "usa solo lo descrito" evita menús y frases inventadas.
- Los textos de ejemplo de las pantallas (puntajes, sugerencias, prompt mejorado) son fijos en el diseño: al importar
  a código se reemplazan por los datos reales de la API.

## Ajustes útiles (frases cortas en el chat de Stitch)
- "Usa exactamente la misma paleta, tipografía y header que la pantalla 1."
- "Más espacio en blanco entre secciones."
- "Quita todo morado o índigo y usa solo la paleta indicada."
- "Quita cualquier menú, sección o texto que no esté en mi prompt."

Guarda aquí los prompts que realmente uses, si los cambias: la guía 22 pide que queden en este archivo.
