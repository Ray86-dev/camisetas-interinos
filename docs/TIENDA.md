# TIENDA.md — decisiones, URLs y dónde se configura cada cosa

Fecha de montaje: 11 de septiembre de 2026 · Autor del montaje: agente Hermes (a partir del encargo del titular)
Documento vivo: cada decisión nueva se añade aquí con su fecha.

---

## 1. URL pública (ya visitable)

- **Web publicada hoy**: https://ray86-dev.github.io/camisetas-interinos/
- Repositorio: https://github.com/ray86-dev/camisetas-interinos (público, rama `gh-pages` sirve el contenido generado; `master` es el código fuente)
- Estado: **prelanzamiento honesto**. La web está en vivo, el catálogo de 24 productos (8 diseños × 3) está completo y las fichas funcionan, pero **no hay botón de compra** porque los imprimibles no existen todavía y no se vende un diseño vacío.
- Los 3 productos placeholder «PRÓXIMAMENTE» están solo en `/_borrador/` (noindex, fuera del menú y del sitemap), tal como pedía el plan.

## 2. Decisión de stack

### Opción elegida: **A — Fourthwall plan Free (vendedor registrado) + producción en España/UE**

Motivos, con datos verificados el 11-09-2026:

| Criterio | Fourthwall Free | Printify Pop-Up | Gelato | Frontend propio + Stripe |
|---|---|---|---|---|
| Coste recurrente | 0 € (plan Free; Pro es opcional a 15 $/mes) | 0 € | 0 € (solo pagas producción) | 0 € de hosting, pero hay que montar webhooks |
| ¿Tienda incluida? | Sí, tienda completa con dominio propio | Sí, pop-up store | No: necesitas Shopify/Etsy/Wix | Sí, pero la construyes tú |
| Checkout | Nativo, con tarjeta, PayPal, Apple/Google Pay y Amazon Pay | Sí, con Stripe | Lo pone la plataforma conectada | Stripe Checkout (requiere cuenta y webhooks) |
| Vendedor registrado (impuestos) | Sí: Fourthwall actúa como *Merchant of Record*, recauda y liquida los impuestos | No: el vendedor es el usuario y debe verificar Stripe | No | No |
| Producción | Red de talleres en UE (incluye rutas con taller español) | Talleres propios en varios países, hay proveedores europeos | Red de 250+ talleres en 32 países, con talleres en España | La que conectes |
| Tracking automático | Sí: estados Placed / In production / Shipped + número y portal del carrier | Sí | Sí | Hay que programarlo |
| Portal de seguimiento para el cliente | Sí, nativo (no hay que reinventarlo) | Básico | No | Hay que programarlo |

Fuentes de la comparación: `fourthwall.com/pricing`, `help.fourthwall.com` (envíos y plazos), `printify.com/pop-up-store`, `help.printify.com` (Pop-Up y verificación Stripe), `gelato.com/es/print-on-demand/españa`, `printful.com` (centro de Barcelona) y `help.printful.com` (regiones de envío).
Además: Printify cambió en 2025 el modelo de cobro de su Pop-Up (el vendedor pasa a ser responsable y debe verificar Stripe), lo que añade configuración manual — justo lo que el encargo quería evitar.

### Producción y plazos a Canarias (para 38410 Tenerife y 35001 Las Palmas)

- **Producción**: 3-5 días laborables en todos los casos (dato de Fourthwall y de Printful).
- **Printful tiene centro en Barcelona** (Sant Climent de Llobregat): pedidos domésticos peninsulares en unos 3 días laborables tras fabricación. Es el taller que interesa para España.
- **Canarias no es península**: el envío pasa por declaración aduanera (DUA). Referencias reales consultadas: Packlink (entrega 2-4 días *excluyendo* despacho aduanero), GLS y Bigblue (guías de aduanas Canarias), Correos (tramitación aduanera de importación).
- **Plazo publicado en la tienda: 6-14 días laborables a Canarias** y 5-9 a península. Es un rango honesto con el colchón aduanero incluido, no una promesa de 24 horas.
- **Rutas DDP**: Fourthwall informa de que en las rutas europeas servidas con DHL eCommerce ya cobra los derechos en el checkout (3 € por artículo en pedidos ≤150 €), con ampliación progresiva a más talleres. En las rutas que aún son DDU, el IGIC y los gastos de gestión se pagan a la entrega. La web lo explica en FAQ, en la ficha de producto y en «Envíos y devoluciones» sin esconderlo.

