# RUNBOOK_PEDIDO.md — qué hacer cuando algo sale mal con un pedido

Regla general: **el cliente no se queda sin respuesta y no se le miente con el plazo**. Todo lo de abajo se resuelve desde el panel de la plataforma POD y el email de contacto de la tienda.

## 0. Datos que hay que pedir siempre

- Número de pedido (formato `LL-0000` o el que asigne la plataforma).
- Email de compra.
- Fecha de compra y qué esperaba.
- Si es defecto: **fotos** del artículo y del paquete.
- Si es dirección: dirección completa tal cual la escribió (calle, número, piso, CP, municipio, isla).

## 1. El pago se ha cobrado pero no hay pedido en el panel POD

1. Buscar por email del cliente y por importe en el panel.
2. Si no aparece: revisar el estado en la pasarela (Stripe/PayPal). Un pago «autorizado» sin capturar no genera pedido.
3. Si el dinero salió y no hay pedido: **reembolso inmediato** desde la pasarela y avisar al cliente por email explicando que se repite el pedido o se le devuelve el importe, a su elección.
4. Registrar el caso en `data/pedidos.json` como incidencia con nota visible.

## 2. El pedido se queda en «En producción» más de 5 días laborables

1. Abrir el pedido en el panel y mirar si tiene avisos (dirección incompleta, archivo rechazado por calidad).
2. Abrir incidencia con el taller desde el propio panel (o email de soporte del POD con el número).
3. Escribir al cliente **antes** de que pregunte: motivo concreto y nueva fecha estimada. Usar la plantilla D de `docs/EMAILS.md`.
4. Si el retraso supera los 10 días laborables en producción, ofrecer reimpresión express o reembolso completo.

## 3. El POD cancela o rechaza el pedido

1. Motivo habitual: el imprimible no cumple requisitos (resolución, transparencia, sangre).
2. Corregir el arte (ver `designs/CHECKLIST_PRINT.md`), volver a subirlo y **relanzar el pedido** sin coste para el cliente.
3. Si la cancelación es definitiva: reembolso completo en 24 h.
4. Anotar en `data/pedidos.json` y en `docs/TIENDA.md` la causa para no repetirla con ese diseño.

## 4. El paquete no avanza en el seguimiento

1. Contrastar el estado en el portal **del carrier real** (ver la tabla de `data/carriers.json`), no en el correo.
2. Los relevos entre transportistas son normales: el número puede quedarse en «etiqueta creada» de 2 a 5 días. Informar al cliente con esa explicación.
3. Plazos antes de declarar pérdida: **2 semanas** en península, **3 semanas** en Canarias desde la fecha de envío.
4. Pasado el plazo: reimprimir y reenviar sin coste, o reembolsar. Lo decide el cliente.

## 5. El paquete llega dañado o con defecto

1. Pedir fotos del artículo y del embalaje.
2. No discutir: en productos personalizados no hay desistimiento, pero **sí hay garantía por falta de conformidad**.
3. Abrir incidencia al POD (la cobertura de daños y errores de fabricación suele cubrir reimpresión o reembolso en 30 días).
4. Responder al cliente en menos de 24 h laborables con la decisión: reimpresión o reembolso.

## 6. Devolución por decisión del cliente (sin defecto)

1. Explicar con educación la excepción del art. 103.f LGDCU: es producto personalizado, no hay desistimiento.
2. Excepciones que sí se aceptan como gesto comercial (y se valoran caso a caso): talla equivocada en el primer pedido, error nuestro en la ficha, artículo sin estrenar y en plazo de 14 días.
3. Si se acepta: la devolución la paga el cliente y el artículo debe volver al taller/almacén que indique el POD. No se reembolsa el envío original salvo error nuestro.

## 7. Canarias: aduanas e IGIC

1. Si el cliente se queja de un cargo del transportista: explicar que es el DUA/IGIC de entrada en las islas y que en las rutas DDU lo cobra el transportista.
2. Si la ruta era DDP (derechos pagados en el checkout) y le vuelven a cobrar: reclamar al POD con la factura del transportista y **reembolsar al cliente** ese importe mientras se resuelve.
3. Nunca prometer que «no pagará nada» si la ruta es DDU. En la web se explica en FAQ, en ficha y en Envíos y devoluciones.

## 8. Reembolsos: cómo y en cuánto tiempo

- **Quién**: la pasarela de la plataforma (Stripe/PayPal) o el propio panel del POD si la incidencia es de fabricación.
- **Plazo legal**: máximo 14 días naturales desde que se acepta el desistimiento; por error nuestro, se hace en 24-48 h.
- **Medio**: siempre el mismo que usó el cliente. Nunca Bizum, nunca transferencia manual.
- **Importe**: completo (artículo + envío) si el fallo es nuestro; solo el artículo si es un gesto comercial sin defecto.

## 9. Reenvíos

- Dirección incorrecta por parte del cliente: el nuevo envío lo paga el cliente. Se reenvía solo tras confirmar la dirección corregida por escrito.
- Error nuestro o del POD: el reenvío va a cargo de la tienda, con el mismo producto y diseño.
- Dejar siempre rastro: actualizar la fila del pedido en `data/pedidos.json` (estado, carrier, tracking y nota).

## 10. Escalado

| Situación | A quién se acude | Tiempo de respuesta esperado |
|---|---|---|
| Pedido atascado en producción | Soporte del POD con el número de pedido | 24-48 h |
| Cargo duplicado o fraude | Pasarela de pago (Stripe/PayPal) | 24 h |
| Paquete perdido | Carrier, con el número de seguimiento | 48-72 h |
| Reclamación formal de consumo | Se facilita la hoja de reclamaciones y la vía de la junta arbitral | — |

## 11. Registro de incidencias

Cada incidencia se anota en `data/pedidos.json` con una `nota` breve y visible para el cliente, y si revela un fallo del sistema (arte que no cumple, plazo mal calculado, carrier equivocado), se corrige en el repo **el mismo día**: el generador y esta documentación se actualizan juntos.
