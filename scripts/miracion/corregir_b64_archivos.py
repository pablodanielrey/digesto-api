"""
    corrige los base64 de los archivos ya migrados en la base.
    los lee de una carpeta y actualiza el contenido en la base, correctamente. 
    para manejar los casos donde se importo el contenido pero sin haberlo decodificado despues de realizado el base64.
    o sea se uso:
        b64c = base64.b64encode(contenido)

    en vez de :
        b64c = base64.b64encode(contenido).decode('utf8')

"""
import logging
logging.getLogger().setLevel(logging.DEBUG)

import logging
import sys
import os
import json
import uuid
import base64
import datetime

from digesto.model.Utils import md5sum
from digesto.model import obtener_session
from digesto.model.entities.Digesto import Archivo

if __name__ == '__main__':

    path = sys.argv[1]
    logging.debug(f'actualizando archivos desde {path}')

    with obtener_session() as session:

        for (dirname, dirs, files) in os.walk(path):
            for f in files:
                path = f
                fullpath = '/'.join([dirname, f])

                with open(fullpath,'rb') as archivo:
                    logging.info(f"leyendo y calculando {fullpath}")
                    contenido = archivo.read()
                    md5s = md5sum(contenido)
                    b64c = base64.b64encode(contenido).decode('utf8')

                    logging.info(f"actualizando {fullpath}")
                    # existen varios archivos con el mismo hash!!!
                    #sarchivo = session.query(Archivo).filter(Archivo.hash_ == md5s).one()
                    sarchivo = session.query(Archivo).filter(Archivo.path == path).one_or_none()
                    if sarchivo:
                        sarchivo.contenido = b64c
                        session.commit()           
