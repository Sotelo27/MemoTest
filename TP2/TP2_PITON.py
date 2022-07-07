from functools import partialmethod
from logging import root
from random import choice
from utiles import *
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import os.path as path
import csv

configuracion = open("configuracion.csv")
palabras_elegidas = open("palabras.csv", "w")

def datos_configuracion(archivo):
    """
    Agarra los datos del archivo configuracion y los devuelve en una lista.
    """
    #AUTOR: IGNACIO OVIEDO
    devolucion = []
    linea = obtener_linea(archivo)
    while linea[0] != 0:
        longitud,maximo_part,reiniciar_archivo = linea
        devolucion.append(int(longitud))
        devolucion.append(int(maximo_part))
        if str(reiniciar_archivo) == "False":
            reiniciar_archivo = False
        else:
            reiniciar_archivo = True
        devolucion.append(reiniciar_archivo)
        linea = obtener_linea(archivo)
    if devolucion == []:
        devolucion = [7,5,False]
    return devolucion

def interrogacion_ajustados(cantidad):
    """
    Es para que la cantidad de signos de interrogacion de las matrices ahora sea ajustable al largo de la palabra.
    """
    #AUTOR: IGNACIO OVIEDO
    signos=""
    for i in range(cantidad):
        signos+="?"
    return signos

def obtener_linea(archivo):
    """
    Toma una linea del archivo y devuelve una lista de sus valores, si se termino el archivo devuelve 999.
    """
    #AUTOR: IGNACIO OVIEDO
    valores = []
    linea = archivo.readline()
    if linea:
        valores = linea.rstrip("\n").split(",")
    else:
        valores = [0,999]
    return valores

def cargar_datos_configuracion():
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE:---

    POST: devuelve una lista que contiene la nueva configuracion para la partida.
    '''
    longitud = ""
    maximo_partidas = "alfa"
    seguir = ""
    lista = []
    while longitud != "5" and longitud != "6" and longitud != "7":
        longitud = input("Ingrese a continuacion la longitud de las palabras, deberan ser entre 5 o 7: ")
    longitud = int(longitud)# simplemente conversiones del tipo str a int
    while maximo_partidas.isalpha():
        maximo_partidas = input("Ingrese a continuacion el maximo de partidas: ")
    maximo_partidas = int(maximo_partidas)
    while seguir != "1" and seguir != "0":
        seguir = input("Ingrese 1 si al finalizar la partida desea cambiar el archivo de configuracion, 0 caso contrario: ")
    seguir = int(seguir)#esto sirve para luego al aplicar bool, al convertir el tipo cambiara de ser false en caso de ser 0, y un booleano true en caso de ser 1
    lista = [longitud,maximo_partidas,bool(seguir)]
    return lista

def cambiar_configuracion(datos_globales):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE: ---

    POST: pregunta al usuario si desea cambiar la configuracion general del juego, caso que el usuario eliga que si, se cargara la nueva informacion en una lista y luego se reescribira el archivo
    "configuracion.csv" con las opciones elegidas por el usuario.
    '''
    print("A continuacion seleccione s si desea cambiar la configuracion, n caso contrario.")
    respuesta = ""
    while respuesta.lower() != "s" and respuesta.lower() != "n": 
        respuesta = input("Ingrese S/N: ")
    if respuesta.lower() == "s":
        nueva_config = cargar_datos_configuracion()
        datos_globales[4] = nueva_config
        datos_globales[5] = crear_archivo_palabras(nueva_config[0])
        configuracion = open("configuracion.csv","w")
        configuracion.write("{},{},{}".format(nueva_config[0],nueva_config[1],nueva_config[2]))

def sumar_palabra_por_cuento(diccionario,tipo_texto,palabra):
    '''
    AUTOR: LAUTARO MARTIN SOTELO:

    PRE: recibe el diccionario con las palabras como claves, el tipo de texto que viene siendo un str que contiene el titulo del archivo/texto y la palabra que se filtro.

    POST:Cada tipo de cuento tiene asignado una posicion en el diccionario, en este caso, la posicion 1 corresponde a las palabras encontradas en archivo "cuentos", la 
    pos 1 corresponde a las palabras encontradas en "La araña negra" y la posicion 2 corresponde a las encontradas en el archivo "Las 1000 noches y 1 noche".Con ello sabido, se le
    sumara a dicha clave en dicha posicion las veces que se repite dicha palabra.
    '''
    if tipo_texto == "cuentos":
        diccionario[palabra][0] += 1
    elif tipo_texto == "arania_negra":
        diccionario[palabra][1] += 1
    else:
        diccionario[palabra][2] += 1

