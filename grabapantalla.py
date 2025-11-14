import datetime
import os
import socket
import time

from PIL import ImageDraw, ImageFont, ImageGrab

intervalo = 30
directorio = "C:/tmp/capturas"
nombre_equipo = socket.gethostname()

os.makedirs(directorio, exist_ok=True)

while True:
    momento_captura = (
        nombre_equipo + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    momento_archivo = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    nombre_archivo = f"captura_{momento_archivo}.png"
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
