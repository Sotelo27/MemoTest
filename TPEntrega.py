from functools import partialmethod
from random import choice
from utiles import *
import time

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
    Funcion que modifica la palabra oculta de la lista de acuerdo a si la posicion es correcta o no , con su color correspondiente.
    '''
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
    Funcion que crea una tupla de 2 usuarios con las validaciones correctas.
    '''
    usuario_1 = validar_usuario()
    usuario_2 = validar_usuario()
    return usuario_1, usuario_2

def Validacion(palabra):
    palabra = ["b","s","c","a","v"]
    '''

    Esta Funcion tiene como objetivo evaluar si la palabra ingresada por el usuario es o no valida

    '''
    #Alan Nestor Cristobo
    Error = 0
    if len(palabra) != 5:   # Evaluo la cantidad de caracteres  
        Error = 1
        print("La palabra no contiene 5 letras")

    for x in palabra:   # Evaluo si posee numeros
        if x.isnumeric() == True:
            Error = 2
    if Error == 2:
        print("La palabra solo puede contener letras")

    separador =""   # Junto la lista con la funcion Join para poner los caracteres en mayusculas
    palabra = separador.join(palabra)
    palabra = palabra.upper()
    eliminar_acentos = (("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"))
    for a, b in eliminar_acentos:   # Elimino los acentos con un Replace
        palabra = palabra.replace(a, b).replace(a, b)
    if palabra.isalnum() == False:  # Evaluo si tiene caracteres especiales 
        Error = 3
    palabra = list(palabra) # La rearmo como cada caracter por separado

    if Error == 0:
        return palabra

def introducir_arriesgo():
    #AUTOR: ANDRES DOSKOCH
    '''
    Funcion que tiene como objetivo ingresar la palabra que el usuario arriesga 
    para adivinar, y retornarla para su uso posterior
    '''
    arriesgo = input("Arriesgo: ")
    while len(arriesgo) != 5:
        print ("El largo de la palabra debe contener 5 letras\n")
        arriesgo = input("Arriesgo: \n")
    return arriesgo.upper()

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

#AUTOR : RENATO VILLALBA
def tiempo_jugado(tiempo_de_juego):
    '''
    Funcion que va a mostrar el tiempo que tarde el usuario en adivinar la palabra
    '''

    #AUTOR: RENATO VILLALBA 
    tiempo_minutos = round(tiempo_de_juego // 60)
    tiempo_segundos = round(tiempo_de_juego % 60)
    tiempo_total = print(f"Te tardaste {tiempo_minutos} minutos y {tiempo_segundos} segundos en adivinar la palabra.")

    return tiempo_total

def determinar_final_partida(arriesgo,palabras,intentos,tiempo_inicial):
    #AUTOR: ANDRES DOSKOCH / MOD : LAUTARO MARTIN SOTELO
    #Funcion que informa cuando se a acabado el turno del jugador y a su vez imprime el tiempo que tardo, como los puntos del jugador .
    partida_terminada = False
    if arriesgo.upper() == palabras[0] :
        print(obtener_color("Defecto") + "\npalabra a adivinar: ", palabras[1])
        print("Ganaste!")
        partida_terminada = True
        tiempoJuego = time.time() - tiempo_inicial
        tiempo_jugado(tiempoJuego)
    elif intentos == 5 and arriesgo.upper() != palabras[0]:
        print(obtener_color("Defecto") + "\npalabra a adivinar: ",palabras[0])
        print("Perdiste")
        partida_terminada = True
    return partida_terminada

def juego():
    #AUTORES: ANDRES DOSKOCH / MOD: RENATO VILLALBA - LAUTARO SOTELO 
    #Funcion que desarolla el juego de palabras, generando una matriz y la palabra que se busca adivinar, asi a su vez mostrando al usuario su tablero.
    palabra_adivinar = choice(obtener_palabras_validas()) 
    palabras = [palabra_adivinar.upper(),"?????"] #Se crea una lista que contiene la palabra que se busca, y una palabra que se ira rellenando deacuerdo si la posicion se cumple
    matriz = generar_matriz()
    intentos = 1
    partida_terminada = False
    print(palabras[0])
    while partida_terminada == False:
        empiezaTiempo = time.time()
        print("Palabra a adivinar: ",palabras[1])
        arriesgo = introducir_arriesgo()
        palabra_color = poner_color(arriesgo,palabras)
        modificar_oculta(arriesgo,palabras)
        reemplazar_palabra(matriz,intentos,palabra_color)
        mostrar_matriz(matriz)
        partida_terminada = determinar_final_partida(arriesgo,palabras,intentos,empiezaTiempo)
        if partida_terminada == False:
            intentos += 1
            print(obtener_color("Defecto") + "")
    return partida_terminada

def main():
    #FUNCION MAIN ()
    #AUTORES: RENATO VILLALBA / MOD : LAUTARO MARTIN SOTELO
    #Su funcionalidad es iniciar el juego de palabras, como tambien determinar si el usuario quiere seguir el juego.
    partida_terminada = juego() #Inicia el juego y retorna el boleano True si la partida termino

    while partida_terminada == True:

        seguir_jugando = input("Desea jugar otra partida? (S/N)\n")

        while seguir_jugando.lower() != 's' and seguir_jugando.lower() != 'n':

            print("No entiendo")
            seguir_jugando = input("Desea jugar otra partida? (S/N)\n")

        if seguir_jugando.lower() == 's':
            juego()#vuelve a llamar la funcion de juego, donde se creara una nueva matriz y buscara una nueva palabra

        elif seguir_jugando.lower() == 'n':

            partida_terminada = False
            print("OK, chau.")

main()