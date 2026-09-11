# /designs — arte final

**Estado actual: los 8 diseños ya están compuestos** (los 7 archivos de cada carpeta) por
`scripts/disenos.py`, con tipografía real y geometría vectorial, y validados por `scripts/qa_disenos.py`.
El humano puede sustituir cualquiera de ellos por su versión de Gemini o Fooocus sobrescribiendo los
mismos archivos: ver `docs/ARTE.md`.

## Convención de nombres

    <nn-slug>/
      master.png              fuente maestra 4500×5400 px, 300 dpi, alfa, RGB
      print-area-camiseta.png área de impresión según plantilla del POD
      print-area-tote.png     área de impresión según plantilla del POD
      print-area-taza.png     2475×1155 px (envolvente)
      mockup-web.webp         1200 px de ancho para la web

Slugs exactos (deben coincidir con `data/disenos.json`):

    01-sigo-en-lista-de-espera
    02-mi-destino-es-un-pdf
    03-llamamiento-2359
    04-interino-es-un-cardio
    05-visto-a-las-347
    06-septiembre-y-la-incertidumbre
    07-funcionario-de-carrera-no
    08-claustro-cafe-y-9-dias

## Qué hacer cuando el arte exista

1. Coloca los PNG con esa estructura.
2. Crea los productos en la plataforma POD (camiseta, tote, taza) con cada `print-area-*.png`.
3. Copia la URL de compra de cada producto en el campo `checkout_url` del diseño correspondiente en `data/disenos.json`.
4. Cambia `"estado": "pendiente_arte"` por `"estado": "listo"` en ese diseño.
5. Ejecuta `python build.py --check` y republica con `./scripts/publish.sh`.

Con eso la ficha de producto pasa automáticamente de «Avísame cuando esté» a botón de compra real.

## Documentos de esta carpeta

- `BRIEF.md` — los 8 conceptos con texto exacto, paleta, estilo, negative prompt y «qué NO hacer».
- `PROMPTS_FOOOCUS.md` — prompts copy-paste, ajustes y flujo de trabajo.
- `PROMPTS_COMFYUI.md` — grafo mínimo descrito nodo a nodo y upscale.
- `PROMPTS_GEMINI.md` — instrucción maestra, prompts por diseño y exportación.
- `CHECKLIST_PRINT.md` — control de calidad antes de subir al POD.

## Reglas duras

- Nada de escudos, banderas como marca, logos de consejerías, centros o sindicatos, ni nombres de cargos.
- Nada de caras fotorrealistas.
- El texto de la frase se compone con tipografía real: no se acepta texto generado por IA con letras deformes.
- No se vende ningún diseño sin imprimible verificado y, para el diseño estrella, una muestra física vista.
