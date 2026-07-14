

from .excel_funciones import *
from .historial import *
from .stock import *


def menu_historial():
     while True:
        print(" ")
        print("== Historial ==")
        opcion = input("1 buscar por fecha / 2 buscar por color / 3 ultimo movimiento / 4 historial completo / 5 volver: ")
        print(" ")
        match opcion:
            case "1":
                buscar_movimientos_por_fecha()         
            case "2":
                buscar_movimientos_por_color()
            case "3":
                mostrar_ultimo_movimiento()
            case "4":
                mostrar_historial_movimientos()
                
            case "5":
                break
            case _:
                print("- Opción inválida -")
        
def menu_stock(stock_filamentos):
    while True:
        print(" ")
        print("== Stock ==")
        opcion = input("1 mostrar stock / 2 mostrar stock clasificado / 3 volver: ")
        print(" ")
        match opcion:
            case "1":
                mostrar_stock(stock_filamentos)
                #mostrar_stock_json("stock.json") este ya no, quiero ver el que tengo cargado en el excel/auxiliar del programa
            case "2":
                mostrar_stock_clasificado(stock_filamentos)
            case "3":
                break
            case _:
                print("- Opción inválida -")


def gestion_de_Stock(stock_filamentos):
    while True:
        print(" ")
        print("== Gestión de Stock ==")
        opcion = input("1 ingresar filamento / 2 buscar filamento / 3 retirar filamento / 4 volver: ")
        print(" ")
        match opcion:
            case "1":
                ingresar_filamento(stock_filamentos)
            case "2":
                buscar_filamento(stock_filamentos)
            case "3":
                retirar_filamento(stock_filamentos)
            case "4":
                break
            case _:
                print("- Opción inválida -")