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

from sqlalchemy.orm import defer

from digesto.model.Utils import md5sum
from digesto.model import obtener_session
from digesto.model.DigestoModelGoogle import DigestoModelGoogle
from digesto.model.entities.Digesto import Archivo



if __name__ == '__main__':

    with obtener_session() as session:
        archivos = session.query(Archivo).options(defer('contenido')).all()
        logging.info(f"{len(archivos)} encontrados")
        DigestoModelGoogle.subir_archivos(archivos)
