# PANEL_FOURTHWALL.md — configuración de la tienda POD

Cuenta creada por el titular el 11-09-2026 con **rayco86@protonmail.com**.
Este documento recoge qué está configurado, qué falta y **con qué valores exactos** hacerlo.

## 1. Estado verificado en el panel

| Dato | Valor |
|---|---|
| Panel | https://admin.fourthwall.com/store/ray-mga/ |
| Identificador de tienda | `ray-mga` |
| URL gratuita de la tienda | `https://ray-mga-shop.fourthwall.com` → hoy redirige a `/password` (tienda **en prelanzamiento protegida**: nadie la ve hasta pulsar «Go live») |
| Plan | Free (0 €/mes) |
| Productos | **0**: todavía no hay ninguno creado (falta el arte) |
| Ajustes que cargan | Shipping, Domain, Checkout, For developers, Platform apps, Billing and payouts |
| Ajustes que fallaban | **General** devolvía «Something went wrong» en dos intentos (error de la propia aplicación; reintentar más tarde) |

Se intentó cambiar el subdominio gratuito de `ray-mga` a `llamamiento2359` en *Settings → Domain*: el formulario aceptó el valor pero **el guardado no llegó a completarse** (el navegador se cerró por falta de memoria del equipo antes de confirmar). `https://llamamiento2359-shop.fourthwall.com` devuelve 404, así que hay que repetirlo.

> Motivo técnico registrado: el equipo tiene 15,7 GB de RAM y estaba al 88 % de uso con el navegador de automatización abierto; el proceso del navegador falló con un error de asignación de memoria. No es un problema de la cuenta ni de la tienda.

## 2. Configuración pendiente, con los valores exactos

### 2.1 Domain (2 minutos)
1. *Settings → Domain → Fourthwall domain*: cambiar `ray-mga` por **`llamamiento2359`** (si estuviera ocupado: `llamamiento-2359`). Guardar y comprobar que `llamamiento2359-shop.fourthwall.com` responde.
2. *Custom domain*: cuando el titular elija dominio, conectarlo aquí y copiar los registros que muestre el propio panel (ver `DNS.md`, opción B).

### 2.2 General (5 minutos)
Los valores de marca que pide la plataforma:

| Campo | Valor |
|---|---|
| Nombre de la tienda | **Llamamiento 23:59** |
| Descripción corta | Merch de tribu para docentes interinos de Canarias |
| Moneda | **EUR (€)** |
| Idioma | **Español** |
| País / región | **España** |
| Color de marca | `#0E1B2A` (azul noche) |
| Color de acento | `#B23A2E` (rojo apagado) |
| Color de texto sobre acento | `#F4EFE6` (crema) |
| Logo | `static/img/marca/logo-cuadrado.png` (1000×1000) |
| Banner de cabecera | `static/img/marca/banner-hero.png` (1600×900) |
| Redes | Instagram/TikTok: pendientes de crear |

### 2.3 Shipping (3 minutos)
- *Shipping pricing for products we ship for you*: **no hay que tocar nada**, los clientes pagan el coste real del envío calculado por peso y destino (así Canarias se cobra bien).
- *Restrict the countries where I ship*: **dejar sin restringir** (o permitir España, resto de UE y resto del mundo). No restringir a «España» excluye Canarias en algunos formularios de terceros: comprobarlo en el checkout con un código postal 38410 y otro 35001.
- Envío gratis a partir de **60 €** (opcional, recomendado para subir el ticket medio). Si se activa, actualizar también `data/site.json → envio.gratis_desde_eur`.
- *Shipping pricing for products you ship yourself*: no aplica (no hay stock propio). Dejar en «Fixed shipping rates» por si algún día se añade algo manual.

### 2.4 Checkout (2 minutos)
- Métodos de pago: dejar activos tarjeta, **PayPal**, **Apple Pay / Google Pay** (Fourthwall es el vendedor registrado y ya los soporta).
- Idioma y moneda del checkout en **es-ES / EUR**.
- Revisar que el aviso automático de aduanas aparece en carritos cross-border: es la única forma de que el cliente canario sepa por adelantado que puede pagar IGIC. Si no aparece, añadir la nota a mano en la página de envíos de la tienda (texto en el punto 2.6).