### Por qué no las otras

- **B (Printify Pop-Up)**: descartada por defecto. Disponible en España (sí), pero el vendedor pasa a ser responsable del cobro y debe verificar Stripe, y el tracking/portal es más pobre. Queda documentada como plan B en el apartado 7.
- **C (Gelato)**: descartada. Buena red de talleres, pero no ofrece tienda ni checkout: habría que conectar Shopify (de pago) o montar todo a mano.
- **D (frontend propio + Stripe + webhooks)**: descartada para el lanzamiento. Es lo que se ha construido *de facto* como escaparate estático, pero sin cobro propio: el pago se delega en la plataforma POD, que es más rápido de activar y no exige mantener webhooks ni claves.

## 3. Cómo queda el reparto de piezas

| Pieza | Dónde vive | Estado |
|---|---|---|
| Escaparate, catálogo, FAQ, legal, seguimiento, contenido | GitHub Pages (este repo) | **En vivo** |
| Cobro, factura fiscal, producción, envío, emails de pedido | Fourthwall (plan Free) | **Pendiente de crear la cuenta** (ver `ACTIVACION.md`) |
| Imprimibles (arte) | `/designs` en local | **Pendiente del humano** |
| Seguimiento del cliente | `/_seguimiento/` de esta web, leyendo `data/pedidos.json` | En vivo y probado (fila demo) |

## 4. Naming y marca

- **Nombre elegido: «Llamamiento 23:59»**. Se descartan «Lista de espera» (demasiado genérico y ya usado por mil tiendas) y «Interinidad Canaria» (demasiado descriptivo, sin gracia).
- El reloj de 7 segmentos con «23:59» es el elemento gráfico de marca y también el dominio lógico a registrar (ver `DNS.md`).
- Prohibiciones respetadas en todo el contenido: ningún escudo, bandera como marca, logo de la Consejería, centro o sindicato, ni nombre de cargo. La ficha 05 se reescribió a propósito: «VISTO A LAS 3:47» en lugar de mencionar a la Consejería.
- El generador valida estas prohibiciones en cada compilación (`python build.py --check`).

## 5. Economía por producto (números de partida)

| Producto | PVP (IVA incl.) | Coste base ref. | Margen bruto | Tras ~3 % de procesamiento de pago |
|---|---|---|---|---|
| Camiseta unisex | 22,90 € | 12,50 € | 10,40 € | ≈ 9,71 € |
| Tote bag | 17,90 € | 8,50 € | 9,40 € | ≈ 8,86 € |
| Taza 11 oz | 15,90 € | 7,50 € | 8,40 € | ≈ 7,92 € |

- En el plan Free de Fourthwall **no hay comisión de plataforma sobre los productos de catálogo**: se descuenta el coste base y el resto es del titular.
- Los costes base son **referencias del catálogo público** y hay que confirmarlos talla por talla al crear los productos en la cuenta. Cuando se confirmen, se actualizan aquí y en `data/productos.json`.
- La comisión de procesamiento de pago depende del método (la propia plataforma publica ≈2,9 % + 0,30 $ en tarjetas estadounidenses; otros métodos varían). Por eso el margen se deja con colchón.
- Los gastos de envío se calculan en el checkout de la plataforma y no se incluyen en esta tabla.
- **Régimen fiscal**: con Fourthwall como *Merchant of Record*, la plataforma recauda y liquida los impuestos de venta. El régimen del titular (IGIC si el domicilio fiscal está en Canarias, IVA si está en península) debe quedar declarado en la cuenta y revisado por su asesor antes de la apertura real. No se ha inventado ninguna cifra fiscal.

## 6. Privacidad y RGPD

- Páginas legales reales (no plantilla vacía): aviso legal, privacidad con tabla de finalidades y encargados, cookies con inventario, condiciones de compra y envíos/devoluciones.
- Encargados declarados: plataforma POD (vendedor registrado), talleres, pasarelas de pago, transportistas, alojamiento y correo, asesoría. Transferencias internacionales cubiertas por decisiones de adecuación o cláusulas tipo.
- Derecho de desistimiento de 14 días explicado **con** su excepción para personalizados (art. 103.f LGDCU) y, al lado, la garantía real por defectos.
- Banner de cookies que permite rechazar la analítica y seguir comprando; la analítica solo se carga si se acepta y existe un ID configurado.
- En `data/pedidos.json` (consultado por el buscador de seguimiento) **no hay direcciones ni importes**: solo pedido, email, estado, carrier y tracking.

