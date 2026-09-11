# BRIEF de diseño — Llamamiento 23:59

Marca: **Llamamiento 23:59** · 8 diseños × 3 productos (camiseta unisex, tote, taza)
Arte final: **lo produce el humano** con Fooocus / ComfyUI / Gemini. Aquí solo se define qué pedir.

## Reglas de marca (aplican a los 8 diseños)

- Humor de tribu docente. Ironía compartida, nunca burla de una persona concreta ni denuncia con nombres.
- **Prohibido**: escudos, banderas oficiales usadas como marca, logos de la Consejería, de centros, de sindicatos, nombres de cargos o de personas reales, tipografías institucionales.
- Nada de caras fotorrealistas: no queremos parecidos con nadie.
- Estilo común: **tipografía bold plana** sobre fondo limpio, alto contraste, 2 líneas máximo (excepción justificada: diseño 04).
- Paleta volcán/atlántico: negro `#111111`, crema `#F4EFE6`, rojo apagado `#B23A2E`, azul noche `#0E1B2A`, azul atlántico `#8FB8DE`, amarillo volcán `#E4C56B`.
- Español de España. Se mantienen los signos de apertura «¿» y «¡» cuando correspondan: son parte del diseño.
- No incluir marcos que se puedan leer como papelería oficial.

## Entrega por diseño (convención de carpetas)

    /designs/<nn-slug>/
      master.png              4500×5400 px, 300 dpi, fondo transparente, RGB
      print-area-camiseta.png según plantilla POD (≈3000×3600 px)
      print-area-tote.png     según plantilla POD (≈2952×3542 px)
      print-area-taza.png     2475×1155 px (área envolvente)
      mockup-web.webp         1200 px de ancho, para la web

La plantilla exacta la publica el POD al crear el producto: si difiere de estas medidas, **manda la del POD**. Las medidas de arriba son las nuestras de partida.

## Los 8 conceptos

### 01 · Sigo en lista de espera
- **Texto exacto (2 líneas, 5 palabras)**: `SIGO EN LISTA` / `DE ESPERA`
- **Paleta**: negro #111111, crema #F4EFE6, rojo #B23A2E
- **Estilo**: tipografía bold condensada, caja alta, componer como sello administrativo ironizado (marco fino de esquinas rectas, sin institucionalidad). El chiste está en el formato, no en el dibujo.
- **Negative prompt**: emblemas, escudos, sellos oficiales, membretes, banderas, texto pequeño ilegible, degradados sucios, relieve 3D, sombras duras
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: no usar tipografía de papelería oficial, no añadir números de registro ni códigos, no meter una bandera de Canarias.

### 02 · Mi destino es un PDF
- **Texto exacto (2 líneas, 5 palabras)**: `MI DESTINO` / `ES UN PDF`
- **Paleta**: azul noche #0E1B2A, crema #F4EFE6, amarillo #E4C56B
- **Estilo**: tipografía bold, guiño a un icono genérico de documento (rectángulo con esquina doblada). Icono plano, geométrico, sin textura de papel.
- **Negative prompt**: folios con membrete, logos de administraciones, fotorealismo, texturas de papel arrugado, manuscritos ilegibles
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: nada que parezca un documento oficial real; sin nombres de organismos ni escudos.

### 03 · Llamamiento 23:59 (diseño de marca)
- **Texto exacto (2 líneas, 2 palabras + hora)**: `LLAMAMIENTO` / `23:59`
- **Paleta**: negro #111111, crema #F4EFE6, rojo #B23A2E
- **Estilo**: display de reloj digital de 7 segmentos, trazo grueso, alto contraste. Es la pieza que identifica la marca: se usará también en redes.
- **Negative prompt**: pantallazos de móviles reales con interfaces de marcas, iconos de sistemas operativos, notificaciones con logos, sombras realistas
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: no reproducir la interfaz de ninguna app real (ni de mensajería ni de portales administrativos).

