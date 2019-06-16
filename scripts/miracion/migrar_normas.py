import logging
logging.getLogger().setLevel(logging.DEBUG)

import logging
import sys
import os
import json
import uuid
import base64
import datetime
import re

from sqlalchemy.orm import defer
from sqlalchemy import extract

from digesto.model import obtener_session
from digesto.model.entities.Digesto import Archivo, Norma, TipoNorma, Emisor, RelacionNorma, TipoRelacionNorma
import psycopg2

if __name__ == '__main__':

    host = os.environ['OLD_DB_HOST']
    port = os.environ['OLD_DB_PORT']
    database = os.environ['OLD_DB_DATABASE']
    user = os.environ['OLD_DB_USER']
    password = os.environ['OLD_DB_PASSWORD']
    
    con = psycopg2.connect(f"host='{host}' port='{port}' dbname='{database}' user='{user}' password='{password}'")
    try:
        cur = con.cursor()
        """ obtengo los datos de las normas """
        cur.execute('select numero, extracto, fecha, nombre_original, path, t.descripcion, e.descripcion from norma inner join tipo_norma t on tipo_id = t.id inner join emisor e on emisor_id = e.id')
        normas = [
            {
                'numero': n[0],
                'extracto': n[1],
                'fecha': n[2],
                'nombre_original': n[3],
                'path': n[4],
                'tipo': n[5],
                'emisor': n[6]
            } 
            for n in cur
        ]

        """ obtengo las relaciones entre normas """
        cur.execute('select a.numero, b.numero as numero_destino, c.descripcion from norma a inner join norma b on a.norma_id = b.id inner join tipo_relacion_normas c on a.tipo_relacion_normas_id = c.id where a.norma_id is not null')
        relaciones = [
            {
                'origen': n[0],
                'destino': n[1],
                'tipo': n[2]
            }
            for n in cur
        ]

    finally:
        con.close()


    """
        chequeo que todos los archivos existan en la base de destino.
        si existen y no tienen nombre, lo actualizo.
        lo armo un poquito mas elavorado para que solo actualice los que faltan
    """
    with obtener_session() as session:
        ''' genero un indice de archivos sin nombre por path '''
        logging.info('obteniendo los archivos que no tienen nombre')
        q = session.query(Archivo).filter(Archivo.nombre == '').options(defer('contenido'))
        archivos_a_actualizar = {}
        for a in q.all():
            archivos_a_actualizar[a.path] = a
        paths = list(archivos_a_actualizar.keys())
        logging.info(f"se encontraron {len(paths)} archivos sin nombre")

        ''' selecciono las normas que contienen esos paths '''
        normas_afectadas = [n for n in normas if n['path'] in paths]
        logging.info(f'hace falta actualizar {len(normas_afectadas)} archivos')

        ''' actualizo los archivos que tienen los paths iguales a las normas seleccionadas '''
        for n in normas_afectadas:
            i = n['path']
            archivos_a_actualizar[i].nombre = n['nombre_original']
            session.commit()


    """
        proceso los números de las normas para que estén correctos
        ya le saco los caracteres que les pusieron antes de los números para solucionar las falencias del sistema
    """
    formato = re.compile(r".*?(\d+)-.*")
    for n in normas:
        try:
            n['numero'] = n['numero'].replace('/','-')
            m = formato.match(n['numero'])
            if not m:
                n['numero_corregido'] = int(n['numero'])
            else:
                numero = int(m.group(1))
                n['numero_corregido'] = numero

        except Exception as e:
            ''' no debería pero seguro algún número no cumple el formato '''
            logging.exception(e)
            logging.warn(n)

    """
        Inserto las normas que no existan en la base
        corrijo los números para el modelo correo. un número se puede repetir en distintos tipos de normas.
    """
    with obtener_session() as session:
        for n in normas:
            ano = n['fecha'].year
            tipo_id = session.query(TipoNorma.id).filter(TipoNorma.tipo == n['tipo']).one_or_none()

            if session.query(Norma).filter(Norma.numero == n['numero_corregido'], extract('year',Norma.fecha) == ano, Norma.tipo_id == tipo_id).count() <= 0:
                try:
                    logging.info(f"agregando norma {n['numero']}")

                    archivo_id = session.query(Archivo.id).filter(Archivo.path == n['path']).one_or_none()
                    emisor_id = session.query(Emisor.id).filter(Emisor.nombre == n['emisor']).one_or_none()

                    norma = Norma()
                    norma.id = str(uuid.uuid4())
                    norma.created = datetime.datetime.utcnow()
                    norma.numero = n['numero_corregido']
                    norma.fecha = n['fecha']
                    norma.extracto = n['extracto']
                    norma.visible = True
                    norma.archivo_id = archivo_id
                    norma.emisor_id = emisor_id
                    norma.tipo_id = tipo_id
                    session.add(norma)
                    session.commit()

                except Exception as e:
                    logging.exception(e)


    for r in relaciones:
        logging.info(r)