def tipo_de_texto(archivo):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE: recibe un archivo, que solo seran los tipo de texto.

    POST: devuelve un string , donde analiza si el nombre del archivo se encuentra en el string y concuerda.
    '''
    texto = ""
    if "Cuentos.txt" in str(archivo):
        texto = "cuentos"
    elif "La araña negra - tomo 1.txt" in str(archivo):
        texto = "arania_negra"
    else :
        texto = "1000_y_1_noche"
    return texto

def procesar_texto(archivo,diccionario,longitud): 
    '''

    AUTOR: ANDRES DOSKOTCH/MOD : SOTELO LAUTARO MARTIN

    PRE: recibe el archivo que variara el tipo de texto, un diccionario inicialmente vacio, y la longitud de las palabras con la que se desea filtrar/buscar en el archivo.

    POST: se agrega valores al diccionario con las palabras que cumplan con la longitud, a su vez, se agrega como valor (a la clave de palabra) las veces que se repite en cada archivo de texto.

    '''
    texto = tipo_de_texto(archivo)
    linea = archivo.readline()
    while (linea):
        palabra_filtrada = ""
        lista_palabras = linea.rstrip("\n").split()
        for elemento in lista_palabras:
            contador = 0
            palabra_filtrada = ""
            for caracter in elemento:
                contador += 1
                if caracter.isalpha() :
                    palabra_filtrada += caracter.lower()
                if len(palabra_filtrada)==longitud and contador == len(elemento):
                    if palabra_filtrada not in diccionario:
                        diccionario[palabra_filtrada.lower()] = [0,0,0]
                        sumar_palabra_por_cuento(diccionario,texto,palabra_filtrada)
                    else:
                        sumar_palabra_por_cuento(diccionario,texto,palabra_filtrada) 
        linea = archivo.readline()
    archivo.close()

def crear_archivo_palabras(longitud):
    '''
    AUTOR: PABLO SASHA/MOD : LAUTARO MARTIN SOTELO

    PRE: recibe la longitud que se desea filtrar

    POST:reescribe el archivo de palabras con longitud que se pide, a su vez, retorna una lista que servira para el desarollo de juego y elegir una palabra del mismo.
    '''
    lista = []
    diccionario_claves = {}
    cuentos = open("Cuentos.txt")
    araña = open("La araña negra - tomo 1.txt")
    noches = open("Las 1000 noches y 1 Noche.txt")
    procesar_texto(cuentos,diccionario_claves,longitud)
    procesar_texto(araña,diccionario_claves,longitud)
    procesar_texto(noches,diccionario_claves,longitud)
    for claves in diccionario_claves:
        lista.append(claves)
    lista.sort()
    for palabra in lista:
        linea=palabra
        palabras_elegidas.write("{},{},{},{}\n".format(linea,diccionario_claves[linea][0],diccionario_claves[linea][1],diccionario_claves[linea][2]))
    return lista

def crear_root():
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE:---

    POST: crea el root necesario para la interfaz grafica, creando el tamanio, y dandole un icono como color y titulo, devolviendolo para su uso futuro
    '''
    root = Tk()
    root.title("Fiuble")
    root.resizable(0,0)
    root.geometry("700x400")
    root.iconbitmap("words.ico")
    root.config(bg = "gray")
    return root

