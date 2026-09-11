# ARTE.md — cómo se han hecho los 8 diseños y cómo se sustituyen

## Resumen

Los **8 diseños están compuestos y listos para imprimir** (`designs/<slug>/`, 7 archivos por diseño,
56 en total, 7,5 MB). Están generados con tipografía real y geometría vectorial a 300 dpi mediante
`scripts/disenos.py`, y validados con `scripts/qa_disenos.py`.

**No llevan texto generado por IA.** Y no es una limitación, es la decisión correcta: en estos 8 diseños
la frase *es* el diseño, y los modelos de imagen escriben mal las frases largas. Un error de una letra se
ve a un metro de distancia en una camiseta.

## Qué ha pasado con Fooocus

Se intentó usar Fooocus para los elementos gráficos, en cuatro intentos distintos:

1. `launch.py --preset lustify` (sin PTY): el proceso moría con un error de terminal (`tcsetattr`).
2. `launch.py --preset merch` con PTY: arrancó, cargó SDXL, imprimió `Running on local URL: http://127.0.0.1:7865`,
   pero el puerto no aceptó ni una conexión (el log se detiene justo ahí, sin traza de error).
3. Lanzado por `cmd /c start` y por `powershell Start-Process` con redirección: los ficheros de log quedaron
   a 0 bytes y el puerto seguía cerrado.
4. Verificación cruzada: `netstat` solo mostraba conexiones `TIME_WAIT` de los intentos previos y **ningún**
   socket en escucha.

Contexto que descarta las causas fáciles: la GPU (RTX 3060 Ti, 8 GB) está libre, el modelo existe en disco
(`D:\ComfyUI_models\checkpoints\RealVisXL_V4.0.safetensors`, vía `path_checkpoints` del `config.txt`), los
auxiliares (`vae_approx`, `clip_vision`, `fooocus_expansion`) están descargados y la RAM disponible era de
6,6 GB. Se creó un preset propio (`D:\Fooocus\presets\merch.json`, modelo RealVisXL) para no depender del
preset fotográfico. El servidor de Gradio es lo único que no llega a levantar.

Vía de arreglo (de la skill `fooocus-windows`), para cuando interese el acento gráfico generado:

1. Comprobar `curl http://127.0.0.1:7865/info`: si responde 500, es el desajuste gradio/gradio_client.
   Reinstalar el stack clavado: `fastapi==0.103.2 starlette==0.27.0 uvicorn==0.23.2 pydantic==2.8.2 gradio-client==0.5.0`.
2. Arrancar Fooocus desde una consola interactiva normal (no desde el agente): es donde el arranque se comporta.
3. Si se automatiza la interfaz, mantener la pestaña en primer plano: con la pestaña en segundo plano
   Gradio congela el pipeline y el botón Generate no encola nada.

Mientras eso no se resuelva, `designs/PROMPTS_FOOOCUS.md` sigue siendo válido y el usuario puede generarlos
a mano en dos clics.

## Cómo sustituir un diseño por el arte del humano (Fooocus o Gemini)

La nomenclatura es la misma para todos, así que **basta sobrescribir los archivos**:

    designs/<slug>/
      master.png                  ← fuente maestra, prenda oscura
      master-claro.png            ← fuente maestra, producto claro
      print-area-camiseta.png     ← camiseta oscura
      print-area-camiseta-clara.png
      print-area-tote.png         ← tote crudo
      print-area-taza.png         ← taza blanca (horizontal)
      mockup-web.webp             ← vista previa que aparece en la web

Después:

    python scripts/qa_disenos.py     # márgenes, sangrado, dpi, transparencia
    python build.py --check          # recoge la nueva preview y publica la web
    bash scripts/publish.sh

Si el arte nuevo viene de Gemini, aviso importante: **exportar con transparencia real** y quitar el fondo
plano. Y si la imagen trae texto generado, rehacer la frase con tipografía real antes de subirla.

## Dos variantes por diseño (esto es importante)

No es lo mismo imprimir sobre camiseta negra que sobre tote crudo o taza blanca. Por eso cada diseño tiene
dos variantes de color:

| Variante | Colores | Va en |
|---|---|---|
| Oscura | crema, amarillo, rojo, azul claro | camiseta negra, azul noche, gris oscuro |
| Clara | negro, rojo apagado, azul noche | camiseta blanca o crema, tote crudo, taza blanca |

Subir la variante oscura a un tote crudo deja el diseño invisible. Lo dice el propio `INFO.md` de cada diseño.

## Qué sigue pendiente

- Confirmar el arte con una **muestra física** antes de anunciar la tienda (diseño 03 como primero).
- Subir los archivos al POD según `docs/PANEL_FOURTHWALL.md` y pegar las URLs en `data/disenos.json`.
- Si el humano produce sus versiones (Gemini), comparar y quedarse con una: no se venden dos artes del mismo chiste.
