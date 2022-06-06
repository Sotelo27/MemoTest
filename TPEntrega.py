from functools import partialmethod
from random import choice
from numpy import true_divide
from utiles import *
import time

def mostrar_puntos_2_jugadores(intento,partida_ganada,puntuaciones_jugador,usuario,turno,puntos):
    #AUTOR: PABLO MARTINEZ / MOD :LAUTARO MARTIN SOTELO
    '''
    Funcion que solo tiene como objetivo printear los puntos de 2 jugadores
    '''
    turno_contrario = cambiar_jugar_partida(turno)
    usuario_2 = list(puntuaciones_jugador.keys())[turno_contrario]
    if intento==1 and partida_ganada==True:
        puntuaciones_jugador[usuario_2] -= puntos
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario],usuario_2,puntos,puntuaciones_jugador[usuario_2]))
    elif intento>1 and partida_ganada==True:
        puntuaciones_jugador[usuario_2] -= puntos
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario],usuario_2,puntos,puntuaciones_jugador[usuario_2]))
    elif intento>1 and partida_ganada==False:
        puntuaciones_jugador[usuario_2] -= 50 
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario],usuario_2,-50,puntuaciones_jugador[usuario_2]))
       

def mostrar_puntos_1_jugador(intento,partida_ganada,puntuaciones_jugador,usuario,puntos):
    #AUTOR : PABLO MARTINEZ
    '''
    Funcion que solo tiene como objetivo printear los puntos de 1 jugador
    '''
    if intento==1 and partida_ganada==True:
        print ("Obtuviste un total de", puntos,"puntos")
    elif intento>1 and partida_ganada==True:
        print ("Obtuviste un total de", puntos ,"puntos, tenes acumulado:",puntuaciones_jugador[usuario])
    elif intento>1 and partida_ganada==False:
        print ("Perdiste un total de", puntos ,"puntos, tenes acumulado:",puntuaciones_jugador[usuario])

def puntos(intento,partida_ganada,puntuaciones_jugador,turno,modo):
    #AUTOR : PABLO MARTINEZ 
    #funcion que dependiendo de la  cantidad de intentos recorre el diccionario de puntos y otorga dichos puntos al jugador.
    intentos_y_puntajes={1:50,2:40,3:30,4:20,5:10,6:-100}
    puntos=intentos_y_puntajes.get(intento)
    if modo == 2:
        usuario = list(puntuaciones_jugador.keys())[turno] # convirtiendolo en lista, la pos 0 sera el jugador 1, y la pos 1 sera el jugador 2.
        puntuaciones_jugador[usuario] += puntos
        mostrar_puntos_2_jugadores(intento,partida_ganada,puntuaciones_jugador,usuario,turno,puntos)
    else:
        #Hacer llamado a funcion de elegir numero del jugador para registrar la acumulacion de puntos del jugador especifico.
        usuario = list(puntuaciones_jugador.keys())[turno] # convirtiendolo en lista, la pos 0 sera el jugador 1, y la pos 1 sera el jugador 2.
        puntuaciones_jugador[usuario] += puntos
        mostrar_puntos_1_jugador(intento,partida_ganada,puntuaciones_jugador,usuario,puntos)

def poner_color(arriesgo,conjunto_palabras):
    '''
    Recibe la palabra que arriesgue el usuario, comprueba que sean iguales con la original.
    Retorna una palabra que contiene los colores de acuerdo a si su posicion es correcta.
    '''
    #AUTOR: ANDRES DOSKOCH / MOD :Lautaro Martin Sotelo
    palabra_color = ""
    palabra = conjunto_palabras[0]
    for i in range (0, len(arriesgo)):

        if i in range (0, len (palabra)):

            if arriesgo[i] == palabra[i]:
                palabra_color += obtener_color("Verde") + arriesgo[i] + obtener_color("Defecto")
            elif (arriesgo[i] in palabra) and arriesgo[i] != palabra[i]:
                palabra_color += obtener_color("Amarillo") + arriesgo[i] + obtener_color("Defecto")
            else:
                palabra_color += obtener_color("Defecto") + arriesgo[i]
    return palabra_color

