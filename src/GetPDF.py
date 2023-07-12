import argparse
from PyPDF2 import PdfReader
import re
import json
import camelot
import ghostscript
import pandas as pd

def extraer_numero_titulo(nombre_archivo):
    with open(nombre_archivo, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)

        numeros_titulos = []

        # Patrón para extraer el número del título
        patron_numero_titulo = r'PRIMER OFRECIMIENTO NÚMERO (\d+)'

        for pagina in pdf_reader.pages:
            contenido = pagina.extract_text()

            # Buscar el número del título en cada página
            resultado = re.search(patron_numero_titulo, contenido)
            if resultado:
                numero_titulo = resultado.group(1)
                numeros_titulos.append(numero_titulo)

        return numeros_titulos


def guardar_json(datos, nombre_archivo):
    with open(nombre_archivo, 'w') as json_file:
        json.dump(datos, json_file)

def extraer_frase_parrafo(nombre_archivo):
    with open(nombre_archivo, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)

        frases_parrafos = []

        # Patrón para extraer una frase en un párrafo
        patron_frase_parrafo = r'ubicadas en el recinto de almacenamiento ([\w\s.,-]+)'

        for pagina in pdf_reader.pages:
            contenido = pagina.extract_text()

            # Buscar la frase en un párrafo en cada página
            resultado = re.search(patron_frase_parrafo, contenido)
            if resultado:
                frase_parrafo = resultado.group(1)
                frases_parrafos.append(frase_parrafo)

        return frases_parrafos

def extraer_tabla_completa(nombre_archivo):
    tablas = camelot.read_pdf(nombre_archivo, pages='all')

    tablas_completas = []

    for tabla in tablas:
        if tabla.df is not None:
            tablas_completas.append(tabla.df)

    if tablas_completas:
        tabla_completa = pd.concat(tablas_completas, ignore_index=True)
        tabla_json = tabla_completa.to_json(orient="records")
        return tabla_json
    else:
        return None

def guardar_json(datos, nombre_archivo):
    with open(nombre_archivo, 'w') as json_file:
        json.dump(datos, json_file)

# Configuración de argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Extracción de información de un archivo PDF')
parser.add_argument('archivo_pdf', type=str, help='Ruta al archivo PDF')

args = parser.parse_args()

# Extraer el nombre del archivo PDF desde los argumentos
nombre_archivo_pdf = args.archivo_pdf

# Extraer el nombre del archivo PDF desde los argumentos
nombre_archivo_pdf = args.archivo_pdf

numeros_titulos = extraer_numero_titulo(nombre_archivo_pdf)
frases_parrafos = extraer_frase_parrafo(nombre_archivo_pdf)
tabla_completa = extraer_tabla_completa(nombre_archivo_pdf)

datos_extraidos = {
    'numeros_titulos': numeros_titulos,
    'frases_parrafos': frases_parrafos,
    'tabla_completa': tabla_completa
}

nombre_archivo_json = 'datos.json'
with open(nombre_archivo_json, 'w', encoding='utf-8') as json_file:
    json.dump(datos_extraidos, json_file, ensure_ascii=False)

guardar_json(datos_extraidos, nombre_archivo_json)
