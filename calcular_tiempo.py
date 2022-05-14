'''
Programa para calcular tiempo
'''
import time

def tiempo_jugado():
    '''
    Funcion que va a mostrar el tiempo que tarde el usuario en adivinar la palabra, solo va a mostrar 
    por pantalla si adivina la palabra.
    '''
    inicio_de_partida = time.time()

    #Vincular con los intentos
    #...

    final_de_partida = time.time()

    tiempo_segundos = round(final_de_partida - inicio_de_partida) # Tiempo de juego en segundos
    tiempo_minutos = round(tiempo_segundos // 60) #tiempo de juego en minutos

    tiempo_total = print(f"Te tardaste {tiempo_minutos} minutos y {tiempo_segundos} segundos en adivinar la palabra") 
    
    if arriesgo == palabras[0]:

            tiempo_total
            #print(f"Te tardaste {tiempo_de_juego_minutos} minutos y {tiempo_de_juego_segundos} segundos en adivinar la palabra")

    return tiempo_total 

tiempo_jugado()

