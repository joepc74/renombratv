#! /root/.venv/bin/python3

import guessit, logging, sys, os
import configparser
import tmdbsimple as tmdb
from pick import pick


if '--log' in sys.argv:
    logging.basicConfig(level=logging.INFO)
elif '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def elige_serie(opciones,archivo):
    options=[
        obj['name']
        for obj in opciones
        ]
    option, index = pick(options=options, title=f"Elige la serie correcta para {archivo}:")
    # print(option, index)
    return opciones[index]['id']

def recorre_carpeta(ruta_carpeta):
    # recorre la carpeta buscardo archivos de series y los renombra
    for root, dirs, files in os.walk(ruta_carpeta):
        for file in files:
            if file.lower().endswith(('.mkv', '.mp4', '.avi', '.mov', '.wmv')):
                ruta_completa = os.path.join(root, file)
                logging.info(f"Analizando archivo: {file}")
                # try:
                info = guessit.guessit(file)
                logging.info(f"Información extraída: {info}")
                if info.get('type', '').lower() in ['episode', 'tv show','series']:
                    search = tmdb.Search()
                    response = search.tv(language='es-ES',query=info.get('title'))
                    if response['results']==[]:
                        logging.info(f"No se encontraron resultados para: {info.get('title')}")
                        continue
                    if len(response['results']) > 1:
                        logging.info(f"Se encontraron múltiples resultados para: {info.get('title')}")
                        idserie=elige_serie(response['results'],file)
                    else:
                        logging.info(f"Se encontraron un único resultado para: {info.get('title')}")
                        idserie=search.results[0]['id']
                    detalles=tmdb.TV_Seasons(tv_id=idserie, season_number=info.get('season', 0))
                    detalles=detalles.info(language='es-ES')
                    episodio=detalles.get('episodes', [])[info.get('episode', 1)-1]
                    logging.info(f"Episodio encontrado: {episodio.get('name', 'Unknown Episode')}")
                    titulo=episodio.get('name', 'Unknown Episode')
                    nuevo_nombre = f"{info.get('title', 'Unknown Title')} - {info.get('season', 0):02d}x{info.get('episode', 0):02d} - {titulo}.{file.split('.')[-1]}"
                    nueva_ruta=os.path.join(carpeta_destino,info.get('title', 'Unknown Title'))
                    if not os.path.exists(nueva_ruta):
                        os.makedirs(nueva_ruta)
                    nueva_ruta_archivo = os.path.join(nueva_ruta, nuevo_nombre)
                    os.rename(ruta_completa, nueva_ruta_archivo)
                    print(f"Renombrado: '{file}' a '{nueva_ruta_archivo}'")
                # except Exception as e:
                #     print(f"Error al procesar '{file}': {e}")

def cargar_configuracion():
    ruta = os.path.abspath(__file__)

    # Comprobar si es un enlace simbólico
    if os.path.islink(ruta):
        logging.info("El script se está ejecutando desde un enlace simbólico.")
        ruta=os.path.realpath(ruta)

    logging.info(f"Cargando configuración desde: {os.path.join(os.path.dirname(ruta),'renombratv.ini')}")
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(ruta),'renombratv.ini'))
    return config

if __name__ == "__main__":
    config=cargar_configuracion()
    tmdb.API_KEY=config.get('General', 'tmdbapikey')
    carpeta_destino=config.get('General', 'carpeta_destino')
    recorre_carpeta('.')