

from tkinter.constants import S
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import numpy as np
import pandas as pd
import math
import csv
from math import log10,floor
from tkinter import Label, StringVar, filedialog as fd
from io import open
import tkinter as tk 
import os
from matplotlib.figure import Figure  #Libreria para dibujar la gráfica
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  #Libreria para dibujar la gráfica


#Clase la cual meneja el proceso de linealización y mínimos cuadrados

class Minimos:
    def __init__(self,n,archivos,nombre_ejex,nombre_ejey,titulo):  
    
        self.titulo = titulo
        
        #--------------------------Declaración de variables usadas para almacenamiento de datos--------------------------------

        
        self.n = n  #Almacena el número de elementos que tiene el archivos txt (número de datos)
        self.delta=[]
        
           
        #------------------------------Declaración de variables que dan nombre a los ejes---------------------------------------

        self.archivos = archivos
        self.n_a = len(self.archivos) #Almacena el número de elementos que hay en la tupla archivos
        
        self.datos_x = np.zeros((self.n_a,self.n)) #Crea matrices con ceros de tamaño #archivos x #datos
        self.datos_y = np.zeros((self.n_a,self.n)) 
        
        
        self.nombre_ejex=nombre_ejex
        self.nombre_ejey=nombre_ejey
        

        self.ancho = 4
        #--------------------------------Declaración de variables usadas para MC----------------------------------------------
        
        self.x=[] #Almacenará los datos que se toman como valores de x para aplicar mínimos cuadrados
        self.xsinlog=[] #En caso de que se aplique el método de logaritmos entonces esta tupla almacenara los datos sin logaritmo
        #mientras que los self.x tendrán logaritmo
        self.y=[] #lo mismo pero para y
        self.ysinlog=[]
        
        self.m=0  #Almacenara la pendiente de la linealización
        self.b=0  #Almacenará la intersección de la linealización
        self.sm=0 #Almacenará el error en la pendiente
        self.sb=0 #Almacenraá el error en la intersección
        self.cc=0 #Almacenará el coeficiente de correlación de la linealización}}
        
    def seleccion_archivos(self): #Método para almacenar las rutas de los archivos que contienen los datos a linealizar
                
        
        self.archivos = fd.askopenfilenames(
        initialdir=".",     #Abre la ventana en el directorio más cercano
        filetypes=(('Ficheros de texto','*.txt'),), #Le dice la extensión de los archivos que leerá
        title="Elección de archivos de datos a linealizar") #Coloca un nombre a la ventana
        
        self.n_a = len(self.archivos) #Almacena el número de elementos que hay en la tupla archivos
        
        self.datos_x = np.zeros((self.n_a,self.n)) #Crea matrices con ceros de tamaño #archivos x #datos
        self.datos_y = np.zeros((self.n_a,self.n)) 
        
        print(self.archivos)

    def Obtener_datos(self):
        for k,archivo in enumerate(self.archivos):  #k indica el numero del elemento del archivo y archivo almacena el nombre 
                                                    #almacena la cadena de texto del nombre del archivo
            data_txt = np.loadtxt(archivo)   #convierte el archivo de txt a csv para así poder usarlo
            data_txtDF = pd.DataFrame(data_txt)
            data_txtDF.to_csv(archivo+".csv",index=False)

            
            with open(archivo+".csv",newline="\n") as csvfile:
                reader = csv.reader(csvfile,delimiter=',') #Lee los datos del archivo csv

                l=0   #contador para el numero del elemento en qué está i o j
                h=0   #contador para evitar que se almacene el 0 y 1
                for i,j in reader:
                    if h != 0:  #para indicar que la primera iteración de i y j no debe ser almacenada
                        self.datos_x[k,l] = float(i)
                        self.datos_y[k,l] = float(j)
                        l+=1
                    h+=1
                    
    
    def Sacar_Logaritmos(self):
        for i in range(self.n):
            self.xsinlog.append(self.x[i])
            self.ysinlog.append(self.y[i])
            if self.x[i]!=0:
                self.x[i]=math.log(self.x[i])
            self.y[i]=math.log(self.y[i])

    def Minimos_cuadrados(self):
        y=0
        x=0
        x_2=0
        y_2=0
        xy=0
        for i in range(self.n):
            y = self.y[i]+y
            x = self.x[i]+x
            xy += self.x[i]*self.y[i]  #Obtiene cada uno de los términos que se necesitan para sacar mínimos cuadrados
            x_2+= self.x[i]**2
            y_2+= self.y[i]**2

        self.m = (self.n*xy-x*y)/(self.n*x_2-x**2)  #Obtiene la pendiente
        self.b = (y*x_2-x*xy)/(self.n*x_2-x**2) #Obtiene la intersección

        sy=0
        for i in range(self.n):
            sy+=((self.y[i]-(self.m*self.x[i]+self.b))**2)/(self.n-2) 
        sy = math.sqrt(sy)

        self.sm=sy*math.sqrt(self.n/(self.n*x_2-x**2)) #Obtiene el error de la pendiente
        self.sb=sy*math.sqrt(x_2/(self.n*x_2-x**2)) #Obtiene el error de la intersección
        self.cc = (self.n*xy-x*y)/(np.sqrt((self.n*x_2-x**2)*(self.n*y_2-y**2))) #Obtiene el coeficiente de correlación

            
    def Sacar_Promedio(self):
        if self.n_a != 1:
            for i in range(self.n):
                sumax=0
                sumay=0
                for j in range(self.n_a):
                    sumax += self.datos_x[j,i]
                    sumay += self.datos_y[j,i]

                self.x.append(sumax/self.n_a)
                self.y.append(sumay/self.n_a)
        else:
            for i in range(self.n):
                self.x.append(self.datos_x[0,i])
                self.y.append(self.datos_y[0,i])
            
    #------------------------------------Graficadores-------------------------------------------
    def Graficar_Recta(self): 
        p=np.arange(self.x[0],self.x[self.n-1],0.1)
        plt.plot(self.x,self.y,'o')
        plt.plot(p,self.m*p+self.b)
        plt.xlabel(self.nombre_ejex)
        plt.ylabel(self.nombre_ejey)
        plt.title(self.titulo)
        plt.grid()
        plt.show()
        
        
    def Graficador(self):  #Este graficador grafica los datos que se tengan en las tuplas de self.y y self.x
        plt.plot(self.x,self.y,"o")
        plt.xlabel(self.nombre_ejex)
        plt.ylabel(self.nombre_ejey) 
        plt.title(self.titulo)
        plt.grid()
        plt.show()
        
    def Graficador_Exp(self):
        x=np.arange(self.xsinlog[0],self.xsinlog[-1],0.001)
        plt.plot(self.xsinlog,self.ysinlog,'o')
        plt.plot(x,np.e**self.b*x**self.m)
        plt.xlabel(self.nombre_ejex)
        plt.ylabel(self.nombre_ejey)
        plt.title(self.titulo)
        plt.grid()
        plt.show()
        
        

    def grafica(self):    #ESTA FUNCIÓN RECIBE LOS DATOS DIGITADOS POR EL USUARIO PARA DESPUÉS GRAFICARLOS
            #Utilizamos **kwargs y a que así los elementos que se pasen a la función son indetermados osea que puede haber un numero n de parametros 
            #Los cuales se van almacenando en un diccionario llamado kwargs
            
                    
                    
            self.ventana2 = tk.Tk()   #Crea una ventana nueva
            self.ventana2.title("Datos")   #Le asigna el título de ventana 'Datos' a la nueva ventana
            self.ventana2.geometry("700x430")  #Ajusta la ventana para que sea de una dimensión de 980x400 pixeles
            self.ventana2.resizable(1,1)   #Esta opcion impide que el usuario pueda redimensionar la ventana
            
            
            #------------------------CÓDIGO DE LA GRAFICA-----------------------
            
            
            
            grafica = tk.Frame(self.ventana2) #Crea un nuevo Frame en el cual irá la grafica
            
            fig = Figure(figsize=(self.ancho, 4), facecolor='white')   #Crea la base de la grafica
            axis = fig.add_subplot(111)
            
            a = [1,2,3,4,5,6,7,8,9,10]
            b = [1,2,3,4,5,6,7,8,9,10]

        
            axis.plot(a,b)  #Imprime los datos en la grafica
            axis.set_ylabel('Distancia (m)')
            axis.set_xlabel('Tiempo (s)')
        
            axis.grid()   #Crea la cuadricula de fondo que se ve en la grafica
            
            canvas = FigureCanvasTkAgg(fig, grafica)
            canvas.draw()
            canvas.get_tk_widget().pack()      #codigo para imprimir la grafica y el menú de opciones que hay debajo de ella
            toolbar = NavigationToolbar2Tk(canvas, grafica)
            toolbar.update()
            canvas._tkcanvas.pack()
            
            grafica.grid(column=0, row=0)  #Imprime la tabla en la columna 0 y fila 0 de la ventana
            tk.Button(self.ventana2, text="Largo", command= self.largo).grid(row = 0, column = 1)
            self.ventana2.rowconfigure(0, weight=1) 
            self.ventana2.mainloop()    #Hace que se repita y se repita como en un ciclo

        
    #-------------------------------------------------------------------------------
    
    def largo(self):
        self.ancho+= 1
        print(self.ancho)
        
    def Imprimir_datos(self):
        print("El valor de la pendiente es:",self.m)
        print("El valor de la intersección es:",self.b)
        
        print("\nLa ecuación de la recta es y={}x+{}".format(self.m,self.b))
        
        print("\nEl error de la pendiente es",self.sm)
        print("El error de la intersección es:",self.sb)
        print("El valor del coeficiente de correlación es:",self.cc)
        
        print("La ecuación de la exponencial es: y=e^({})x^({})".format(self.b,self.m))

        
    #----------------------Creación de archivos .txt con los datos para graficar en Gnu-Plot---------------------------------
    
    
    def Escribir_logaritmos(self): 
        for i in range(self.n):
            x = abs(0.02/self.ysinlog[i])
            self.delta.append(round(x,1-int(floor(log10(x)))-1))
        
        fichero1 = open("datos_con_log.txt", 'w')
        for i in range(self.n):
            fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:4f}\n'.format(self.x[i], 0 ,  self.y[i], self.delta[i]))
    def Escribir_datos(self):
        fichero2 = open("datos_sin_log.txt","w")

        for i in range(self.n):
            fichero2.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:4f}\n'.format(self.xsinlog[i], 0 ,  self.ysinlog[i], 0.01))
        


