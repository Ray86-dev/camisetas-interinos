# Grafo mínimo para ComfyUI — arte de camiseta print-ready

Objetivo: obtener un PNG grande, limpio y con fondo transparente (o fondo plano fácil de recortar) sobre el que componer la tipografía exacta del BRIEF.

## Grafo mínimo (SDXL)

| # | Nodo | Parámetros clave |
|---|---|---|
| 1 | `CheckpointLoaderSimple` | `sd_xl_base_1.0.safetensors` o un SDXL ilustrado tipo Juggernaut XL / RealVisXL. Un solo checkpoint: no hace falta refiner si usas SDXL turbo/lightning (entonces baja steps a 6-8 y cfg a 1.5) |
| 2 | `CLIPTextEncode` (positivo) | Prompt del diseño (abajo) |
| 3 | `CLIPTextEncode` (negativo) | Negativo común de `PROMPTS_FOOOCUS.md` |
| 4 | `EmptyLatentImage` | 1024×1024 (o 1152×896 para composición horizontal), batch 4-8 |
| 5 | `KSampler` | sampler `dpmpp_2m`, scheduler `karras`, steps 30, cfg 7, denoise 1.0, seed fija cuando aciertas |
| 6 | `VAEDecode` | — |
| 7 | `SaveImage` | prefijo `ll2359/<slug>_` |

Conexiones: 1→2, 1→3 (CLIP), 1→5 (MODEL), 4→5 (LATENT), 5→6 (LATENT), 1→6 (VAE), 6→7 (IMAGE).

## Upscale (obligatorio para imprimir)

Dos opciones, en orden de calidad:

1. **Ultimate SD Upscale**: `LoadImage` → `Upscale Image (using Model)` con `4x-UltraSharp.pth` → `UltimateSDUpscale` (tile 1024, denoise 0.2, steps 20, seed fija) → `SaveImage`. Resultado: detalle sin inventar cosas raras.
2. **Sencilla**: `ImageUpscaleWithModel` (4x-UltraSharp) → `ImageScale` a 1800 px de ancho → reescalado final a 4500×5400 en Photoshop/GIMP con remuestreo bicúbico suave.

## Fondo transparente

ComfyUI puede sacar máscara con `SAM` o `RMBG` (`Image Remove Background (RMBG)` si tienes el nodo instalado). Si no:

1. Genera sobre fondo **plano** (crema `#F4EFE6` o negro `#111111`, según el diseño: en el prompt pide `solid flat background, no texture, no shadow`).
2. Recorta en GIMP con *Selección por color* + *Crecer 1 px* + *Suavizar borde*.
3. Exporta PNG con alfa y revisa a 400 % que no quede halo ni flecos.

## El texto: componerlo a mano (no lo generes)

Los checkpoints SDXL escriben mal las frases largas, y en merch un error de una letra se ve a un metro de distancia. Flujo correcto:

1. Genera solo la parte gráfica (marco, icono, fondo) con el negativo común, que **excluye texto**.
2. Exporta a 300 dpi.
3. Compón el texto exacto del BRIEF en Inkscape (SVG, escalable) con una tipografía tipo Inter Black, Archivo Black, Anton o Barlow Condensed Bold. Caja alta, máximo 2 líneas.
4. Vectoriza o rasteriza a 4500×5400 px y exporta el PNG final.
5. Pasa `designs/CHECKLIST_PRINT.md` antes de subirlo al POD.

## Nodos que NO merecen la pena aquí

- `ControlNet` de pose/depth: no aporta a un diseño tipográfico plano.
- `FaceDetailer`, `IPAdapter` con caras: el BRIEF prohíbe caras fotorrealistas.
- Cualquier nodo de "text rendering": da resultados peores que componer el texto con tipografía real.

## Prompts positivos por diseño

Usa exactamente los del apartado «Variantes por diseño» de `PROMPTS_FOOOCUS.md`: son válidos tanto en Fooocus como en ComfyUI (mismo CLIP, mismo negativo).
