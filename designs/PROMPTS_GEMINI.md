# Prompts para Gemini (imagen) — arte de camiseta

Gemini es el más cómodo para iterar ideas rápido y para pedir variaciones de composición. Tiene dos limitaciones que debes conocer antes de empezar:

1. **La tipografía larga sigue siendo poco fiable.** Si el texto sale con una letra cambiada, no lo aceptes: rehazlo con tipografía real.
2. **El fondo transparente no siempre sale transparente.** Casi siempre devuelve un fondo plano de color. Trabájalo como ventaja: pide siempre fondo crema `#F4EFE6` o negro `#111111` y recórtalo después.

## Instrucción maestra (pégala al principio de cada prompt)

```
Genera una ilustración gráfica plana para estampar en una camiseta, con estos requisitos técnicos:
- Composición centrada, 5:6 vertical.
- Fondo PLANO de un solo color sin textura, sin sombras, sin degradados.
- Estilo: vector plano, alto contraste, bordes limpios, estética de serigrafía.
- Máximo 3 colores de la paleta: negro #111111, crema #F4EFE6, rojo apagado #B23A2E, azul noche #0E1B2A, amarillo volcán #E4C56B.
- Deja un espacio libre generoso en el centro para colocar después el texto con tipografía real.
- NO incluyas textos, letras, números ni firmas.
- NO incluyas escudos, banderas, sellos oficiales, logotipos ni símbolos de administraciones o sindicatos.
- NO incluyas caras humanas ni personas.
Al final, dime en dos líneas qué has dibujado y qué colores exactos has usado.
```

## Prompts por diseño (sustituyen a la parte gráfica; el texto se compone después)

**01 · Sigo en lista de espera**
```
Marco rectangular fino con esquinas rectas, estilo sello estampado con tinta ligeramente irregular, en rojo apagado #B23A2E sobre fondo negro #111111. Dentro, el centro vacío y limpio. Estética serigráfica, muy plano.
```

**02 · Mi destino es un PDF**
```
Icono geométrico plano de una página de documento con la esquina doblada, en crema #F4EFE6 con línea de acento amarillo #E4C56B sobre azul noche #0E1B2A. Nada de folios reales ni membretes. Centro vacío para el texto.
```

**03 · Llamamiento 23:59**
```
Display digital de siete segmentos, trazo grueso, segmentos rojo apagado #B23A2E sobre negro #111111 sin efecto de brillo difuso. Estilo reloj de mesita. Sin ninguna interfaz de móvil ni de aplicación. Centro inferior vacío.
```

**04 · Interino: no es un estado, es un cardio**
```
Un único trazo de subrayado hecho a mano alzada, textura de lápiz, color gris azulado #7A8B99 sobre crema #F4EFE6, en la parte central de la composición. Mucho espacio vacío arriba y abajo. Nada de dibujos anatómicos ni electrocardiogramas.
```

**05 · Visto a las 3:47**
```
Estampación de tampón de goma: rectángulo de esquinas redondeadas con silueta irregular por tinta desigual, azul noche #0E1B2A sobre crema #F4EFE6, centro vacío. Sin escudos, sin textos, sin números.
```

**06 · Septiembre, yo y la incertidumbre**
```
Tres bandas horizontales planas y de bordes duros: negro #111111, crema #F4EFE6 y terracota #C97B4A. Composición de cartel, sin textura, sin gente, sin aulas. Zona central amplia y limpia para tres líneas de texto.
```

**07 · ¿Funcionario de carrera? En esta vida no**
```
Dos formas abstractas grandes inspiradas en dos signos de interrogación enfrentados, planas, en negro #111111 y rojo apagado #B23A2E sobre crema #F4EFE6. Espacio central libre para tipografía. Sin otros símbolos.
```

**08 · Claustro, café y un contrato de 9 días**
```
Ticket de caja estilizado con tres líneas de viñetas vacías, cuadrícula monoespaciada, azul noche #0E1B2A y crema #F4EFE6 con acento amarillo #E4C56B. Fondo plano, sin logotipos ni marcas. Espacio para dos líneas de texto abajo.
```

## Iteración

- Si sale con texto o con símbolos prohibidos: `Rehazlo sin ningún texto y sin ningún símbolo institucional.`
- Si sale con fondo degradado: `Fondo plano de un único color, sin degradado ni textura.`
- Si sale con demasiado detalle: `Simplifica: menos elementos, más espacio vacío, estética de serigrafía plana.`
- Pide siempre **dos variantes** y quédate con la que deje más hueco para el texto.

## Exportar y guardar

1. Descarga la imagen en la mayor resolución disponible.
2. Recorta el fondo en GIMP / Photopea / Inkscape. Revisa el borde al 400 %: sin halo blanco.
3. Monta el texto exacto del BRIEF con tipografía real (Inter Black, Archivo Black, Anton, Barlow Condensed Bold). 2 líneas máximo, caja alta.
4. Exporta a la nomenclatura de `designs/BRIEF.md`:

```
/designs/01-sigo-en-lista-de-espera/master.png                 (4500×5400, 300 dpi, alfa)
/designs/01-sigo-en-lista-de-espera/print-area-camiseta.png
/designs/01-sigo-en-lista-de-espera/print-area-tote.png
/designs/01-sigo-en-lista-de-espera/print-area-taza.png
/designs/01-sigo-en-lista-de-espera/mockup-web.webp            (1200 px)
```

5. Pasa `designs/CHECKLIST_PRINT.md`. Si algo no cuadra, se corrige antes de subir al POD: imprimir es irreversible.
