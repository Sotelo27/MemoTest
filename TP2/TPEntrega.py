from functools import partialmethod
from random import choice
from utiles import *
import time

def mostrar_puntos_2_jugadores(datos_partida,puntuaciones_jugador,usuario,puntos):
    '''
    AUTOR: PABLO MARTINEZ / MOD :LAUTARO MARTIN SOTELO
    Funcion que solo tiene como objetivo printear los puntos de 2 jugadores
    recibe una lista llamada datos_partida que contiene [arriesgo,intentos,turno,modo,partida_ganada]y las puntuaciones de jugador que es un diccionario, con el usuario numero 1 y los puntos 
    que sera variable int
    '''
    turno_contrario = cambiar_jugador(datos_partida[2])
    usuario_2 = list(puntuaciones_jugador.keys())[turno_contrario]
    if datos_partida[1] ==1 and datos_partida[4] == True:
        puntuaciones_jugador[usuario_2] -= puntos
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario],usuario_2,puntos,puntuaciones_jugador[usuario_2]))
    elif datos_partida[1] > 1 and datos_partida[4] == True:
        puntuaciones_jugador[usuario_2] -= puntos
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario],usuario_2,puntos,puntuaciones_jugador[usuario_2]))
    elif datos_partida[1] > 1 and datos_partida[4] == False:
        puntuaciones_jugador[usuario_2] -= 100 
        puntuaciones_jugador[usuario] += 50
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,-50,puntuaciones_jugador[usuario],usuario_2,-100,puntuaciones_jugador[usuario_2]))
       

def mostrar_puntos_1_jugador(datos_partida,puntuaciones_jugador,usuario,puntos):
    '''
    AUTOR : PABLO MARTINEZ

    Funcion que solo tiene como objetivo printear los puntos de 1 jugador
    recibe una lista llamada datos_partida que contiene [arriesgo,intentos,turno,modo,partida_ganada]y las puntuaciones de jugador que es un diccionario, con el usuario numero 1 y los puntos 
    que sera variable int
    '''
    if datos_partida[1] ==1 and datos_partida[4] == True:
        print ("Obtuviste un total de", puntos,"puntos")
    elif datos_partida[1] > 1 and datos_partida[4] == True:
        print ("Obtuviste un total de", puntos ,"puntos, tenes acumulado:",puntuaciones_jugador[usuario])
    elif datos_partida[1] >1 and datos_partida[4] == False:
        print ("Perdiste un total de", puntos ,"puntos, tenes acumulado:",puntuaciones_jugador[usuario])

def puntos(datos_partida,puntuaciones_jugador):
    '''
    AUTOR : PABLO MARTINEZ 

    PRE: recibe una lista llamada datos_partida que contiene [arriesgo,intentos,turno,modo,partida_ganada] y las puntuaciones de jugador que es un diccionario.

    POST: recorre el diccionario de puntos y otorga dichos puntos al jugador.
    '''
    intentos_y_puntajes={1:50,2:40,3:30,4:20,5:10,6:-100}
    puntos=intentos_y_puntajes.get(datos_partida[1])
    if datos_partida[3] == 2:
        usuario = list(puntuaciones_jugador.keys())[datos_partida[2]]# convirtiendolo en lista, la pos 0 sera el jugador 1, y la pos 1 sera el jugador 2.
        puntuaciones_jugador[usuario] += puntos
        mostrar_puntos_2_jugadores(datos_partida,puntuaciones_jugador,usuario,puntos)
    else:
        #Hacer llamado a funcion de elegir numero del jugador para registrar la acumulacion de puntos del jugador especifico.
        usuario = list(puntuaciones_jugador.keys())[datos_partida[2]] # convirtiendolo en lista, la pos 0 sera el jugador 1, y la pos 1 sera el jugador 2.
        puntuaciones_jugador[usuario] += puntos
        mostrar_puntos_1_jugador(datos_partida,puntuaciones_jugador,usuario,puntos)

