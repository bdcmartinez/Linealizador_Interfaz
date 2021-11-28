import tkinter as tk 
import os
from tkinter import filedialog as FileDialog
from io import open
from tkinter import filedialog as fd
from io import open

ruta = "" #La utilizaremos para almacenar la ruta del fichero

root = tk.Tk()
root.title("Mi editor")
root.geometry("700x400")
root.resizable(0,0)

def nuevo():
    mensaje.set("Nueva linealización")
    
def abrir():
    global ruta
    mensaje.set("Abrir proyecto")
    ruta = FileDialog.askopenfilename(
        initialdir=".",
        filetypes=(("Ficheros de texto",".txt"),),
        title="Abrir un fichero de texto")
    if ruta != "":
        fichero = open(ruta,"r")
        contenido = fichero.read()
        

def guardar():
    mensaje.set("Guardar linealización")

def guardar_como():
    mensaje.set("Guardar como")
    
def seleccion_archivos():
    
    archivos_rutas = fd.askopenfilenames(
    initialdir=".",     #Abre la ventana en el directorio más cercano
    filetypes=(('Ficheros de texto','*.txt'),), #Menciona la extensión de los archivos que leerá
    title="Elección de archivos de datos a linealizar") #Coloca un nombre a la ventana
    archivos_nombres=[]
    for i in archivos_rutas:
        archivos_nombres.append(os.path.basename(i))
        
    contador = 2        
    for i in archivos_nombres:
        tk.Label(root,text=i).grid(row=contador,column=3)
        contador+=1

def linealizar():
    print("hola")

        
        
menubar = tk.Menu(root)
filemenu =tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="Nuevo",command = nuevo)
filemenu.add_command(label="Abrir", command = abrir)
filemenu.add_command(label="Guardar", command = guardar)
filemenu.add_command(label="Guardar como" , command = guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir",command=root.quit)
menubar.add_cascade(menu=filemenu,label="Archivo")

root.config(menu=menubar)

#Creación de etiqueta inferior
mensaje = tk.StringVar()
mensaje.set("Programa creado por Brayan")
monitor = tk.Label(root,textvar=mensaje,justify="left")
monitor.grid(row=0,column=0)

boton1 = tk.Button(root,text = "Elegir archivos\n a linealizar",command=seleccion_archivos)
boton1.grid(row = 1,column=1)
boton2 = tk.Button(root,text="Linealizar datos",command=linealizar)
boton2.grid(row=1,column=2)
label1 = tk.Label(root,text="Los archivos seleccionados son:")
label1.grid(row = 1, column = 3)



root.mainloop()