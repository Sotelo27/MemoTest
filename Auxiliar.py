'''
Escribir una función que reciba un texto y devuelva una lista anidada que representa un
ranking de palabras.
El texto puede tener gran cantidad de palabras.
La función deberá devolver una lista anidada, en la que cada sublista, esté formada por un par
[palabra, cantidad de veces en el texto], ordenada por la cantidad de veces que aparece la
palabra.
Las palabras sólo deben aparecer una vez en la lista.
'''

def contar_palabras(texto):
    lista_anidada = []
    lista_palabras = []
    contador = 0
    for palabras in texto.split():
        if palabras not in lista_palabras:
            lista_palabras.append(palabras)
    for posicion in range(len(lista_palabras)):
        lista_anidada.append([lista_palabras[posicion],texto.count(lista_palabras[posicion])])
    lista_anidada = sorted(lista_anidada,key=lambda x:x[1] ,reverse=True)
    print(lista_anidada)
        
oracion ="Una casa sobre una roca donde cayo una casa"
contar_palabras(oracion)