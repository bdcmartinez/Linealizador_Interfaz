import tkinter as tk 
import os
from tkinter import filedialog as FileDialog
from io import open
from tkinter import filedialog as fd
from io import open


class Interfaz:
    def __init__(self,ventana):
        self.ventana = ventana 
        self.ventana.title("Mi editor")
        self.ventana.geometry("700x400")
        self.ventana.resizable(0,0)

            
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
        self.mensaje = tk.StringVar()
        self.mensaje.set("Programa creado por Brayan")
        monitor = tk.Label(self.ventana,textvar=self.mensaje,justify="left")
        monitor.grid(row=0,column=0)

        boton1 = tk.Button(self.ventana,text = "Elegir archivos\n a linealizar",command=self.seleccion_archivos)
        boton1.grid(row = 1,column=1)
        boton2 = tk.Button(self.ventana,text="Linealizar datos",command=self.linealizar)
        boton2.grid(row=1,column=2)
        label1 = tk.Label(self.ventana,text="Los archivos seleccionados son:")
        label1.grid(row = 1, column = 3)


    def nuevo(self):
        self.mensaje.set("Nueva linealización")
        
    def abrir(self):
        pass
            

    def guardar(self):
        self.mensaje.set("Guardar linealización")

    def guardar_como(self):
        self.mensaje.set("Guardar como")
        
    def seleccion_archivos(self):
        
        self.archivos_rutas = fd.askopenfilenames(
        initialdir=".",     #Abre la ventana en el directorio más cercano
        filetypes=(('Ficheros de texto','*.txt'),), #Menciona la extensión de los archivos que leerá
        title="Elección de archivos de datos a linealizar") #Coloca un nombre a la ventana
        self.archivos_nombres=[]
        for i in  self.archivos_rutas:
             self.archivos_nombres.append(os.path.basename(i))
            
        contador = 2        
        for i in  self.archivos_nombres:
            tk.Label(self.ventana,text=i).grid(row=contador,column=3)
            contador+=1

    def linealizar(self):
        print("hola")

        
        



root = tk.Tk()
ventana_principal = Interfaz(root)





root.mainloop()