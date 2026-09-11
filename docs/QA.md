# QA.md — pruebas hechas y checklist móvil

Web verificada: https://ray86-dev.github.io/camisetas-interinos/ (11-09-2026, móvil 390-420 px y escritorio)

## 1. Pruebas automáticas del generador

```
python build.py --check
→ Fichas de producto: 24 (8 diseños × 3 productos)
→ Páginas generadas: 38
→ Avisos: 0
→ Validación OK
```

Qué comprueba `--check`:

- [x] Todas las páginas tienen `<title>`, meta description y `og:image`.
- [x] Ningún enlace interno roto (recorre los 38 HTML y valida cada `href`/`src`).
- [x] Ningún recurso inexistente (CSS, JS, SVG, PNG, JSON).
- [x] Ningún término prohibido aparece en la web (escudos, siglas sindicales, «Consejería de Educación»).
- [x] Ningún precio por debajo de su coste base; avisa si el margen baja de 5 €.
- [x] Aviso si un diseño supera 2 líneas de texto u 8 palabras.

## 2. URLs publicadas comprobadas una a una (todas 200)

| Página | Estado |
|---|---|
| Portada `/` | 200 |
| Catálogo `/catalogo/` | 200 |
| Ficha de producto (camiseta / tote / taza) | 200 (24 fichas) |
| Mi lista `/carrito/` | 200 |
| Cómo funciona `/como-funciona/` | 200 |
| FAQ `/faq/` | 200 |
| Contacto `/contacto/` | 200 |
| Seguimiento `/seguimiento/` | 200 |
| Aviso legal, Privacidad, Cookies, Condiciones, Envíos | 200 |
| Borrador `/_borrador/` (noindex, fuera del menú) | 200 |
| `robots.txt`, `sitemap.xml`, CSS, JS, JSON de seguimiento | 200 |

## 3. QA funcional

- [x] **Buscador de seguimiento**: con `DEMO-0000` + `demo@ejemplo.com` devuelve la línea de tiempo completa y el aviso «Te hemos enviado con **Correos Express**. Tracking: …» con enlace al portal de ese carrier (no dice Correos porque no es Correos).
- [x] La fila demo se marca en la web como **EJEMPLO DE PRUEBA — no es un pedido real**.
- [x] Caso negativo (número o email que no coinciden): mensaje claro, sin filtrar datos de otros pedidos.
- [x] `data/pedidos.json` no contiene direcciones ni importes: solo pedido, email, estado, carrier y tracking.
- [x] Banner de cookies: aparece, se puede rechazar la analítica y seguir navegando; la analítica solo se carga si se acepta **y** hay ID configurado (hoy está vacío, así que no se carga nada).
- [x] Navegación por teclado: enlace «Saltar al contenido», foco visible con contorno rojo, formularios con `<label>`.
- [x] Fichas en modo prelanzamiento: muestran «Avísame cuando esté» en lugar de un botón de compra falso.

## 4. QA móvil (390-420 px)

- [x] Cabecera compacta con botón **Menú** que despliega la navegación; en escritorio el menú desaparece y la barra se ve completa.
- [x] Tipografía grande legible sin zoom; h1 en dos líneas reales (`Sigo en` / `lista de espera`) con separación correcta en lectores de pantalla.
- [x] Formulario de seguimiento usable con el pulgar: campos de 44 px de alto mínimo y botón a ancho completo.
- [x] Tarjetas de producto en una columna, imágenes con proporción reservada (sin saltos de maquetación).
- [x] Banner de cookies apilado en vertical, texto completo y botones a ancho completo.
- [x] Sin desbordes horizontales ni texto cortado en: portada, catálogo, ficha, FAQ, legal y seguimiento.

## 5. Pendiente de probar (bloqueado por la cuenta, no por la web)

- [ ] Checkout real y emails de pedido: requieren crear la cuenta POD (`docs/ACTIVACION.md`, bloqueo 1).
- [ ] Precios finales y costes base por talla: confirmar en la cuenta antes de publicar precios definitivos.
- [ ] Muestra física del diseño 03 antes de anunciar en redes.
- [ ] GA4: sin ID configurado; la web publica igual y no bloquea el lanzamiento (era requisito del encargo).

## 6. Cómo repetir estas pruebas

```
python build.py --check
bash scripts/publish.sh
curl -s -o /dev/null -w "%{http_code}\n" https://ray86-dev.github.io/camisetas-interinos/seguimiento/
```
