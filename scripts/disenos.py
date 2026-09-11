#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compone los 8 diseños de Llamamiento 23:59 listos para imprimir.

Dos reglas del BRIEF que manda este script:

1. **El texto se compone con tipografía real**, nunca texto generado por IA. Aquí
   se dibuja con Pillow a 300 dpi: la frase sale nítida y bien escrita siempre.
2. **Cada diseño tiene dos variantes de color**: una para prenda oscura y otra para
   producto claro (tote crudo, taza blanca, camiseta clara). Sin esto, un diseño en
   crema desaparece sobre un tote crudo.

Uso:
    python scripts/disenos.py                      # compone los 8 diseños completos
    python scripts/disenos.py --solo 03-llamamiento-2359

Salidas por diseño (designs/<slug>/):
    master.png                        4500×5400, 300 dpi, alfa — variante prenda oscura
    master-claro.png                  4500×5400, 300 dpi, alfa — variante producto claro
    print-area-camiseta.png           3000×3600 (variante oscura, camiseta negra)
    print-area-camiseta-clara.png     3000×3600 (variante clara)
    print-area-tote.png               2952×3542 (variante clara, tote crudo)
    print-area-taza.png               2475×1155 (horizontal, zona libre junto al asa)
    mockup-web.webp                   1200×1500 (vista previa del arte, no foto de producto)
    INFO.md                           qué se ha generado y con qué tipografías
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
DISENOS_DIR = RAIZ / "designs"
ILUSTRACIONES = DISENOS_DIR / "_ilustraciones"

MASTER = (4500, 5400)
AREAS = {
    "camiseta": (3000, 3600),
    "tote": (2952, 3542),
    "taza": (2475, 1155),
}

FUENTE_DISPLAY = "C:/Windows/Fonts/ariblk.ttf"      # Arial Black
FUENTE_DISPLAY_2 = "C:/Windows/Fonts/seguibl.ttf"    # Segoe UI Black
FUENTE_MONO = "C:/Windows/Fonts/consolab.ttf"        # Consolas Bold

NEGRO = "#111111"
CREMA = "#F4EFE6"
ROJO = "#B23A2E"
AZUL = "#0E1B2A"
AZUL_CLARO = "#8FB8DE"
AMARILLO = "#E4C56B"
TERRACOTA = "#C97B4A"
GRIS_AZUL = "#7A8B99"

W, H = MASTER


# --------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------
def hexa(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def fuente(ruta: str, tam: int):
    return ImageFont.truetype(ruta, tam)


def medir(draw, texto: str, font):
    caja = draw.textbbox((0, 0), texto, font=font)
    return caja[2] - caja[0], caja[3] - caja[1], caja


def paleta(modo: str) -> dict[str, str]:
    """modo 'oscuro' = para prenda oscura; 'claro' = para producto claro."""
    if modo == "claro":
        return {"principal": NEGRO, "acento": ROJO, "linea": ROJO,
                "marco": AZUL, "detalle": AZUL, "suave": GRIS_AZUL}
    return {"principal": CREMA, "acento": AMARILLO, "linea": ROJO,
            "marco": ROJO, "detalle": AZUL_CLARO, "suave": GRIS_AZUL}


def fuente_ajustada(draw, texto: str, ruta: str, ideal: int, ancho_max: int):
    for tam in range(ideal, 20, -4):
        f = fuente(ruta, tam)
        ancho, _, _ = medir(draw, texto, f)
        if ancho <= ancho_max:
            return f
    return fuente(ruta, 24)


def texto_centrado(draw, y: int, texto: str, font, color: str, ancho: int, x0: int = 0, x1: int | None = None) -> int:
    x1 = ancho if x1 is None else x1
    a, _, caja = medir(draw, texto, font)
    x = x0 + ((x1 - x0) - a) // 2
    draw.text((x - caja[0], y), texto, font=font, fill=hexa(color))
    return y + (caja[3] - caja[1])


def bloque(draw, lineas: list[str], ruta: str, ideal: int, colores: list[str],
           y_centro: int, max_ancho: int, interlineado: float = 1.05, x0: int = 0, x1: int | None = None) -> None:
    x1 = W if x1 is None else x1
    cuerpo = min(fuente_ajustada(draw, l, ruta, ideal, max_ancho).size for l in lineas)
    f = fuente(ruta, cuerpo)
    salto = int(cuerpo * interlineado)
    y = y_centro - (salto * len(lineas)) // 2
    for i, linea in enumerate(lineas):
        texto_centrado(draw, y + i * salto, linea, f, colores[i], W, x0, x1)


# --------------------------------------------------------------------------
# elementos gráficos vectoriales
# --------------------------------------------------------------------------
def marco_sello(capa, caja, color: str, grosor: int = 22, grosor_interno: int = 7):
    d = ImageDraw.Draw(capa)
    d.rectangle(caja, outline=hexa(color), width=grosor)
    d.rectangle((caja[0] + 46, caja[1] + 46, caja[2] - 46, caja[3] - 46),
                outline=hexa(color), width=grosor_interno)


def icono_documento(capa, x: int, y: int, w: int, h: int, color: str, acento: str):
    d = ImageDraw.Draw(capa)
    pliegue = int(w * 0.32)
    d.polygon([(x, y), (x + w - pliegue, y), (x + w, y + pliegue), (x + w, y + h), (x, y + h)], fill=hexa(color))
    d.polygon([(x + w - pliegue, y), (x + w - pliegue, y + pliegue), (x + w, y + pliegue)], fill=hexa(acento))


SEGMENTOS = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
             "5": "afgcd", "6": "afgecd", "7": "abc", "8": "abcdefg", "9": "abcdfg"}