def modificar_oculta(palabra_sin_revelar,conjunto_palabras):
    #AUTOR : Lautaro Martin Sotelo
    '''
    Funcion que modifica la palabra oculta de la lista de acuerdo a si la posicion es correcta o no , 
    con su color correspondiente.
    '''
    auxiliar = conjunto_palabras[0] #palabra revelada
    auxiliar_2 = conjunto_palabras[1] #palabra sin revelar, con los "?????"
    palabra_oculta = "" #string que reemplazara el valor de la posicion 1 de la lista
    for i in range(len(auxiliar)):
        if auxiliar_2[i] != "?":
            palabra_oculta += auxiliar_2[i] #Aqui se busca que en el caso de que el usuario haya revelado antes una palabra, se le agrega esa letra a la variable
        elif palabra_sin_revelar[i] == auxiliar[i] :
            palabra_oculta += palabra_sin_revelar[i]
        else:
            palabra_oculta += "?"
    conjunto_palabras[1] = palabra_oculta

def validar_usuario():
    #AUTOS > ANDRES DOSKOCH
    '''
    Funcion donde se ingresa el usuario y valida el ingreso, para luego retornar el usuario valido.
    '''
    valido = False
    while valido == False:
        usuario = (input("Ingrese nombre de Jugador : "))
        if usuario.isdigit() or usuario == '':
            print("¡ERROR!. Ingresaste solo numeros / nombre vacio.")
            print("Ejemplo: Juan123 , Andres River Plate, Gallardo_por_siempre")
        else:
            valido = True
    return usuario

def registrar_usuarios (): #AUTOR> ANDRES DOSKOCH / 
    '''
    Funcion que crea un diccionario de 2 usuarios ,validando primero su ingreso.
    '''
    print("USUARIO_1: ")
    usuario_1 = validar_usuario()
    print("USUARIO_2: ")
    usuario_2 = validar_usuario()
    diccionario = {usuario_1:0,usuario_2:0}
    return diccionario

def buscar_invalidaciones(arriesgo):
    '''
    Funcion que recorre el arriesgo hasta que encuentre un caracter no valido
    '''
    #AUTOR: ALAN NESTOR CRISTOBO
    caracteres_validos = ("QWERTYUIOPASDFGHJKLZXCVBNMÁÉÍÓÚ")
    valido = True
    contador = 0
    while valido and contador < len(arriesgo):
        caracter = arriesgo[contador].upper()
        if caracter.isnumeric() or caracter not in caracteres_validos:
            print("Su ingreso de palabra posee caracteres numericos, reingrese nuevamente.")
            valido = False
        contador += 1
    return valido

def Validacion(arriesgo):
    '''

    Esta Funcion tiene como objetivo evaluar si la palabra ingresada por el usuario es o no valida

    '''
    #AUTOR: ALAN NESTOR CRISTOBO
    valido = True
    if len(arriesgo) != 5:   # Evaluo la cantidad de caracteres  
        print("La palabra no contiene 5 letras")
        valido = False
    elif arriesgo.isalnum() == False:  # Evaluo si tiene caracteres especiales 
        print("Su ingreso posee caracteres especiales")
        valido = False
    else:
        valido = buscar_invalidaciones(arriesgo)
    return valido

def reemplazar_caracteres_acentuados(arriesgo):
    '''
    Funcion que reemplaza los caracteres acentuados
    '''
    #AUTOR: ALAN NESTOR CRISTOBO
    palabra = ""
    for caracteres in arriesgo:
        if caracteres == "Á":
            palabra += "A"
        elif caracteres == "É":
            palabra += "E"
        elif caracteres == "Í":
            palabra += "I"
        elif caracteres == "Ó":
            palabra += "O"
        elif caracteres == "Ú":
            palabra += "U"
        else:
            palabra += caracteres.upper()
    return palabra

def introducir_arriesgo():
    #AUTOR: ANDRES DOSKOCH
    '''
    Funcion que tiene como objetivo ingresar la palabra que el usuario arriesga 
    para adivinar, y retornarla para su uso posterior
    '''
    valido = False
    while valido == False:
        arriesgo = input("Arriesgo: ")
        arriesgo = arriesgo.upper()
        valido = Validacion(arriesgo.upper())
    arriesgo = reemplazar_caracteres_acentuados(arriesgo)
    return arriesgo

