import os # Manejo de directorios
import re # Manejo de expresiones regulares
import tkinter as tk
from tkinter import filedialog
import shutil
import os
from tkinter import font as tkfont 
import pandas as pd
import re  # para RE
from io import StringIO
import numpy as np
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from copy import copy
import openpyxl.utils
from openpyxl.styles import Alignment
from openpyxl.styles import Border, Side
from openpyxl.worksheet.page import PageMargins
import string
from tkinter import messagebox

########################################################################################################
########## PARTE1: Conjunto de rutas
########################################################################################################


# Crear la ventana principal
root = tk.Tk()
root.title("Selección de Directorio")
root.geometry("400x200")

# Crear una etiqueta para el título
label_title = tk.Label(root, text="Selecciona un directorio", font=("Arial", 16))
label_title.pack(pady=20)

# Crear una etiqueta para mostrar el directorio seleccionado
label_dir = tk.Label(root, text="", font=("Arial", 10))
label_dir.pack(pady=10)

# Función para seleccionar el directorio
selected_directory = None
def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        label_dir.config(text=f"Directorio seleccionado: {selected_directory}")
        label_title.config(text="Procesando...")
        btn_select_dir.pack_forget()  # Ocultamos el botón de seleccionar directorio
        root.update()  # Mantener la ventana abierta mientras se procesa el código

# Crear un botón para seleccionar el directorio
btn_select_dir = tk.Button(root, text="Seleccionar Directorio", command=select_directory)
btn_select_dir.pack(pady=10)

# Mostrar la ventana y permitir que el usuario seleccione un directorio
root.update()

# Esperar a que el usuario seleccione el directorio
while not selected_directory:
    root.update()


# Ruta de la carpeta Main
#folder_path = r"C:\Users\fpino\OneDrive - CSI Ingenieros - CIEMSA\Escritorio\Queue Tables\test"
folder_path = selected_directory

year = 0  # Para almacenar el año más grande

Mit = False #

hcm_am_files = []
hcm_pm_files = []
hcm_sat_files = []

synchro_am_files = []
synchro_pm_files = []
synchro_sat_files = []

simtraffic_am_files = []
simtraffic_pm_files = []
simtraffic_sat_files = []

year_pattern = re.compile(r'\d{4}')  # Busca un número de 4 dígitos 

# Recorre todos los archivos en la carpeta
for file_name in os.listdir(folder_path):
    match = year_pattern.search(file_name)
    if match is not None:
        file_year = int(match.group())  # Convierte el año encontrado en entero

        if file_year > year:
            year = file_year

# Clasificamos los archivos en las listas con el año encontrado
if year != 0:
    for file_name in os.listdir(folder_path):

        if str(year) in file_name:
            # Clasifica en AM, PM o SAT
            if "AM" in file_name:
                if "Synchro" in file_name:
                    synchro_am_files.append(file_name)
                elif "Simtraffic " in file_name:
                    simtraffic_am_files.append(file_name)
                else:
                    hcm_am_files.append(file_name)

            elif "PM" in file_name:
                if "Synchro" in file_name:
                    synchro_pm_files.append(file_name)
                elif "Simtraffic " in file_name:
                    simtraffic_pm_files.append(file_name)
                else:
                    hcm_pm_files.append(file_name)

            elif "SAT" in file_name:
                if "Synchro" in file_name:
                    synchro_sat_files.append(file_name)
                elif "Simtraffic " in file_name:
                    simtraffic_sat_files.append(file_name)
                else:
                    hcm_sat_files.append(file_name)
else:
    print("no se encontraron patrones de 4 dígitos en los archivos proporcionados")


########################################################################################################
########## PARTE2: Estructura de datos
########################################################################################################

#EXTRACIÓN DE INTERSECCIONES 

#Tomamos un archivo del HBC
ruta_completa = os.path.join(folder_path, hcm_am_files[0])

with open(ruta_completa, 'r') as file:
    contenido = file.read()

paginas = re.split(r'Page \d+', contenido) # separamos en paginas cuando encuentra la palabra Page seguido de un número

Addresses = []

for i in range(len(paginas)):
    lineas = paginas[i].splitlines()
    lineas_filtradas = [linea for linea in lineas if linea.strip()]
    texto_procesado = "\n".join(lineas_filtradas)
    texto_procesado = texto_procesado.splitlines()
    texto_procesado = texto_procesado[:2]
    texto_procesado = "\n".join(texto_procesado)

    match = re.search(r':\s*(.*?)\t', texto_procesado) # procesa entre el ":" hasta el primer tabulado
    if match:
        Addresses.append(match.group(1))

print("Las direcciones son:", Addresses)