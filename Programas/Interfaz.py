import tkinter as tk 
from tkinter import filedialog as FileDialog
from io import open

ruta = "" #La utilizaremos para almacenar la ruta del fichero

root = tk.Tk()
root.title("Mi editor")

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

menubar = tk.Menu(root)
filemenu =tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="Nuevo",command = nuevo)
filemenu.add_command(label="Abrir", command = abrir)
filemenu.add_command(label="Guardar", command = guardar)
filemenu.add_command(label="Guardar como" , command = guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir",command=root.quit)
menubar.add_cascade(menu=filemenu,label="Archivo")

#Creación de etiqueta inferior
mensaje = tk.StringVar()
mensaje.set("Programa creado por Brayan")
monitor = tk.Label(root,textvar=mensaje,justify="left")
monitor.pack(side="left")

root.config(menu=menubar)

root.mainloop()