def generar_matriz()->list:
    '''
    Este tablero "vacio" inicialmente, sera el que visualizen los jugadores durante la partida,
    rellenandose con los ingresos del usuario.
    '''
    #AUTOR : Lautaro Martin Sotelo
    matriz_vacia = []
    for filas in range(5):
        matriz_vacia.append(["?????"]) # a la matriz vacia , introduzco sublistas que contienen string con "?" para luego rellenarse.
    return matriz_vacia 


def mostrar_matriz(matriz:list):
    '''
    Funcion que tiene como objetivo mostrar al usuario la palabra introducida y las anteriores,informando tambien el color que corresponde.
    '''
    #AUTOR :Lautaro Martin Sotelo
    for filas in matriz: 
        print(filas[0])# accedo a cada sublista y printeo su contenido

def reemplazar_palabra(matriz,intento,palabra):
    '''
    Funcion que recibe la matriz, el numero de intento, y la palabra introducida.
    Reemplaza en la matriz por la palabra arriesgada y retorna la nueva matriz con la posicion cambiada
    '''
    #AUTOR : Lautaro Martin Sotelo
    if intento == 1:
        matriz[intento - 1][0] = palabra #Para saber a que fila se debe acceder, el intento -1 sera la fila del usuario, y 0 sera siempre su columna
    elif intento == 2:
        matriz[intento - 1][0] = palabra 
    elif intento == 3:
        matriz[intento - 1][0] = palabra
    elif intento == 4:
        matriz[intento - 1][0] = palabra
    elif intento == 5:
        matriz[intento - 1][0] = palabra
    return matriz