def digito_siete_segmentos(capa, x: int, y: int, ancho: int, alto: int, caracter: str, color: str, hueco: int = 14):
    d = ImageDraw.Draw(capa)
    t = max(18, int(alto * 0.11))
    m = hueco
    if caracter == ":":
        r = int(t * 0.6)
        for cy in (y + int(alto * 0.30), y + int(alto * 0.70)):
            d.ellipse([x + ancho // 2 - r, cy - r, x + ancho // 2 + r, cy + r], fill=hexa(color))
        return
    on = set(SEGMENTOS.get(caracter, ""))
    seg = {
        "a": [(x + m, y), (x + ancho - m, y), (x + ancho - m - t, y + t), (x + m + t, y + t)],
        "b": [(x + ancho, y + m), (x + ancho, y + alto // 2 - m), (x + ancho - t, y + alto // 2 - m - t), (x + ancho - t, y + m + t)],
        "c": [(x + ancho, y + alto // 2 + m), (x + ancho, y + alto - m), (x + ancho - t, y + alto - m - t), (x + ancho - t, y + alto // 2 + m + t)],
        "d": [(x + m, y + alto), (x + ancho - m, y + alto), (x + ancho - m - t, y + alto - t), (x + m + t, y + alto - t)],
        "e": [(x, y + alto // 2 + m), (x, y + alto - m), (x + t, y + alto - m - t), (x + t, y + alto // 2 + m + t)],
        "f": [(x, y + m), (x, y + alto // 2 - m), (x + t, y + alto // 2 - m - t), (x + t, y + m + t)],
        "g": [(x + m, y + alto // 2), (x + ancho - m, y + alto // 2), (x + ancho - m - t, y + alto // 2 + t), (x + m + t, y + alto // 2 + t)],
    }
    for letra, puntos in seg.items():
        if letra in on:
            d.polygon(puntos, fill=hexa(color))


def reloj_digital(capa, centro_x: int, y: int, alto: int, color: str, texto: str = "23:59"):
    ancho_d = int(alto * 0.62)
    sep = int(alto * 0.16)
    total = sum(int(ancho_d * 0.35) if c == ":" else ancho_d for c in texto) + sep * (len(texto) - 1)
    x = centro_x - total // 2
    for ch in texto:
        an = int(ancho_d * 0.35) if ch == ":" else ancho_d
        digito_siete_segmentos(capa, x, y, an, alto, ch, color)
        x += an + sep


def ticket(capa, x: int, y: int, w: int, h: int, color: str, acento: str, lineas: int = 3):
    d = ImageDraw.Draw(capa)
    d.rectangle([x, y, x + w, y + h], fill=hexa(color))
    dientes = 16
    paso = w // dientes
    for i in range(dientes):
        if i % 2 == 0:
            d.polygon([(x + i * paso, y + h), (x + (i + 1) * paso, y + h),
                       (x + i * paso + paso // 2, y + h + paso // 2)], fill=hexa(color))
    for i in range(lineas):
        yy = y + int(h * (0.22 + i * 0.26))
        d.rectangle([x + int(w * 0.10), yy, x + int(w * 0.145), yy + int(h * 0.075)], fill=hexa(acento))
        d.rectangle([x + int(w * 0.20), yy + int(h * 0.018), x + int(w * 0.88), yy + int(h * 0.05)], fill=hexa(acento))


def trazo_subrayado(capa, x1: int, x2: int, y: int, color: str, grosor: int = 30):
    d = ImageDraw.Draw(capa)
    puntos = []
    ancho = x2 - x1
    for i in range(0, ancho, 8):
        t = i / ancho
        dy = int(math.sin(t * math.pi * 2.2) * grosor * 0.8 + math.sin(t * math.pi * 7) * grosor * 0.2)
        puntos.append((x1 + i, y + dy))
    d.line(puntos, fill=hexa(color), width=grosor, joint="curve")


# --------------------------------------------------------------------------
# composiciones (coordenadas sobre 4500×5400). Reciben el modo de color.
# --------------------------------------------------------------------------
def comp_01(capa, modo):
    p = paleta(modo)
    marco_sello(capa, (700, 1150, W - 700, H - 1150), p["marco"])
    d = ImageDraw.Draw(capa)
    f1 = fuente_ajustada(d, "SIGO EN LISTA", FUENTE_DISPLAY, 470, W - 1800)
    f2 = fuente_ajustada(d, "DE ESPERA", FUENTE_DISPLAY, 470, W - 1800)
    f = fuente(FUENTE_DISPLAY, min(f1.size, f2.size))
    texto_centrado(d, 1880, "SIGO EN LISTA", f, p["principal"], W)
    texto_centrado(d, 1880 + int(f.size * 1.06), "DE ESPERA", f, p["principal"], W)
    texto_centrado(d, 3320, "INTERINIDAD · CANARIAS", fuente(FUENTE_MONO, 120), p["marco"], W)


def comp_02(capa, modo):
    p = paleta(modo)
    icono_documento(capa, W // 2 - 620, 800, 1240, 1500, p["principal"], p["acento"])
    d = ImageDraw.Draw(capa)
    f1 = fuente_ajustada(d, "MI DESTINO", FUENTE_DISPLAY, 440, W - 1500)
    f2 = fuente_ajustada(d, "ES UN PDF", FUENTE_DISPLAY, 440, W - 1500)
    f = fuente(FUENTE_DISPLAY, min(f1.size, f2.size))
    texto_centrado(d, 2680, "MI DESTINO", f, p["principal"], W)
    texto_centrado(d, 2680 + int(f.size * 1.06), "ES UN PDF", f, p["acento"], W)
    texto_centrado(d, 3820, "ARCHIVO · ADJUNTO · SIN NOVEDAD", fuente(FUENTE_MONO, 96), p["marco"], W)


def comp_03(capa, modo):
    p = paleta(modo)
    d = ImageDraw.Draw(capa)
    reloj_digital(capa, W // 2, 1450, 900, p["principal"], "23:59")
    f = fuente_ajustada(d, "LLAMAMIENTO", FUENTE_DISPLAY, 470, W - 1300)
    texto_centrado(d, 2820, "LLAMAMIENTO", f, p["principal"], W)
    texto_centrado(d, 3560, "DISPONIBLE A LAS 23:59", fuente(FUENTE_MONO, 150), p["marco"], W)


def comp_04(capa, modo):
    p = paleta(modo)
    d = ImageDraw.Draw(capa)
    f1 = fuente_ajustada(d, "INTERINO: NO ES UN ESTADO,", FUENTE_DISPLAY_2, 330, W - 800)
    f2 = fuente_ajustada(d, "ES UN CARDIO", FUENTE_DISPLAY_2, 470, W - 1400)
    texto_centrado(d, 2100, "INTERINO: NO ES UN ESTADO,", f1, p["principal"], W)
    texto_centrado(d, 2530, "ES UN CARDIO", f2, p["acento"], W)
    trazo_subrayado(capa, 1250, W - 1250, 3180, p["linea"], grosor=36)


def comp_05(capa, modo):
    p = paleta(modo)
    d = ImageDraw.Draw(capa)
    caja = (820, 1150, W - 820, H - 1500)
    d.rounded_rectangle(caja, radius=120, outline=hexa(p["detalle"]), width=26)
    d.rounded_rectangle((caja[0] + 60, caja[1] + 60, caja[2] - 60, caja[3] - 60),
                        radius=90, outline=hexa(p["detalle"]), width=8)
    f1 = fuente_ajustada(d, "VISTO", FUENTE_DISPLAY, 540, W - 2000)
    texto_centrado(d, 1800, "VISTO", f1, p["principal"], W)
    f2 = fuente_ajustada(d, "A LAS 3:47", FUENTE_MONO, 360, W - 2100)
    texto_centrado(d, 2600, "A LAS 3:47", f2, p["detalle"], W)
    texto_centrado(d, 3380, "SIN FIRMA · SIN SELLO OFICIAL", fuente(FUENTE_MONO, 104), p["marco"], W)


def comp_06(capa, modo):
    """Bandas de color con la frase repartida: funciona igual en prenda clara y oscura.

    Las bandas van sangradas 400 px (3,4 cm) a cada lado para no tocar el borde del
    área de impresión: lo que toca el borde se recorta al estampar.
    """
    d = ImageDraw.Draw(capa)
    alto_banda = 900
    y0 = 1200
    x_izq, x_der = 400, W - 400
    colores_banda = [NEGRO, CREMA, TERRACOTA]
    textos = ["SEPTIEMBRE, YO", "Y LA", "INCERTIDUMBRE"]
    colores_texto = [CREMA, NEGRO, NEGRO]
    for i, (color_b, texto) in enumerate(zip(colores_banda, textos)):
        y = y0 + i * alto_banda
        d.rectangle([x_izq, y, x_der, y + alto_banda], fill=hexa(color_b))
        f = fuente_ajustada(d, texto, FUENTE_DISPLAY, 360, x_der - x_izq - 300)
        a, alto_t, caja = medir(d, texto, f)
        texto_centrado(d, y + (alto_banda - alto_t) // 2 - caja[1], texto, f, colores_texto[i], W, x_izq, x_der)
    texto_centrado(d, y0 + 3 * alto_banda + 260, "SEPTIEMBRE: LA MISMA PREGUNTA DE SIEMPRE",
                   fuente(FUENTE_MONO, 96), paleta(modo)["marco"], W)


def comp_07(capa, modo):
    p = paleta(modo)
    d = ImageDraw.Draw(capa)
    f1 = fuente_ajustada(d, "¿FUNCIONARIO", FUENTE_DISPLAY, 520, W - 700)
    f2 = fuente_ajustada(d, "DE CARRERA?", FUENTE_DISPLAY, 520, W - 900)
    texto_centrado(d, 1150, "¿FUNCIONARIO", f1, p["marco"], W)
    texto_centrado(d, 1850, "DE CARRERA?", f2, p["marco"], W)
    d.rectangle([900, 3300, W - 900, 3340], fill=hexa(p["principal"]))
    f3 = fuente_ajustada(d, "EN ESTA VIDA NO", FUENTE_MONO, 300, W - 1400)
    texto_centrado(d, 3500, "EN ESTA VIDA NO", f3, p["principal"], W)


def comp_08(capa, modo):
    p = paleta(modo)
    d = ImageDraw.Draw(capa)
    ticket(capa, 800, 700, W - 1600, 2400, p["principal"], p["detalle"], lineas=3)
    f1 = fuente_ajustada(d, "CLAUSTRO, CAFÉ", FUENTE_DISPLAY, 460, W - 1200)
    texto_centrado(d, 3450, "CLAUSTRO, CAFÉ", f1, p["principal"], W)
    f2 = fuente_ajustada(d, "Y UN CONTRATO DE 9 DÍAS", FUENTE_DISPLAY, 280, W - 800)
    texto_centrado(d, 4020, "Y UN CONTRATO DE 9 DÍAS", f2, p["acento"], W)


COMPOSICIONES = {
    "01-sigo-en-lista-de-espera": comp_01,
    "02-mi-destino-es-un-pdf": comp_02,
    "03-llamamiento-2359": comp_03,
    "04-interino-es-un-cardio": comp_04,
    "05-visto-a-las-347": comp_05,
    "06-septiembre-y-la-incertidumbre": comp_06,
    "07-funcionario-de-carrera-no": comp_07,
    "08-claustro-cafe-y-9-dias": comp_08,
}

TEXTO_TASA = {
    "01-sigo-en-lista-de-espera": (["SIGO EN LISTA", "DE ESPERA"], "marco"),
    "02-mi-destino-es-un-pdf": (["MI DESTINO", "ES UN PDF"], "doc"),
    "03-llamamiento-2359": (["LLAMAMIENTO", "23:59"], "reloj"),
    "04-interino-es-un-cardio": (["INTERINO: NO ES", "UN ESTADO, ES UN CARDIO"], "linea"),
    "05-visto-a-las-347": (["VISTO", "A LAS 3:47"], "sello"),
    "06-septiembre-y-la-incertidumbre": (["SEPTIEMBRE, YO", "Y LA INCERTIDUMBRE"], "bandas"),
    "07-funcionario-de-carrera-no": (["¿FUNCIONARIO", "DE CARRERA?"], "pregunta"),
    "08-claustro-cafe-y-9-dias": (["CLAUSTRO, CAFÉ", "Y UN CONTRATO DE 9 DÍAS"], "ticket"),
}


# --------------------------------------------------------------------------
# ilustración del personaje: se recorta el círculo y se pega sobre el texto
# --------------------------------------------------------------------------
def capa_ilustracion(slug: str) -> Image.Image | None:
    """Devuelve el círculo ilustrado con transparencia, recortado y limpio.

    El recorte es geométrico (elipse sobre la caja del círculo crema), no por color:
    así el contorno oscuro del dibujo no se pierde ni queda un halo negro alrededor.
    """
    origen = ILUSTRACIONES / f"{slug}.png"
    if not origen.exists():
        return None
    from PIL import ImageFilter

    im = Image.open(origen).convert("RGBA")
    r, g, b = im.convert("RGB").split()
    crema = b.point(lambda v: 255 if v > 170 else 0)          # zona clara = círculo
    caja = crema.getbbox()
    if caja is None:
        return None
    # margen de seguridad para incluir lo que el personaje tapa del círculo
    izq, arriba, der, abajo = caja
    im = im.crop((max(0, izq - 6), max(0, arriba - 6), min(im.width, der + 6), min(im.height, abajo + 6)))

    mascara = Image.new("L", im.size, 0)
    ImageDraw.Draw(mascara).ellipse((1, 1, im.width - 2, im.height - 2), fill=255)
    mascara = mascara.filter(ImageFilter.GaussianBlur(2))
    im.putalpha(mascara)
    return im


def composicion_ilustrada(capa, modo, slug) -> None:
    """Personaje dentro del círculo crema arriba y la frase debajo.

    Cada línea se ajusta a su propio cuerpo: las frases cortas salen grandes y las
    largas más pequeñas, en vez de encogerlo todo al tamaño de la línea más larga.
    """
    lineas = TEXTO_TASA[slug][0]
    p = paleta(modo)
    ilustracion = capa_ilustracion(slug)
    alto_badge = 2700
    y_badge = 340
    if ilustracion:
        escala = alto_badge / ilustracion.height
        badge = ilustracion.resize((int(ilustracion.width * escala), alto_badge), Image.LANCZOS)
        capa.alpha_composite(badge, ((W - badge.width) // 2, y_badge))
        y_texto = 3400
    else:
        y_texto = 1500

    d = ImageDraw.Draw(capa)
    ancho_max = W - 900
    fuentes = [fuente_ajustada(d, l, FUENTE_DISPLAY, 560, ancho_max) for l in lineas]
    colores = [p["principal"], p["acento"]]
    y = y_texto
    for i, (linea, f) in enumerate(zip(lineas, fuentes)):
        texto_centrado(d, y, linea, f, colores[i % 2], W)
        y += int(f.size * 1.02)


# --------------------------------------------------------------------------
# variante horizontal para la taza (siempre sobre taza blanca: modo claro)
# --------------------------------------------------------------------------
def composicion_taza(slug: str, ancho: int, alto: int) -> Image.Image:
    """Variante horizontal para taza blanca.

    Respeta 1,5 cm (180 px) libres junto al asa y en los bordes: en la taza la
    curvatura se come lo que quede pegado al borde.
    """
    lineas, elemento = TEXTO_TASA[slug]
    capa = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    margen = 180

    # Si hay ilustración, la taza lleva el círculo del personaje a la izquierda
    ilustracion = capa_ilustracion(slug)
    if ilustracion is not None:
        alto_badge = min(alto - margen, 820)
        escala = alto_badge / ilustracion.height
        badge = ilustracion.resize((int(ilustracion.width * escala), alto_badge), Image.LANCZOS)
        capa.alpha_composite(badge, (margen, (alto - badge.height) // 2))
        zona_izq = margen + badge.width + 120
        ancho_texto = ancho - zona_izq - margen
        f1 = fuente_ajustada(d, lineas[0], FUENTE_DISPLAY, 200, ancho_texto)
        f2 = fuente_ajustada(d, lineas[1], FUENTE_DISPLAY, 200, ancho_texto)
        f = fuente(FUENTE_DISPLAY, min(f1.size, f2.size))
        cuerpo = f.size
        y = alto // 2 - int(cuerpo * 1.05)
        for i, linea in enumerate(lineas):
            a, _, caja = medir(d, linea, f)
            d.text((zona_izq + (ancho - zona_izq - a) // 2 - caja[0], y + i * int(cuerpo * 1.06)),
                   linea, font=f, fill=hexa(NEGRO if i == 0 else ROJO))
        return capa

    zona_izq = int(ancho * 0.40)
    centro_graf = margen + (zona_izq - 2 * margen) // 2
    # altura de reloj que cabe en la zona gráfica (4 dígitos + 3 separadores)
    alto_reloj = int((zona_izq - 2 * margen) / (4 * 0.62 + 3 * 0.16))

    if elemento == "marco":
        d.rectangle([margen, margen, zona_izq - margen, alto - margen], outline=hexa(ROJO), width=12)
        reloj_digital(capa, centro_graf, alto // 2 - alto_reloj // 2, int(alto_reloj * 0.7), ROJO, "23:59")
    elif elemento == "reloj":
        reloj_digital(capa, centro_graf, alto // 2 - alto_reloj // 2, alto_reloj, NEGRO, "23:59")
    elif elemento == "doc":
        icono_documento(capa, centro_graf - 160, alto // 2 - 260, 320, 520, NEGRO, ROJO)
    elif elemento == "sello":
        d.rounded_rectangle([margen, alto // 2 - 260, zona_izq - margen, alto // 2 + 260], radius=60,
                            outline=hexa(AZUL), width=16)
        texto_centrado(d, alto // 2 - 130, "3:47", fuente(FUENTE_MONO, 220), AZUL, zona_izq, margen, zona_izq - margen)
    elif elemento == "bandas":
        d.rectangle([margen, alto // 2 - 300, zona_izq - margen, alto // 2 - 60], fill=hexa(NEGRO))
        d.rectangle([margen, alto // 2 - 60, zona_izq - margen, alto // 2 + 120], fill=hexa(CREMA))
        d.rectangle([margen, alto // 2 + 120, zona_izq - margen, alto // 2 + 300], fill=hexa(TERRACOTA))
    elif elemento == "pregunta":
        texto_centrado(d, alto // 2 - 300, "¿?", fuente(FUENTE_DISPLAY, 560), ROJO, zona_izq, margen, zona_izq - margen)
    elif elemento == "ticket":
        ticket(capa, margen, alto // 2 - 240, zona_izq - 2 * margen, 460, NEGRO, CREMA, lineas=3)
    elif elemento == "linea":
        trazo_subrayado(capa, margen, zona_izq - margen, alto // 2, ROJO, grosor=24)

    ancho_texto = ancho - zona_izq - 2 * margen
    f1 = fuente_ajustada(d, lineas[0], FUENTE_DISPLAY, 210, ancho_texto)
    f2 = fuente_ajustada(d, lineas[1], FUENTE_DISPLAY, 210, ancho_texto)
    f = fuente(FUENTE_DISPLAY, min(f1.size, f2.size))
    cuerpo = f.size
    y = alto // 2 - int(cuerpo * 1.05)
    for i, linea in enumerate(lineas):
        a, _, caja = medir(d, linea, f)
        x = zona_izq + (ancho - zona_izq - a) // 2
        d.text((x - caja[0], y + i * int(cuerpo * 1.06)), linea, font=f,
               fill=hexa(NEGRO if i == 0 else ROJO))
    return capa


# --------------------------------------------------------------------------
# salidas
# --------------------------------------------------------------------------
def encajar(capa: Image.Image, destino: tuple[int, int], factor: float, y_rel: float = 0.5) -> Image.Image:
    ancho, alto = destino
    escala = (ancho * factor) / capa.width
    nueva = capa.resize((int(capa.width * escala), int(capa.height * escala)), Image.LANCZOS)
    lienzo = Image.new("RGBA", destino, (0, 0, 0, 0))
    lienzo.alpha_composite(nueva, ((ancho - nueva.width) // 2, int((alto - nueva.height) * y_rel)))
    return lienzo


def vista_previa(master: Image.Image, slug: str) -> Image.Image:
    """Vista del arte sobre panel oscuro. No es una foto de producto y así se dice."""
    ancho, alto = 1200, 1500
    lienzo = Image.new("RGB", (ancho, alto), hexa(CREMA))
    d = ImageDraw.Draw(lienzo)
    d.rectangle([30, 30, ancho - 30, alto - 30], outline=hexa(NEGRO), width=3)
    d.rectangle([30, 30, ancho - 30, 130], fill=hexa(NEGRO))
    texto_centrado(d, 58, "VISTA PREVIA DEL DISEÑO", fuente(FUENTE_MONO, 36), CREMA, ancho)
    panel = (70, 160, ancho - 70, alto - 170)
    d.rectangle(panel, fill=hexa(NEGRO))
    util = (panel[2] - panel[0] - 80, panel[3] - panel[1] - 80)
    escala = min(util[0] / master.width, util[1] / master.height)
    reducido = master.resize((max(1, int(master.width * escala)), max(1, int(master.height * escala))), Image.LANCZOS)
    lienzo.paste(reducido, (panel[0] + (panel[2] - panel[0] - reducido.width) // 2,
                            panel[1] + (panel[3] - panel[1] - reducido.height) // 2), reducido)
    texto_centrado(d, alto - 118, "El mockup oficial del producto lo genera la tienda POD",
                   fuente(FUENTE_MONO, 24), NEGRO, ancho)
    return lienzo


def info_md(slug: str, lineas: list[str], colores: list[str], con_ilustracion: bool) -> str:
    return "\n".join([
        f"# {slug}",
        "",
        "Generado con `python scripts/disenos.py`.",
        "",
        "## Reglas aplicadas",
        "",
        *(["- Ilustración de personaje en círculo crema (estilo plano, contorno grueso, tres colores).",
           "  El recorte es geométrico: sin halo negro ni bordes sucios al estampar."] if con_ilustracion else
          ["- Composición tipográfica con elementos geométricos, sin ilustración."]),
        "- La frase está compuesta con **tipografía real** (Arial Black / Segoe UI Black / Consolas Bold).",
        "  Las letras generadas por modelos de imagen se deforman y en una camiseta se ven a un metro.",
        "- Geometría vectorial dibujada a 300 dpi: bordes nítidos, sin artefactos de compresión.",
        "- **Dos variantes de color**: una para prenda oscura y otra para producto claro.",
        "  Subir la clara a un tote crudo o a una taza blanca haría desaparecer el diseño.",
        "",
        "## Frase",
        "",
        *[f"- `{l}`" for l in lineas],
        "",
        "## Colores de marca",
        "",
        *[f"- `{c}`" for c in colores],
        "",
        "## Archivos y para qué sirve cada uno",
        "",
        "| Archivo | Tamaño | Úsalo en |",
        "|---|---|---|",
        "| `master.png` | 4500×5400 | Fuente maestra, variante prenda oscura |",
        "| `master-claro.png` | 4500×5400 | Fuente maestra, variante producto claro |",
        "| `print-area-camiseta.png` | 3000×3600 | Camiseta negra o azul |",
        "| `print-area-camiseta-clara.png` | 3000×3600 | Camiseta crema, blanca o color claro |",
        "| `print-area-tote.png` | 2952×3542 | Tote crudo (variante clara) |",
        "| `print-area-taza.png` | 2475×1155 | Taza blanca (horizontal, con hueco junto al asa) |",
        "| `mockup-web.webp` | 1200×1500 | Vista previa del arte para la web |",
        "",
        "## Antes de vender",
        "",
        "Pasa `designs/CHECKLIST_PRINT.md` y pide una muestra física del diseño estrella.",
    ])


def main() -> None:
    solo = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
    estilo = sys.argv[sys.argv.index("--estilo") + 1] if "--estilo" in sys.argv else "ilustracion"
    datos = json.loads((RAIZ / "data" / "disenos.json").read_text(encoding="utf-8"))
    hechos = 0
    for d in datos:
        slug = d["slug"]
        if solo and slug != solo:
            continue
        carpeta = DISENOS_DIR / slug
        carpeta.mkdir(parents=True, exist_ok=True)

        capas = {}
        for modo in ("oscuro", "claro"):
            capa = Image.new("RGBA", MASTER, (0, 0, 0, 0))
            if estilo == "ilustracion" and capa_ilustracion(slug) is not None:
                composicion_ilustrada(capa, modo, slug)
            else:
                COMPOSICIONES[slug](capa, modo)
            capas[modo] = capa

        capas["oscuro"].save(carpeta / "master.png", dpi=(300, 300))
        capas["claro"].save(carpeta / "master-claro.png", dpi=(300, 300))
        encajar(capas["oscuro"], AREAS["camiseta"], 0.86, 0.46).save(carpeta / "print-area-camiseta.png", dpi=(300, 300))
        encajar(capas["claro"], AREAS["camiseta"], 0.86, 0.46).save(carpeta / "print-area-camiseta-clara.png", dpi=(300, 300))
        encajar(capas["claro"], AREAS["tote"], 0.80, 0.42).save(carpeta / "print-area-tote.png", dpi=(300, 300))
        composicion_taza(slug, *AREAS["taza"]).save(carpeta / "print-area-taza.png", dpi=(300, 300))
        vista_previa(capas["oscuro"], slug).save(carpeta / "mockup-web.webp", "WEBP", quality=88, method=6)
        con_ilus = estilo == "ilustracion" and capa_ilustracion(slug) is not None
        (carpeta / "INFO.md").write_text(
            info_md(slug, d["texto_camiseta"].split("\n"), d["paleta"], con_ilus), encoding="utf-8"
        )
        hechos += 1
        print("compuesto:", slug)

    print(f"Total: {hechos} diseños con 7 archivos cada uno en {DISENOS_DIR}")


if __name__ == "__main__":
    main()