def crear_frame(root):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE: recibe el root para poder crear el frame

    POST: devuelve el frame creado para el uso del resto de funciones.
    '''
    frame1 = Frame(root, width = 500, height = 400) 
    frame1.config(bg = "#09B1C3")
    frame1.pack()
    return frame1

def mensaje_inicial(root,frame1):
    #Mensaje de bienvenida al juego
    texto_juego = Label(frame1, text = "Bienvenido a Fiuble!!")
    texto_juego.config(bg = "#2D508F", font = ("Comic Sans", 30))
    texto_juego.place(x = 70, y = 70)
    boton_empezar = Button(frame1, text = "Empezar", command = lambda:empezar(root,frame1), bg = "gray")
    boton_empezar.place(x = 150, y = 200, width = 100, height = 60)

    boton_salir = Button(frame1, text = "Salir", command = root.destroy, bg = "gray")
    boton_salir.place(x = 270, y = 200, width = 100, height = 60)

def empezar(root,frame1):
#Cambia de ventana para comenzar la partida
#Autor: Renato Villalba
    ingresar_usuarios(root,frame1)
    frame1.destroy() 

def ingresar_usuarios(root,frame1):
#Funcion que se encarga de ingresar los usuarios, en el caso de no existir en el registro permite registrarse
#Autor: Renato Villalba

    global frame2
    global nombre
    global clave

    nombre = StringVar()
    clave = StringVar()

    frame2 = Frame(width = 500, height = 400)
    frame2.config(bg = "#2D508F")
    frame2.pack()
    
    usuario = Label(frame2, text = "Nombre:", bg = "green", fg = "white", justify = "right", font = 25)
    usuario.place(x = 110, y = 130, width = 80, height = 30)
    texto_usuario = Entry(frame2, bg = "#2D508F", fg = "white", justify = "left", font = 18, textvariable = nombre)
    texto_usuario.place(x = 200, y = 130, width = 180, height = 30)

    clave_1 = Label(frame2, text = "Clave:", bg = "green", fg = "white", justify = "left", font = 25)
    clave_1.place(x = 110, y = 190, width = 80, height = 30)
    texto_clave = Entry(frame2, bg = "#2D508F", fg = "white", justify = "left", font = 18, textvariable = clave)
    texto_clave.place(x = 200, y = 190, width = 180, height = 30)
    texto_clave.config(show = "*")

    boton_registrar = Button(frame2, text = "Registrarse", command = registro_nuevo, bg = "gray")
    boton_registrar.place(x = 140, y = 280, width = 70, height = 30)

    boton_acceder = Button(frame2, text = "Acceder", command = lambda:acceder(root), bg = "gray")
    boton_acceder.place(x = 220, y = 280, width = 70, height = 30)

    boton_salir = Button(frame2, text = "Salir", command = root.destroy, bg = "gray")
    boton_salir.place(x = 300, y = 280, width = 70, height = 30)

def registro_nuevo():
#Funcion encargada de mostrar la ventana para registrar los usuarios nuevos 
#Autor: Renato Villalba
    global frame_registro

    frame_registro = Tk()
    frame_registro.title("Registro de Usuarios")
    frame_registro.resizable(0, 0)
    frame_registro.geometry("300x300")
    frame_registro.iconbitmap("user.ico")
    frame_registro.config(bg = "#FF8966")
    
    global nombre
    global clave
    
    global nuevo_nombre 
    global nueva_clave 
    
    global reingreso_clave
    global confirmar_clave 

    nombre = StringVar()
    clave = StringVar()
    reingreso_clave = StringVar()

    frame3 = Frame(frame_registro, width = 400, height = 400)
    frame3.config(bg = "#FF8966")
    frame3.pack()

    label_nombre = Label(frame3, text = "Nombre de Usuario", bg = "LightGreen")
    label_nombre.place(x = 30, y = 20)

    nuevo_nombre = Entry(frame3, fg = "black", textvariable = nombre)
    nuevo_nombre.place(x = 30, y = 50)

    label_clave = Label(frame3, text = "Clave", bg = "LightGreen")
    label_clave.place(x = 30, y = 80)

    nueva_clave = Entry(frame3, fg = "black", textvariable = clave)
    nueva_clave.place(x = 30, y = 110)
    nueva_clave.config(show = "*")

    reingresar_clave = Label(frame3, text = "Reingresar clave", bg = "LightGreen")
    reingresar_clave.place(x = 30, y = 140)

    confirmar_clave = Entry(frame3, fg = "black", textvariable = reingreso_clave)
    confirmar_clave.place(x = 30, y = 170)
    confirmar_clave.config(show = "*")
    
    boton_registrar = Button(frame3, text = "Registrar",  command = registro_usuario, bg = "LightGreen")
    boton_registrar.place(x = 30, y = 240, width = 100, height = 30)

    boton_cancelar = Button(frame3, text = "Cancelar", command  = frame_registro.destroy, bg = "LightGreen")
    boton_cancelar.place(x = 150, y = 240, width = 100, height = 30)

def registro_usuario():
#Función encargada de crear un archivo nuevo por usuario guardando la información de usuario y claves.
#Autor: Renato Villalba
    global frame_registro
    global nombre 
    global clave
    global confirmar_clave
    
    dic_usuario = {}

    informacion_usuario = nuevo_nombre.get()
    informacion_clave = nueva_clave.get()
    reconfirmar_clave = confirmar_clave.get()

    with open("usuarios.csv", "r+", newline = "") as archivo_csv:

        writer = csv.writer(archivo_csv, delimiter = ",")

        nombre_valido = False
        letras_nombre = False
        numeros_nombre = False
        guion_nombre = 0

        clave_valida = False
        mayus = False
        minus = False
        clave_numero = False
        caracteres_clave = False

        if 4 <= len(informacion_usuario) <= 15:
            nombre_valido = True

            if informacion_usuario.isalpha():
                letras_nombre = True
            
            if informacion_usuario.isnumeric():
                numeros_nombre = True

            if "_" in informacion_usuario:
                guion_nombre += 1
        
        if (letras_nombre) and (numeros_nombre) and (guion_nombre > 0):
            nombre_valido = True

        if 8 <= len(informacion_clave) <= 12:
            clave_valida = True
            
            if informacion_clave.isupper():
                mayus = True
            
            if informacion_clave.islower():
                minus = True

            if informacion_clave.isnumeric():
                clave_numero = True

            if "_" or "-" in informacion_clave:
                caracteres_clave = True 

        if reconfirmar_clave != informacion_clave:
              
            Label(frame_registro, bg = "#FF8966", fg = "black", text = "La clave no coincide").place(x = 170, y = 170)
            clave_valida = False

        if (mayus) and (minus) and (clave_numero) and (caracteres_clave):
            clave_valida = True
        
        
        if nombre_valido and clave_valida:          

            for i in dic_usuario.keys():

                if nombre == i:

                    print("Usuario existente")   
            
                if informacion_usuario not in archivo_csv:
                    writer.writerow([informacion_usuario, informacion_clave])
                    dic_usuario[informacion_usuario] = informacion_clave
                    print(dic_usuario)     
                
            Label(frame_registro, bg = "#FF8966", fg = "black", text = "Creacion correcta").place(x = 30, y = 210)
            nuevo_nombre.delete(0, END)
            nueva_clave.delete(0, END)
            confirmar_clave.delete(0, END)

        else:
            
            Label(frame_registro, bg = "#FF8966", fg = "black", text = "Creacion invalida").place(x = 180, y = 50)
            nuevo_nombre.delete(0, END)
            nueva_clave.delete(0, END)
            confirmar_clave.delete(0, END)

def message_info():
#Si los datos son ingresados correctamente permite el acceso
        messagebox.showinfo("Confirmado", "Acceso exitoso") 

def error_info():
#Si los datos no coinciden muestra un mensaje deerror
        messagebox.showwarning("Error", "Datos incorrectos")

def acceder(root):
    '''
    
    Función que verifica si los usuarios existen para dar acceso al juego
    AUTOR: SOTELO LAUTARO MARTIN

    '''
    
    global nombre
    global clave
    strnombre = nombre.get()
    intclave = clave.get()
    usuarios= open('usuarios.csv')
    linea = obtener_linea(usuarios)
    usuario , clave_archivo = linea
    validacion = False
    while usuario and validacion == False:
        if (strnombre == usuario) and (intclave == clave_archivo):
            message_info()
            root.destroy() 
            validacion = True
        linea = obtener_linea(usuarios)
        usuario,clave_archivo = linea
    if validacion == False:
        error_info()

def interfaz():
    #Funcion principal de la interfaz
    #Autor: Renato Villalba
    root = crear_root()
    frame = crear_frame(root)
    mensaje_inicial(root,frame)
    root.mainloop()

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
        puntuaciones_jugador[usuario_2][1] -= puntos
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario][1],usuario_2,puntos,puntuaciones_jugador[usuario_2][1]))
    elif datos_partida[1] > 1 and datos_partida[4] == True:
        puntuaciones_jugador[usuario_2][1] -= puntos
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,puntos,puntuaciones_jugador[usuario][1],usuario_2,puntos,puntuaciones_jugador[usuario_2][1]))
    elif datos_partida[1] > 1 and datos_partida[4] == False:
        puntuaciones_jugador[usuario_2][1] -= 100 
        puntuaciones_jugador[usuario][1] += 50
        print ("El usuario {} obtuvo un total de {} puntos,acumulando {} y el usuario {} perdio un total de {} puntos acumulando {}".format(usuario,-50,puntuaciones_jugador[usuario][1],usuario_2,-100,puntuaciones_jugador[usuario_2][1]))
       
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
        print ("Obtuviste un total de", puntos ,"puntos, tenes acumulado:",puntuaciones_jugador[usuario][1])
    elif datos_partida[1] >1 and datos_partida[4] == False:
        print ("Perdiste un total de", puntos ,"puntos, tenes acumulado:",puntuaciones_jugador[usuario][1])

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
        puntuaciones_jugador[usuario][1] += puntos
        puntuaciones_jugador[usuario][0] += 1
        mostrar_puntos_2_jugadores(datos_partida,puntuaciones_jugador,usuario,puntos)
    else:
        #Hacer llamado a funcion de elegir numero del jugador para registrar la acumulacion de puntos del jugador especifico.
        usuario = list(puntuaciones_jugador.keys())[datos_partida[2]] # convirtiendolo en lista, la pos 0 sera el jugador 1, y la pos 1 sera el jugador 2.
        puntuaciones_jugador[usuario][1] += puntos
        puntuaciones_jugador[usuario][0] += 1
        mostrar_puntos_1_jugador(datos_partida,puntuaciones_jugador,usuario,puntos)

def asignar_color_amarillo(conjunto_palabras,dic_letras,palabra_color_lista,posicion):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE: recibe lista conjunto palabras(contiene arriesgo del jugador y palabra a revelar), el dic letras vacio o no, la palabra color lista y 
    por ultimo la posicion.

    POST: agregara en caso de haber una palabra sin agregar al dicletras, y modifica los colores por defecto o no en color amarillo, informando que falta 1 letra de ese tipo
    por adivinar.
    '''
    arriesgo = conjunto_palabras[0]
    palabra = conjunto_palabras[1]
    letra = arriesgo[posicion]
    palabra_color = ''
    if (letra in palabra) and arriesgo[posicion] != palabra[posicion] and dic_letras[letra] < palabra.count(letra):
        asignar_letras(dic_letras,letra)
        palabra_color += obtener_color("Amarillo") + arriesgo[posicion] + obtener_color("Defecto")
        palabra_color_lista[posicion] = palabra_color

