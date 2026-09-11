# Llamamiento 23:59 — merchandising para docentes interinos de Canarias

Tienda online de merchandising humorístico para interinos docentes (Primaria y Secundaria) de Canarias.
Print on demand, sin stock propio. Precios en EUR. Idioma es-ES.

- Web publicada (pre-lanzamiento): https://ray86-dev.github.io/camisetas-interinos/
- Documentación operativa: `docs/TIENDA.md` (empieza por ahí)
- DNS del dominio: `docs/DNS.md`
- Manual de incidencias de pedido: `docs/RUNBOOK_PEDIDO.md`
- Qué falta para vender de verdad (15 min del humano): `docs/ACTIVACION.md`

## Estructura

    data/          Datos de la tienda (catálogo, diseños, productos, pedidos, carriers)
    content/       Textos de páginas y publicaciones de redes
    legal/         Textos legales y de envíos/devoluciones (fragmentos HTML reales)
    templates/     Plantillas HTML del generador
    static/        CSS, JS e imágenes de la tienda
    designs/       BRIEF y prompts para Fooocus / ComfyUI / Gemini + arte del humano
    docs/          Decisiones, DNS, runbook, activación, QA
    dist/          Salida generada (lo que se publica). No editar a mano.

## Uso

    python build.py          # genera dist/
    python build.py --check  # genera y valida enlaces, meta y precios

Publicar (GitHub Pages):

    ./scripts/publish.sh     # genera dist/ y lo empuja a la rama gh-pages

## Estado

Fase 1 (esta noche): tienda publicada, catálogo de 8 diseños × 3 productos listo,
checkout delegado en la plataforma POD (pendiente de activar la cuenta: ver `docs/ACTIVACION.md`).
Fase 2: subir los PNG de `designs/`, crear los 24 productos en el POD y pegar las URLs
de compra en `data/disenos.json` (campo `checkout_url`).
