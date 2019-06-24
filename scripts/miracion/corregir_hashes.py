"""
    chequea el hash del archivo a ver si es el md5 correcto. en caso controario lo actualiza en la base.
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
        for archivo in archivos:
            try:
                logging.info(f'controlando hash de {archivo.nombre}')
                contenido = archivo.contenido
                contenido_binario = base64.b64decode(contenido.encode())
                hash_ = md5sum(contenido_binario)

                if archivo.hash_ != hash_:
                    logging.info(f'hash incorrecto {archivo.hash_}, actualizando en la base a {hash_}')
                    archivo.hash_ = hash_
                    session.commit()

            except Exception as e:
                logging.exception(e)
