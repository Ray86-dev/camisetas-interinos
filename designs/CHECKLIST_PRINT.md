# Checklist de impresión — antes de subir cualquier diseño al POD

Se revisa **mirando el archivo final a tamaño de impresión**, no al 100 % en pantalla. Un diseño que falla cualquiera de estos puntos no se sube.

## 1. Contraste y legibilidad

- [ ] Contraste texto/fondo ≥ **4,5:1** (mínimo WCAG AA). Para texto fino o de menos de 5 mm, exigir **7:1**.
- [ ] El texto se lee a **50 cm** de distancia sobre una camiseta puesta (pruébalo de verdad, con la camiseta puesta).
- [ ] Comprobado con medidor de color, no a ojo. Herramienta: cualquier contrast checker con los hex reales.
- [ ] Si el texto va en blanco sobre negro, no hay bordes grisáceos ni transparencias al 80 % (en DTG se ven sucios).

## 2. Márgenes y tamaño de texto

- [ ] Margen mínimo **3 mm** entre cualquier elemento y el borde del área de impresión. En camiseta, mejor 15-20 mm: el estampado no llega al borde de la prenda.
- [ ] Ningún texto con altura de letra (mayúscula) inferior a **5 mm** en el tamaño real de impresión.
- [ ] Nada importante en los 20 mm superiores de la taza (se pierde por la curvatura y el borde) ni pegado al asa.
- [ ] Trazos de línea fina ≥ **1 mm** de grosor real (por debajo desaparecen o salen punteados).

## 3. Color

- [ ] Paleta CMYK-safe: nada de **neón imposible** (`#00FF00`, `#FF00FF`, verdes fluorescentes, azules eléctricos saturados). En tinta no existen y el resultado decepciona.
- [ ] Sin degradados sucios ni transiciones largas a negro: se convierten en manchas y bandas.
- [ ] Colores planos y sólidos; si hay transparencias, ya están **aplanadas** (flatten) con el resultado final visible.
- [ ] Sobre prenda oscura: el diseño lleva **base blanca** donde haga falta o los colores oscuros desaparecerán. Validado con el POD.
- [ ] Coincide con la paleta de marca declarada en `designs/BRIEF.md`.

## 4. Técnica del archivo

- [ ] **300 dpi** al tamaño real de impresión (no "300 dpi" de un archivo de 500 px).
- [ ] Master **4500×5400 px** con fondo transparente (alfa real, sin fondo blanco embebido).
- [ ] PNG con área de impresión según plantilla del POD elegido (si la plantilla difiere de nuestras medidas, manda la del POD).
- [ ] Sin metadatos ni marcas de agua (ni del generador de imágenes, ni firmas).
- [ ] Texto **nítido**, sin interpolación: si la frase venía de una imagen generada, se ha recomposed con tipografía real.
- [ ] Sin halo blanco en los bordes recortados (revisado al 400 % de zoom con fondo oscuro).

## 5. Cumplimiento de marca

- [ ] Cero escudos, banderas como marca, logos de consejerías, centros o sindicatos, ni nombres de cargos o personas.
- [ ] Cero parecidos razonables con papelería o sellos oficiales.
- [ ] Texto en español de España, con «¿» y «¡» cuando correspondan.
- [ ] Máximo 2 líneas (la excepción del diseño 04 está justificada en el BRIEF).
- [ ] No se usa tipografía que imite la de un organismo público.

## 6. Prueba final antes de publicar

- [ ] Pedir **una muestra física** del diseño estrella (o el pack de muestras del POD) antes de anunciar la tienda en redes.
- [ ] Verificar en la muestra: encaje del estampado, tacto, lavado a 30 °C del revés sin secadora.
- [ ] Solo entonces se marca el diseño como `"estado": "listo"` en `data/disenos.json` y se pega su URL de compra en `checkout_url`.

Nota operativa: en `data/disenos.json` los 8 diseños están como `pendiente_arte` y la tienda se publica en modo prelanzamiento. El cambio a `listo` habilita la compra en la ficha de producto (el generador `build.py` lo detecta solo).
