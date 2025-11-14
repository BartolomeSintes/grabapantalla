import datetime
import os
import socket
import threading
import time
import tkinter as tk

from PIL import ImageDraw, ImageFont, ImageGrab


def graba():
    global directorio, intervalo, grabando

    grabando = True
    while grabando:
        nombre_equipo = socket.gethostname()
        momento_captura = (
            nombre_equipo + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        momento_archivo = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        nombre_archivo = f"captura-{momento_archivo}.png"
        texto_en_captura = momento_captura
        ruta_completa = os.path.join(directorio, nombre_archivo)
        captura = ImageGrab.grab()
        dibujo = ImageDraw.Draw(captura)
        try:
            fuente = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            fuente = ImageFont.load_default()
        posicion = (50, 50)
        color = (255, 0, 0)
        dibujo.text(posicion, texto_en_captura, fill=color, font=fuente)
        captura.save(ruta_completa)
        # print(f"Captura de pantalla guardada como: {ruta_completa}")
        time.sleep(intervalo)


def funcion_1():
    global info
    info.config(text="🔴 Grabando...", fg="red")
    hilo = threading.Thread(target=graba, daemon=True)
    hilo.start()


def funcion_2():
    global grabando, info
    info.config(text="⚫ Inactivo", fg="black")
    grabando = False


intervalo = 5
directorio = "C:/tmp/capturas"
grabando = True

os.makedirs(directorio, exist_ok=True)

ventana = tk.Tk()
ventana.title("Capturador de pantalla")
ventana.geometry("300x200")

info = tk.Label(ventana, text="⚫ Inactivo", font=("Arial", 14), fg="black")
info.pack(pady=15)

boton1 = tk.Button(ventana, text="Grabar", command=funcion_1, width=20)
boton2 = tk.Button(ventana, text="Detener", command=funcion_2, width=20)

boton1.pack(pady=10)
boton2.pack(pady=10)

ventana.mainloop()