def asignar_color_verde(conjunto_palabras,dic_letras,palabra_color_lista,posicion):
    '''
    AUTOR: LAUTARO MARTIN SOTELO 

    PRE: recibe lista conjunto palabras(contiene arriesgo del jugador y palabra a revelar), el dic letras vacio(se rellenara con las palabras acertadas), la palabra color lista y 
    por ultimo la posicion.

    POST: no tiene retorno, modifica dic letras con los aciertos en verde, modifica la lista de palabras con color agregandolas .

    '''
    arriesgo = conjunto_palabras[0]
    palabra = conjunto_palabras[1]
    palabra_color = ''
    letra = arriesgo[posicion]
    if arriesgo[posicion] == palabra[posicion]:
        asignar_letras(dic_letras,letra)
        palabra_color += obtener_color("Verde") + arriesgo[posicion] + obtener_color("Defecto")
        palabra_color_lista.append(palabra_color)
    else:
        asignar_letras(dic_letras,letra)
        palabra_color += obtener_color("Defecto") + arriesgo[posicion]
        palabra_color_lista.append(palabra_color)

def asignar_letras(dic_letras,letra):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE:recibe el diccionario vacio y un string letra que proviene el arriesgo introducido por el jugador

    POST: devuelve el diccinario con clave letra y valor la cantidad que se encuentra
    '''
    if letra not in dic_letras:
        dic_letras[letra] = 1
    else:
        dic_letras[letra] += 1

def poner_color(arriesgo,conjunto_palabras):
    '''
    AUTOR: Lautaro Martin Sotelo

    PRE:Recibe la palabra que arriesgue el usuario, comprueba que sean iguales con la original.

    POST:Retorna una palabra que contiene los colores de acuerdo a si su posicion es correcta.
    '''
    
    palabra_color= []
    palabra_color_str = ''
    palabra = conjunto_palabras[0]
    dic_letras = {}
    agrupar_palabras = [arriesgo,palabra] #simplemente sirve para guardarlos en una lista y luego desempaquetarlos y evitar uso excesivo de parametros
    for posicion in range(0,len(arriesgo)):
        asignar_color_verde(agrupar_palabras,dic_letras,palabra_color,posicion)
    #recorro dos veces, para primero asegurar las palabras en color verde, y luego en amarillo, asi evitar letras de color amarillas de mas.
    for posicion in range(0,len(arriesgo)):
        asignar_color_amarillo(agrupar_palabras,dic_letras,palabra_color,posicion)
    #ahora lo que hago es obtener el contenido de la lista palabra color y sumarle a un str vacio, asi adecuandose al tipo de dato de la matriz.
    for elementos in palabra_color:
        palabra_color_str += elementos
    return palabra_color_str

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

def registrar_usuarios ():  
    '''
    AUTOR: ANDRES DOSKOCH 

    Funcion que crea un diccionario de 2 usuarios ,validando primero su ingreso.

    PRE: ----

    POST: devuelve un diccionario con clave los nombre de usuario y puntos como valor.
    '''
    interfaz()
    usuario_1 = nombre.get()
    interfaz()
    usuario_2 = nombre.get()
    diccionario = {usuario_1:[0,0],usuario_2:[0,0]}
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

def Validacion(arriesgo,longitud):
    '''
    AUTOR: ALAN NESTOR CRISTOBO
    Esta Funcion tiene como objetivo evaluar si la palabra ingresada por el usuario es o no valida
    
    PRE: recibe como parametro un string introducido por el usuario.

    POST: devuelve un booleano que informa TRUE en caso de que su longitud sea de 5, FALSE si es menor o mayor o no cumple las condiciones.
    '''
    valido = True
    if len(arriesgo) != longitud:   # Evaluo la cantidad de caracteres  
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

def introducir_arriesgo(longitud_config):
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
        valido = Validacion(arriesgo.upper(),longitud_config)
    arriesgo = reemplazar_caracteres_acentuados(arriesgo)
    return arriesgo

def generar_matriz(longitud)->list:
    '''
    AUTOR: LAUTARO MARTIN SOTELO
    Este tablero "vacio" inicialmente, sera el que visualizen los jugadores durante la partida,
    rellenandose con los ingresos del usuario.

    PRE: ---

    POST: devuelve una matriz.
    '''
    matriz_vacia = []
    for filas in range(longitud):
        matriz_vacia.append([interrogacion_ajustados(longitud)]) # a la matriz vacia , introduzco sublistas que contienen string con "?" para luego rellenarse.
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
    longitud_config = datos_globales[4][0]
    palabras_validas = datos_globales[5]
    palabra_adivinar = choice(palabras_validas)
    palabras = [palabra_adivinar.upper(),interrogacion_ajustados(longitud_config)] #Se crea una lista que contiene la palabra que se busca, y una palabra que se ira rellenando deacuerdo si la posicion se cumple
    print(palabras)
    matriz = generar_matriz(longitud_config)
    intentos = 1
    partida_terminada = False
    datos_partida = ['',intentos,datos_globales[1],datos_globales[0],partida_terminada] #Empaqueto los datos necesarios para llevar a cabo el juego y no usar el uso de parametros de mas.
    print(palabras[0])
    while partida_terminada == False:
        print("Es el turno de {}".format(list(usuarios.keys())[datos_partida[2]])) #Similar que en la funcion puntos, al convertirlo en lista, solo accediendo a la posicion accedo a la clave/nombre del usuario.
        empiezaTiempo = time.time()
        print("Palabra a adivinar: ",palabras[1])
        mostrar_matriz(matriz)
        arriesgo = introducir_arriesgo(longitud_config)
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
    return datos_partida

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
    print("El ganador es {} con un total de {} puntos.".format(ganador[0][0],ganador[0][1][1]))

def obtener_tiempo_partida():
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE:---

    POST: Devuelve una lista con 2 listas, que contiene el final de la partida, dia y horario.
    '''
    tiempo = datetime.now()
    hora = tiempo.hour
    minutos = tiempo.minute
    dia = tiempo.day
    mes = tiempo.month
    anio = tiempo.year
    fecha_partida = [anio,mes,dia]
    hora_finalizacion = [hora,minutos]
    tiempo_partida = [fecha_partida,hora_finalizacion]
    return tiempo_partida

