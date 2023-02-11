
from MainWindow import *
from LogaritmWindow import * 
from LogaritmWindow import Ui_LogaritmWindow

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
        self.xy=[]
        self.x_2=[]
        
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
                    
    
    def Sacar_LogaritmosPot(self):
        for i in range(self.n):
            self.xsinlog.append(self.x[i])
            self.ysinlog.append(self.y[i])
            if self.x[i]!=0:
                self.x[i]=math.log(self.x[i])
            if self.y[i]!=0:
                self.y[i]=math.log(self.y[i])
    def Sacar_LogaritmosExp(self):
        for i in range(self.n):
            self.ysinlog.append(self.y[i])
            if self.y[i]!=0:
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
            self.xy.append(self.x[i]*self.y[i])
            x_2+= self.x[i]**2
            self.x_2.append(self.x[i]**2)
            y_2+= self.y[i]**2

        self.xy.append(xy)
        self.x_2.append(x_2)
        self.x.append(x)
        self.y.append(y)
        
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
        
        fig, ax1 = plt.subplots()
        
        salto = (self.x[self.n-1]-self.x[0])/100
        p=np.arange(self.x[0],self.x[self.n-1],salto)
        #-----------
        aux1 = self.y[-1]
        self.y.pop(-1)
        aux2 = self.y[-1]
        self.x.pop(-1)
        
        ax1.plot(self.x,self.y,'o')
        print(self.m,self.b)
        ax1.plot(p,self.m*p+self.b)
        ax1.set_xlabel(self.nombre_ejex)
        ax1.set_ylabel(self.nombre_ejey)
        ax1.set_title(self.titulo)
        ax1.grid()
        plt.show()
        
        self.y.append(aux1)
        self.x.append(aux2)

    def Graficador(self):  #Este graficador grafica los datos que se tengan en las tuplas de self.y y self.x
        plt.plot(self.x,self.y,"o")
        plt.xlabel(self.nombre_ejex)
        plt.ylabel(self.nombre_ejey) 
        plt.title(self.titulo)
        plt.grid()
        plt.show()
        
        
    def Graficador_Pot(self):

        
        fig, ax2 = plt.subplots()
        salto = (self.xsinlog[self.n-1]-self.xsinlog[0])/100
        x=np.arange(self.xsinlog[0],self.xsinlog[-1],salto)
        ax2.plot(self.xsinlog,self.ysinlog,'o')
        ax2.plot(x,np.e**self.b*x**self.m)
        ax2.set_xlabel(self.nombre_ejex)
        ax2.set_ylabel(self.nombre_ejey)
        ax2.set_title(self.titulo)
        ax2.grid()
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
        

    #----------------------Creación de archivos .txt con los datos para graficar en Gnu-Plot---------------------------------
    
    def RS_Minimos(self):
        
        fichero1 = open("RS MétodoMínimos.txt", 'w')
        fichero1.write('{} \t {} \t {} \t {} \t {} \t {}\n'.format("x","y","ln x","ln y","xy","xx") )
        for i in range(self.n):
            fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f}\n '.format(self.x[i],  self.y[i], self.xy[i], self.x_2[i]))
        fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f} \n '.format(self.x[-1] , self.y[-1], self.xy[-1], self.x_2[-1]))
        fichero1.write("y={}x+{}\n".format(round(self.m,3),round(self.b,3)))   #Ecuación de la recta
    
    def RS_Potencial(self): 

        
        fichero1 = open("RS MétodoFPotencial.txt", 'w')
        fichero1.write('{} \t {} \t {} \t {} \t {} \t {}\n'.format("x","y","ln x","ln y","xy","xx") )
        for i in range(self.n):
            fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f} \t {4:3f} \t {5:3f}\n '.format(self.xsinlog[i],  self.ysinlog[i], self.x[i],  self.y[i], self.xy[i], self.x_2[i]))
        fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f} \n '.format(self.x[-1] , self.y[-1], self.xy[-1], self.x_2[-1]))
        fichero1.write("y={}x+{}\n".format(round(self.m,3),round(self.b,3)))   #Ecuación de la recta
        fichero1.write("y={}x^({})".format(round(np.exp(self.b),3),round(self.m,3))) #Ecuación de la exponencial
    
    def RS_Exponencial(self): 

        
        fichero1 = open("RS MétodoFExponencial.txt", 'w')
        fichero1.write('{} \t {} \t {} \t {} \t {} \t {}\n'.format("x","y","ln x","ln y","xy","xx") )
        for i in range(self.n):
            fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f} \t {4:3f} \t {5:3f}\n '.format(self.xsinlog[i],  self.ysinlog[i], self.x[i],  self.y[i], self.xy[i], self.x_2[i]))
        fichero1.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f} \n '.format(self.x[-1] , self.y[-1], self.xy[-1], self.x_2[-1]))
        fichero1.write("y={}x+{}\n".format(round(self.m,3),round(self.b,3)))   #Ecuación de la recta
        fichero1.write("y={}x^({})".format(round(np.exp(self.b),3),round(self.m,3))) #Ecuación de la exponencial
    
    def Escribir_datosMinimos(self):
        fichero2 = open("Datos.dat","w")

        for i in range(self.n):
            fichero2.write('{0:3f} \t {1:3f}\n'.format(self.x[i],  self.y[i]))
    
    def Escribir_datosPotencial(self):
        fichero2 = open("Datos.dat","w")

        for i in range(self.n):
            fichero2.write('{0:3f} \t {1:3f} \t {2:3f} \t {3:3f}\n'.format(self.xsinlog[i],  self.ysinlog[i], self.x[i],  self.y[i]))

    def Escribir_datosExponencial(self):
        fichero2 = open("Datos.dat","w")

        for i in range(self.n):
            fichero2.write('{0:3f} \t {1:3f} \t {2:3f}\n'.format(self.x[i],  self.ysinlog[i],  self.y[i]))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.w = None
        
        #Botones principales
        self.Boton_ElegirA.clicked.connect(self.seleccion_archivos)
        self.Boton_Linealizar.clicked.connect(self.linealizar)
        
        #Opciones de la parte superior

        self.actionCreditos.triggered.connect(self.creditos)
        self.actionAbrir.triggered.connect(self.abrir)
        self.actionMinimosCuadrados.triggered.connect(self.FuncMinimosCuadrados)
        self.actionPotencial.triggered.connect(self.FuncPotencial)
        self.actionExponencial.triggered.connect(self.FuncExponencial)
    
    def creditos(self):
        print("Acerca de")
    def abrir(self):
        print("Abrir")      
    def FuncMinimosCuadrados(self):
        self.OpcLinealizador.setText("Obtencion de mínimos cuadrados")
        print("MinimosCuadrados")
    def FuncPotencial(self):
        self.OpcLinealizador.setText("Método de potencia")
        print("Potencial")
    def FuncExponencial(self):
        self.OpcLinealizador.setText("Método exponencial")
        print("Exponencial")

    def seleccion_archivos(self): #Este método lo que hace es premitir que el usuario seleccione los archivos que el usuario eligirá
        self.archivos_rutas = fd.askopenfilenames(
        initialdir=".",     #Abre la ventana en el directorio más cercano
        filetypes=(('Ficheros de texto','*.txt'),), #Menciona la extensión de los archivos que leerá
        title="Elección de archivos de datos a linealizar") #Coloca un nombre a la ventana
        self.archivos_nombres=[]
        for i in  self.archivos_rutas:
             self.archivos_nombres.append(os.path.basename(i))
             
        #Escribe los nombres de los archivos junto con su extensión 
        #en la parte inferior de la interfaz
        _translate = QtCore.QCoreApplication.translate
        for i,c in enumerate(self.archivos_nombres):#i es un contador y c toma los elementos de la lista archivos_rutas
            item = QtWidgets.QListWidgetItem()
            self.Nom_Archivos.addItem(item)
            item = self.Nom_Archivos.item(i+1) 
            item.setText(_translate("MainWindow",c)) #Escribe el texto "c" en la fila i+1



        
    #Abre una nueva ventana en la que se mostrarán los resultados de la linealización
    def linealizar(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_LogaritmWindow()
        self.ui.setupUi(self.window) 
        
        #1-Número de datos del documento 
        #2-Tupla que contiene lo nombres de las rutas de los archivos a los cuales se les desea linealizar
        #3-Nombre del eje x
        #4-Nombre del eje y
                
        #Instancia del objeto "p" de la clase Minimos
        self.p = Minimos(int(self.Num_datos.text()),self.archivos_rutas,self.Nom_ejex.text(),self.Nom_ejey.text(),self.Titulo_grafica.text())  


        self.p.Obtener_datos()  #Almacena los datos del archivo txt para luego trabajarlos
        self.p.Sacar_Promedio() #Obtiene el promedio de los datos, Nota: Si solo se trabaja con un archivo entonces esto no afecta en nada
        #self.p.Graficador()          
        
        if self.OpcLinealizador.text() == "Obtención de mínimos cuadrados":
        
            self.p.Minimos_cuadrados()
            self.p.Graficar_Recta() 
            
            self.p.RS_Minimos()
            self.p.Escribir_datosMinimos()

        if self.OpcLinealizador.text() == "Método de potencia":
            
        
            self.p.Sacar_LogaritmosPot()
            self.p.Minimos_cuadrados()
            self.p.Graficar_Recta() 
            self.p.Graficador_Pot()
            
            
            self.p.RS_Potencial()
            self.p.Escribir_datosPotencial()

        if self.OpcLinealizador.text() == "Método Exponencial":
        
            self.p.Sacar_LogaritmosExp()
            self.p.Minimos_cuadrados()
            self.p.Graficar_Recta() 
            
            
            self.p.RS_Exponencial()
            self.p.Escribir_datosExponencial()


        self.Imprimir_datos()  #Función la cual imprime los datos calculados en la nueva ventana creada
        self.window.show()   
            
    def Imprimir_datos(self):
        self.ui.Label_Pendiente.setText(str(self.p.m)) #Impresión... del valor de la pendiente
        self.ui.Label_Interseccion.setText(str(self.p.b)) #...valor de la intersección
        
        self.ui.Label_ePendiente.setText(str(self.p.sm)) #valor del error de la pendiente
        self.ui.Label_eInterseccion.setText(str(self.p.sb))  #valor del error de la intersección
        
        self.ui.Label_Correlaccion.setText(str(self.p.cc)) #valor del coeficiente de correlación
              
        self.ui.Label_ecRecta.setText("y={}x+{}".format(self.p.m,self.p.b,))   #Ecuación de la recta
        self.ui.Label_ecExponencial.setText("y={}x^({})".format(np.e**self.p.b,self.p.m,)) #Ecuación de la exponencial


    #------------------

          
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()