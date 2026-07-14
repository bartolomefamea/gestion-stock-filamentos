import json
from dataclasses import asdict
from .modelos import Filamento
from datetime import datetime

def guardar_stock(stock_filamentos):
    #forma para escribir archivo, utf-8 reconoce Ñ
    with open("stock.json", "w", encoding="utf-8") as archivo:
        #indent=4 le agrega 4 espacios al formato 'mas prolijidad'
        json.dump([asdict(filamento) for filamento in stock_filamentos], archivo, indent=4)



def cargar_stock():
    try:
        #leo archivo
        with open("stock.json", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
            #lee datos del archivo y guarda en este formato
            return [Filamento(filamento["color"], filamento["fabricante"], filamento["cantidad"]) for filamento in data]
    #si no hay archivo devuelve lista vacia
    except FileNotFoundError:
        return []    
    
    
def mostrar_stock_json(nombre_archivo):
    print('Stock de filamentos: ')
    with open("stock.json", "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
        
        #pensar que forma es mas comoda de ver
        #formato excel creo que va a ser mejor
        print(f'{"Color":<12} | {"Filamento":<12} | {"Cantidad":<8}')
        for filamento in data:
            print(f'{filamento["color"]:<12} | {filamento["fabricante"]:<12} | {filamento["cantidad"]:<8}')
 
 
 
 #utilizo try siempre por si es la primera vez que corre el programa y no hay archivo de historial
#tambien por si se llega a borrar el movimientos.json

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
        