def ordenar_por_aciertos(archivo):
    '''

    AUTOR:LAUTARO MARTIN SOTELO

    PRE: recibe el archivo que contiene la informacion de los jugadores en partidas jugadas.

    POST: sobreescribe el archivo que contiene dicha informacion, ordenandolo de forma decendente de acuerdo a los aciertos.

    '''
    linea = obtener_linea(archivo)
    dic = {}
    while linea[0] != 0:
        fecha,hora,nombre,aciertos,intentos = linea
        dic[nombre] = [fecha,hora,aciertos,intentos]
        linea = obtener_linea(archivo)
    diccionario_ordenado = sorted(dic.items(),key= lambda x:x[1][2], reverse= True)
    with open('partidas.csv','w') as reescritura:
        for nombres in diccionario_ordenado:
            jugador = nombres[0]
            horario = nombres[1][1]
            adivinados = nombres[1][2]
            intento = nombres[1][3]
            fecha_jug = nombres[1][0]
            reescritura.write('{},{},{},{},{}\n'.format(fecha_jug,horario,jugador,adivinados,intento))

def agregar_archivo_de_partida(datos_partida,tiempo_partida,datos_globales):
    '''
    AUTOR: LAUTARO MARTIN SOTELO

    PRE: recibe los datos de partida, con los datos globales y el tiempo jugado .

    POST: crea un archivo o en otro caso agrega datos a un archivo de acuerdo a lo que jugo el jugador.
    '''
    usuarios = datos_globales[3]
    fecha_partida = tiempo_partida[0]
    hora_finalizacion = tiempo_partida[1]
    archivo = open('partidas.csv','r+')
    linea = obtener_linea(archivo)
    with open('partidas.csv','r+'):
        for nombre in usuarios:
            if linea[0] != 0:
                if linea != ['']:
                    comprobar_usuario_en_archivo(usuarios,nombre,datos_partida)
                intentos_partida = datos_partida[1]
                aciertos_partida = usuarios[nombre][0]
                archivo.write('{}/{}/{},{}:{},{},{},{}\n'.format(fecha_partida[0],fecha_partida[1],fecha_partida[2],hora_finalizacion[0],hora_finalizacion[1],nombre,aciertos_partida,intentos_partida))
            else:
                intentos_partida = datos_partida[1]
                aciertos_partida = usuarios[nombre][0]
                archivo.write('{}/{}/{},{}:{},{},{},{}\n'.format(fecha_partida[0],fecha_partida[1],fecha_partida[2],hora_finalizacion[0],hora_finalizacion[1],nombre,aciertos_partida,intentos_partida))
    archivo.close()
    archivo = open('partidas.csv')
    ordenar_por_aciertos(archivo)
    archivo.close()
    
