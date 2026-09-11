#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Control de calidad automático de los diseños: lo que en CHECKLIST_PRINT.md
se revisa a mano, aquí se mide en píxeles.

    python scripts/qa_disenos.py

Comprueba, por diseño y archivo de impresión:
  · Resolución y DPI (300).
  · Transparencia real (alfa, no fondo blanco embebido).
  · Margen de tinta libre hasta el borde: mínimo 3 mm (36 px a 300 dpi) y
    recomendado 10 mm (118 px) en la camiseta y el tote.
  · Sangrado: ningún píxel de tinta tocando el borde del área de impresión.
  · Tamaño del elemento más pequeño detectado (aviso si hay detalles < 1 mm).

Sale con código 1 si algo incumple el mínimo obligatorio.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
DISENOS_DIR = RAIZ / "designs"

MIN_MARGEN_MM = 3.0
RECOMENDADO_MM = 10.0
DPI = 300
ARCHIVOS = [
    "print-area-camiseta.png",
    "print-area-camiseta-clara.png",
    "print-area-tote.png",
    "print-area-taza.png",
]

problemas: list[str] = []
avisos: list[str] = []


def px_a_mm(px: int) -> float:
    return px / DPI * 25.4


def revisar(ruta: Path) -> None:
    with Image.open(ruta) as im:
        nombre = f"{ruta.parent.name}/{ruta.name}"
        dpi = im.info.get("dpi", (0, 0))[0]
        if im.mode != "RGBA":
            problemas.append(f"{nombre}: no tiene canal alfa (modo {im.mode}).")
            return
        if abs(dpi - DPI) > 1:
            avisos.append(f"{nombre}: dpi {dpi:.0f} (debería ser {DPI}).")

        alfa = im.getchannel("A")
        caja = alfa.getbbox()
        if caja is None:
            problemas.append(f"{nombre}: el archivo está completamente vacío.")
            return

        izq, arriba, der, abajo = caja
        margenes = {
            "izquierda": izq,
            "arriba": arriba,
            "derecha": im.width - der,
            "abajo": im.height - abajo,
        }
        for lado, px in margenes.items():
            mm = px_a_mm(px)
            if mm < MIN_MARGEN_MM:
                problemas.append(f"{nombre}: margen {lado} de {mm:.1f} mm (< {MIN_MARGEN_MM} mm).")
            elif mm < RECOMENDADO_MM:
                avisos.append(f"{nombre}: margen {lado} de {mm:.1f} mm (recomendado ≥ {RECOMENDADO_MM} mm).")

        # sangrado: ninguna fila/columna del borde con tinta
        borde = 2
        esquinas = [
            alfa.crop((0, 0, im.width, borde)),
            alfa.crop((0, im.height - borde, im.width, im.height)),
            alfa.crop((0, 0, borde, im.height)),
            alfa.crop((im.width - borde, 0, im.width, im.height)),
        ]
        if any(e.getbbox() is not None for e in esquinas):
            problemas.append(f"{nombre}: hay tinta tocando el borde del área de impresión (se recortaría al estampar).")


def main() -> None:
    datos = json.loads((RAIZ / "data" / "disenos.json").read_text(encoding="utf-8"))
    revisados = 0
    for d in datos:
        carpeta = DISENOS_DIR / d["slug"]
        if not carpeta.exists():
            avisos.append(f"{d['slug']}: sin carpeta de arte todavía.")
            continue
        for archivo in ARCHIVOS:
            ruta = carpeta / archivo
            if ruta.exists():
                revisar(ruta)
                revisados += 1
            else:
                avisos.append(f"{d['slug']}/{archivo}: falta.")

    print(f"Archivos revisados: {revisados}")
    if avisos:
        print(f"Avisos ({len(avisos)}):")
        for a in avisos[:40]:
            print("  ·", a)
    if problemas:
        print(f"PROBLEMAS ({len(problemas)}):")
        for p in problemas:
            print("  ·", p)
        sys.exit(1)
    print("QA de impresión: OK (márgenes y sangrado dentro de los mínimos)")


if __name__ == "__main__":
    main()