### 04 · Interino: no es un estado, es un cardio
- **Texto exacto (2 líneas, 8 palabras)**: `INTERINO: NO ES UN ESTADO,` / `ES UN CARDIO`
- **Paleta**: negro #111111, crema #F4EFE6, gris azulado #7A8B99
- **Estilo**: bloque editorial, dos pesos de tipografía, subrayado hecho a mano alzada digital. Sin gráficos médicos literales.
- **Negative prompt**: electrocardiogramas detallados, corazones anatómicos, pictogramas médicos, ambulancias
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: no convertirlo en un cartel sanitario. La gracia es la frase, no un dibujo de corazón.

### 05 · Visto a las 3:47
- **Texto exacto (2 líneas, 4 palabras)**: `VISTO` / `A LAS 3:47`
- **Paleta**: azul noche #0E1B2A, crema #F4EFE6, azul atlántico #8FB8DE
- **Estilo**: sello de hora con estética de tampón, tipografía monoespaciada, tinta ligeramente irregular (no perfecta).
- **Negative prompt**: sellos oficiales con escudo, referencias a organismos, caras, relojes realistas
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: **aquí se cambió el texto propuesto a propósito**: el original mencionaba a la Consejería. Se elimina toda referencia institucional y se conserva el chiste de la hora intempestiva. No reintroducir menciones a organismos.

### 06 · Septiembre, yo y la incertidumbre
- **Texto exacto (2 líneas, 6 palabras)**: `SEPTIEMBRE, YO` / `Y LA INCERTIDUMBRE`
- **Paleta**: negro #111111, crema #F4EFE6, terracota #C97B4A
- **Estilo**: cartel de temporada, tres pesos tipográficos, «incertidumbre» en rojo apagado. Jerarquía clara: lo importante es la última palabra.
- **Negative prompt**: fotos de aulas reales, pizarras con texto inventado, calendarios oficiales, dibujos infantiles
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: nada de folios de calendario escolar con logos; sin emojis.

### 07 · ¿Funcionario de carrera? En esta vida no
- **Texto exacto (2 líneas, 7 palabras)**: `¿FUNCIONARIO DE CARRERA?` / `EN ESTA VIDA NO`
- **Paleta**: negro #111111, crema #F4EFE6, rojo #B23A2E
- **Estilo**: pregunta en bold, respuesta en caja baja, broma tipográfica. Los signos «¿» forman parte del diseño.
- **Negative prompt**: sellos de oposición aprobada, banderas, escudos, corbatas, fotos de funcionarios
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: no ridiculizar a quien sí aprueba. Es humor propio, no burla ajena.

### 08 · Claustro, café y un contrato de 9 días
- **Texto exacto (2 líneas, 8 palabras)**: `CLAUSTRO, CAFÉ` / `Y UN CONTRATO DE 9 DÍAS`
- **Paleta**: azul noche #0E1B2A, crema #F4EFE6, amarillo #E4C56B
- **Estilo**: lista de tres elementos con viñetas, estética de recibo de cafetería. Tipografía monoespaciada para los números.
- **Negative prompt**: nombres de centros educativos, logotipos, tazas de marcas reales, personas identificables
- **Tamaño**: master 4500×5400 px
- **Qué NO hacer**: no nombrar ni insinuar centros concretos ni usar la estética de un documento contractual real.

## Cómo se valida un diseño antes de subirlo

1. `designs/CHECKLIST_PRINT.md` en mano, mirando el archivo real a tamaño de impresión (no al 100 % en pantalla).
2. Contraste de texto comprobado con un medidor de color, no «a ojo».
3. El texto se lee a 50 cm de distancia sobre una camiseta puesta.
4. Si va a taza: tiene en cuenta que la curvatura no permite texto cerca del asa ni pegado al borde superior.
5. Nada del diseño puede leerse como símbolo oficial. Ante la duda: fuera.