def comprobar_usuario_en_archivo(jugadores,nom_partida,datos_partida):
    '''
    Función que verifica si los usuarios existen para actualizar sus datos de aciertos e intentos.
    AUTOR: SOTELO LAUTARO MARTIN
    '''
    estadisticas = open('partidas.csv')
    linea = obtener_linea(estadisticas)
    existe = False
    usuario = nom_partida
    fecha,hora,nombre,aciertos,intentos = linea
    while linea[0] != 0 and existe == False :
        fecha,hora,nombre,aciertos,intentos = linea
        if (usuario == str(nombre)):
            datos_partida[1] += int(intentos)
            jugadores[nom_partida][0] += int(aciertos)
            existe = True
        linea = obtener_linea(estadisticas)           

def volver_a_jugar(datos_partida,seguir_jugando,usuarios,datos_globales):
    '''
    AUTOR: RENATO VILLALBA /MOD : LAUTARO MARTIN SOTELO

    Funcion que tiene como objetivo determinar o no el inicio de otro juego.

    PRE: recibe un booleno que indica la finalizacion de la partida, un string que indica si el usuario desea continuar el juego, un diccionario con nombre y puntos de usuarios , y 
    una lista con el turno y el modo de juego.

    POST: devuelve un boleano que variara , siendo FALSE para terminar la partida y TRUE en caso de seguir.
    '''
    modo = datos_globales[0]
    partidas = datos_globales[2]
    max_partidas = datos_globales[4][1]
    if partidas < max_partidas:
        if seguir_jugando.lower() == 's':
            if modo == 2:
                datos_globales[1] = cambiar_jugador(datos_globales[1])
                datos_partida = juego(usuarios,datos_globales)
            else:
                datos_partida = juego(usuarios,datos_globales)
        elif seguir_jugando.lower() == 'n':
            cambiar_configuracion(datos_globales)
            tiempo_partida = obtener_tiempo_partida()
            if modo == 2:
                ganador_2_jugadores(usuarios)
                agregar_archivo_de_partida(datos_partida,tiempo_partida,datos_globales)
                datos_partida[4] = False
                print("Hasta luego!Fiuble cerrando.")
            else:
                tiempo_partida = obtener_tiempo_partida()
                agregar_archivo_de_partida(datos_partida,tiempo_partida,datos_globales)
                datos_partida[4] = False
                print("Hasta luego!Fiuble cerrando.")
    elif partidas == max_partidas and seguir_jugando.lower() == "s":
        print("\n----Han jugado el limite de partidas permitidas por la configuracion----\n")
        cambiar_configuracion(datos_globales)
        tiempo_partida = obtener_tiempo_partida()
        agregar_archivo_de_partida(datos_partida,tiempo_partida,datos_globales)
        if modo == 2:
            datos_globales[1] = cambiar_jugador(datos_globales[1])
            datos_partida = juego(usuarios,datos_globales)
        else:
            datos_partida = juego(usuarios,datos_globales)
    else:
        cambiar_configuracion(datos_globales)
        tiempo_partida = obtener_tiempo_partida()
        agregar_archivo_de_partida(datos_partida,tiempo_partida,datos_globales)
        datos_partida[4] = False
        print("Hasta luego!Fiuble cerrando.")
    return datos_partida

