import os  # Manejo de directorios
import re  # Manejo de expresiones regulares
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd  # Para manejar la tabla de inputs

########################################################################################################
########## PARTE1: Conjunto de rutas
########################################################################################################

# Crear la ventana principal
root = tk.Tk()
root.title("Selección de Directorio")
root.geometry("900x400")

# Crear un frame para los elementos que usan pack()
frame_pack = tk.Frame(root)
frame_pack.pack(pady=20)

# Crear otro frame para los elementos que usan grid()
frame_grid = tk.Frame(root)
frame_grid.pack()

# Crear la etiqueta para el título dentro del frame de pack()
label_title = tk.Label(frame_pack, text="Selecciona un directorio", font=("Arial", 16))
label_title.pack(pady=10)

# Crear un botón para seleccionar el directorio dentro del frame de pack()
selected_directory = None
def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        label_dir.config(text=f"Directorio seleccionado: {selected_directory}")
        label_title.config(text="Procesando...")
        btn_select_dir.pack_forget()  # Ocultamos el botón de seleccionar directorio
        root.update()  # Mantener la ventana abierta mientras se procesa el código

btn_select_dir = tk.Button(frame_pack, text="Seleccionar Directorio", command=select_directory)
btn_select_dir.pack(pady=10)

# Crear una etiqueta para mostrar el directorio seleccionado
label_dir = tk.Label(frame_pack, text="", font=("Arial", 10))
label_dir.pack(pady=10)

# Esperar a que el usuario seleccione el directorio
root.update()
while not selected_directory:
    root.update()

# Ruta de la carpeta Main
folder_path = selected_directory

year = 0  # Para almacenar el año más grande
Mit = False

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
    print("No se encontraron patrones de 4 dígitos en los archivos proporcionados")

listas = [hcm_am_files, hcm_pm_files, hcm_sat_files, synchro_am_files, synchro_pm_files, synchro_sat_files, simtraffic_am_files, simtraffic_pm_files, simtraffic_sat_files]
archivos = []  

# Iteramos sobre cada sublista dentro de 'listas'
for sublista in listas:
    for elemento in sublista:
        archivos.append(elemento)

########################################################################################################
########## PARTE2: Estructura de datos
########################################################################################################

# Tomamos un archivo del HBC
if hcm_am_files:
    ruta_completa = os.path.join(folder_path, hcm_am_files[0])

    with open(ruta_completa, 'r') as file:
        contenido = file.read()

    paginas = re.split(r'Page \d+', contenido)  # separamos en paginas cuando encuentra la palabra Page seguido de un número

    Addresses = []

    for i in range(len(paginas)):
        lineas = paginas[i].splitlines()
        lineas_filtradas = [linea for linea in lineas if linea.strip()]
        texto_procesado = "\n".join(lineas_filtradas)
        texto_procesado = texto_procesado.splitlines()
        texto_procesado = texto_procesado[:2]
        texto_procesado = "\n".join(texto_procesado)

        match = re.search(r':\s*(.*?)\t', texto_procesado)  # procesa entre el ":" hasta el primer tabulado
        if match:
            Addresses.append(match.group(1))

    print("Las direcciones son:", Addresses)

    Addresses.append("Page")

    diccionario = {}  # Crear un diccionario vacío

    # Iteramos hasta el penúltimo índice de la lista, ya que queremos pares n y n+1
    for i in range(len(Addresses) - 1):
        diccionario[i] = [Addresses[i], Addresses[i + 1]]

    print(diccionario)

########################################################################################################
########## PARTE3: Tabla de inputs
########################################################################################################

# Crear la tabla de inputs dentro del frame de grid
labels = ['EB', 'WB', 'NB', 'SB']
entries = {}

# Mostrar los nombres de las direcciones en lugar de los índices en las filas
for i, label in enumerate(labels):
    tk.Label(frame_grid, text=label, font=("Arial", 12)).grid(row=0, column=i+1)  # Usar frame_grid para los títulos de las columnas (orientaciones)

Addresses = Addresses[:-1]
# Aquí iteramos sobre las direcciones (Addresses) en lugar de los índices
for j, address in enumerate(Addresses):
    tk.Label(frame_grid, text=address, font=("Arial", 10)).grid(row=j+1, column=0)  # Nombres de las direcciones como filas
    for i, label in enumerate(labels):
        entry = tk.Entry(frame_grid)  # Crear un campo de entrada por cada orientación (EB, WB, NB, SB)
        entry.grid(row=j+1, column=i+1)
        if label not in entries:
            entries[label] = []
        entries[label].append(entry)


########################################################################################################
########## PARTE4: Convertir la tabla a pandas y modificar los archivos con verificación
########################################################################################################

def procesar_archivos():
    # Convertimos los inputs de la tabla a un DataFrame de pandas
    data = {col: [entry.get() for entry in entries[col]] for col in entries}
    df = pd.DataFrame(data)

    # Recorremos todos los archivos .txt en la carpeta seleccionada
    for archivo_txt in archivos:
        ruta_completa = os.path.join(folder_path, archivo_txt)

        with open(ruta_completa, 'r') as file:
            contenido = file.read()  # Leemos todo el contenido original del archivo

        modificado = False  # Bandera para saber si el archivo fue modificado

        # Iteramos sobre cada columna (EB, WB, NB, SB)
        for col in df.columns:
            for idx, valor in df[col].items():
                if valor:  # Si la fila tiene algún dato ingresado
                    # Obtenemos las cadenas del diccionario para esa fila
                    inicio, fin = diccionario[idx]

                    # Verificación: Mostrar entre qué bloques estamos buscando
                    print(f"Buscando entre: '{inicio}' y '{fin}' para el valor '{valor}' en la columna '{col}'.")

                    # Buscamos el bloque entre las cadenas de inicio y fin
                    bloque_patron = re.escape(inicio) + "(.*?)" + re.escape(fin)
                    bloques = re.findall(bloque_patron, contenido, re.DOTALL)

                    for bloque in bloques:
                        # Verificación: mostrar el bloque encontrado
                        print(f"Bloque encontrado: {bloque.strip()}")

                        # Verificar si el valor ingresado por el usuario está en el bloque
                        if valor in bloque:
                            nuevo_bloque = bloque.replace(valor, col)  # Reemplazo solo el valor por la columna
                            contenido = contenido.replace(bloque, nuevo_bloque)  # Actualizamos el contenido total
                            print(f"Reemplazado '{valor}' por '{col}' en el archivo {archivo_txt}.")
                            modificado = True  # Marcamos que el archivo ha sido modificado

        # Si el archivo fue modificado, lo guardamos con un nuevo nombre
        if modificado:
            nombre_nuevo = archivo_txt.replace(".txt", "_actualizado.txt")
            ruta_nueva = os.path.join(folder_path, nombre_nuevo)

            with open(ruta_nueva, 'w') as file:
                file.write(contenido)  # Guardamos el contenido modificado
            print(f"Archivo guardado como: {nombre_nuevo}")

    messagebox.showinfo("Éxito", "Todos los archivos han sido procesados y guardados correctamente con el sufijo '_actualizado'.")
    root.quit()  # Cierra la ventana de Tkinter después de procesar todos los archivos

# Crear el botón para procesar los archivos dentro del frame de pack
btn_procesar = tk.Button(frame_pack, text="Procesar Archivos", command=procesar_archivos)
btn_procesar.pack(pady=10)

root.mainloop()