### 2.5 Billing and payouts (solo el titular)
- Cuenta bancaria o PayPal de cobro: **solo la puede configurar el titular**.
- Datos fiscales (NIF y domicilio): si el domicilio está en Canarias el régimen propio es **IGIC**; si está en península o Baleares, **IVA**. Confirmar con el asesor antes de la apertura.
- Sin este apartado completo no se puede pulsar «Go live».

### 2.6 Páginas de la tienda (textos listos para pegar)

**Sobre / About**

> Merch de tribu para docentes interinos de Canarias. Hacemos camisetas, totes y tazas con los chistes que nos contamos en la sala de profesores: sin escudos, sin siglas sindicales, sin logos de ninguna administración y sin usar el nombre de nadie.
>
> Todo se imprime bajo demanda: nada se fabrica hasta que alguien lo pide. Enviamos a Canarias y a la península, y contamos los plazos reales antes de que compres.

**Envíos (Shipping policy)**

> Producción: 3-5 días laborables. Canarias: 6-14 días laborables en total. Península y Baleares: 5-9 días. Resto de la UE: 7-14 días.
>
> Imprimimos en talleres de España y de la Unión Europea y asignamos el transportista que llega antes a cada destino: Correos, Correos Express, DHL, GLS o SEUR. Cuando el envío no es con Correos, lo decimos con el nombre real del transportista y damos su número de seguimiento.
>
> Los envíos a Canarias pasan por despacho aduanero (DUA). Según la ruta, el importe puede ir ya cobrado en el checkout (derechos pagados) o reclamarlo el transportista al entregar. Lo indicamos en el propio proceso de pago.

**Devoluciones (Returns policy)**

> Los artículos son personalizados y se imprimen tras la compra, por lo que no existe derecho de desistimiento (art. 103.f LGDCU). Si el artículo llega con defecto de impresión, con una talla, color o diseño equivocados o dañado en el transporte, lo reimprimimos o devolvemos el importe, incluidos los gastos, sin discusión. Escríbenos con fotos y el número de pedido en un plazo de 30 días desde la recepción.

**FAQ (las preguntas que ya están en la web)**: se pueden copiar de https://ray86-dev.github.io/camisetas-interinos/faq/.

### 2.7 Mensajes de la tienda
Los cuatro textos de email (pedido confirmado, en producción, en camino con carrier real, incidencia) están en `docs/EMAILS.md`. En Fourthwall se pegan en los mensajes personalizados de la tienda y en el correo de confirmación; el envío de los estados lo hace la plataforma de forma nativa.

### 2.8 Productos (cuando exista el arte)
Por cada diseño (8) × producto (3): *Create a new product* → camiseta / tote / taza → subir `print-area-*.png` → fijar precio (22,90 / 17,90 / 15,90 €) → publicar → copiar la URL del producto en `data/disenos.json → checkout_url` y cambiar `estado` a `listo` → `python build.py --check && bash scripts/publish.sh`.

## 3. Bloqueos que quedan (todos del titular)

| Bloqueo | Quién | Por qué |
|---|---|---|
| Cuenta de cobro y datos fiscales | Titular | KYC bancario y alta fiscal |
| Dominio (aún sin elegir) | Titular | Decisión de marca |
| Arte de los 8 diseños | Titular | Fooocus/ComfyUI/Gemini según `designs/` |
| RAM del equipo para terminar la configuración por automatización | Titular | 15,7 GB con 88 % en uso: cerrar aplicaciones antes de que el agente vuelva a navegar |

## 4. Aviso de seguridad

La contraseña de la cuenta de Fourthwall se envió por el chat: **no se ha usado, no se ha guardado y no se usará**. Recomendación: cambiarla en *Settings → General → Password* (o desde el enlace «Forgot password» de auth.fourthwall.com) y no reutilizarla en ningún otro sitio. Para futuras sesiones, la contraseña se guarda en el gestor cifrado de Hermes desde la propia pantalla de acceso, sin pasar por el chat.
