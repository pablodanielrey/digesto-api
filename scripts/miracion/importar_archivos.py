"""
    obtiene todos los archivos de una carpeta y los importa dentro de la tabla de Archivos de la base.
    calculando el hash determinado para cada archivo.
    el contenido del archivo queda dentro de la base codificado en base64
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
    logging.debug(f'subiendo normas desde {path}')

    archivos = []
    for (dirname, dirs, files) in os.walk(path):
        for f in files:
            archivos.append({
                'nombre': f,
                'archivo': '/'.join([dirname, f])
            })

    with obtener_session() as session:
        logging.info(f'{len(archivos)} archivos a importar en la base')
        count = 0
        for a in archivos:
            count = count + 1
            logging.info(f"importando {count} - {a['nombre']}")
            with open(a['archivo'],'rb') as f:
                path = a['nombre']
                contenido = f.read()
                md5s = md5sum(contenido)
                b64c = base64.b64encode(contenido)

                if session.query(Archivo).filter(Archivo.path == path, Archivo.hash_ == md5s).count() <= 0:
                    a = Archivo()
                    a.id = str(uuid.uuid4())
                    a.created = datetime.datetime.utcnow()
                    a.nombre = path
                    a.path = path
                    a.hash_ = md5s
                    a.contenido = b64c
                    a.tipo = 'application/pdf' if '.pdf' in path else ''
                    session.add(a)
                    session.commit()
                else:
                    logging.info('ya existe asi que no se importa')
        
        
        
