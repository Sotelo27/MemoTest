'''
Programa que pregunta al usuario si desea seguir jugando
'''
def volver_a_jugar():
    '''
    La funcion puede recibir dos respuestas, si es afirmativo 
    se va a seguir jugando caso contrario el juego termina
    '''
    partida_terminada = palabra_arriesgo()
    
    while ganaste == True:

        seguir_jugando = input("Desea jugar otra partida? (S/N)\n")

        if seguir_jugando == 'S':

            palabra_arriesgo()

        elif seguir_jugando == 'N':

            print("OK, chau.")

        else:

            print("No entiendo")
            seguir_jugando = input("Desea jugar otra partida? (S/N)\n")

volver_a_jugar()
