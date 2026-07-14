from .modelos import Filamento
from .excel_funciones import *
from .historial import *
from .funciones_json_backup import guardar_stock, registrar_movimiento



def ingresar_filamento(stock_filamentos):
    print(' ')
    cantidad_ingresar = input('-- Cuantos filamentos distintos quiere ingresar? --')
    #por si no se ingresa numero
    while cantidad_ingresar.isdigit() == False:
        print('Debe ingresar un número')
        cantidad_ingresar = input('cuantos filamentos desea ingresar? ')
    for i in range(int(cantidad_ingresar)):
        print(' ------ ')
    #cuantas veces se repite el for
        print('- Filamento ',  i+1 ,' de ', cantidad_ingresar + ' -')
    #datos string 
        color_filamento = input('- Ingrese el color del filamento -')
        fabricante_del_filamento = input('- Ingrese el fabricante -')
    #pedir un digito como cantidad a sumar   
        cantidad_filamentos = input('- Ingrese la cantidad de filamentos del color -' + color_filamento.capitalize() + ' ')##este numero seguramente lo tenga que pasar a string para ponerlo en el excel
        while cantidad_filamentos.isdigit() == False:
            print('== Error ==')
            print('- La cantidad de filamentos debe ser un numero, vuelva a ingresar el dato -')
          
            cantidad_filamentos = input('- Ingrese la cantidad de filamentos del color -' + color_filamento.capitalize() + ' ')
    #necesite igualar la estructura porque no me tomaba el filamento_ingresado en la siguiente funcion
    #de esta forma va a quedar guardado el filametno que ingrese
        filamento_ingresado = Filamento(
            color_filamento.capitalize(),
            fabricante_del_filamento.capitalize(),
            int(cantidad_filamentos)
        )
        
        actualizar_stock(filamento_ingresado, stock_filamentos)
        print(' ')
        print('= Ingreso '+ cantidad_filamentos + ' filamentos del color ' + color_filamento.capitalize() + ' del fabricante ' + fabricante_del_filamento.capitalize() + ' al stock =')
        #quiere ver la fecha de ingreso? o un consultar fechas mas adelante
        print('= Fecha de ingreso: ' + str(datetime.now().strftime('%Y-%m-%d')) + ' =')   
        filamento_ingresado = color_filamento.capitalize(), fabricante_del_filamento.capitalize(), int(cantidad_filamentos)
 
 
        
#actualizo con lista aux el stock del .json
def actualizar_stock(filamento_ingresado : Filamento, stock_filamentos):
    print(' ')
    #recorro la lista de stock_filamentos para ver si ya esta el color y el fabricante, si esta solo sumo la cantidad, si no esta lo agrego a la lista
    
    for filamento in stock_filamentos:
        if filamento.color == filamento_ingresado.color and filamento.fabricante == filamento_ingresado.fabricante:
            print('== Hay ' + str(filamento.cantidad) + ' filamentos ' + filamento.color + 's de ' + filamento.fabricante + ' en stock ==')
            filamento.cantidad += filamento_ingresado.cantidad
            break
    #si esta en stock me pasa la update del filamento, si no esta agrega el nuevo al stock
    else:
            stock_filamentos.append(filamento_ingresado)
            print('== Se registro el filamento correctament == ')
            
    stock_filamentos.sort(key=lambda filamento: (filamento.color.lower(), filamento.fabricante.lower()))
    exportar_stock_a_excel(stock_filamentos)
    guardar_stock(stock_filamentos)
    registrar_movimiento("Agrego", filamento_ingresado, filamento_ingresado.cantidad)
    
   
    
def buscar_filamento(stock_filamentos):
    color_buscado = input("- Color a buscar: ").strip().capitalize()#implementar strip en todas, si el usuario escribe con espacio se corrige
    fabricante_buscado = input("- Fabricante a buscar, enter para omitir: ").strip().capitalize()

    encontrado = False
#tener en cuenta que estoy utilizando stock que viene a ser un aux
    for filamento in stock_filamentos:
        coincide_color = filamento.color == color_buscado
        coincide_fabricante = fabricante_buscado == "" or filamento.fabricante == fabricante_buscado

        if coincide_color and coincide_fabricante:
            print(f'{filamento.color:<12} | {filamento.fabricante:<12} | {filamento.cantidad:<8}')
            encontrado = True

    if encontrado == False:
        print("- No se encontró ningún filamento -")



