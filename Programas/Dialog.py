    
import tkinter as tk 
from tkinter import filedialog as fd
from io import open
    
root = tk.Tk()
root.title("Mi editor")

ruta = fd.askopenfilenames(
initialdir=".",
filetypes=(('Ficheros de texto','*.txt'),),
title="Elección de archivos de datos a linealizar")

print(ruta)
root.mainloop()