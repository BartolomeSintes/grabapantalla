import datetime
import os
import socket
import sys
import threading
import time
import tkinter as tk

from PIL import ImageDraw, ImageFont, ImageGrab, ImageTk


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
            fuente = ImageFont.load_default()  # Si no encuentra la fuente
        posicion = (50, 50)
        color = (255, 0, 0)
        dibujo.text(posicion, texto_en_captura, fill=color, font=fuente)
        captura.save(ruta_completa)
        time.sleep(intervalo)

def lista():
    global directorio

    momento_listado = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    path = os.path.abspath(
        os.path.join(directorio, "listado-" + momento_listado + ".txt")
    )
    elementos = os.listdir(directorio)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Listado del directorio: {directorio}\n")
        f.write("=" * 80 + "\n")
        with os.scandir(directorio) as elementos:
            for entrada in elementos:
                if entrada.is_file():
                    try:
                        infor = entrada.stat()
                        tamano = infor.st_size
                        fecha_mod = datetime.datetime.fromtimestamp(infor.st_mtime)
                        f.write(
                            f"{entrada.name}  {tamano}   {fecha_mod.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        )
                    except Exception as e:
                        f.write(f"No se pudo leer {entrada.name}: {e}\n\n")
                elif entrada.is_dir():
                    f.write(f"{entrada.name}/\n\n")

def funcion_1():
    global info, ventana

    dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

    # path = os.path.abspath(os.path.join(dir, "img/circulo-rojo-128.png"))
    # icono = ImageTk.PhotoImage(file=path)
    # ventana.iconphoto(True, icono)

    path = os.path.abspath(os.path.join(dir, "img/circulo-rojo.ico"))
    ventana.after(201, lambda: ventana.iconbitmap(path))

    info.config(text="🔴 Grabando...", fg="red")

    hilo = threading.Thread(target=graba, daemon=True)
    hilo.start()

def funcion_2():
    global grabando, info, ventana

    dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

    # path = os.path.abspath(os.path.join(dir, "img/circulo-rojo-128.png"))
    # icono = ImageTk.PhotoImage(file=path)
    # ventana.iconphoto(True, icono)

    path = os.path.abspath(os.path.join(dir, "img/circulo-negro.ico"))
    ventana.after(201, lambda: ventana.iconbitmap(path))

    info.config(text="⚫ Inactivo", fg="black")

    hilo = threading.Thread(target=lista, daemon=True)
    hilo.start()

    grabando = False


intervalo = 30
directorio = "C:/tmp/capturas"
# directorio = "/home/tu_usuario/mis_archivos"
grabando = True

os.makedirs(directorio, exist_ok=True)

ventana = tk.Tk()
ventana.title("Capturador de pantalla")
ventana.geometry("300x200")  # Ancho x Alto

dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
path = os.path.abspath(os.path.join(dir, "img/circulo-negro.ico"))
ventana.after(201, lambda: ventana.iconbitmap(path))

info = tk.Label(ventana, text="⚫ Inactivo", font=("Arial", 14), fg="black")
info.pack(pady=15)

# Crear botones
boton1 = tk.Button(ventana, text="Grabar", command=funcion_1, width=20)
boton2 = tk.Button(ventana, text="Detener", command=funcion_2, width=20)

# Colocar los botones en la ventana
boton1.pack(pady=10)
boton2.pack(pady=10)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
