from datetime import datetime#, timedelta
import json

def registrar_movimiento(accion, filamento, cantidad):
    #Creo un diccionario con los datos del movimiento
    movimiento = {
        'fecha' : datetime.now().strftime('%Y-%m-%d'),
        'accion' : accion,
        'color_del_filamento' : filamento.color,
        'fabricante_del_filamento' : filamento.fabricante,
        'cantidad' : cantidad
    }
    #tengo que guardarlo aparte
    try: #en caso de haber hecho un reset del historial
        with open('movimientos.json', 'r', encoding='utf-8') as archivo:
            movimientos = json.load(archivo)
    except FileNotFoundError:
        movimientos = []
    movimientos.append(movimiento)
    
    with open('movimientos.json', 'w', encoding='utf-8') as archivo:
        json.dump(movimientos, archivo, indent=4)
        
def mostrar_ultimo_movimiento():
    try:
        with open('movimientos.json', 'r', encoding='utf-8') as archivo:
            movimientos = json.load(archivo)
        if len(movimientos) == 0:
            print("- No hay movimientos registrados -")
            return
        
        #guardo el ultimo movimiento para mostrarlo
        ultimo = movimientos[-1]
        
        print("== Último movimiento ==")
        print(f"Fecha: {ultimo['fecha']}")
        print(f"Acción: {ultimo['accion']}")
        print(f"Color: {ultimo['color_del_filamento']}")
        print(f"Fabricante: {ultimo['fabricante_del_filamento']}")
        print(f"Cantidad: {ultimo['cantidad']}")
            
    except FileNotFoundError:
        print("- No hay movimientos registrados -")
        
def mostrar_historial_movimientos():
    try:
        with open('movimientos.json', 'r', encoding='utf-8') as archivo:
            movimientos = json.load(archivo)
        if len(movimientos) == 0:
            print("- No hay movimientos registrados -")
            return
        
        print("== Historial de movimientos ==")
        
        ultima_fecha_mostrada = ""
        #consigo datos por el diccionario
        for movimiento in movimientos:
            fecha_del_movimiento = movimiento["fecha"]

            if fecha_del_movimiento != ultima_fecha_mostrada:
                ultima_fecha_mostrada = fecha_del_movimiento

                print(" ")
                print("== " + fecha_del_movimiento + " ==")
                print(f'{"Acción":<10} | {"Color":<12} | {"Fabricante":<12} | {"Cantidad":<8}')

            print(f'{movimiento["accion"]:<10} | {movimiento["color_del_filamento"]:<12} | {movimiento["fabricante_del_filamento"]:<12} | {movimiento["cantidad"]:<8}')

    except FileNotFoundError:
        print("- No hay movimientos registrados -")
    
    
def buscar_movimientos_por_fecha():
    fecha_buscada = input("- Fecha a buscar por dia y mes: ").strip()
    fecha_buscada = fecha_buscada.replace(" ", "-")  # Reemplazo los espacios por guiones para que coincida con el formato de fecha
    dia, mes = fecha_buscada.split("-") #toma lo que esta antes como mes y lo que esta despues como dia, si no hay guion da error
    dia = dia.zfill(2)
    mes = mes.zfill(2)
    anio_actual = datetime.now().strftime("%Y")
    fecha_buscada = anio_actual + "-" + mes + "-" + dia #ahorro al usuario de tener que escribir el año, lo pongo automaticamente
    
    try:
        with open("movimientos.json", "r", encoding="utf-8") as archivo:
            movimientos = json.load(archivo)
        encontrados = False
        print("== Movimientos encontrados ==")
        print(fecha_buscada)
        print(" ")
        print(f'{"Acción":<10} | {"Color":<12} | {"Fabricante":<12} | {"Cantidad":<8}')
        print(" ")
        for movimiento in movimientos:
            if movimiento["fecha"] == fecha_buscada:
                print(f'{movimiento["accion"]:<10} | {movimiento["color_del_filamento"]:<12} | {movimiento["fabricante_del_filamento"]:<12} | {movimiento["cantidad"]:<8}')
                encontrados = True
        if encontrados == False:
            print("- No hay movimientos para esa fecha -")
    except FileNotFoundError:
        print("- No hay movimientos registrados -")
    
    
def buscar_movimientos_por_color():
    color_buscado = input("- Color a buscar: ").strip().capitalize()
    print(" ")
    
    try:
        with open("movimientos.json", "r", encoding="utf-8") as archivo:
            movimientos = json.load(archivo)
        encontrados = False
        print("== Movimientos encontrados ==")
        print(f'{"Fecha":<12} | {"Acción":<10} | {"Color":<12} | {"Fabricante":<12} | {"Cantidad":<8}')
        print(" ")
        for movimiento in movimientos:
            if movimiento["color_del_filamento"] == color_buscado:
                print(f'{movimiento["fecha"]:<12} | {movimiento["accion"]:<10} | {movimiento["color_del_filamento"]:<12} | {movimiento["fabricante_del_filamento"]:<12} | {movimiento["cantidad"]:<8}')
                encontrados = True
        if encontrados == False:
            print("- No hay movimientos para ese color -")
            
    except FileNotFoundError:
        print("- No hay movimientos registrados -")