def tiempo_jugado(tiempo_de_juego):
    '''
    Funcion que va a mostrar el tiempo que tarde el usuario en adivinar la palabra
    '''

    #AUTOR: RENATO VILLALBA 
    tiempo_minutos = round(tiempo_de_juego // 60)
    tiempo_segundos = round(tiempo_de_juego % 60)
    tiempo_total = print(f"Ganaste! Tardaste {tiempo_minutos} minutos y {tiempo_segundos} segundos en adivinar la palabra.")

    return tiempo_total

def determinar_final_partida(arriesgo,palabras,intentos,tiempo_inicial,usuarios,turno,modo):
    #AUTOR: ANDRES DOSKOCH / MOD : LAUTARO MARTIN SOTELO - RENADO VILLALBA
    #Funcion que informa cuando se a acabado el turno del jugador y a su vez imprime el tiempo que tardo, como los puntos del jugador .
    partida_terminada = False
    if arriesgo.upper() == palabras[0] :
        print(obtener_color("Defecto") + "\npalabra a adivinar: ", palabras[1])
        partida_terminada = True
        tiempoJuego = time.time() - tiempo_inicial
        tiempo_jugado(tiempoJuego)
        puntos(intentos,partida_terminada,usuarios,turno,modo)
    elif intentos == 6 and arriesgo.upper() != palabras[0]:
        print(obtener_color("Defecto") + "\npalabra a adivinar: ",palabras[0])
        puntos(intentos,partida_terminada,usuarios,turno,modo)
        print("Perdiste!")
        partida_terminada = True
    return partida_terminada

def elegir_quien_comienza(lista):
    #AUTOR: IGNACIO OVIEDO 
    '''
    Elige al azar quien comenzara el juego
    '''
    valor = [0,1]
    turno = choice(valor)
    lista[0] = turno

def cambiar_jugador_global(lista):
    #AUTOR:IGNACIO OVIEDO
    """
    Es para ir variando el inicio de los jugadores en el modo dos jugadores,variando el valor de la lista
    """
    if lista[0] == 0:
        lista[0] = 1
    else:
        lista[0] = 0

def cambiar_jugar_partida(numero):
    #AUTOR:IGNACIO OVIEDO
    #cambia el jugador durante la ronda.
    if numero == 0:
        numero = 1
    else:
        numero = 0
    return numero

def juego(usuarios,turno,modo):
    #AUTORES: ANDRES DOSKOCH / MOD: RENATO VILLALBA - LAUTARO SOTELO 
    #Funcion que desarolla el juego de palabras, generando una matriz y la palabra que se busca adivinar, asi a su vez mostrando al usuario su tablero.
    palabra_adivinar = choice(obtener_palabras_validas()) 
    palabras = [palabra_adivinar.upper(),"?????"] #Se crea una lista que contiene la palabra que se busca, y una palabra que se ira rellenando deacuerdo si la posicion se cumple
    matriz = generar_matriz()
    intentos = 1
    partida_terminada = False
    print(palabras[0])
    while partida_terminada == False:
        print("Es el turno de {}".format(list(usuarios.keys())[turno])) #Similar que en la funcion puntos, al convertirlo en lista, solo accediendo a la posicion accedo a la clave/nombre del usuario.
        empiezaTiempo = time.time()
        print("Palabra a adivinar: ",palabras[1])
        mostrar_matriz(matriz)
        arriesgo = introducir_arriesgo()
        palabra_color = poner_color(arriesgo,palabras)
        modificar_oculta(arriesgo,palabras)
        reemplazar_palabra(matriz,intentos,palabra_color)
        mostrar_matriz(matriz)
        if modo == 2:
            turno = cambiar_jugar_partida(turno)
        partida_terminada = determinar_final_partida(arriesgo,palabras,intentos,empiezaTiempo,usuarios,turno,modo)
        if partida_terminada == False:
            intentos += 1
            print(obtener_color("Defecto") + "")
    return partida_terminada

def eleccion_jugadores():
    #AUTOR: IGNACIO OVIEDO
    """
    Esta funcion es para que el usuario elija de a cuantos jugadores quiere jugar.
    """
    eleccion = int(input("¿De a cuantos jugadores quiere jugar?¿De 1 jugador o 2 jugadores?: "))
    while eleccion!=1 and eleccion!=2 :
        print(f"Disculpe, no entendi. Recuerde que solo puede responder 1 o 2")
        eleccion=input("¿De a cuantos jugadores quiere jugar?¿De 1 jugador o 2 jugadores?: ")
    return eleccion

def ganador_2_jugadores(usuarios):
    #AUTOR : IGNACIO OVIEDO
    ganador = sorted(usuarios,key=lambda x:x )
    print("El ganador es {} con un total de {} puntos.".format(ganador[0],usuarios[ganador[0]]))

def volver_a_jugar(partida_terminada,seguir_jugando,usuarios,modo,turno):
    #AUTOR: RENATO VILLALBA
    if seguir_jugando.lower() == 's':
        if modo == 2:
            cambiar_jugador_global(turno)
            partida_terminada = juego(usuarios,turno[0],modo)
        else:
            partida_terminada = juego(usuarios,turno[0],modo)
    elif seguir_jugando.lower() == 'n':
        if modo == 2:
            ganador_2_jugadores(usuarios)
        partida_terminada = False
        print("Hasta luego!Fiuble cerrando.")
    return partida_terminada

def main():
    #FUNCION MAIN ()
    #AUTORES: RENATO VILLALBA / MOD: IGNACIO OVIEDO - SOTELO LAUTARO MARTIN
    #Su funcionalidad es iniciar el juego de palabras, como tambien determinar si el usuario quiere seguir el juego.
    print("---Bienvenido a FIUBLE---\n")
    print("El objetivo del juego es adivinar una palabra en menos de 5 intentos\n")
    print("A continuacion , eliga si quiere jugar solo 1 jugador o 2.\n")
    modo = eleccion_jugadores() # se elige el modo el cual se desarrolla el juego, de 1 solo jugador o 2.
    turno_global = [0] #Los turnos seran una lista, para evitar el uso de muchos returns, y para que su valor sea mutable continuamente, asi alterar entre jugador y jugador.
    if modo == 2:
        usuarios = registrar_usuarios() #Se registra a los usuarios que desarrollaran el juego.
        elegir_quien_comienza(turno_global)#Se toma al azar el valor del turno.
        partida_terminada = juego(usuarios,turno_global[0],modo)
    else:
        usuarios = {"Jugador_1":0} #Se crea un diccionario generico para el caso de que sea 1 solo jugador.
        partida_terminada = juego(usuarios,turno_global[0],modo)
    while partida_terminada == True:
        seguir_jugando = input("Desea jugar otra partida? (S/N): ")

        while seguir_jugando.lower() != 's' and seguir_jugando.lower() != 'n':

            print("No entiendo")
            seguir_jugando = input("Desea jugar otra partida? (S/N): ")
        partida_terminada = volver_a_jugar(partida_terminada,seguir_jugando,usuarios,modo,turno_global)
    
main()