#Clase la cual maneja las opciones de la interfaz

class Interfaz:
    def __init__(self,ventana):
        self.ventana = ventana 
        self.ventana.title("Linealizador")
        self.ventana.geometry("355x400")
        self.ventana.resizable(0,0)
        self.ventana.config(bd=50)   #Agrega un borde de 10 espacios


            
        menubar = tk.Menu(self.ventana)
        filemenu =tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Nuevo",command = self.nuevo)
        filemenu.add_command(label="Abrir", command = self.abrir)
        filemenu.add_command(label="Guardar", command = self.guardar)
        filemenu.add_command(label="Guardar como" , command = self.guardar_como)
        filemenu.add_separator()
        filemenu.add_command(label="Salir",command=self.ventana.quit)
        menubar.add_cascade(menu=filemenu,label="Archivo")

        self.ventana.config(menu=menubar)

    #Creación de etiqueta inferior
    
        
        v_padx = 5
        v_pady = 5
        
        boton_elegir_archivos = tk.Button(self.ventana,text = "Elegir archivos",command=self.seleccion_archivos,padx = 10,pady = 10,)
        boton_elegir_archivos.grid(row = 7,column=1)
        boton_linealizar_datos = tk.Button(self.ventana,text="Linealizar datos",command=self.linealizar,padx = 10 ,pady = 10)
        boton_linealizar_datos.grid(row=7,column=2)
        boton_guardar = tk.Button(self.ventana,text = "Guardar sesión", command = self.guardar,padx = 10 ,pady = 10 )
        boton_guardar.grid(row = 8, column = 1)

        self.numero_datos = StringVar()
        self.nombre_ejex = StringVar()
        self.nombre_ejey = StringVar()
        self.nombre_titulo = StringVar()

        tk.Label(self.ventana, text = "Numero de datos",padx = v_padx,pady = v_pady).grid(row = 3, column = 1)
        tk.Label(self.ventana, text = "Nombre eje x",padx = v_padx,pady = v_pady).grid(row = 4, column = 1)
        tk.Label(self.ventana, text = "Nombre eje y",padx = v_padx,pady = v_pady).grid(row = 5, column = 1 )
        tk.Label(self.ventana, text = "Titulo gráfica",padx = v_padx,pady = v_pady).grid(row = 6, column = 1)
        
        tk.Entry(self.ventana, textvariable = self.numero_datos).grid(row = 3,column = 2)
        tk.Entry(self.ventana, textvariable = self.nombre_ejex).grid(row = 4,column = 2)
        tk.Entry(self.ventana, textvariable = self.nombre_ejey).grid(row = 5, column = 2)
        tk.Entry(self.ventana, textvariable = self.nombre_titulo).grid(row = 6, column = 2)

    #Opciones para el menu despegable de la ventana

    def nuevo(self):
        self.mensaje.set("Nueva linealización")
        
    def abrir(self):
        pass
            
    def guardar(self):
        self.mensaje.set("Guardar linealización")
    
    def guardar_como(self):
        self.mensaje.set("Guardar como")
        
    #-------------------------------------------------------  
    
    def seleccion_archivos(self):
        
        self.archivos_rutas = fd.askopenfilenames(
        initialdir=".",     #Abre la ventana en el directorio más cercano
        filetypes=(('Ficheros de texto','*.txt'),), #Menciona la extensión de los archivos que leerá
        title="Elección de archivos de datos a linealizar") #Coloca un nombre a la ventana
        self.archivos_nombres=[]
        for i in  self.archivos_rutas:
             self.archivos_nombres.append(os.path.basename(i))
            
        contador = 9        
        for i in  self.archivos_nombres:
            tk.Label(self.ventana,text=i,pady = 10).grid(row=contador,column=2)
            contador+=1

            
    def linealizar(self):
        
        p = Minimos(int(self.numero_datos.get()),self.archivos_rutas,self.nombre_ejex.get(),self.nombre_ejey.get(),self.nombre_titulo.get())  #1-Número de datos del documento, 2-Tupla que contiene lo
        #nombres de los archivos los cuales tienen datos a promediar, 3-Obtiene el numero de archivos que hay, 4-Nombre del eje x, 
        # 5- Nombre del eje y

        p.Obtener_datos()  #Almacena los datos del archivo txt para luego trabajarlos
        p.Sacar_Promedio() #Obtiene el promedio de los datos, Nota: Si solo se trabaja con un archivo entonces esto no afecta en nada
        #p.Graficador()  
        p.Sacar_Logaritmos()        
        #p.Graficador()  
        p.Minimos_cuadrados()
        #p.Graficar_Recta() 
        #p.Graficador_Exp()
        p.Escribir_logaritmos()
        p.Imprimir_datos()
        p.grafica()
        
        
root = tk.Tk()
ventana_principal = Interfaz(root)

root.mainloop()
