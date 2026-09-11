#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los recursos de marca para configurar la tienda POD y las redes.

Salida en static/img/marca/ (y se copian a dist/assets/img/marca/ al compilar).

    python scripts/brand_assets.py

Recursos:
    logo-cuadrado.png   1000×1000  avatar/logo de tienda
    banner-hero.png     1600×900   cabecera de tienda y OG de redes
    banner-canal.png    1280×720   cabecera de canal/YouTube y post de anuncio
    favicon.png          512×512   icono

Solo usa la librería estándar + Pillow. Si Pillow no está, aborta con un mensaje claro.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "static" / "img" / "marca"

NEGRO = (17, 17, 17)
CREMA = (244, 239, 230)
ROJO = (178, 58, 46)
AZUL = (14, 27, 42)
AMARILLO = (228, 197, 107)

FUENTES = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/Arialbd.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
    "C:/Windows/Fonts/consolab.ttf",
]
FUENTE_MONO = [
    "C:/Windows/Fonts/consolab.ttf",
    "C:/Windows/Fonts/courbd.ttf",
]


def cargar_fuente(tamanos: list[str], tam: int):
    from PIL import ImageFont

    for ruta in tamanos:
        if Path(ruta).exists():
            return ImageFont.truetype(ruta, tam)
    return ImageFont.load_default()


def centrar(draw, texto, font, ancho, y, color):
    caja = draw.textbbox((0, 0), texto, font=font)
    draw.text(((ancho - (caja[2] - caja[0])) / 2, y), texto, font=font, fill=color)


def logo_cuadrado() -> None:
    from PIL import Image, ImageDraw

    W = H = 1000
    img = Image.new("RGB", (W, H), AZUL)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, W - 40, H - 40], outline=CREMA, width=6)
    f_arriba = cargar_fuente(FUENTES, 92)
    f_hora = cargar_fuente(FUENTE_MONO, 250)
    f_pie = cargar_fuente(FUENTES, 46)
    centrar(d, "LLAMAMIENTO", f_arriba, W, 150, AMARILLO)
    centrar(d, "23:59", f_hora, W, 330, CREMA)
    d.rectangle([330, 640, 670, 660], fill=ROJO)
    centrar(d, "MERCH DE TRIBU DOCENTE", f_pie, W, 720, CREMA)
    centrar(d, "CANARIAS", f_pie, W, 790, AMARILLO)
    img.save(SALIDA / "logo-cuadrado.png", "PNG")


def banner_hero(ancho: int, alto: int, nombre: str, subtitulo: str, linea2: str) -> None:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (ancho, alto), AZUL)
    d = ImageDraw.Draw(img)
    escala = ancho / 1600
    margen = int(80 * escala)
    disponible = ancho - 2 * margen

    def fuente_ajustada(texto: str, ideal: int, rutas: list[str]):
        for tam in range(ideal, 12, -4):
            f = cargar_fuente(rutas, tam)
            caja = d.textbbox((0, 0), texto, font=f)
            if caja[2] - caja[0] <= disponible:
                return f
        return ImageFont.load_default()

    d.rectangle([0, alto - int(22 * escala), ancho, alto], fill=ROJO)
    f_top = cargar_fuente(FUENTE_MONO, int(46 * escala))
    f_big = cargar_fuente(FUENTES, int(190 * escala))
    f_sub = fuente_ajustada(subtitulo, int(62 * escala), FUENTES)
    f_sub2 = fuente_ajustada(linea2, int(62 * escala), FUENTES)
    d.text((margen, int(70 * escala)), "LLAMAMIENTO", font=f_top, fill=AMARILLO)
    d.text((margen, int(130 * escala)), "23:59", font=f_big, fill=CREMA)
    d.text((margen, int(410 * escala)), subtitulo, font=f_sub, fill=CREMA)
    d.text((margen, int(505 * escala)), linea2, font=f_sub2, fill=AMARILLO)
    img.save(SALIDA / nombre, "PNG")


def favicon() -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (512, 512), NEGRO)
    d = ImageDraw.Draw(img)
    f = cargar_fuente(FUENTE_MONO, 190)
    centrar(d, "23", f, 512, 70, CREMA)
    centrar(d, "59", f, 512, 270, ROJO)
    img.save(SALIDA / "favicon.png", "PNG")


def main() -> None:
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Falta Pillow. Instálalo con: python -m pip install pillow")
        sys.exit(1)

    SALIDA.mkdir(parents=True, exist_ok=True)
    logo_cuadrado()
    banner_hero(
        1600, 900, "banner-hero.png",
        "Camisetas, totes y tazas para docentes interinos",
        "Humor de tribu · Canarias · impresión bajo demanda",
    )
    banner_hero(
        1280, 720, "banner-canal.png",
        "Merch de tribu para docentes interinos",
        "Sigo en lista de espera · Canarias",
    )
    favicon()
    for f in sorted(SALIDA.glob("*.png")):
        from PIL import Image

        with Image.open(f) as im:
            print(f"{f.relative_to(RAIZ)}  {im.size[0]}×{im.size[1]}")


if __name__ == "__main__":
    main()
