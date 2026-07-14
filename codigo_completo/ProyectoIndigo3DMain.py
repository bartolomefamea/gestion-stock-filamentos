#from ProyectI3DFunciones import *
from .funciones_json_backup import *
from .excel_funciones import *
from .stock import *
from .menus import *
from .historial import *
from .modelos import *
print(' ')
##MENU PRINCIPAL

print('== Menu principal ==')
print(' ')

#cuando corro el proyecto cargo en el stock del programa el stock del excel(en este acso del .json)
#stock_filamentos = cargar_stock()

#lo mismo pero par ael excel
stock_filamentos = importar_stock_desde_excel()
exportar_stock_a_excel(stock_filamentos)

#bucle para "estar" en el Menu
while True:
    opcion = input("1 gestion de stock / 2 stock / 3 historial / 4 cerrar: ")# 

    match opcion:
        case "1":
            gestion_de_Stock(stock_filamentos)
            #ingresar_filamento(stock_filamentos)
        case "2":
            menu_stock(stock_filamentos)
            #mostrar_stock(stock_filamentos)
        case "3": #historial --> dar opciones ultimo ingreso, ultimo retiro, mostrar todo el historial, buscar por fecha, buscar por color, buscar por fabricante
            menu_historial()
        case "4":
            break
        case _:
            print("Opción inválida")
    
#-pregunta
#-funcion 1 stock
#-funcion 2 ingresar filamento
#-funcion 3 x cosa



