# ACTIVACION.md — lo que falta para que la tienda cobre de verdad

Todo lo demás está hecho y publicado. Quedan **3 bloqueos reales** que solo puede resolver el titular,
porque implican su email, su identidad fiscal y su banco. Ninguno lleva más de 20 minutos.

---

## Bloqueo 1 · Crear la cuenta de la plataforma (10 min) — el único paso imprescindible

1. Entrar en https://fourthwall.com/get-started
2. Registrarse con el email de la tienda (o el personal, da igual: será el email de avisos de pedidos).
3. Elegir el nombre de usuario de la tienda. **Sugerencia (coherente con la marca)**: `llamamiento2359`
   → la URL provisional quedaría `https://llamamiento2359-shop.fourthwall.com`.
   El nombre de usuario (`llamamiento2359`) se reserva sin pagar nada.
4. En *Settings → Payouts*, configurar la cuenta de cobro (banco o PayPal). Sin esto no se puede publicar.
5. En *Settings → Taxes*, declarar el domicilio fiscal. **Aquí hay que decidir con el asesor**: si el domicilio está en Canarias, el régimen propio es **IGIC**; si está en península o Baleares, **IVA**. La plataforma actúa como *Merchant of Record* y recauda el impuesto correspondiente al destino, pero el alta fiscal del titular es cosa suya.
6. En *Settings → Domains*, conectar el dominio (los registros están en `docs/DNS.md`, opción B). Si no se conecta ahora, la tienda funciona igual en su URL de fourthwall.com.

**Qué necesito yo para hacerlo por ti**: si prefieres delegarlo, dime el email y te dejo el formulario relleno hasta el paso de la verificación (el código de verificación lo tendrás que abrir tú). No guardo ni te pido nunca contraseñas.

## Bloqueo 2 · Arte (esta noche el humano, el tiempo que necesite)

- Generar los PNG siguiendo `designs/PROMPTS_FOOOCUS.md`, `PROMPTS_COMFYUI.md` o `PROMPTS_GEMINI.md`.
- Guardarlos con la nomenclatura de `designs/README.md`.
- El diseño 03 (Llamamiento 23:59) conviene hacerlo primero: es la pieza de marca y sirve para la muestra física.

## Bloqueo 3 · Productos y precios finales (15 min)

Por cada diseño (8) × producto (3):

1. *Products → Create product* → camiseta / tote / taza.
2. Subir el `print-area-*.png` correspondiente según la plantilla que muestre la plataforma.
3. Poner el precio de `data/productos.json` (22,90 / 17,90 / 15,90 €) y comprobar el coste base real.
4. Copiar la **URL de compra del producto** y pegarla en `data/disenos.json`, en el campo `checkout_url` del diseño correspondiente.
5. En `data/disenos.json`, cambiar `"estado": "pendiente_arte"` por `"estado": "listo"`.

Después:

```
python build.py --check
bash scripts/publish.sh
```

Con eso la ficha de producto pasa de «Avísame cuando esté» a botón de compra real que lleva al checkout nativo.

## Bloqueo 4 (opcional, 5 min) · Dominio y correo

- Decidir entre opción A u opción B de `docs/DNS.md` y aplicar los registros.
- Si se quiere buzón propio, seguir el apartado 3 de `DNS.md`. Si no, se puede usar un alias del correo actual y actualizar `data/site.json → email_contacto`.

---

## Prueba de extremo a extremo (10 min, después de los pasos anteriores)

1. Crear un producto de prueba con precio **1,00 €** y título `TEST-NO-COMPRAR`.
2. Comprarlo con una tarjeta real (o el modo test de la pasarela si la plataforma lo ofrece).
3. Comprobar los emails: confirmado, en producción, en camino con el carrier real y su tracking.
4. Consultar el estado en https://ray86-dev.github.io/camisetas-interinos/seguimiento/ con el número de pedido y el email usado.
5. Verificar que el número de seguimiento del email coincide con el que devuelve el portal del carrier.
6. Borrar el producto de prueba y anotar el resultado (fecha, carrier, plazo real) en `docs/TIENDA.md`.
7. Añadir la fila del pedido real a `data/pedidos.json` si se quiere que el buscador lo muestre a alguien (el portal del POD ya muestra el estado al cliente; nuestra página es un extra).

## Lo que NO hay que hacer

- No hace falta contratar Shopify, VPS ni Printify Premium: el plan Free elegido cubre todo.
- No hace falta configurar webhooks ni claves API para el lanzamiento.
- No hace falta que el titular confirme pedidos a mano: la plataforma los envía al taller y avisa al cliente sola.
- No hace falta Bizum ni transferencias: el checkout nativo acepta tarjeta, PayPal y Apple/Google Pay.

## Si la plataforma no convence tras verla por dentro

Plan B en dos pasos, sin rehacer nada de la web:

1. Crear una **Printify Pop-Up Store** (gratis, disponible para vendedores en España) y verificar Stripe.
2. Pegar las URLs de compra de cada producto en `data/disenos.json → checkout_url` y republicar.

El escaparate, los legales, el seguimiento y el catálogo sirven igual con las dos plataformas.