def retirar_filamento(stock_filamentos):
    color_buscado = input("- Color a retirar: ").strip().capitalize()
    fabricante_buscado = input("- Fabricante del filamento: ").strip().capitalize()
    
    for filamento in stock_filamentos:
        if filamento.color == color_buscado and filamento.fabricante == fabricante_buscado:
            
            cantidad_a_retirar = input("- Cantidad a retirar: ").strip()
            #que pasa si no es un numero? o si es mayor a la cantidad que hay en stock?
            while (
            not cantidad_a_retirar.isdigit() 
            or int(cantidad_a_retirar) <= 0 
            or int(cantidad_a_retirar) > filamento.cantidad
            ):
                if not cantidad_a_retirar.isdigit():
                    print("- Cantidad inválida. Intente nuevamente.")
                else:
                    print("- No hay suficiente stock -")
                    print(f"- Stock actual: {filamento.cantidad} -")
                cantidad_a_retirar = input("- Cantidad a retirar: ").strip()
            #lo tengo que pasar a int para poder restarlo
            filamento.cantidad -= int(cantidad_a_retirar)
            exportar_stock_a_excel(stock_filamentos)
            guardar_stock(stock_filamentos)
            registrar_movimiento("retiro", filamento, int(cantidad_a_retirar))
            print("- Stock retirado correctamente -")
            print(f"- Quedan {filamento.cantidad} filamentos -")
            return
    #si sale del for es porque no encontro el filamento
    print("- No se encontró ese filamento -")
    respuesta = input('- Volver al menu principal/Descontar filamento? (1/2): ').strip()
    if respuesta == '1':
        return
    elif respuesta == '2':
        retirar_filamento(stock_filamentos)



def mostrar_stock(stock_filamentos):
    print("== Stock ==")
    print(f'{"Color":<12} | {"Fabricante":<12} | {"Cantidad":<8}')

    for filamento in stock_filamentos:
        print(f'{filamento.color:<12} | {filamento.fabricante:<12} | {filamento.cantidad:<8}')



def mostrar_stock_clasificado(stock_filamentos):
    #creo 3 listas para clasificar los filamentos por cantidad
    sin_stock = []
    stock_bajo = []
    stock_ok = []

    for filamento in stock_filamentos:
        if filamento.cantidad == 0:
            sin_stock.append(filamento)
        elif filamento.cantidad <= 2:
            stock_bajo.append(filamento)
        else:
            stock_ok.append(filamento)

    print("== Sin stock ==")
    imprimir_lista_filamentos(sin_stock)

    print("== Stock bajo ==")
    imprimir_lista_filamentos(stock_bajo)

    print("== Stock disponible ==")
    imprimir_lista_filamentos(stock_ok)
    

#lista_filametnos asi no hay que repetir el codigo, si la lista esta vacia no hace nada, si tiene datos los muestra
def imprimir_lista_filamentos(stock_filamentos):
    if len(stock_filamentos) == 0:
        print("- No hay filamentos para mostrar -")
        return

    print(f'{"Color":<12} | {"Fabricante":<12} | {"Cantidad":<8}')

    for filamento in stock_filamentos:
        print(f'{filamento.color:<12} | {filamento.fabricante:<12} | {filamento.cantidad:<8}')



def ordenar_stock(stock_filamentos):
    stock_filamentos.sort(
        key=lambda filamento: (
            filamento.color.lower(),
            filamento.fabricante.lower()
        )
    )
    
    
#solucion fallo de filmaneto duplicado
def unificar_stock(stock_filamentos):

    stock_unificado = {}

    for filamento in stock_filamentos:

        clave = (
            filamento.color.lower(),
            filamento.fabricante.lower()
        )

        if clave in stock_unificado:
            stock_unificado[clave].cantidad += filamento.cantidad
        else:
            stock_unificado[clave] = filamento

    stock_filamentos.clear()
    stock_filamentos.extend(stock_unificado.values())

    stock_filamentos.sort(
        key=lambda f: (f.color.lower(), f.fabricante.lower())
    )

    exportar_stock_a_excel(stock_filamentos)