def main():
    '''
    FUNCION MAIN ()

    AUTORES: RENATO VILLALBA / MOD: SOTELO LAUTARO MARTIN

    Su funcionalidad es iniciar el juego de palabras, como tambien determinar si el usuario quiere seguir el juego.
    '''
    print("---Bienvenido a FIUBLE---\n")
    print("El objetivo del juego es adivinar una palabra en menos de 5 intentos\n")
    print("La configuracion de la partida es la siguiente: ")
    configuracion_partida = datos_configuracion(configuracion)
    print(f"Longitud de la palabra: {configuracion_partida[0]}\nMaximo de partidas: {configuracion_partida[1]}\nReinicio de archivo: {configuracion_partida[2]}\n")
    print("Al finalizar el juego , podra cambiar si desea la configuracion.")
    print("A continuacion , eliga si quiere jugar solo 1 jugador o 2.\n")
    partidas = 0
    palabras_validas = crear_archivo_palabras(configuracion_partida[0])
    datos_globales = [eleccion_jugadores(),0,partidas,"",configuracion_partida,palabras_validas] #se empaquetan los datos globales para evitar el uso de parametros innecesarios,los turnos seran la posicion 1 guardados en tipo lista y el modo de juego la posicion 0 .
    if datos_globales[0] == 2:
        usuarios = registrar_usuarios() #Se registra a los usuarios que desarrollaran el juego.
        datos_globales[3] = usuarios
        elegir_quien_comienza(datos_globales)#Se toma al azar el valor del turno.
        datos_partida = juego(usuarios,datos_globales)
    else:
        interfaz()
        usuarios = {nombre.get():[0,0]} #Se crea un diccionario generico para el caso de que sea 1 solo jugador.
        datos_globales[3] = usuarios
        datos_partida = juego(usuarios,datos_globales)
    while datos_partida[4] == True:
        datos_globales[2] += 1
        seguir_jugando = input("Desea jugar otra partida? (S/N): ")

        while seguir_jugando.lower() != 's' and seguir_jugando.lower() != 'n':

            print("No entiendo")
            seguir_jugando = input("Desea jugar otra partida? (S/N): ")
        datos_partida = volver_a_jugar(datos_partida,seguir_jugando,usuarios,datos_globales)
    
main()