## 7. Plan B si Fourthwall falla

1. **Printify Pop-Up Store** (gratis, disponible en España). Requiere verificar Stripe y el vendedor pasa a ser responsable de impuestos. La web actual sirve igual: se pegan las URLs de compra en `data/disenos.json → checkout_url`.
2. **Gelato + Shopify Basic** (de pago, 1 €/mes promocional): se descarta por el requisito de coste recurrente 0 €.
3. **Frontend propio + Stripe Payment Links + pedido manual en Gelato**: solo si el titular acepta mantener a mano el paso pago → pedido. No es automático, así que no se elige.

## 8. Dónde se configura cada cosa (sin secretos en el repo)

| Qué | Dónde |
|---|---|
| Nombre de tienda, dominio, email, plazos, GA | `data/site.json` |
| Diseños (texto, paleta, estado, `checkout_url`) | `data/disenos.json` |
| Productos, precios, costes base, plantillas de impresión | `data/productos.json` |
| Estados y carriers del seguimiento | `data/carriers.json` |
| Pedidos del buscador de seguimiento | `data/pedidos.json` |
| Placeholders del borrador | `data/placeholders.borrador.json` |
| Textos legales | `legal/*.html` |
| Claves y tokens (nunca en el repo) | `.env` a partir de `.env.example` |
| Cuenta POD, pagos, impuestos, emails de pedido | Panel de la plataforma POD (ver `ACTIVACION.md`) |
| DNS del dominio | `docs/DNS.md` |

## 9. Definición de hecho — estado real a esta hora

- [x] **URL pública de la tienda funcionando**: https://ray86-dev.github.io/camisetas-interinos/
- [x] **Catálogo listo a falta de PNG**: 24 fichas generadas y publicadas; los botones de compra se activan solos al marcar un diseño como `listo` y pegar su URL de compra. La tienda en vivo está en modo prelanzamiento, explicado en portada. No hay producto comprable todavía porque no hay arte.
- [ ] **Checkout automático**: *bloqueado por credenciales*. Requiere crear la cuenta de Fourthwall (email + verificación) y decidir el dominio. Pasos exactos en `ACTIVACION.md`. El checkout que se usará es el nativo de la plataforma: tarjeta, PayPal, Apple/Google Pay.
- [x] **Emails de pedido**: texto de los 4 emails redactado y listo para pegar (`docs/EMAILS.md`); la plataforma los envía de forma nativa. Sin probar con pedido real (no hay cuenta aún).
- [x] **Tracking explicado y activado donde se puede**: buscador propio en vivo (`/seguimiento/`), mapa de carriers reales, y política de «nunca llamar Correos a lo que no es Correos» implementada en los textos.
- [x] **ETA a Canarias publicado con honestidad**: 6-14 días laborables, con la aduana explicada.
- [x] **DNS.md** con registros listos para copiar.
- [x] **BRIEF de diseño + prompts** para Fooocus, ComfyUI y Gemini, más checklist de impresión.
- [x] **RUNBOOK y TIENDA.md**.
- [x] Repo con commits claros y publicador reproducible (`scripts/publish.sh`).

## 10. Cambios previstos (fase 2)

**Pendiente inmediato (respuesta del titular del 11-09-2026):** el titular eligió que **el agente abra la cuenta POD hasta el paso de verificación** y que él meta el código. Para arrancar faltan dos datos:

1. **Email con el que se abre la tienda** (será el email de avisos de pedidos y el de contacto de la web).
2. **Dominio confirmado**, para generar el `CNAME` y concretar los registros de `DNS.md`.

Cuando lleguen, el registro se hace en `auth.fourthwall.com` (email + contraseña). La contraseña **nunca** la escribe el agente ni se pega en el chat: se guarda con el gestor de contraseñas de Hermes cuando el titular esté delante para autorizarlo. Después queda la verificación por email, que también es del titular.

1. El humano genera el arte y lo deja en `/designs` con la nomenclatura del BRIEF.
2. Se crea la cuenta POD, se suben los 24 productos con mockups oficiales y se copian las URLs.
3. Se pegan las URLs en `data/disenos.json`, se marca `estado: listo` y se ejecuta `python build.py --check && bash scripts/publish.sh`.
4. Se apunta el dominio según `DNS.md` (opción A: al escaparate; opción B: a la tienda POD).
5. Se hace un pedido de prueba real de 1 € con el producto `TEST-NO-COMPRAR` y se documenta el resultado aquí.
