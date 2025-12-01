
from tkinter import messagebox

def mensajes_informacion(mensaje): 
        messagebox.showinfo("INFORMACION",mensaje)

def mensajes_Error(mensaje): 
        messagebox.showerror("ERROR",mensaje)

def mensajes_askyesno(mensajes):
        return messagebox.askyesno("CONFIRMAR",mensajes)