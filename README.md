# Change_Of_Orientations

## Descripción

Este proyecto está diseñado para modificar archivos `.txt` generados por el equipo de transporte en Wooster. Estos archivos contienen información sobre el movimiento en intersecciones, pero a menudo presentan orientaciones no estándar (desplazadas). La finalidad del proyecto es ajustar estas orientaciones y estandarizarlas a las direcciones correctas: **East Bound (EB)**, **West Bound (WB)**, **North Bound (NB)** y **South Bound (SB)**.

El código permite al usuario ingresar correcciones para las orientaciones desplazadas y aplicar estos cambios a los archivos de forma automática, asegurando que las direcciones estén correctamente alineadas en los reportes de tráfico.

### Características principales:

1. **Selección de Directorio:**
   - El usuario puede seleccionar un directorio que contenga los archivos `.txt` generados por el equipo de transporte. El programa procesará todos los archivos en el directorio seleccionado.
   
2. **Identificación de Bloques de Texto:**
   - El programa identifica bloques específicos de texto dentro de los archivos `.txt`, correspondientes a las direcciones que se deben modificar. Estas direcciones suelen estar desplazadas o no alineadas con las convenciones estándar de **EB**, **WB**, **NB** y **SB**.

3. **Ingreso de Valores de Corrección:**
   - A través de una interfaz gráfica, el usuario puede ingresar valores en una tabla que representa las orientaciones. Estas correcciones son aplicadas a los archivos `.txt` para estandarizar las direcciones según las convenciones del tráfico.

4. **Modificación y Guardado de Archivos:**
   - Una vez ingresadas las correcciones, el programa procesa los archivos `.txt`, busca los bloques de texto entre las direcciones identificadas, y realiza los cambios necesarios en las orientaciones. Los archivos modificados se guardan con un sufijo `_actualizado.txt` para mantener los originales intactos.

## Uso

### Requisitos:

- **Python**
- Librerías necesarias:
  - `tkinter` para la interfaz gráfica.
  - `pandas` para manejar la tabla de inputs.
  - `re` para manejar las expresiones regulares.


