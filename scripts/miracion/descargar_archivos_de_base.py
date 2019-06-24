"""
    descarga todos los archivos de la base y los deja en una carpeta
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

from sqlalchemy.orm import defer

from digesto.model.Utils import md5sum
from digesto.model import obtener_session
from digesto.model.entities.Digesto import Archivo



if __name__ == '__main__':

    path = sys.argv[1]
    logging.info(f"Descargando archivos dentro de la carpeta : {path}")

    with obtener_session() as session:
        try:
            archivos = session.query(Archivo).options(defer('contenido')).all()
            for archivo in archivos:
                nombre = archivo.nombre
                path_completo = f"{path}/{nombre}"
                if not os.path.isfile(path_completo):
                    logging.info(f"escribiendo archivo {nombre}")
                    contenido = archivo.contenido
                    contenido_binario = base64.b64decode(contenido.encode())
                    
                    with open(path_completo, 'wb') as f:
                        f.write(contenido_binario)

        except Exception as e:
            logging.exception(e)
