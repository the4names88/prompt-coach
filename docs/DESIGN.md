# Design System: Prompt Coach

Dirección visual de las 3 vistas. Se definió con ayuda de las skills `stitch-skill` y `soft-skill`
(taste-skill) y se adaptó a este producto: es una herramienta de uso diario, no una página de marketing,
así que se descartaron las reglas de héroes con fotos, menús a pantalla completa y animación constante.

## 1. Visual Theme & Atmosphere
Estructuralismo suave: superficies blancas que flotan sobre un fondo plata, con sombras largas y muy
difusas, esquinas muy redondeadas y mucho aire. Pocos elementos, cada uno bien trabajado. El hilo
conductor es el marcador: el texto del usuario se resalta como en una hoja corregida.
- Densidad 3 (aireada). Variación 6 (división editorial asimétrica). Movimiento 2 (solo respuesta a acciones).

## 2. Color Palette & Roles
- **Plata Verdosa** (#EEF1EC): fondo de la página.
- **Superficie** (#FFFFFF): núcleo de los contenedores.
- **Bandeja** (rgba(20,33,61,0.04)): marco exterior translúcido de los contenedores.
- **Tinta Marina** (#14213D): texto principal. No se usa negro puro.
- **Pizarra Suave** (#5B6577): texto secundario.
- **Verde Azulado Profundo** (#0F5C5A): único acento. Botón principal, paso activo y foco.
- **Marcador** (#FFE45C): solo para resaltar texto del prompt. Es un estado funcional, no decoración.
- **Rojo Lápiz** (#D64545) y **Verde Aprobado** (#1F9D6B): chequeos fallidos y aprobados, siempre con
  símbolo ✓ o ✕ y texto.

## 3. Typography Rules
- **Títulos:** Bricolage Grotesque, grande y de peso fuerte, espaciado ajustado (alternativa: Plus Jakarta Sans).
- **Texto:** Plus Jakarta Sans, interlineado 1.6, máximo 65 caracteres por línea.
- **Código:** JetBrains Mono, para el texto que escribe el usuario y el prompt mejorado.
- **Prohibido:** Inter, Roboto, Arial, tipografías serif.

## 4. Component Stylings
- **Doble marco:** todo contenedor importante lleva una bandeja exterior translúcida con borde fino y 6 px
  de relleno, y dentro un núcleo blanco con esquinas concéntricas (28 px afuera, 22 px adentro) y un brillo
  interior sutil. Sombras muy suaves, teñidas de verde, nunca grises duras.
- **Botón principal:** píldora completa en verde azulado con texto blanco y un pequeño círculo con flecha
  dentro del propio botón, a la derecha. Se hunde ligeramente al pulsar.
- **Botón secundario:** píldora con borde fino en tinta, sin relleno.
- **Área de texto:** núcleo blanco dentro de un doble marco, texto monoespaciado y contador a la derecha.
- **Indicador de pasos:** píldora flotante con 3 pasos; el activo va relleno en verde azulado.
- **Fila de chequeo:** símbolo ✓ o ✕, nombre del criterio y borde izquierdo de 3 px en verde o rojo.
- **Puntaje:** número grande dentro de un círculo con anillo de color según el rango. Sin degradados.
- **Prompt mejorado:** fragmentos resaltados con marcador al 60% dentro de un doble marco.
- **Iconos:** de línea ultrafina.
- **Errores:** mensaje en línea debajo del control, con qué pasó y cómo corregirlo.

## 5. Layout Principles
- Escritorio: división editorial. Columna izquierda (~55%) con título grande y la acción; columna derecha
  (~45%) con una tarjeta de apoyo.
- Header: píldora flotante separada del borde superior, nunca pegada.
- Móvil (menos de 768 px): una sola columna, sin scroll horizontal, botones de al menos 44 px.

## 6. Motion & Interaction
Sin animación decorativa. Solo foco, estado pulsado y la aparición del resultado tras una acción, con
curva suave. Se respeta `prefers-reduced-motion`.

## 7. Anti-Patterns (Prohibido)
- Morado, índigo, neón, degradados decorativos y brillos.
- Inter, negro puro (#000000), emojis, bordes grises duros de 1 px, sombras negras duras.
- Menús o enlaces a páginas que no existen, y pie de página con enlaces.
- Afirmaciones o cifras inventadas ("auditado por...", "líderes", porcentajes falsos).
- Secciones, plantillas o funciones que el prompt no pidió.
- Filas de 3 tarjetas iguales, nombres de relleno, lorem ipsum, imágenes.

## 8. Contrato con el código
Los ids y clases que necesita `static/app.js` están en `docs/GUIA-STITCH.md`, sección 4. Cualquier
rediseño debe conservarlos.

## 9. Valores finales de Stitch
(Completar al importar las pantallas: paleta, tipografías y componentes que Stitch realmente generó, y qué
se cambió respecto a este documento.)
