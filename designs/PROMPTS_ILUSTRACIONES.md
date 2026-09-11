# PROMPTS_ILUSTRACIONES.md — los personajes de los 8 diseños

Los 8 diseños llevan un **personaje ilustrado dentro de un círculo crema** y la frase debajo compuesta con
tipografía real. Aquí están los prompts exactos que se usaron para cada personaje, para poder regenerarlos,
pedir variantes o cambiarlos por otros.

## Reglas del estilo (van en todos los prompts)

- Ilustración **vectorial plana**, estilo pegatina: contorno grueso y uniforme, formas geométricas simples,
  ojos de punto, mofletes.
- Paleta limitada: crema, rojo ladrillo apagado, azul noche (y un toque de amarillo apagado cuando hace falta).
- El dibujo va **dentro de un círculo grande de color crema**. Todo lo que queda fuera del círculo es
  **negro puro**: así se recorta el círculo en un paso automático, sin halo ni bordes sucios.
- **Sin texto, sin letras, sin números, sin firmas ni marcas de agua.** La frase se compone aparte con
  tipografía de verdad; los modelos de imagen escriben mal y una letra torcida se ve a un metro en una camiseta.
- Tono: simpático e irónico, nunca caricatura de una persona real ni de un colectivo.

Plantilla para pedir uno nuevo:

    Flat vector cartoon illustration, sticker style, for a t-shirt print: [ESCENA].
    Thick uniform outlines, bold flat colors, minimal geometric shapes, simple dot eyes, rosy cheeks,
    limited palette: cream, muted brick red, dark navy. The drawing is inside a big flat cream coloured
    circle badge. Everything outside the circle is pure solid black. Centered composition.
    No text, no letters, no numbers, no watermark, no signature.

## Los 8 personajes

| # | Diseño | Escena del prompt |
|---|---|---|
| 01 | Sigo en lista de espera | Docente agotado tras una mesa llena de papeles, con el móvil en una mano y un café en la otra, una gota de sudor en la frente |
| 02 | Mi destino es un PDF | Un folio con la esquina doblada, carita triste y suplicante, alitas blancas y una flecha alejándose |
| 03 | Llamamiento 23:59 | Despertador de toda la vida con carita preocupada y ojos como platos, campanas sonando con líneas de movimiento y una gota de sudor |
| 04 | Interino: no es un estado, es un cardio | Corazón con dos tiritas, ojos cansados, sudando y con patitas corriendo |
| 05 | Visto a las 3:47 | Persona metida en la cama tapada con la manta, solo se le ven el pelo revuelto y dos ojos abiertos con ojeras, sujetando el móvil encendido que ilumina la escena; luna y estrellitas alrededor |
| 06 | Septiembre, yo y la incertidumbre | Docente con una mochila enorme y sonrisa preocupada, con una nube encima de la cabeza que contiene un signo de interrogación |
| 07 | ¿Funcionario de carrera? En esta vida no | Birrete de graduación con cara, guiñando un ojo y sacando la lengua, encima de un diploma enrollado con cinta y confeti alrededor |
| 08 | Claustro, café y un contrato de 9 días | Taza de café sonriente y dormilona con rizos de vapor, junto a un contrato enrollado con un clip y un lápiz |

## Cómo se integran en el diseño final

1. El personaje se guarda en `designs/_ilustraciones/<slug>.png` (1024×1024, fondo negro).
2. `scripts/disenos.py` recorta el círculo de forma **geométrica** (elipse sobre la caja del círculo crema,
   no por color: así no se pierde el contorno oscuro ni queda halo) y lo escala a 2700 px de diámetro.
3. Debajo se compone la frase con tipografía real, en dos líneas y con jerarquía (la línea corta sale más
   grande). Dos variantes de color: prenda oscura y producto claro.
4. Se genera todo lo que necesita el taller: maestras, áreas de impresión de camiseta/tote/taza y la vista
   previa de 1200 px para la web.

Para cambiar un personaje: sustituye su PNG en `designs/_ilustraciones/` y ejecuta

    python scripts/disenos.py --solo <slug>
    python scripts/qa_disenos.py
    python build.py --check && bash scripts/publish.sh

## Si prefieres hacerlo sin ilustración

    python scripts/disenos.py --estilo texto

Recompone los 8 diseños en versión solo tipográfica y geométrica (la anterior). La web coge lo último que
haya en `designs/<slug>/mockup-web.webp`.
