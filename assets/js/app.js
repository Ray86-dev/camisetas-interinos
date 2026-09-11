/* Llamamiento 23:59 — JS de tienda (sin dependencias, sin cookies de terceros) */
(function () {
  "use strict";

  var BASE = document.documentElement.getAttribute("data-base") || "";

  /* ---------- Carrito ligero (localStorage) ----------
     Fase 1: el pago lo cobra la plataforma POD. Este carrito es una lista de
     traspaso: guarda lo elegido y enlaza a cada producto en la tienda POD.
     Nunca simula un cobro. */
  var KEY = "ll2359_carrito";

  function leer() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; }
  }
  function guardar(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
    pintarCarrito();
  }
  function pintarCarrito() {
    var items = leer();
    document.querySelectorAll(".carrito-link").forEach(function (el) {
      el.setAttribute("data-count", String(items.length));
    });
  }
  function annadir(btn) {
    var items = leer();
    var item = {
      id: btn.getAttribute("data-id"),
      titulo: btn.getAttribute("data-titulo"),
      tipo: btn.getAttribute("data-tipo"),
      talla: (document.getElementById("talla") || {}).value || "",
      precio: btn.getAttribute("data-precio"),
      checkout: btn.getAttribute("data-checkout") || ""
    };
    items.push(item);
    guardar(items);
    btn.textContent = "Añadido a tu lista";
    setTimeout(function () { btn.textContent = "Añadir a mi lista"; }, 1800);
  }

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-accion='annadir']");
    if (btn) { ev.preventDefault(); annadir(btn); }
    var quitar = ev.target.closest("[data-accion='quitar']");
    if (quitar) {
      ev.preventDefault();
      var id = quitar.getAttribute("data-id");
      guardar(leer().filter(function (i) { return i.id !== id; }));
    }
    var vaciar = ev.target.closest("[data-accion='vaciar']");
    if (vaciar) { ev.preventDefault(); guardar([]); }
  });

  /* ---------- Pintar la página de carrito ---------- */
  function renderCarrito() {
    var cont = document.getElementById("carrito-lista");
    if (!cont) return;
    var items = leer();
    var vacio = document.getElementById("carrito-vacio");
    var tabla = document.getElementById("carrito-tabla");
    if (!items.length) {
      if (vacio) vacio.classList.remove("oculto");
      if (tabla) tabla.classList.add("oculto");
      return;
    }
    if (vacio) vacio.classList.add("oculto");
    if (tabla) tabla.classList.remove("oculto");
    cont.innerHTML = "";
    var total = 0;
    items.forEach(function (i) {
      var tr = document.createElement("tr");
      var p = parseFloat(i.precio || "0");
      total += p;
      tr.innerHTML =
        "<td>" + i.titulo + (i.talla ? " <span class='small'>· " + i.talla + "</span>" : "") + "</td>" +
        "<td>" + p.toFixed(2).replace(".", ",") + " €</td>" +
        "<td>" + (i.checkout
            ? "<a class='btn' href='" + i.checkout + "' rel='noopener'>Comprar</a>"
            : "<span class='tag'>Próximamente</span>") +
          " <button class='btn btn-2' data-accion='quitar' data-id='" + i.id + "'>Quitar</button></td>";
      cont.appendChild(tr);
    });
    var celda = document.getElementById("carrito-total");
    if (celda) celda.textContent = total.toFixed(2).replace(".", ",") + " €";
  }

  /* ---------- Seguimiento de pedido ---------- */
  function buscarPedido(pedido, email) {
    var urlPedidos = BASE + "/data/pedidos.json";
    var urlCarriers = BASE + "/data/carriers.json";
    return Promise.all([
      fetch(urlPedidos).then(function (r) { return r.json(); }),
      fetch(urlCarriers).then(function (r) { return r.json(); })
    ]).then(function (res) {
      var pedidos = res[0].pedidos || [];
      var datos = res[1];
      var p = String(pedido || "").trim().toUpperCase();
      var em = String(email || "").trim().toLowerCase();
      var encontrado = pedidos.find(function (x) {
        return String(x.pedido).toUpperCase() === p && String(x.email).toLowerCase() === em;
      });
      if (!encontrado) return null;
      var carrier = (datos.carriers || []).find(function (c) { return c.id === encontrado.carrier; }) || null;
      return {
        pedido: encontrado,
        carrier: carrier,
        url: carrier && encontrado.tracking ? carrier.url.replace("{code}", encodeURIComponent(encontrado.tracking)) : "",
        estados: datos.estados || []
      };
    });
  }

  function pintarSeguimiento(datos) {
    var cont = document.getElementById("seguimiento-resultado");
    if (!cont) return;
    if (!datos) {
      cont.innerHTML =
        "<div class='aviso'><p><strong>No encontramos ese pedido.</strong> Revisa el número " +
        "(formato LL-0000) y el email exacto que usaste al comprar. Si acabas de pagar, el pedido " +
        "tarda unos minutos en aparecer. Si sigue sin salir, escríbenos y lo miramos a mano.</p></div>";
      return;
    }
    var p = datos.pedido;
    var orden = datos.estados.map(function (e) { return e.id; });
    var actual = orden.indexOf(p.estado);
    var html = "";
    if (p.demo) {
      html += "<p class='tag estado-demo'>EJEMPLO DE PRUEBA — no es un pedido real</p>";
    }
    html += "<h3>Pedido " + p.pedido + "</h3>";
    html += "<p class='small'>Fecha del pedido: " + p.fecha_pedido +
            (p.destino ? " · Destino: " + (p.destino === "canarias" ? "Canarias" : "Península") : "") + "</p>";
    html += "<ul class='timeline'>";
    datos.estados.forEach(function (e, i) {
      var hecho = i <= actual;
      html += "<li class='" + (hecho ? "hecho" : "") + "'><strong>" + e.etiqueta + "</strong><br><span class='small'>" +
              e.texto + "</span></li>";
    });
    html += "</ul>";
    if (p.tracking) {
      var nombreCarrier = datos.carrier ? datos.carrier.nombre : p.carrier;
      html += "<div class='aviso aviso-azul'><p><strong>Te hemos enviado con " + nombreCarrier +
              ".</strong> Tracking: <span class='mono'>" + p.tracking + "</span></p>" +
              (datos.url ? "<p><a class='btn' href='" + datos.url + "' rel='noopener'>Ver seguimiento en " +
                nombreCarrier + "</a></p>" : "") + "</div>";
    } else {
      html += "<p class='small'>Cuando salga del taller te damos el número de seguimiento del carrier real.</p>";
    }
    if (p.nota) html += "<p class='small'>" + p.nota + "</p>";
    cont.innerHTML = html;
  }

  /* ---------- Filtros del catálogo ---------- */
  function initFiltros() {
    var botones = document.querySelectorAll("[data-filtro]");
    if (!botones.length) return;
    botones.forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-filtro");
        botones.forEach(function (x) { x.classList.remove("btn-rojo"); x.classList.add("btn-2"); });
        b.classList.remove("btn-2"); b.classList.add("btn-rojo");
        document.querySelectorAll("[data-tipo-producto]").forEach(function (c) {
          c.classList.toggle("oculto", f !== "todos" && c.getAttribute("data-tipo-producto") !== f);
        });
      });
    });
  }

  /* ---------- Cookies (RGPD) ---------- */
  function initCookies() {
    var caja = document.getElementById("cookies");
    if (!caja) return;
    var GA = caja.getAttribute("data-ga") || "";
    var eleccion = null;
    try { eleccion = localStorage.getItem("ll2359_cookies"); } catch (e) {}
    if (!eleccion) caja.classList.add("visible");
    if (eleccion === "todo" && GA) cargarGA(GA);
    caja.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-cookie]");
      if (!b) return;
      var v = b.getAttribute("data-cookie");
      try { localStorage.setItem("ll2359_cookies", v); } catch (e) {}
      caja.classList.remove("visible");
      if (v === "todo" && GA) cargarGA(GA);
    });
  }
  function cargarGA(id) {
    if (!id || window.__ga) return;
    window.__ga = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", id, { anonymize_ip: true });
  }

  /* ---------- Arranque ---------- */
  document.addEventListener("DOMContentLoaded", function () {
    pintarCarrito();
    renderCarrito();
    initFiltros();
    initCookies();

    var form = document.getElementById("form-seguimiento");
    if (form) {
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var cont = document.getElementById("seguimiento-resultado");
        cont.innerHTML = "<p>Buscando…</p>";
        buscarPedido(
          document.getElementById("pedido").value,
          document.getElementById("email").value
        ).then(pintarSeguimiento).catch(function () {
          cont.innerHTML = "<div class='aviso'><p>No hemos podido consultar el estado ahora mismo. " +
            "Inténtalo de nuevo en un minuto o escríbenos.</p></div>";
        });
      });
    }
  });
})();
