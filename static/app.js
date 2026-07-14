/* ==============================
   PANELES GENERALES
============================== */

function mostrarPanel(id){
    document.querySelectorAll(".panel-formulario").forEach(panel => {
        panel.style.display = "none";
    });

    document.getElementById(id).style.display = "block";
}

function cerrarPanel(id){
    document.getElementById(id).style.display = "none";
}

/* ==============================
   PANEL EDITAR
============================== */

function abrirPanelEditar(event, color, fabricante, cantidad){
    mostrarPanel("panelEditar");

    const panel = document.getElementById("panelEditar");
    const boton = event.currentTarget;
    const rect = boton.getBoundingClientRect();

    panel.style.top = window.scrollY + rect.top - 105 + "px";
    panel.style.left = window.scrollX + rect.left - panel.offsetWidth - 140 + "px";

    if (parseInt(panel.style.left) < 20) {
        panel.style.left = "20px";
    }

    document.getElementById("editarStockColor").value = color;
    document.getElementById("editarStockFabricante").value = fabricante;

    document.getElementById("colorOriginal").value = color;
    document.getElementById("fabricanteOriginal").value = fabricante;

    document.getElementById("corregirColor").value = color;
    document.getElementById("corregirFabricante").value = fabricante;
    document.getElementById("corregirCantidad").value = cantidad;

    document.getElementById("formEditarStock").style.display = "none";
    document.getElementById("formEditarDatos").style.display = "none";
}

function mostrarEdicion(tipo){
    document.getElementById("formEditarStock").style.display = "none";
    document.getElementById("formEditarDatos").style.display = "none";

    if (tipo === "stock") {
        document.getElementById("formEditarStock").style.display = "grid";
    }

    if (tipo === "datos") {
        document.getElementById("formEditarDatos").style.display = "flex";
    }
}

/* ==============================
   PANEL ELIMINAR
============================== */

function abrirPanelEliminar(event, color, fabricante){
    mostrarPanel("panelEliminar");

    const panel = document.getElementById("panelEliminar");
    const boton = event.currentTarget;
    const rect = boton.getBoundingClientRect();

    panel.style.top = window.scrollY + rect.top - 105 + "px";
    panel.style.left = window.scrollX + rect.left - panel.offsetWidth - 180 + "px";

    if (parseInt(panel.style.left) < 20) {
        panel.style.left = "20px";
    }

    document.getElementById("eliminarColor").value = color;
    document.getElementById("eliminarFabricante").value = fabricante;
    document.getElementById("textoFilamentoEliminar").textContent = color + " - " + fabricante;
}


/* ==============================
   BUSCADORES Y FILTROS
============================== */


function filtrarStock(tipo) {
    const filas = document.querySelectorAll(".fila-stock");

    filas.forEach(fila => {
        if (tipo === "todos") {
            fila.style.display = "";
        } else if (tipo === "sin") {
            fila.style.display = fila.classList.contains("sin-stock-row") ? "" : "none";
        } else if (tipo === "bajo") {
            fila.style.display = fila.classList.contains("bajo-stock-row") ? "" : "none";
        }
    });
}

const buscador = document.getElementById("buscadorStock");
if (buscador) {
    buscador.addEventListener("input", function () {
        const texto = buscador.value.toLowerCase();
        const filas = document.querySelectorAll(".fila-stock");

        filas.forEach(fila => {
            const contenido = fila.textContent.toLowerCase();
            fila.style.display = contenido.includes(texto) ? "" : "none";
        });
    });
}

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function () {
        sessionStorage.setItem("scrollStock", window.scrollY);
    });
});

window.addEventListener("load", function () {
    const scrollGuardado = sessionStorage.getItem("scrollStock");

    if (scrollGuardado) {
        window.scrollTo(0, parseInt(scrollGuardado));
        sessionStorage.removeItem("scrollStock");
    }
});


const inputExcel = document.getElementById("archivo_excel");
const nombreArchivo = document.getElementById("nombreArchivo");
if (inputExcel && nombreArchivo) {
    inputExcel.addEventListener("change", function () {
        if (inputExcel.files.length > 0) {
            nombreArchivo.textContent = inputExcel.files[0].name;
        } else {
            nombreArchivo.textContent = "Ningún archivo seleccionado";
        }
    });
}

/* ==============================
   MENSAJES FLASH
============================== */

const mensajes = document.querySelectorAll(".mensaje");
mensajes.forEach((mensaje) => {
    setTimeout(() => {
        mensaje.style.opacity = "0";
        mensaje.style.transform = "translateX(20px)";

        setTimeout(() => {
            mensaje.remove();
        }, 400);
    }, 10000);
});