def poner_color(arriesgo,conjunto_palabras):
    '''
    AUTOR: ANDRES DOSKOCH / MOD :Lautaro Martin Sotelo

    PRE:Recibe la palabra que arriesgue el usuario, comprueba que sean iguales con la original.

    POST:Retorna una palabra que contiene los colores de acuerdo a si su posicion es correcta.
    '''
    
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
    '''
    AUTOR : LAUTARO MARTIN SOTELO

    Funcion que modifica la palabra oculta de la lista de acuerdo a si la posicion es correcta o no , 
    con su color correspondiente.

    PRE: recibe el arriesgo y el conjunto de palabras que es una lista que contiene la palabra revelada y la palabra que se ira rellenando.

    POST: modifica los caracteres de la palabra no revelada.
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
    '''
    AUTOR: ANDRES DOSKOCH

    Funcion donde se ingresa el usuario y valida el ingreso, para luego retornar el usuario valido.

    PRE: -----

    POST: devuelve un string que contiene el nombre de usuario
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

def registrar_usuarios ():  
    '''
    AUTOR: ANDRES DOSKOCH 

    Funcion que crea un diccionario de 2 usuarios ,validando primero su ingreso.

    PRE: ----

    POST: devuelve un diccionario con clave los nombre de usuario y puntos como valor.
    '''
    print("USUARIO_1: ")
    usuario_1 = validar_usuario()
    print("USUARIO_2: ")
    usuario_2 = validar_usuario()
    diccionario = {usuario_1:0,usuario_2:0}
    return diccionario

def buscar_invalidaciones(arriesgo):
    '''
    AUTOR: ALAN NESTOR CRISTOBO

    Funcion que recorre el arriesgo hasta que encuentre un caracter no valido.

    PRE: recibe como parametro un string introducido por el usuario.

    POST: devuelve un boleano que indica TRUE si es valido el string ingresado o FALSE si no cumple las condiciones.
    '''
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
    AUTOR: ALAN NESTOR CRISTOBO
    Esta Funcion tiene como objetivo evaluar si la palabra ingresada por el usuario es o no valida
    
    PRE: recibe como parametro un string introducido por el usuario.

    POST: devuelve un booleano que informa TRUE en caso de que su longitud sea de 5, FALSE si es menor o mayor o no cumple las condiciones.
    '''
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
    #AUTOR: ALAN NESTOR CRISTOBO
    Funcion que reemplaza los caracteres acentuados

    PRE: recibe como parametro un string que fue la palabra introducida por el usuario para recorrerla.

    POST: devuelve un string con los los caracteres acentuados reemplazados por caracteres sin acentuar.
    '''
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
    '''
    AUTOR: ANDRES DOSKOCH
    Funcion que tiene como objetivo ingresar la palabra que el usuario arriesga.

    PRE: ---

    POST: devuelve una variable string que contiene la palabra que arriesga el jugador.

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
    AUTOR: LAUTARO MARTIN SOTELO
    Este tablero "vacio" inicialmente, sera el que visualizen los jugadores durante la partida,
    rellenandose con los ingresos del usuario.

    PRE: ---

    POST: devuelve una matriz.
    '''
    matriz_vacia = []
    for filas in range(5):
        matriz_vacia.append(["?????"]) # a la matriz vacia , introduzco sublistas que contienen string con "?" para luego rellenarse.
    return matriz_vacia 


