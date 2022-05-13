from utiles import *
palabras = ["holap","?????"]
arriesgo = "manco"
def poner_color(arriesgo,conjunto_palabras):
    '''

    Recibe la palabra que arriesgue el usuario, comprueba que sean iguales con la original.
    Retorna una palabra que contiene los colores de acuerdo a si su posicion es correcta.
    '''
    #ANDRES
    palabra_color = ""
    palabra = conjunto_palabras[0]
    auxiliar = ""
    for i in range (0, len(arriesgo)):
    
        if i in range (0, len (palabra)):

            if arriesgo[i] == palabra[i]:
                palabra_color += obtener_color("Verde") + arriesgo[i]
                auxiliar += arriesgo[i]
            elif (arriesgo[i] in palabra) and arriesgo[i] != palabra[i]:
                palabra_color += obtener_color("Amarillo") + arriesgo[i]
                auxiliar += "?"
            else:
                palabra_color += obtener_color("Defecto") + arriesgo[i]
                auxiliar += "?"
    modificar_oculta(auxiliar,conjunto_palabras)
    return palabra_color

def modificar_oculta(palabra_sin_revelar,conjunto_palabras):
    auxiliar = conjunto_palabras[0]
    palabra_oculta = ""
    for i in range(len(auxiliar)):
        if palabra_sin_revelar[i] == auxiliar[i]:
            palabra_oculta += palabra_sin_revelar[i]
            print("hola")
        else:
            palabra_oculta += "?"
    conjunto_palabras[1] = palabra_oculta
    print(conjunto_palabras[1])

modificar_oculta("alfas",palabras)
        

