from functools import partialmethod
from random import choice
from utiles import *
import time

PALABRA_ADIVINAR = choice(obtener_palabras_validas())

def adivinar(): #elige una palabra al azar
    '''

    Funcion que tiene como objetivo retornar una palabra elegida al azar para que el usuario descubra.

    '''
    #ANDRES
    LISTA = ["abran", "besos", "espia", "gatos", "manda"]
    palabra = choice(LISTA)
    return palabra

def poner_color(arriesgo,conjunto_palabras):
    '''

    Recibe la palabra que arriesgue el usuario, comprueba que sean iguales con la original.
    Retorna una palabra que contiene los colores de acuerdo a si su posicion es correcta.
    '''
    #ANDRES
    palabra_color = ""
    palabra = conjunto_palabras[0]
    for i in range (0, len(arriesgo)):
    
        if i in range (0, len (palabra)):

            if arriesgo[i] == palabra[i]:
                palabra_color += obtener_color("Verde") + arriesgo[i]
            elif (arriesgo[i] in palabra) and arriesgo[i] != palabra[i]:
                palabra_color += obtener_color("Amarillo") + arriesgo[i]
            else:
                palabra_color += obtener_color("Defecto") + arriesgo[i]
    #modificar_oculta(arriesgo,conjunto_palabras)
    return palabra_color

def modificar_oculta(palabra_sin_revelar,conjunto_palabras):
    auxiliar = conjunto_palabras[0]
    auxiliar_2 = conjunto_palabras[1]
    palabra_oculta = ""
    for i in range(len(auxiliar)):
        if auxiliar_2[i] != "?":
            palabra_oculta += auxiliar_2[i]
        elif palabra_sin_revelar[i] == auxiliar[i] :
            palabra_oculta += palabra_sin_revelar[i]
        else:
            palabra_oculta += "?"
    conjunto_palabras[1] = palabra_oculta

def introducir_arriesgo():
    '''
    Funcion que tiene como objetivo ingresar la palabra que el usuario arriesga para adivinar, y retornarla para su uso posterior
    '''
    arriesgo = input("Arriesgo: ")
    while len(arriesgo) != 5:
        print ("El largo de la palabra debe contener 5 letras\n")
        arriesgo = input("Arriesgo: \n")
    return arriesgo

def palabra_arriesgo (): #Recibe una palabra al azar 
    palabras = [adivinar(),"?????"]
    ganaste = False
    matriz = generar_matriz()
    intentos = 1

    while intentos <= 5:
        print("Palabra a adivinar: ",palabras[1])
        arriesgo = introducir_arriesgo()
        palabra_color = poner_color(arriesgo,palabras)
        modificar_oculta(arriesgo,palabras)
        reemplazar_palabra(matriz,intentos,palabra_color)
        mostrar_matriz(matriz)
        if arriesgo == palabras[0] :
            intentos = 6
            print(obtener_color("Defecto") + "\npalabra a adivinar: ", palabras[1])
            print("Ganaste!")
            ganaste = True

        else:
            intentos += 1
            print(obtener_color("Defecto") + "Incorrecto")
    
    return ganaste


def generar_matriz()->list:
    '''

    Este tablero "vacio" sera el que visualizen los jugadores durante la partida.

    '''
    #Lautaro Martin Sotelo
    matriz_vacia = []
    for filas in range(5):
        matriz_vacia.append(["?????"]) # a la matriz vacia , introduzco sublistas que contienen string con "?" para luego rellenarse.
    return matriz_vacia 

def mostrar_matriz(matriz:list):
    '''

    Funcion que tiene como objetivo mostrar al usuario la palabra introducida y las anteriores.

    '''
    #Lautaro Martin Sotelo
    for filas in matriz: 
        print(filas[0])# accedo a cada sublista y printeo su contenido


def reemplazar_palabra(matriz,intento,palabra):
    '''

    Funcion que recibe la matriz, el numero de intento, y la palabra introducida.
    Reemplaza en la matriz por la palabra arriesgada y retorna la nueva matriz con la posicion cambiada

    '''
    #Lautaro Martin Sotelo
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


def tiempo_jugado():
    '''
    Funcion que va a mostrar el tiempo que tarde el usuario en adivinar la palabra
    '''
    #Renato Villalba

    intento = introducir_arriesgo()
    inicio_de_partida = time.time() #Comienza el temporizador desde 0
    tiempo_total = 0
    if intento == PALABRA_ADIVINAR: 

        final_de_partida = time.time() #finaliza el temporizador

        tiempo_segundos = round(final_de_partida - inicio_de_partida)
        tiempo_minutos = round(tiempo_segundos // 60)
        tiempo_total = print(f"Te tardaste {tiempo_minutos} minutos y {tiempo_segundos} segundos en adivinar la palabra")

    return tiempo_total

def volver_a_jugar():
    '''
    Funcion que recibe la respuesta del usuario para saber si se vuelve a jugar o termina el programa
    '''
    #Renato Villalba
    partida_terminada = palabra_arriesgo() #Recibe un booleano

    while partida_terminada == True:

        seguir_jugando = input("Desea jugar otra partida? (S/N)\n")

        while seguir_jugando.lower() != 's' and seguir_jugando.lower() != 'n':

            print("No entiendo")
            seguir_jugando = input("Desea jugar otra partida? (S/N)\n")

        if seguir_jugando.lower() == 's':

            PALABRA_ADIVINAR = choice(obtener_palabras_validas()) #Genera la palabra al azar
            palabra_arriesgo()

        elif seguir_jugando.lower() == 'n':
            
            partida_terminada = False
            print("OK, chau.")

#tiempo_jugado()
volver_a_jugar()
