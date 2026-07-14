from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from codigo_completo.modelos import Filamento
from codigo_completo.excel_funciones import (
     importar_stock_desde_excel,
     exportar_stock_a_excel,
)
from codigo_completo.stock import  actualizar_stock, ordenar_stock, unificar_stock
from codigo_completo.funciones_json_backup import guardar_stock, registrar_movimiento
import json

app = Flask(__name__) 
app.secret_key = "indigo3d_stock"

stock_filamentos = importar_stock_desde_excel()

unificar_stock(stock_filamentos)

# @app.route("/")
# def inicio():
#     return render_template("index.html", stock=stock_filamentos)
@app.route("/")
def inicio():
    ordenar_stock(stock_filamentos)
    return render_template(
        "index.html",
        stock=stock_filamentos
    )

# ACCIONES

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":

        filamento = Filamento(
            request.form["color"].strip().capitalize(),
            request.form["fabricante"].strip().capitalize(),
            int(request.form["cantidad"])
        )
        actualizar_stock(filamento, stock_filamentos)
        # stock_filamentos.append(filamento)

        exportar_stock_a_excel(stock_filamentos)
        flash("Filamento agregado correctamente.", "exito")
        return redirect(url_for("inicio"))

    return redirect(url_for("inicio"))
    
@app.route("/retirar", methods=["GET", "POST"])
def retirar():
    if request.method == "POST":
        color = request.form["color"].strip().capitalize()
        fabricante = request.form["fabricante"].strip().capitalize()
        cantidad = int(request.form["cantidad"])

        for filamento in stock_filamentos:
            if filamento.color == color and filamento.fabricante == fabricante:
                if filamento.cantidad >= cantidad:
                    filamento.cantidad -= cantidad
                    guardar_stock(stock_filamentos)
                    exportar_stock_a_excel(stock_filamentos)
                    registrar_movimiento("Retiro", filamento, cantidad)

                    flash("Stock retirado correctamente.", "exito")
                else:
                    flash("No hay suficiente stock.", "error")

                break
        else:
            flash("No se encontró el filamento.", "error")

        return redirect(url_for("inicio"))

    return redirect(url_for("inicio"))


@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    resultados = None

    if request.method == "POST":
        color = request.form["color"].strip().capitalize()
        fabricante = request.form["fabricante"].strip().capitalize()

        resultados = []

        for filamento in stock_filamentos:
            coincide_color = color == "" or filamento.color == color
            coincide_fabricante = fabricante == "" or filamento.fabricante == fabricante

            if coincide_color and coincide_fabricante:
                resultados.append(filamento)

    return redirect(url_for("inicio"))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    color = request.form["color"]
    fabricante = request.form["fabricante"]

    for filamento in stock_filamentos:
        if filamento.color == color and filamento.fabricante == fabricante:
            registrar_movimiento("Eliminado", filamento, filamento.cantidad)
            stock_filamentos.remove(filamento)
            flash("Filamento eliminado correctamente.", "exito")
            break

    guardar_stock(stock_filamentos)
    exportar_stock_a_excel(stock_filamentos)

    return redirect(url_for("inicio"))

@app.route("/editar_stock", methods=["POST"])
def editar_stock():
    color = request.form["color"]
    fabricante = request.form["fabricante"]
    accion = request.form["accion"]
    cantidad = int(request.form["cantidad"])

    for filamento in stock_filamentos:
        if filamento.color == color and filamento.fabricante == fabricante:

            if accion == "agregar":
                filamento.cantidad += cantidad
                registrar_movimiento("Ingreso", filamento, cantidad)
                flash("Se agrego correctamente.", "exito")

            elif accion == "retirar":
                if filamento.cantidad >= cantidad:
                    filamento.cantidad -= cantidad
                    registrar_movimiento("Retiro", filamento, cantidad)
                    flash("Se retiro correctamente.", "exito")

            break

    guardar_stock(stock_filamentos)
    exportar_stock_a_excel(stock_filamentos)

    return redirect(url_for("inicio"))

@app.route("/corregir_filamento", methods=["POST"])
def corregir_filamento():
    color_original = request.form["color_original"]
    fabricante_original = request.form["fabricante_original"]

    nuevo_color = request.form["color"].strip().capitalize()
    nuevo_fabricante = request.form["fabricante"].strip().capitalize()
    nueva_cantidad = int(request.form["cantidad"])

    for filamento in stock_filamentos:
        if filamento.color == color_original and filamento.fabricante == fabricante_original:
            filamento.color = nuevo_color
            filamento.fabricante = nuevo_fabricante
            filamento.cantidad = nueva_cantidad
            registrar_movimiento("Corregido", filamento, nueva_cantidad)
            flash("Datos del filamento actualizados correctamente.", "exito")
            break

    ordenar_stock(stock_filamentos)
    guardar_stock(stock_filamentos)
    exportar_stock_a_excel(stock_filamentos)
    

    return redirect(url_for("inicio"))

@app.route("/historial")
def historial():
    try:
        with open("movimientos.json", "r", encoding="utf-8") as archivo:
            movimientos = json.load(archivo)
    except FileNotFoundError:
        movimientos = []
        
    movimientos.reverse()

    return render_template("historial.html", movimientos=movimientos)


@app.route("/descargar_excel")
def descargar_excel():
    exportar_stock_a_excel(stock_filamentos)

    return send_file(
        "stock.xlsx",
        as_attachment=True,
        download_name="stock_filamentos.xlsx"
    )
    
@app.route("/importar_excel", methods=["GET", "POST"])
def importar_excel():
    global stock_filamentos

    if request.method == "POST":
        archivo = request.files["archivo_excel"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo.", "error")
            return redirect(url_for("importar_excel"))

        archivo.save("stock.xlsx")

        stock_filamentos = importar_stock_desde_excel()
        unificar_stock(stock_filamentos)
        ordenar_stock(stock_filamentos)
        exportar_stock_a_excel(stock_filamentos)

        flash("Excel importado correctamente.", "exito")
        return redirect(url_for("inicio"))

    return render_template("importar_excel.html")

if __name__ == "__main__":
    app.run(debug=True)
    