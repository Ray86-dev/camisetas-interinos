# Emails automáticos de pedido — qué envía la plataforma y con qué texto

La tienda no envía emails propios: los envía la plataforma de impresión bajo demanda (vendedor registrado)
al email que el cliente deja en el checkout. Esto es lo que cubre hoy y lo que hay que comprobar al activar la cuenta.

## 1. Qué debe quedar configurado en la plataforma

| Momento | Email | Contenido mínimo | ¿Automático? |
|---|---|---|---|
| Pago aceptado | **Pedido confirmado** | Número de pedido, artículos, importe con impuestos, dirección | Sí, nativo |
| El taller acepta | **En producción** | Aviso de que la pieza se está fabricando (3-5 días laborables) | Sí, nativo |
| Sale del taller | **En camino** | Nombre del carrier real + número de seguimiento + enlace | Sí, nativo |
| Entrega | **Entregado** (si el carrier lo reporta) | Confirmación | Sí, nativo |

El humano **no confirma pedidos a mano** en ningún caso. Si un email no llega, se revisa la configuración de la tienda, no se parchea escribiendo correos manuales.

## 2. Plantillas de texto (para pegar en «custom messages» de la plataforma)

### A. Pedido confirmado
> Asunto: Pedido {NUMERO} confirmado — {MARCA}
>
> Ya tenemos tu pedido {NUMERO}. Esto es lo que viene ahora:
> · Producción: 3-5 días laborables en el taller.
> · Envío a Canarias: 6-14 días laborables en total desde hoy. A la península, 5-9 días.
> · Te escribiremos otra vez cuando salga del taller, con el nombre del transportista y el número de seguimiento.
>
> Puedes consultar el estado cuando quieras en {URL}/seguimiento/ con tu número de pedido y este email.
>
> Cualquier duda: {EMAIL}. Respondemos en menos de 24 horas laborables.

### B. En producción
> Asunto: Tu pedido {NUMERO} está en producción
>
> Tu pieza está en la cola del taller. No hay stock: se imprime la tuya. Tarda 3-5 días laborables en estar lista para salir.
> Si tu envío va a Canarias, recuerda que después pasa por despacho aduanero y el transportista puede liquidar el IGIC en la entrega cuando la ruta no se cobró con derechos pagados.

### C. En camino (el importante: nunca decir «Correos» si no es Correos)
> Asunto: Tu pedido {NUMERO} va en camino
>
> Te hemos enviado con **{CARRIER}**. Tracking: **{CODIGO}**
> Síguelo aquí: {ENLACE_SEGUIMIENTO}
>
> ¿Por qué no es siempre Correos? Imprimimos en talleres de España y de la Unión Europea y elegimos el transportista que llega antes a tu isla. Si el que te toca es Correos Express, DHL o GLS, te lo decimos con su nombre real: no vamos a llamar Correos a un envío que no lo es.
>
> Si el seguimiento tarda unas horas en actualizarse tras el relevo entre transportistas, es normal.

### D. Incidencia / retraso (manual, solo si hay un problema real)
> Asunto: Tu pedido {NUMERO} se retrasa — te contamos por qué
>
> {MOTIVO_CONCRETO}. Nueva fecha estimada: {FECHA}. Si prefieres cancelar y que te devolvamos el importe, responde a este correo y lo hacemos sin preguntas.

## 3. Cómo se comprueba que funcionan (prueba E2E)

1. Crear un producto de prueba con precio 1 € y título `TEST-NO-COMPRAR`.
2. Hacer un pedido real con la cuenta del titular (modo test de la pasarela si existe).
3. Verificar los tres emails (confirmado, en producción, enviado) y que el tracking apunta al carrier correcto.
4. Consultar el estado en `/seguimiento/` con número y email.
5. Borrar/ocultar el producto de prueba y anotar el resultado en `docs/TIENDA.md`.

## 4. Seguimiento en la web

El buscador de `/seguimiento/` lee `data/pedidos.json` (público, sin datos sensibles: número de pedido, email, estado, carrier y tracking). Se actualiza pegando las filas del pedido cuando la plataforma no ofrezca exportación automática. Si algún día se automatiza, se hará con la API de la plataforma y un cron; nunca inventando estados.

**Privacidad**: el buscador exige número de pedido **y** email exactos, y no usa cookies. No expone direcciones postales ni importes.