def mostrar_matriz(matriz:list):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    Funcion que tiene como objetivo mostrar al usuario la palabra introducida y las anteriores,informando tambien el color que corresponde.

    PRE: recibe un parametro matriz de tipo lista.

    POST: unicamente printea por filas la matriz.
    '''
    
    for filas in matriz: 
        print(filas[0])# accedo a cada sublista y printeo su contenido

def reemplazar_palabra(matriz,intento,palabra):
    '''
    AUTOR : LAUTARO MARTIN SOTELO

    PRE:recibe la matriz, el numero de intento, y la palabra introducida.

    POST:Reemplaza en la matriz por la palabra arriesgada y retorna la nueva matriz con la posicion cambiada
    '''
    
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
    AUTOR: RENATO VILLALBA

    Funcion que va a mostrar el tiempo que tarde el usuario en adivinar la palabra

    PRE: recibe la variable que contiene el tiempo de juego.

    POST: consigue y redondea los minutos y segundos en sus respectivas variables, printeando el tiempo en que se consiguio adivinar la palabra.

    '''
 
    tiempo_minutos = round(tiempo_de_juego // 60)
    tiempo_segundos = round(tiempo_de_juego % 60)
    tiempo_total = print(f"Ganaste! Tardaste {tiempo_minutos} minutos y {tiempo_segundos} segundos en adivinar la palabra.")


def determinar_final_partida(datos_partida,palabras,tiempo_inicial,usuarios):
    '''
    AUTOR: ANDRES DOSKOCH / MOD : LAUTARO MARTIN SOTELO - RENADO VILLALBA

    Funcion que informa cuando se a acabado el turno del jugador y a su vez imprime el tiempo que tardo, como los puntos del jugador.
    
    PRE: recibe como parametro la lista DATOS_PARTIDA que contiene la informacion del juego, la lista palabras que contiene la palabra oculta y la palabra a revelar, el tiempo en adivinar y un diccionario con los usuarios.

    POST: determina cuando se acaba un turno de jugador, y sus puntos , con su tiempo en caso de acertar,a su vez modificando la variable booleana en la posicion 3 de la lista empaquetada.


    '''
    arriesgo = datos_partida[0] #desempaqueto de la lista los datos que necesito para la partida.
    intentos = datos_partida[1]
    if arriesgo.upper() == palabras[0] :
        print(obtener_color("Defecto") + "\npalabra a adivinar: ", palabras[1])
        datos_partida[4] = True
        tiempoJuego = time.time() - tiempo_inicial
        tiempo_jugado(tiempoJuego)
        puntos(datos_partida,usuarios)
    elif intentos == 6 and arriesgo.upper() != palabras[0]:
        print(obtener_color("Defecto") + "\npalabra a adivinar: ",palabras[0])
        puntos(datos_partida,usuarios)
        print("Perdiste!")
        datos_partida[4] = True
    

def elegir_quien_comienza(lista):
     
    '''
    AUTOR: IGNACIO OVIEDO

    Elige al azar quien comenzara el juego

    PRE: recibe como parametro LISTA que contiene el turno global con el que se iniciara la partida.

    POST: devuelve la lista modificando el valor int que contiene, siendo el turno global.
    '''
    valor = [0,1]
    turno = choice(valor)
    lista[1] = turno

def cambiar_jugador(numero):
    '''
    AUTOR:IGNACIO OVIEDO

    PRE: recibe como parametro numero, que sera el turno de la partida.

    POST: devuelve una variable int cambiando el numero inicial, en este caso si es 0 valdra 1 y si es 1 valdra 0.

    '''
    if numero == 0:
        numero = 1
    else:
        numero = 0
    return numero

def juego(usuarios,datos_globales):
    '''
    #AUTORES: ANDRES DOSKOCH / MOD: RENATO VILLALBA - LAUTARO SOTELO 

    Funcion que desarolla el juego de palabras, generando una matriz y la palabra que se busca adivinar, asi a su vez mostrando al usuario su tablero.

    PRE: recibe los parametros USUARIOS que jugaran la partida, el TURNO del jugador que iniciara y el MODO de 1 o 2 jugadores.

    POST: devuelve un booleano que indica si la partida finalizo o no.

    '''

    palabra_adivinar = choice(obtener_palabras_validas()) 
    palabras = [palabra_adivinar.upper(),"?????"] #Se crea una lista que contiene la palabra que se busca, y una palabra que se ira rellenando deacuerdo si la posicion se cumple
    matriz = generar_matriz()
    intentos = 1
    partida_terminada = False
    datos_partida = ['',intentos,datos_globales[1],datos_globales[0],partida_terminada] #Empaqueto los datos necesarios para llevar a cabo el juego y no usar el uso de parametros de mas.
    print(palabras[0])
    while partida_terminada == False:
        print("Es el turno de {}".format(list(usuarios.keys())[datos_partida[2]])) #Similar que en la funcion puntos, al convertirlo en lista, solo accediendo a la posicion accedo a la clave/nombre del usuario.
        empiezaTiempo = time.time()
        print("Palabra a adivinar: ",palabras[1])
        mostrar_matriz(matriz)
        arriesgo = introducir_arriesgo()
        datos_partida[0] = arriesgo # le asigno en la posicion 0 el valor del arriesgo.
        palabra_color = poner_color(datos_partida[0],palabras)
        modificar_oculta(datos_partida[0],palabras)
        reemplazar_palabra(matriz,datos_partida[1],palabra_color)
        mostrar_matriz(matriz)
        determinar_final_partida(datos_partida,palabras,empiezaTiempo,usuarios)
        partida_terminada = datos_partida[4]
        if datos_globales[0] == 2:
            datos_partida[2] = cambiar_jugador(datos_partida[2])
        if datos_partida[4] == False:
            datos_partida[1] += 1
            print(obtener_color("Defecto") + "")
    return datos_partida[4]

def eleccion_jugadores():
    '''
    AUTOR: IGNACIO OVIEDO

    Esta funcion es para que el usuario elija de a cuantos jugadores quiere jugar.

    PRE: ----

    POST: Devuelve una variable int que indica la cantidad de jugadores de la partida.
    
    '''
    eleccion = int(input("¿De a cuantos jugadores quiere jugar?¿De 1 jugador o 2 jugadores?: "))
    while eleccion!=1 and eleccion!=2 :
        print(f"Disculpe, no entendi. Recuerde que solo puede responder 1 o 2")
        eleccion=int(input("¿De a cuantos jugadores quiere jugar?¿De 1 jugador o 2 jugadores?: "))
    return eleccion

def ganador_2_jugadores(usuarios):
    '''
    AUTOR : IGNACIO OVIEDO

    PRE: recibe un diccionario que contiene los nombres de los usuarios y los puntos ganados, para ordenarlo y decidir el ganador.

    POST: unicamente printea el ganador de la partida de acuerdo a un ordenamiento del diccionario.

    '''
    ganador = sorted(usuarios.items(),key=lambda x:x[1],reverse=True)
    print("El ganador es {} con un total de {} puntos.".format(ganador[0][0],ganador[0][1]))

def volver_a_jugar(partida_terminada,seguir_jugando,usuarios,datos_globales):
    '''
    AUTOR: RENATO VILLALBA

    Funcion que tiene como objetivo determinar o no el inicio de otro juego.

    PRE: recibe un booleno que indica la finalizacion de la partida, un string que indica si el usuario desea continuar el juego, un diccionario con nombre y puntos de usuarios , y 
    una lista con el turno y el modo de juego.

    POST: devuelve un boleano que variara , siendo FALSE para terminar la partida y TRUE en caso de seguir.
    '''
    modo = datos_globales[0]
    if seguir_jugando.lower() == 's':
        if modo == 2:
            datos_globales[1] = cambiar_jugador(datos_globales[1])
            partida_terminada = juego(usuarios,datos_globales)
        else:
            partida_terminada = juego(usuarios,datos_globales)
    elif seguir_jugando.lower() == 'n':
        if modo == 2:
            ganador_2_jugadores(usuarios)
        partida_terminada = False
        print("Hasta luego!Fiuble cerrando.")
    return partida_terminada

def main():
    '''
    FUNCION MAIN ()

    AUTORES: RENATO VILLALBA / MOD: IGNACIO OVIEDO - SOTELO LAUTARO MARTIN

    Su funcionalidad es iniciar el juego de palabras, como tambien determinar si el usuario quiere seguir el juego.
    '''
    print("---Bienvenido a FIUBLE---\n")
    print("El objetivo del juego es adivinar una palabra en menos de 5 intentos\n")
    print("A continuacion , eliga si quiere jugar solo 1 jugador o 2.\n")
    datos_globales =[eleccion_jugadores(),0] #se empaquetan los datos globales para evitar el uso de parametros innecesarios,los turnos seran la posicion 1 guardados en tipo lista y el modo de juego la posicion 0 .
    if datos_globales[0] == 2:
        usuarios = registrar_usuarios() #Se registra a los usuarios que desarrollaran el juego.
        elegir_quien_comienza(datos_globales)#Se toma al azar el valor del turno.
        partida_terminada = juego(usuarios,datos_globales)
    else:
        usuarios = {"Jugador_1":0} #Se crea un diccionario generico para el caso de que sea 1 solo jugador.
        partida_terminada = juego(usuarios,datos_globales)
    while partida_terminada == True:
        seguir_jugando = input("Desea jugar otra partida? (S/N): ")

        while seguir_jugando.lower() != 's' and seguir_jugando.lower() != 'n':

            print("No entiendo")
            seguir_jugando = input("Desea jugar otra partida? (S/N): ")
        partida_terminada = volver_a_jugar(partida_terminada,seguir_jugando,usuarios,datos_globales)
    
main()