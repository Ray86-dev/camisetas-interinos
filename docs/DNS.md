# DNS.md — registros para el dominio del titular

Dominio: **pendiente de que el titular confirme cuál es** (los registros de abajo son los definitivos en cuanto se sustituya `tudominio.com`).
Hospedaje actual del escaparate: **GitHub Pages** → https://ray86-dev.github.io/camisetas-interinos/
Hospedaje previsto de la tienda completa: **Fourthwall** (plan Free, admite dominio propio).

> Decisión pendiente del titular (opción A u opción B, ver el final). Los dos juegos de registros están listos para copiar; no se pueden aplicar los dos a la vez.

## 1. Requisito previo en GitHub Pages

1. Añadir el dominio en el repo: *Settings → Pages → Custom domain* → escribir `tudominio.com` → Save.
2. Crear el fichero `CNAME` (lo hace el generador automáticamente si se rellena `dominio_previsto` en `data/site.json`). Contenido: una sola línea con el dominio, sin `https://`.
3. Esperar a que GitHub valide el DNS y marcar *Enforce HTTPS* (certificado gratuito de Let's Encrypt; tarda unos minutos tras validar el DNS).

## 2. Registros DNS

### 2.1 Opción A — el dominio apunta al escaparate (GitHub Pages)

| Tipo | Nombre / Host | Valor | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 3600 |
| A | `@` | `185.199.109.153` | 3600 |
| A | `@` | `185.199.110.153` | 3600 |
| A | `@` | `185.199.111.153` | 3600 |
| CNAME | `www` | `ray86-dev.github.io` | 3600 |

Opcional (IPv6):

| Tipo | Nombre / Host | Valor |
|---|---|---|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

Notas: los cuatro registros A son obligatorios (son los servidores de GitHub Pages). No usar comodín `*`. Si el panel del registrador pide «host» en lugar de «nombre», escribir `@` para el dominio raíz y `www` para el subdominio.

### 2.2 Opción B — el dominio apunta a la tienda Fourthwall (recomendado a medio plazo)

Estos son los registros genéricos que Fourthwall pide. **Hay que confirmar el valor exacto en el panel de Fourthwall** (*Settings → Domains → Connect a domain*): la plataforma muestra el CNAME definitivo de su cuenta y desde ahí debe copiarse.

| Tipo | Nombre / Host | Valor | TTL |
|---|---|---|---|
| A | `@` | *(valor que indique Fourthwall, habitualmente `75.2.60.5`)* | 3600 |
| CNAME | `www` | *(valor que indique Fourthwall, tipo `xxxxx.fourthwall.com`)* | 3600 |

## 3. Correo del dominio

El email de contacto de la tienda (`hola@tudominio.com`) necesita registros propios si se quiere recibir correo real:

| Tipo | Nombre | Valor | Prioridad |
|---|---|---|---|
| MX | `@` | *(servidor del proveedor de correo elegido)* | 10 |
| TXT | `@` | `v=spf1 include:<proveedor> ~all` | — |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:hola@tudominio.com` | — |

Alternativa 0 €: usar un alias del proveedor de correo actual y dejar el dominio solo para la web. Los emails de pedido los envía la plataforma POD (no dependen de este buzón); este buzón es para consultas, facturas y devoluciones.

## 4. Cómo comprobar que ha propagado

```
nslookup tudominio.com
dig +short tudominio.com A
dig +short www.tudominio.com CNAME
curl -sI https://tudominio.com | head -5
```

En Windows, `nslookup tudominio.com 1.1.1.1` fuerza a preguntar a Cloudflare y evita cachés locales.

## 5. Errores típicos

- **Dejar el registro A antiguo del parking del registrador**: si el dominio sigue mostrando la página de «dominio aparcado», hay que borrar ese registro.
- **CNAME en el dominio raíz**: no es válido en la mayoría de registradores; para el raíz se usan los A (o un ALIAS/ANAME si el panel lo ofrece).
- **Poner `https://` o una barra final en el valor del CNAME**: el valor es solo el host (`ray86-dev.github.io`), nada más.
- **Mezclar las dos opciones**: si el dominio apunta a GitHub Pages, no se puede apuntar a la vez a Fourthwall. Decidir una y limpiar los registros de la otra.
- **Propagación**: cambios de 5 minutos a 24 horas según el TTL anterior. Si el TTL previo era de 86400, hay que esperar.

## 6. Decisión que debe tomar el titular

- **Opción A (hoy mismo)**: dominio → escaparate de GitHub Pages. Todo el tráfico llega a la web que ya funciona; los botones de compra llevan al checkout de la plataforma POD cuando exista. Es la opción para no dejar el dominio parado ni un día.
- **Opción B (recomendada a medio plazo)**: dominio → tienda Fourthwall, donde el cliente compra sin salir del dominio. La web de GitHub Pages queda como escaparate secundario o se retira.

Lo razonable: poner **A** ahora (esta noche, con los registros del apartado 2.1) y pasar a **B** cuando la tienda POD tenga los 24 productos cargados y probados. Cambiar de A a B es editar dos o tres registros, y el escaparate sigue disponible en su URL de github.io.
