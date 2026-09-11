# Prompts para Fooocus — arte de camiseta print-ready

Fooocus está pensado para hacer la **imagen**, no el texto. Regla de oro: **la tipografía final se compone a mano** (Inkscape, GIMP, Affinity, Canva, Illustrator). Fooocus sirve para generar el fondo, el icono o el tratamiento gráfico; el texto exacto del BRIEF se añade después con una tipografía real. Los modelos de imagen siguen escribiendo mal frases largas, y una letra mal escrita en una camiseta es un producto defectuoso.

## Ajustes comunes (Presets / Advanced)

- Rendimiento: **Quality**
- Relación de aspecto: **1:1** para iconos y para trabajar cómodo; recorta luego a 5:6 (4500×5400 px en el master final)
- Estilos activables: **Fooocus V2** desactivado, **Sai Enhancer** activado, **MRE Spontaneous** desactivado
- Image Number: 6–8 por tanda y elegir una
- Sharpness: 2 · Guidance Scale: 4–6 · Seed: fija cuando des con la buena

## Negativo común (pégalo en las 8 tandas)

```
watermark, signature, logo, escudo, coat of arms, flag, official seal, government emblem, text, letters, typography, gibberish text, blurry, jpeg artifacts, low contrast, muddy gradients, neon colors, neon green, fluorescent, photorealistic face, human face, hands, 3d render, bevel effect, drop shadow, paper texture, dirt, dust, noise, frame border like letterhead, halftone dots, small unreadable details
```

## Positivo común (base, se ajusta por diseño)

```
flat vector graphic design for screen printed apparel, bold geometric shapes, high contrast two tone composition, limited palette of black cream and muted red, clean edges, crisp lines, centered composition, large empty negative space for typography, minimalist poster style, print ready
```

## Variantes por diseño (pega y cambia solo la parte de estilo)

**01 · Sigo en lista de espera**
```
flat vector badge design for t-shirt, thin rectangular stamp frame, muted red ink on black, minimal geometric, centered, large empty space in the middle for two lines of bold uppercase text, screen print aesthetic, high contrast, clean edges, no text
```

**02 · Mi destino es un PDF**
```
flat vector icon of a generic document page with folded corner, geometric, night blue and cream, thin accent outline in muted yellow, centered, generous negative space for typography, screen print aesthetic, no text
```

**03 · Llamamiento 23:59**
```
flat vector illustration of a digital seven segment clock display, thick segments, black background, muted red glowing segments without glow blur, retro alarm clock display, centered, large empty area for text below, screen print aesthetic, no text, no phone interface
```

**04 · Interino: no es un estado, es un cardio**
```
subtle hand drawn underline stroke sweeping under an empty area, graphite texture, single stroke, muted grey blue on cream, editorial minimal background, lots of negative space, screen print aesthetic, no text, no anatomical drawing
```

**05 · Visto a las 3:47**
```
flat vector rubber stamp impression, rounded rectangle outline, slightly irregular silhouette as if inked unevenly, night blue on cream, monospaced industrial feel, centered, empty middle for text, screen print aesthetic, no text, no coat of arms
```

**06 · Septiembre, yo y la incertidumbre**
```
poster style background for apparel, three stacked horizontal bands of black cream and terracotta, flat, hard edges, big negative space to place three lines of type, screen print aesthetic, no text, no people, no classroom
```

**07 · ¿Funcionario de carrera? En esta vida no**
```
minimal flat composition of two large question marks mirrored as abstract shapes, bold, black and muted red on cream, negative space in the middle for typography, screen print aesthetic, no text other than abstract question mark shapes
```

**08 · Claustro, café y un contrato de 9 días**
```
flat vector receipt paper with three bullet lines as empty placeholders, monospaced grid feeling, night blue and cream with muted yellow accent, centered, generous negative space for typography, screen print aesthetic, no text, no brand logos
```

## Flujo de trabajo recomendado en Fooocus

1. Genera 6-8 variantes con el prompt del diseño.
2. Elige la que tenga **más espacio limpio** para el texto (el arte tiene que dejar respirar la tipografía).
3. Upscale en Fooocus (Upscale 2x) y exporta PNG.
4. Quita el fondo (Fooocus no exporta alfa): en GIMP/Inkscape/Photopea con selección por color, o RemBG. Comprueba el borde a 400 % de zoom: sin halo blanco.
5. Compón el texto exacto del BRIEF con tipografía real: caja alta, 2 líneas, sin efectos 3D.
6. Recorta al tamaño de la plantilla del POD y guarda con la nomenclatura de `designs/BRIEF.md`.

## Errores que arruinan una camiseta (revisa antes de subir)

- Texto generado por IA con letras deformes o inventadas: **si aparece texto generado, descártalo**.
- Fondos con degradado sucio sobre negro: en DTG se convierte en una mancha.
- Colores neón imposibles en tinta: el CMYK no los reproduce igual que la pantalla.
- Detalles finos menores de 1 mm: desaparecen al estampar.
- Diseños con escudos, banderas o cualquier cosa que parezca un símbolo oficial.
