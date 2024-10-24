
from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import time
import pygame


def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()

    archivo = open(usuario_info, "w") 
    archivo.write(usuario_info + "\n")   
    archivo.write(contra_info)
    archivo.close()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    Label(pantalla1, text = "Registro Convencional Exitoso", fg = "green", font = ("Calibri",11)).pack()
    

    
def registro_facial():

    cap = cv2.VideoCapture(0)               
    while(True):
        ret,frame = cap.read()           
        cv2.imshow('Registro Facial',frame)         
        if cv2.waitKey(1) == 27:         
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",frame)     
    cap.release()                              
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)   
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",11)).pack()

    
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)   
    
def registro():
    global usuario
    global contra 
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) 
    pantalla1.title("Registro")
    pantalla1.geometry("300x250")  
    
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text = "Registro facial: debe de asignar un usuario:").pack()
    #Label(pantalla1, text = "").pack()  
    Label(pantalla1, text = "Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text = "").pack()
    Label(pantalla1, text = "Usuario * ").pack() 
    usuario_entrada = Entry(pantalla1, textvariable = usuario)
    usuario_entrada.pack()
    Label(pantalla1, text = "Contraseña * ").pack() 
    contra_entrada = Entry(pantalla1, textvariable = contra)
    contra_entrada.pack()
    Label(pantalla1, text = "").pack() 
    Button(pantalla1, text = "Registro Tradicional", width = 15, height = 1, command = registrar_usuario).pack()  

    Label(pantalla1, text = "").pack()
    Button(pantalla1, text = "Registro Facial", width = 15, height = 1, command = registro_facial).pack()

    
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()   
    if log_usuario in lista_archivos:  
        archivo2 = open(log_usuario, "r")  
        verificacion = archivo2.read().splitlines() 
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
            reproducir_video(ruta_video)
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text = "Contraseña Incorrecta", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
    
def login_facial():
    cap = cv2.VideoCapture(0)             
    while(True):
        ret,frame = cap.read()             
        cv2.imshow('Login Facial',frame)        
        if cv2.waitKey(1) == 27:          
            break
    usuario_login = verificacion_usuario.get()  
    cv2.imwrite(usuario_login+"LOG.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)   #Limpiamos los text variables
    contra_entrada2.delete(0, END)

    #----------------- Funcion para guardar el rostro --------------------------
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    #-------------------------- Detectamos el rostro-------------------------------------------------------
    
    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    #-------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
        kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
    #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
    
    im_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if usuario_login+".jpg" in im_archivos:   #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread(usuario_login+".jpg",0)     #Importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)  #Importamos el rostro del inicio de sesion
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del registro: ",similitud)
            reproducir_video(ruta_video)
        else:
            print("Rostro incorrecto, Cerifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
            
def reproducir_video(ruta_video):
  
    cap = cv2.VideoCapture(ruta_video)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Video', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):  # Presiona 'q' para salir
            break



    cap.release()
    cv2.destroyAllWindows()
    

# Especifica la ruta de tu video aquí
ruta_video = 'C:\\Users\\LAPTOP-24\\Desktop\\reco\\jaja.mp4'  # Cambia 'jaja.mp4' por el nombre real del archivo
#------------------------Funcion que asignaremos al boton login -------------------------------------------------
        
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x250")   #Creamos la ventana
    Label(pantalla2, text = "Login facial: debe de asignar un usuario:").pack()
    Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla2, text = "").pack()  #Dejamos un poco de espacio
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    
    #---------------------------------- Ingresamos los datos --------------------------
    Label(pantalla2, text = "Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text = "Contraseña * ").pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
    contra_entrada2.pack()
    Label(pantalla2, text = "").pack()
    Button(pantalla2, text = "Inicio de Sesion Tradicional", width = 20, height = 1, command = verificacion_login).pack()

    #------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text = "").pack()
    Button(pantalla2, text = "Inicio de Sesion Facial", width = 20, height = 1, command = login_facial).pack()
        
#------------------------- Funcion de nuestra pantalla principal ------------------------------------------------
    
def pantalla_principal():
    global pantalla          #Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("300x250")  #Asignamos el tamaño de la ventana 
    pantalla.title("ROLON TE AMO CON TODO MI SER")       #Asignamos el titulo de la pantalla
    Label(text = "Login Inteligente", bg = "gray", width = "300", height = "2", font = ("Verdana", 13)).pack() #Asignamos caracteristicas de la ventana
    
#------------------------- Vamos a Crear los Botones ------------------------------------------------------
    
    Label(text = "").pack()  #Creamos el espacio entre el titulo y el primer boton
    Button(text = "Iniciar Sesion", height = "2", width = "30", command = login).pack()
    Label(text = "").pack() #Creamos el espacio entre el primer boton y el segundo boton
    Button(text = "Registro", height = "2", width = "30", command = registro).pack()

    pantalla.mainloop()

pantalla_principal()
