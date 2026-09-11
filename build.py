#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generador estático de la tienda «Llamamiento 23:59».

Uso:
    python build.py            # genera dist/
    python build.py --check    # genera y valida (enlaces, meta, precios, palabras prohibidas)

Sin dependencias externas: solo la librería estándar.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
FUENTES = ["static", "legal"]

# Palabras que NO pueden aparecer como marca/mención institucional en la tienda.
PROHIBIDAS = [
    "Consejería de Educación",
    "Escudo de Canarias",
    "STEC",
    "ANPE",
    "CCOO",
    "UGT",
    "CSIF",
]

errores: list[str] = []
avisos: list[str] = []


# --------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------
def leer_json(ruta: Path):
    with ruta.open(encoding="utf-8") as fh:
        return json.load(fh)


def eur(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def esc(texto: str) -> str:
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def escribe(ruta_rel: str, contenido: str) -> None:
    destino = DIST / ruta_rel
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")


def fecha_hoy() -> str:
    return date.today().isoformat()


# --------------------------------------------------------------------------
# carga de datos
# --------------------------------------------------------------------------
SITE = leer_json(ROOT / "data" / "site.json")
DISENOS = leer_json(ROOT / "data" / "disenos.json")
PRODUCTOS = leer_json(ROOT / "data" / "productos.json")
CARRIERS = leer_json(ROOT / "data" / "carriers.json")
PLACEHOLDERS = leer_json(ROOT / "data" / "placeholders.borrador.json")

BASE = SITE.get("base_path") or re.sub(r"^https?://[^/]+", "", SITE["url_publicada"]).rstrip("/")
BASE = "" if BASE == "/" else BASE

MARCA = SITE["marca"]
EMAIL = SITE["email_contacto"]
DOMINIO = SITE["dominio_previsto"]
CHECKOUT_ACTIVO = bool(SITE.get("checkout_activo"))
URL_TIENDA = SITE.get("url_tienda_pod") or ""
CANARIAS = SITE["plazos"]["canarias"]
PENINSULA = SITE["plazos"]["peninsula"]
REPO_ISSUES = "https://github.com/ray86-dev/camisetas-interinos/issues"


def ruta(url: str) -> str:
    """Convierte una ruta interna ('/catalogo/') en URL usable."""
    return f"{BASE}{url}"


def mailto(asunto: str, cuerpo: str = "") -> str:
    from urllib.parse import quote

    return f"mailto:{EMAIL}?subject={quote(asunto)}&body={quote(cuerpo)}"


def producto_id(d: dict, p: dict) -> str:
    return f"{p['id']}-{d['slug']}"


def crear_matriz() -> list[dict]:
    """8 diseños × 3 productos = 24 fichas de producto."""
    fichas = []
    for d in DISENOS:
        for p in PRODUCTOS:
            disponible = d.get("estado") == "listo" and CHECKOUT_ACTIVO
            fichas.append(
                {
                    "id": producto_id(d, p),
                    "diseno": d,
                    "producto": p,
                    "titulo": f"{p['nombre']} · {d['titulo']}",
                    "precio": float(p["precio_eur"]),
                    "coste_base": float(p["coste_base_eur_ref"]),
                    "margen": round(float(p["precio_eur"]) - float(p["coste_base_eur_ref"]), 2),
                    "disponible": disponible,
                    "checkout_url": d.get("checkout_url") or URL_TIENDA,
                    "url": f"/producto/{producto_id(d, p)}/",
                }
            )
    return fichas


FICHAS = crear_matriz()


# --------------------------------------------------------------------------
# plantilla base
# --------------------------------------------------------------------------
NAV = [
    ("/", "Inicio"),
    ("/catalogo/", "Catálogo"),
    ("/como-funciona/", "Cómo funciona"),
    ("/envios/", "Envíos y devoluciones"),
    ("/faq/", "FAQ"),
    ("/seguimiento/", "Seguimiento"),
    ("/contacto/", "Contacto"),
]

FOOTER_LEGAL = [
    ("/aviso-legal/", "Aviso legal"),
    ("/privacidad/", "Privacidad"),
    ("/cookies/", "Cookies"),
    ("/condiciones/", "Condiciones de compra"),
    ("/envios/", "Envíos y devoluciones"),
    ("/seguimiento/", "Seguimiento de pedido"),
]


def layout(titulo: str, descripcion: str, ruta_actual: str, cuerpo: str, noindex: bool = False, extra: str = "") -> str:
    nav = "".join(
        '<li><a href="{u}"{c}>{t}</a></li>'.format(
            u=ruta(u) or "/",
            t=esc(t),
            c=' aria-current="page"' if u == ruta_actual else "",
        )
        for u, t in NAV
    )
    legal = "".join(
        f'<li><a href="{ruta(u)}">{esc(t)}</a></li>' for u, t in FOOTER_LEGAL
    )
    canonical = f'<link rel="canonical" href="{"https://" + DOMINIO + ruta_actual if DOMINIO != "PENDIENTE-CONFIRMAR" else ruta(ruta_actual)}">'
    og_url = f'https://{DOMINIO}{ruta_actual}' if DOMINIO != "PENDIENTE-CONFIRMAR" else ruta(ruta_actual)
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else '<meta name="robots" content="index,follow">'
    ga = SITE["analytics"].get("ga_measurement_id") or ""

    return f"""<!DOCTYPE html>
<html lang="es-ES" data-base="{BASE}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
{robots}
{canonical}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(MARCA)}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{ruta('/assets/img/og.png')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#111111">
<link rel="icon" href="{ruta('/assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{ruta('/assets/css/style.css')}">
{extra}
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{ruta('/') or '/'}"><span class="reloj">23:59</span> {esc(MARCA)}</a>
    <input type="checkbox" id="menu-abierto" class="menu-check" aria-label="Abrir o cerrar el menú">
    <label class="menu-btn" for="menu-abierto">Menú</label>
    <nav aria-label="Principal">
      <ul class="nav">
        {nav}
        <li><a class="carrito-link" href="{ruta('/carrito/')}" data-count="0">Mi lista</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="contenido">
{cuerpo}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="grid grid-3">
      <div>
        <h4>{esc(MARCA)}</h4>
        <p>{esc(SITE['lema'])}. Merch impreso bajo demanda para docentes interinos de Canarias. Sin stock, sin tiendas intermediarias y sin fingir que somos otra cosa.</p>
      </div>
      <div>
        <h4>Tienda</h4>
        <ul>
          <li><a href="{ruta('/catalogo/')}">Catálogo</a></li>
          <li><a href="{ruta('/como-funciona/')}">Cómo funciona</a></li>
          <li><a href="{ruta('/envios/')}">Envíos y devoluciones</a></li>
          <li><a href="{ruta('/faq/')}">Preguntas frecuentes</a></li>
          <li><a href="{ruta('/seguimiento/')}">Seguimiento de pedido</a></li>
          <li><a href="{ruta('/contacto/')}">Contacto</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>{legal}</ul>
      </div>
    </div>
    <p class="small">Precios en euros con impuestos incluidos. Envíos a Canarias y a la península. Impresión bajo demanda en talleres de España y de la Unión Europea.</p>
    <p class="small">Titular: {esc(SITE['responsable']['nombre'])} · NIF {esc(SITE['responsable']['nif'])} · {esc(SITE['responsable']['direccion'])} · Contacto: {esc(EMAIL)}</p>
    <p class="small">© {date.today().year} {esc(MARCA)}. Los diseños son humor de tribu docente: ninguna referencia a organismos, escudos ni sindicatos.</p>
  </div>
</footer>
<div id="cookies" data-ga="{esc(ga)}" role="dialog" aria-live="polite" aria-label="Aviso de cookies">
  <p>Usamos solo cookies técnicas necesarias para que la tienda funcione. Si aceptas, activamos además analítica anónima para saber qué diseños interesan. Puedes rechazarla y seguir comprando igual.</p>
  <div class="acciones">
    <button class="btn" data-cookie="todo">Aceptar</button>
    <button class="btn btn-2" data-cookie="tecnica">Solo técnicas</button>
  </div>
</div>
<script src="{ruta('/assets/js/app.js')}" defer></script>
</body>
</html>
"""


def aviso_lanzamiento() -> str:
    if CHECKOUT_ACTIVO:
        return ""
    return f"""<div class="wrap"><div class="aviso aviso-amarillo">
  <p><strong>Tienda en prelanzamiento.</strong> Los 8 diseños están definidos y el catálogo cerrado,
  pero <strong>todavía no hemos subido los imprimibles</strong>: no vamos a vender una camiseta sin arte.
  Déjanos tu email en cualquier ficha y te avisamos el día que se pueda comprar de verdad.</p>
</div></div>"""


# --------------------------------------------------------------------------
# imágenes placeholder (SVG etiquetado: nunca simulamos un mockup real)
# --------------------------------------------------------------------------
def svg_placeholder(ficha: dict) -> str:
    d, p = ficha["diseno"], ficha["producto"]
    lineas = d["texto_camiseta"].split("\n")
    textos = "".join(
        f'<tspan x="60" dy="{0 if i == 0 else 68}">{esc(l)}</tspan>' for i, l in enumerate(lineas)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" role="img" aria-label="Placeholder de {esc(p['nombre'])} para el diseño {esc(d['titulo'])}">
<rect width="800" height="1000" fill="#F4EFE6"/>
<rect x="20" y="20" width="760" height="960" fill="none" stroke="#111111" stroke-width="3"/>
<text x="60" y="110" font-family="ui-monospace, monospace" font-size="26" fill="#B23A2E">{esc(p['nombre'].upper())}</text>
<text x="60" y="150" font-family="ui-monospace, monospace" font-size="20" fill="#5A5A5A">diseño {d['numero']:02d} · {esc(d['slug'])}</text>
<text x="60" y="330" font-family="system-ui, sans-serif" font-size="58" font-weight="800" fill="#111111">{textos}</text>
<text x="60" y="700" font-family="ui-monospace, monospace" font-size="22" fill="#0E1B2A">ILUSTRACIÓN PLACEHOLDER</text>
<text x="60" y="740" font-family="system-ui, sans-serif" font-size="22" fill="#111111">El mockup real lo genera la plataforma POD</text>
<text x="60" y="772" font-family="system-ui, sans-serif" font-size="22" fill="#111111">cuando el imprimible exista en /designs.</text>
<text x="60" y="860" font-family="ui-monospace, monospace" font-size="20" fill="#5A5A5A">plantilla: {esc(p['plantilla'])}</text>
<text x="60" y="900" font-family="ui-monospace, monospace" font-size="20" fill="#5A5A5A">precio previsto: {eur(ficha['precio'])}</text>
</svg>
"""


def svg_og() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#0E1B2A"/>
<text x="70" y="150" font-family="ui-monospace, monospace" font-size="34" fill="#E4C56B">LLAMAMIENTO</text>
<text x="70" y="300" font-family="system-ui, sans-serif" font-size="150" font-weight="800" fill="#F4EFE6">23:59</text>
<text x="70" y="400" font-family="system-ui, sans-serif" font-size="40" font-weight="700" fill="#F4EFE6">Merch de tribu para docentes interinos</text>
<text x="70" y="460" font-family="system-ui, sans-serif" font-size="40" font-weight="700" fill="#E4C56B">Camisetas · totes · tazas · Canarias</text>
<rect x="70" y="520" width="420" height="60" fill="#B23A2E"/>
<text x="100" y="560" font-family="system-ui, sans-serif" font-size="30" font-weight="800" fill="#F4EFE6">SIGO EN LISTA DE ESPERA</text>
</svg>
"""


def svg_favicon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" fill="#111111"/>
<text x="8" y="30" font-family="ui-monospace, monospace" font-size="18" fill="#F4EFE6">23</text>
<text x="8" y="52" font-family="ui-monospace, monospace" font-size="18" fill="#B23A2E">59</text>
</svg>
"""


# --------------------------------------------------------------------------
# páginas
# --------------------------------------------------------------------------
def tarjeta_producto(ficha: dict) -> str:
    d, p = ficha["diseno"], ficha["producto"]
    estado = (
        f'<span class="tag tag-rojo">Comprar</span>'
        if ficha["disponible"]
        else '<span class="tag">Próximamente</span>'
    )
    return f"""<article class="card" data-tipo-producto="{p['id']}">
  <div class="card-img"><img src="{ruta('/assets/img/' + ficha['id'] + '.svg')}" alt="Placeholder del diseño «{esc(d['titulo'])}» sobre {esc(p['nombre'].lower())}" width="800" height="1000" loading="lazy"></div>
  <div class="card-body">
    <div>{estado} <span class="tag mono">{esc(p['nombre'])}</span></div>
    <h3><a href="{ruta(ficha['url'])}">{esc(d['titulo'])}</a></h3>
    <p class="small mono">{esc(d['texto_camiseta'].replace(chr(10), ' / '))}</p>
    <p class="precio">{eur(ficha['precio'])} <small>IVA incluido · envío calculado al pagar</small></p>
    <a class="btn" href="{ruta(ficha['url'])}">Ver ficha</a>
  </div>
</article>"""


def pagina_inicio() -> str:
    destacados = "".join(tarjeta_producto(f) for f in FICHAS[:3])
    lista_disenos = "".join(
        f'<li><strong>{d["numero"]:02d}. {esc(d["titulo"])}</strong><br>'
        f'<span class="small mono">{esc(d["texto_camiseta"].replace(chr(10), " / "))}</span> — '
        f'{"listo para vender" if d.get("estado") == "listo" else "imprimible en producción"}</li>'
        for d in DISENOS
    )
    cuerpo = f"""
{aviso_lanzamiento()}
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="tag tag-azul mono">Canarias · interinos · Primaria y Secundaria</span>
      <h1><span>Sigo en</span><span>lista de espera</span></h1>
      <p class="lead">{esc(SITE['claim_home'])}</p>
      <div class="btn-row">
        <a class="btn" href="{ruta('/catalogo/')}">Ver catálogo</a>
        <a class="btn btn-2" href="{ruta('/como-funciona/')}">Cómo funciona</a>
      </div>
      <p class="small">Impresión bajo demanda: nada se fabrica hasta que alguien lo pide. Envíos a las islas con plazos honestos, sin promesas de 24 horas.</p>
    </div>
    <div class="hero-card">
      <h2>Lo que sí y lo que no</h2>
      <ul>
        <li>Sí: humor de tribu docente, en canario y en castellano de aquí.</li>
        <li>Sí: camiseta, tote y taza. Tres productos, bien hechos.</li>
        <li>No: escudos, logos institucionales, siglas sindicales ni nombres de centros.</li>
        <li>No: plazos de mentira. Mira la ficha de cada producto antes de comprar.</li>
      </ul>
      <p><a href="{ruta('/faq/')}">Preguntas frecuentes de interinos →</a></p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Productos destacados</h2>
    <p class="small">Tres ejemplos del catálogo. Los 24 productos (8 diseños × 3 productos) están en el catálogo completo.</p>
    <div class="grid grid-3">
      {destacados}
    </div>
    <p class="center"><a class="btn" href="{ruta('/catalogo/')}">Ver los 24 productos</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Los 8 diseños</h2>
    <div class="grid grid-2">
      <ul class="pasos">{lista_disenos}</ul>
      <div>
        <div class="aviso">
          <p><strong>Plazos reales a Canarias: {CANARIAS['min_dias']}–{CANARIAS['max_dias']} días.</strong>
          {esc(CANARIAS['nota'])}</p>
        </div>
        <div class="aviso aviso-azul">
          <p><strong>Península: {PENINSULA['min_dias']}–{PENINSULA['max_dias']} días.</strong> {esc(PENINSULA['nota'])}</p>
        </div>
        <p class="small">{esc(SITE['envio']['texto_canarias'])}</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Cómo funciona, en cuatro líneas</h2>
    <ol class="pasos">
      <li><strong>Pides.</strong> Eliges diseño, talla y color, y pagas con tarjeta, PayPal o Bizum a través de la pasarela de la tienda.</li>
      <li><strong>Se imprime.</strong> Tu prenda entra en producción en un taller de España o de la Unión Europea. Tarda de 3 a 5 días laborables.</li>
      <li><strong>Se envía.</strong> Sale con el carrier que más rápido llegue a tu isla: Correos o Correos Express cuando toca, DHL o GLS cuando toca.</li>
      <li><strong>Lo sigues.</strong> Te llega el número de seguimiento real y puedes consultarlo en la página de <a href="{ruta('/seguimiento/')}">seguimiento</a>.</li>
    </ol>
    <p class="center"><a class="btn btn-2" href="{ruta('/como-funciona/')}">Ver el detalle completo</a></p>
  </div>
</section>
"""
    return layout(
        f"{MARCA} — camisetas, totes y tazas para docentes interinos de Canarias",
        "Merch humorístico para docentes interinos de Canarias: camisetas, totes y tazas impresas bajo demanda. Envíos a las islas con plazos honestos.",
        "/",
        cuerpo,
    )


def pagina_catalogo() -> str:
    tarjetas = "\n".join(tarjeta_producto(f) for f in FICHAS)
    botones = "".join(
        f'<button class="btn {"btn-rojo" if p["id"] == "camiseta" else "btn-2"}" data-filtro="{p["id"]}">{esc(p["nombre"])}</button>'
        for p in PRODUCTOS
    )
    cuerpo = f"""
{aviso_lanzamiento()}
<section>
  <div class="wrap">
    <h1>Catálogo</h1>
    <p class="lead">8 diseños × 3 productos = 24 combinaciones. Nada de stock: cada pieza se imprime cuando la pides.</p>
    <div class="btn-row" role="group" aria-label="Filtrar por producto">
      <button class="btn btn-2" data-filtro="todos">Todo</button>
      {botones}
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="grid grid-3">
      {tarjetas}
    </div>
  </div>
</section>
"""
    return layout(
        f"Catálogo · {MARCA}",
        "Los 8 diseños de Llamamiento 23:59 en camiseta, tote bag y taza. Impresión bajo demanda y envío a Canarias y península.",
        "/catalogo/",
        cuerpo,
    )


def pagina_producto(ficha: dict) -> str:
    d, p = ficha["diseno"], ficha["producto"]
    tallas = "".join(f"<li>{esc(t)}</li>" for t in p["tallas"])
    disponible = ficha["disponible"]

    if disponible:
        compra = f"""<a class="btn btn-block" href="{esc(ficha['checkout_url'])}" rel="noopener">Comprar ahora</a>
        <button class="btn btn-2 btn-block" data-accion="annadir" data-id="{ficha['id']}" data-titulo="{esc(ficha['titulo'])}" data-tipo="{p['id']}" data-precio="{ficha['precio']}" data-checkout="{esc(ficha['checkout_url'])}">Añadir a mi lista</button>"""
    else:
        compra = f"""<a class="btn btn-block" href="{mailto(f"Avísame: {ficha['titulo']}", 'Quiero que me aviséis cuando este producto se pueda comprar.')}">Avísame cuando esté</a>
        <p class="small">Este producto aún no se puede comprar: el imprimible no está terminado y no vendemos aire.</p>"""

    cuerpo = f"""
<section>
  <div class="wrap">
    <p class="small"><a href="{ruta('/catalogo/')}">Catálogo</a> / {esc(p['nombre'])} / {esc(d['titulo'])}</p>
    <div class="ficha">
      <div>
        <div class="ficha-img"><img src="{ruta('/assets/img/' + ficha['id'] + '.svg')}" alt="Placeholder del diseño «{esc(d['titulo'])}» sobre {esc(p['nombre'].lower())}" width="800" height="1000"></div>
        <p class="small">Imagen de marcador de posición. Cuando el imprimible exista, esta ficha muestra el mockup oficial del fabricante.</p>
      </div>
      <div>
        <h1>{esc(d['titulo'])}</h1>
        <p class="mono">{esc(d['texto_camiseta'].replace(chr(10), ' / '))}</p>
        <p class="precio">{eur(ficha['precio'])} <small>IVA incluido. Gastos de envío calculados en el checkout.</small></p>
        {"<span class='tag tag-rojo'>Disponible</span>" if disponible else "<span class='tag tag-azul'>Próximamente</span>"}

        <h2 style="margin-top:1.25rem">Elige talla</h2>
        <ul class="tallas" id="tallas">{tallas}</ul>

        <div class="aviso aviso-azul">
          <p><strong>Envío a Canarias: {CANARIAS['min_dias']}–{CANARIAS['max_dias']} días</strong> desde el pago
          (producción {SITE['plazos']['produccion_dias'][0]}–{SITE['plazos']['produccion_dias'][1]} días laborables + transporte).
          A la península, {PENINSULA['min_dias']}–{PENINSULA['max_dias']} días.</p>
          <p class="small">{esc(SITE['envio']['texto_canarias'])}</p>
        </div>

        <div class="btn-row" style="flex-direction:column">{compra}</div>

        <h2 style="margin-top:1.5rem">Detalles</h2>
        <ul class="specs">
          <li><strong>Producto</strong> <span>{esc(p['nombre_largo'])}</span></li>
          <li><strong>Confección</strong> <span>{esc(p['confeccion'])}</span></li>
          <li><strong>Tallas</strong> <span>{esc(', '.join(p['tallas']))}</span></li>
          <li><strong>Impresión</strong> <span>Bajo demanda, {esc(p['plantilla'])}</span></li>
          <li><strong>Devoluciones</strong> <span>Producto personalizado: sin derecho de desistimiento salvo defecto de fabricación o error nuestro (<a href="{ruta('/envios/')}">condiciones</a>).</span></li>
          <li><strong>Referencia</strong> <span class="mono">{esc(ficha['id'].upper())}</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""
    titulo_pagina = f"{p['nombre']} · {d['titulo']}"
    if MARCA not in titulo_pagina:
        titulo_pagina += f" · {MARCA}"
    return layout(
        titulo_pagina,
        f"{d['titulo']} en {p['nombre'].lower()}. {eur(ficha['precio'])} IVA incluido. Impresión bajo demanda y envío a Canarias en {CANARIAS['min_dias']}-{CANARIAS['max_dias']} días.",
        ficha["url"],
        cuerpo,
    )


def pagina_carrito() -> str:
    cuerpo = f"""
<section>
  <div class="wrap">
    <h1>Mi lista</h1>
    <p class="lead">Aquí se guarda lo que vas marcando mientras la tienda está en prelanzamiento. El cobro lo hace siempre la pasarela de pago de la plataforma de impresión: esta web nunca pide datos de tarjeta.</p>
    <div class="aviso aviso-azul">
      <p><strong>Cómo se paga (fase actual).</strong> Cada producto se compra en el checkout de la plataforma POD,
      con tarjeta, PayPal o Apple/Google Pay. Desde esta página te llevamos a la ficha de compra de cada artículo.</p>
    </div>
    <div id="carrito-vacio">
      <p>Tu lista está vacía.</p>
      <a class="btn" href="{ruta('/catalogo/')}">Ver catálogo</a>
    </div>
    <div id="carrito-tabla" class="oculto table-scroll">
      <table>
        <caption class="small">Productos marcados en este navegador</caption>
        <thead><tr><th scope="col">Producto</th><th scope="col">Precio</th><th scope="col">Acciones</th></tr></thead>
        <tbody id="carrito-lista"></tbody>
        <tfoot><tr><th scope="row">Total orientativo</th><td id="carrito-total">0,00 €</td><td><button class="btn btn-2" data-accion="vaciar">Vaciar</button></td></tr></tfoot>
      </table>
      <p class="small">El total no incluye envío: se calcula en el checkout de la plataforma, donde verás también los posibles gastos de despacho aduanero si tu envío va a Canarias.</p>
    </div>
  </div>
</section>
"""
    return layout(
        f"Mi lista · {MARCA}",
        "Tu lista de productos de Llamamiento 23:59. El pago se realiza en el checkout de la plataforma de impresión bajo demanda.",
        "/carrito/",
        cuerpo,
    )


def pagina_como_funciona() -> str:
    cuerpo = f"""
<section>
  <div class="wrap">
    <h1>Cómo funciona</h1>
    <p class="lead">Sin almacén, sin intermediarios y sin prometer lo que no se puede cumplir. Esto es exactamente lo que pasa desde que pagas hasta que abres el paquete.</p>
    <ol class="pasos">
      <li><strong>Pagas de forma automática.</strong> Checkout alojado en la plataforma de impresión: tarjeta, PayPal, Apple Pay o Google Pay. Recibes la confirmación por email en minutos, con número de pedido.</li>
      <li><strong>Entra en producción.</strong> Tu pieza se imprime en un taller de España (Barcelona) o de la Unión Europea, según disponibilidad del artículo. No hay stock previo: se fabrica la tuya.</li>
      <li><strong>Se envía.</strong> Sale con el carrier que dé el mejor plazo real a tu código postal. En Canarias eso es Correos o Correos Express cuando está disponible; si no, DHL o GLS. Nunca llamamos Correos a lo que no es Correos.</li>
      <li><strong>Te avisamos y lo sigues.</strong> Email con el número de seguimiento real y enlace al carrier. Botón en la web para consultar el estado con tu número de pedido y tu email.</li>
    </ol>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Plazos por destino</h2>
    <div class="table-scroll">
    <table>
      <caption class="small">Plazos orientativos desde el pago, con producción incluida ({SITE['plazos']['produccion_dias'][0]}–{SITE['plazos']['produccion_dias'][1]} días laborables).</caption>
      <thead><tr><th scope="col">Destino</th><th scope="col">Plazo</th><th scope="col">Qué tener en cuenta</th></tr></thead>
      <tbody>
        <tr><td><strong>Canarias</strong> (Tenerife, Gran Canaria, islas)</td><td>{CANARIAS['min_dias']}–{CANARIAS['max_dias']} días</td><td>El envío pasa por despacho aduanero al entrar en las islas. Puede haber IGIC y gastos de gestión del carrier. Si la ruta del taller ya cobra los derechos en el checkout (DDP), no pagas nada al recibir.</td></tr>
        <tr><td><strong>Península y Baleares</strong></td><td>{PENINSULA['min_dias']}–{PENINSULA['max_dias']} días</td><td>Sin aduanas: circulación dentro del territorio aduanero de la UE.</td></tr>
        <tr><td><strong>Resto de la UE</strong></td><td>7–14 días</td><td>Según país y carrier asignado por el taller.</td></tr>
      </tbody>
    </table>
    </div>
    <div class="aviso">
      <p><strong>Por qué no es siempre Correos.</strong> Imprimimos en talleres de España y de la UE. Según el artículo y el día,
      el taller asigna Correos, Correos Express, DHL o GLS. Elegimos la combinación que llega antes a tu isla, no la que más suena.
      Te damos siempre el nombre del carrier real y su número de seguimiento.</p>
    </div>
    <h2>Bajo demanda: sin stock, sin desperdicio</h2>
    <p>Cada pieza se imprime cuando se compra. Eso significa dos cosas: no hay rebajas de liquidación de stock sobrante, y tu pedido tarda en producirse lo que tarde en producirse de verdad. A cambio, no se fabrica ni una camiseta que nadie haya pedido.</p>
  </div>
</section>
"""
    return layout(
        f"Cómo funciona · {MARCA}",
        "Proceso completo de compra, producción bajo demanda y envío a Canarias, con plazos reales por destino y el carrier que se use en cada caso.",
        "/como-funciona/",
        cuerpo,
    )


def pagina_faq() -> str:
    pregs = [
        ("¿Cuánto tarda en llegar a Canarias?",
         f"Entre {CANARIAS['min_dias']} y {CANARIAS['max_dias']} días desde que pagas. Se fabrica en 3–5 días laborables y luego viaja a la isla. Las islas no son península: el paquete pasa despacho aduanero."),
        ("¿Por qué no es siempre Correos?",
         "Porque imprimimos en talleres de España y de la UE y no controlamos qué carrier asigna cada taller cada día. Elegimos el que llega antes. Si el envío va con Correos Express, DHL o GLS, te lo decimos con su nombre real y su número de seguimiento."),
        ("¿Qué son los gastos de aduanas o el IGIC?",
         "Canarias está fuera del territorio fiscal del IVA: al entrar mercancía desde la península se genera una declaración (DUA) y puede aplicarse IGIC, más gastos de gestión del carrier. En algunas rutas la plataforma ya cobra ese importe en el checkout (DDP) y no pagas nada al recibir; en otras te lo cobra el carrier en la entrega. Te avisamos en el propio checkout cuando la ruta es aduanera."),
        ("¿Qué tallas hay?",
         "Camiseta unisex de S a 2XL, corte estándar. Si dudas entre dos tallas, coge la grande: el algodón peinado encoge poco pero el corte unisex no es generoso. Tote tamaño único y taza de 11 oz (325 ml)."),
        ("¿Puedo devolver una camiseta?",
         "En productos personalizados no hay derecho de desistimiento (art. 103.f del texto refundido de la LGDCU). Sí respondemos si hay defecto de impresión, error de talla por nuestra parte o paquete dañado: reimprimimos o devolvemos el importe. Ver <a href=\"" + ruta('/envios/') + "\">Envíos y devoluciones</a>."),
        ("¿La impresión se cae a los dos lavados?",
         "Es estampado digital DTG sobre algodón: aguanta bien si lavas del revés, a 30 °C y sin secadora. Es la recomendación oficial del fabricante, no un truco de ventas."),
        ("¿Puedo pagar con Bizum?",
         "No. El pago es siempre automático a través de la pasarela (tarjeta, PayPal, Apple Pay o Google Pay). Nada de transferencias ni de «te paso mi número»."),
        ("¿Hacéis factura?",
         "Sí, factura con IVA español. Pídela al email de contacto con el número de pedido y a nombre de quién la necesitas."),
        ("¿Y si no soy interino?",
         "Se puede comprar igual. El chiste no discrimina: hay maestros de carrera, técnicos y algún cuñado que también lo entiende."),
        ("¿Se puede comprar sin crear cuenta?",
         "Sí. El checkout solo pide email, dirección y pago. No hay registro obligatorio."),
    ]
    cuerpo = f"""
<section>
  <div class="wrap">
    <h1>Preguntas frecuentes</h1>
    <p class="lead">Dudas reales de interinos comprando en las islas. Si falta la tuya, escríbenos y la añadimos.</p>
    {''.join(f'<details><summary>{esc(p)}</summary><div class="faq-body"><p>{r}</p></div></details>' for p, r in pregs)}
    <p style="margin-top:1.5rem"><a class="btn btn-2" href="{ruta('/contacto/')}">Hacer otra pregunta</a></p>
  </div>
</section>
"""
    return layout(
        f"FAQ interinos · {MARCA}",
        "Tallas, envíos a Canarias, aduanas e IGIC, devoluciones de producto personalizado, factura y pagos de la tienda de merchandising para interinos.",
        "/faq/",
        cuerpo,
    )


def pagina_contacto() -> str:
    m_pedido = mailto("Pedido LL-0000", "Número de pedido: LL-\nQué ocurre:\n")
    m_devol = mailto("Devolución / defecto", "Número de pedido:\nDefecto observado (adjunta foto):\n")
    m_factura = mailto(
        "Solicitud de factura",
        "Número de pedido:\nNombre o razón social:\nNIF:\nDirección fiscal:\n",
    )
    m_diseno = mailto("Propuesta de diseño")
    m_consulta = mailto("Consulta desde la web")
    cuerpo = f"""
<section>
  <div class="wrap">
    <h1>Contacto</h1>
    <p class="lead">Respondemos en menos de {SITE['respuesta_horas']} horas laborables. Si es por un pedido, incluye el número (formato LL-0000) y el email de compra.</p>
    <div class="grid grid-2">
      <div>
        <h2>Escríbenos</h2>
        <div class="btn-row">
          <a class="btn" href="{m_consulta}">Abrir email de consulta</a>
        </div>
        <p class="small">Se abre tu cliente de correo con el asunto ya puesto. Así no guardamos tus datos en ningún formulario.</p>
        <ul class="specs">
          <li><strong>Pedidos</strong> <span><a href="{m_pedido}">Abrir incidencia de pedido</a></span></li>
          <li><strong>Devoluciones</strong> <span><a href="{m_devol}">Abrir solicitud de devolución</a></span></li>
          <li><strong>Facturas</strong> <span><a href="{m_factura}">Pedir factura con IVA</a></span></li>
          <li><strong>Diseños y colaboraciones</strong> <span><a href="{m_diseno}">Proponer diseño</a></span></li>
        </ul>
      </div>
      <div>
        <h2>Quién está detrás</h2>
        <p>Proyecto pequeño, de docentes y para docentes. Sin escudos, sin siglas sindicales y sin usar el nombre de ninguna administración como marca.</p>
        <ul class="specs">
          <li><strong>Titular</strong> <span>{esc(SITE['responsable']['nombre'])}</span></li>
          <li><strong>NIF</strong> <span>{esc(SITE['responsable']['nif'])}</span></li>
          <li><strong>Dirección</strong> <span>{esc(SITE['responsable']['direccion'])}</span></li>
          <li><strong>Email</strong> <span>{esc(EMAIL)}</span></li>
          <li><strong>Incidencias técnicas</strong> <span><a href="{REPO_ISSUES}" rel="noopener">Abrir aviso en el repositorio</a></span></li>
        </ul>
        <p class="small">Los datos del titular se completan antes de la apertura real de la tienda. Están marcados con corchetes en la documentación del proyecto.</p>
      </div>
    </div>
  </div>
</section>
"""
    return layout(
        f"Contacto · {MARCA}",
        "Contacto de la tienda Llamamiento 23:59: pedidos, devoluciones, facturas con IVA y propuestas de diseño.",
        "/contacto/",
        cuerpo,
    )


def pagina_seguimiento() -> str:
    filas = "".join(
        f'<li>{esc(c["nombre"])} — {esc(c["ambito"])}</li>' for c in CARRIERS["carriers"]
    )
    cuerpo = f"""
<section>
  <div class="wrap">
    <h1>Seguimiento de pedido</h1>
    <p class="lead">Pega tu número de pedido y el email con el que compraste. Verás el estado y, si ya salió, el carrier real con su número de seguimiento.</p>
    <form id="form-seguimiento" class="grid grid-2" novalidate>
      <div class="form-row">
        <label for="pedido">Número de pedido</label>
        <input id="pedido" name="pedido" placeholder="LL-0000" autocomplete="off" required>
      </div>
      <div class="form-row">
        <label for="email">Email de compra</label>
        <input id="email" name="email" type="email" placeholder="tu@email.com" autocomplete="email" required>
      </div>
      <div class="form-row">
        <button class="btn btn-block" type="submit">Ver estado</button>
      </div>
    </form>
    <div id="seguimiento-resultado" aria-live="polite"></div>
    <p class="small">Consejo de pruebas: <span class="mono">DEMO-0000</span> + <span class="mono">demo@ejemplo.com</span> muestra un ejemplo del resultado.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Estados posibles</h2>
    <ul class="timeline">
      <li class="hecho"><strong>Pagado</strong><br><span class="small">Pago aceptado y pedido registrado.</span></li>
      <li class="hecho"><strong>En producción</strong><br><span class="small">El taller está imprimiendo tu pieza.</span></li>
      <li class="hecho"><strong>Enviado</strong><br><span class="small">Con número de seguimiento del carrier real.</span></li>
      <li><strong>Entregado</strong><br><span class="small">El carrier marca la entrega.</span></li>
    </ul>
    <h2>Carriers que podemos asignar</h2>
    <ul>{filas}</ul>
    <div class="aviso">
      <p>Canarias no es península: el envío pasa despacho aduanero. Si el carrier te reclama el IGIC o gastos de gestión, no es un error del pedido; si la ruta se cobró con derechos pagados (DDP), no pagarás nada al recibir.</p>
    </div>
  </div>
</section>
"""
    return layout(
        f"Seguimiento de pedido · {MARCA}",
        "Consulta el estado de tu pedido: pagado, en producción, enviado y número de seguimiento del carrier real.",
        "/seguimiento/",
        cuerpo,
    )


def pagina_legal(nombre: str, titulo: str, descripcion: str, url: str) -> str:
    fragmento = (ROOT / "legal" / f"{nombre}.html").read_text(encoding="utf-8")
    fragmento = fragmento.replace("{{BASE}}", BASE)
    cuerpo = f'<section><div class="wrap">{fragmento}</div></section>'
    return layout(titulo, descripcion, url, cuerpo)


def pagina_borrador() -> str:
    tarjetas = ""
    for ph in PLACEHOLDERS["placeholders"]:
        tarjetas += f"""<article class="card">
  <div class="card-img" style="display:grid;place-items:center"><span class="tag tag-azul" style="font-size:1.2rem;padding:.6rem 1rem">PRÓXIMAMENTE</span></div>
  <div class="card-body">
    <h3>{esc(ph['titulo'])}</h3>
    <p class="precio">{eur(ph['precio_eur'])}</p>
    <p class="small">Producto de relleno para montar la maqueta de la tienda. NO está a la venta.</p>
    <span class="btn" aria-disabled="true">No comprable</span>
  </div>
</article>"""
    cuerpo = f"""
<section>
  <div class="wrap">
    <h1>Borrador · placeholders</h1>
    <div class="aviso">
      <p><strong>Página de maqueta, no publicada en la tienda.</strong> Contiene los 3 productos de relleno marcados
      «PRÓXIMAMENTE» que pide el plan de lanzamiento. Está en <span class="mono">noindex</span>, no aparece en el menú
      ni en el sitemap, y se borra cuando existan los imprimibles reales. Regla: no se vende un diseño vacío.</p>
    </div>
    <div class="grid grid-3">{tarjetas}</div>
  </div>
</section>
"""
    return layout("Borrador (no publicado)", "Página interna de borrador con productos placeholder.", "/_borrador/", cuerpo, noindex=True)


# --------------------------------------------------------------------------
# escritura
# --------------------------------------------------------------------------
def copiar_estaticos() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "assets").mkdir()
    shutil.copytree(ROOT / "static" / "css", DIST / "assets" / "css")
    shutil.copytree(ROOT / "static" / "js", DIST / "assets" / "js")
    (DIST / "assets" / "img").mkdir(parents=True)
    (DIST / "data").mkdir(parents=True)
    if (ROOT / "static" / "img" / "marca").exists():
        shutil.copytree(ROOT / "static" / "img" / "marca", DIST / "assets" / "img" / "marca")

    for ficha in FICHAS:
        (DIST / "assets" / "img" / f"{ficha['id']}.svg").write_text(svg_placeholder(ficha), encoding="utf-8")
    (DIST / "assets" / "img" / "og.svg").write_text(svg_og(), encoding="utf-8")
    (DIST / "assets" / "img" / "og.png").write_bytes(png_og())
    (DIST / "assets" / "img" / "favicon.svg").write_text(svg_favicon(), encoding="utf-8")

    shutil.copy(ROOT / "data" / "pedidos.json", DIST / "data" / "pedidos.json")
    shutil.copy(ROOT / "data" / "carriers.json", DIST / "data" / "carriers.json")


def png_og() -> bytes:
    """OG en PNG. Se intenta renderizar con PIL; si no está, se devuelve un PNG
    mínimo válido generado a mano (color plano azul noche)."""
    try:
        from PIL import Image, ImageDraw  # type: ignore

        img = Image.new("RGB", (1200, 630), (14, 27, 42))
        d = ImageDraw.Draw(img)
        d.rectangle([70, 520, 490, 580], fill=(178, 58, 46))
        img.save(DIST / "assets" / "img" / "og_pil.png", "PNG")
        return (DIST / "assets" / "img" / "og_pil.png").read_bytes()
    except Exception:
        avisos.append("PIL no disponible: el og.png se genera como respaldo plano. og.svg es la versión con texto.")
        return png_plano(1200, 630, (14, 27, 42))


def png_plano(ancho: int, alto: int, color: tuple[int, int, int]) -> bytes:
    import struct
    import zlib

    fila = bytes([0]) + bytes(color) * ancho
    datos = zlib.compress(fila * alto, 9)

    def chunk(tipo: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tipo
            + payload
            + struct.pack(">I", zlib.crc32(tipo + payload) & 0xFFFFFFFF)
        )

    cabecera = struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", cabecera) + chunk(b"IDAT", datos) + chunk(b"IEND", b"")


def escribir_sitio() -> None:
    escribe("index.html", pagina_inicio())
    escribe("catalogo/index.html", pagina_catalogo())
    for ficha in FICHAS:
        escribe(f"producto/{ficha['id']}/index.html", pagina_producto(ficha))
    escribe("carrito/index.html", pagina_carrito())
    escribe("como-funciona/index.html", pagina_como_funciona())
    escribe("faq/index.html", pagina_faq())
    escribe("contacto/index.html", pagina_contacto())
    escribe("seguimiento/index.html", pagina_seguimiento())
    escribe("_borrador/index.html", pagina_borrador())

    legales = [
        ("aviso-legal", "Aviso legal", "Titular, condiciones de uso y responsabilidad de la tienda Llamamiento 23:59.", "/aviso-legal/"),
        ("privacidad", "Política de privacidad", "Tratamiento de datos personales, base jurídica, encargados (Stripe, plataforma POD) y derechos RGPD.", "/privacidad/"),
        ("cookies", "Política de cookies", "Cookies técnicas y analítica opcional de la tienda de merchandising para interinos.", "/cookies/"),
        ("condiciones", "Condiciones de compra", "Proceso de compra, precios, IVA, personalización, derecho de desistimiento y garantías.", "/condiciones/"),
        ("envios-devoluciones", "Envíos y devoluciones", "Plazos a Canarias y península, carriers, aduanas/IGIC, defectos y reimpresiones.", "/envios/"),
    ]
    for nombre, titulo, desc, url in legales:
        escribe(f"{url.strip('/')}/index.html", pagina_legal(nombre, f"{titulo} · {MARCA}", desc, url))

    # data pública que consume el buscador de seguimiento
    shutil.copy(ROOT / "data" / "pedidos.json", DIST / "data" / "pedidos.json")

    rutas = ["/", "/catalogo/", "/carrito/", "/como-funciona/", "/faq/", "/contacto/", "/seguimiento/"] + [
        f["url"] for f in FICHAS
    ] + [u for _, _, _, u in legales]
    dominio_base = f"https://{DOMINIO}" if DOMINIO != "PENDIENTE-CONFIRMAR" else SITE["url_publicada"].rstrip("/")
    urls = "".join(
        f"<url><loc>{dominio_base}{u if u != '/' else '/'}</loc><lastmod>{fecha_hoy()}</lastmod>"
        f"<changefreq>{'weekly' if u == '/catalogo/' else 'monthly'}</changefreq>"
        f"<priority>{'1.0' if u == '/' else '0.7' if u.startswith('/producto') else '0.5'}</priority></url>"
        for u in rutas
    )
    escribe(
        "sitemap.xml",
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
    )
    escribe("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_borrador/\nSitemap: {dominio_base}/sitemap.xml\n")

    escribe(
        "404.html",
        layout(
            f"Página no encontrada · {MARCA}",
            "Esa página no existe.",
            "/404.html",
            f"""<section><div class="wrap center">
            <h1>404</h1>
            <p class="lead">Esa página no existe. Como ciertas plazas en agosto: se intentó, no salió.</p>
            <div class="btn-row center"><a class="btn" href="{ruta('/catalogo/')}">Volver al catálogo</a>
            <a class="btn btn-2" href="{ruta('/') or '/'}">Ir al inicio</a></div>
            </div></section>""",
            noindex=True,
        ),
    )

    # GitHub Pages no necesita CNAME si el dominio es el de github.io; si el humano
    # confirma su dominio, se escribe el fichero CNAME.
    if DOMINIO != "PENDIENTE-CONFIRMAR":
        escribe("CNAME", DOMINIO + "\n")


# --------------------------------------------------------------------------
# validaciones (--check)
# --------------------------------------------------------------------------
def validar() -> None:
    htmls = list(DIST.rglob("*.html"))
    if not htmls:
        errores.append("No se ha generado ningún HTML.")
    destinos = set()
    for h in htmls:
        rel = h.relative_to(DIST).parent.as_posix()
        destinos.add("/" + ("" if rel == "." else rel + "/"))
    destinos |= {"/", "/404.html"}

    for h in htmls:
        txt = h.read_text(encoding="utf-8")
        rel = h.relative_to(DIST).as_posix()
        for palabra in PROHIBIDAS:
            if palabra.lower() in txt.lower():
                errores.append(f"{rel}: aparece el término prohibido «{palabra}».")
        if "<title>" not in txt:
            errores.append(f"{rel}: sin <title>.")
        if 'name="description"' not in txt:
            errores.append(f"{rel}: sin meta description.")
        if rel != "_borrador/index.html" and "noindex" not in txt.split("</head>")[0] and "og:image" not in txt:
            errores.append(f"{rel}: sin og:image.")
        for href in re.findall(r'(?:href|src)="([^"]+)"', txt):
            if href.startswith(("http", "mailto:", "#", "data:")):
                continue
            limpio = href.replace(BASE, "", 1) if BASE and href.startswith(BASE) else href
            limpio = limpio.split("#")[0]
            if limpio in ("", "/"):
                continue
            if limpio.endswith((".css", ".js", ".svg", ".png", ".json", ".txt", ".xml", ".ico")):
                if not (DIST / limpio.lstrip("/")).exists():
                    errores.append(f"{rel}: recurso inexistente {limpio}")
            elif limpio.endswith(".html"):
                if not (DIST / limpio.lstrip("/")).exists():
                    errores.append(f"{rel}: página inexistente {limpio}")
            else:
                if not limpio.endswith("/"):
                    limpio += "/"
                if limpio not in destinos:
                    errores.append(f"{rel}: enlace interno roto {limpio}")

    for f in FICHAS:
        if f["precio"] <= f["coste_base"]:
            errores.append(f"{f['id']}: precio {f['precio']} <= coste base {f['coste_base']}.")
        if f["margen"] < 5:
            avisos.append(f"{f['id']}: margen bajo ({f['margen']} €) antes de gastos de envío y comisión de pago.")

    for d in DISENOS:
        lineas = d["texto_camiseta"].split("\n")
        palabras = len(d["texto_camiseta"].split())
        if len(lineas) > 2:
            avisos.append(f"{d['slug']}: más de 2 líneas de texto.")
        if palabras > 8:
            avisos.append(f"{d['slug']}: {palabras} palabras (objetivo 6-8).")

    print(f"Fichas de producto: {len(FICHAS)} ({len(DISENOS)} diseños × {len(PRODUCTOS)} productos)")
    print(f"Páginas generadas: {len(list(DIST.rglob('*.html')))}")
    print(f"Avisos: {len(avisos)}")
    for a in avisos:
        print("  · aviso:", a)
    if errores:
        print(f"ERRORES: {len(errores)}")
        for e in errores:
            print("  · error:", e)
        sys.exit(1)
    print("Validación OK")


def main() -> None:
    copiar_estaticos()
    escribir_sitio()
    if "--check" in sys.argv:
        validar()
    else:
        print(f"Tienda generada en {DIST} ({len(FICHAS)} fichas, {len(list(DIST.rglob('*.html')))} páginas)")


if __name__ == "__main__":
    main()
