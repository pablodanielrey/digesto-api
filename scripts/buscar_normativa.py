
import logging
logging.getLogger().setLevel(logging.DEBUG)

from digesto.model.DigestoModel import DigestoModel

import sys
import os
import json

if __name__ == '__main__':

    termino = sys.argv[1]
    logging.debug(f'buscando normativas que contengan {termino}')
    try:
        archivos = DigestoModel.buscar_normativa(termino)
        for a in archivos:
            logging.info(f"{a['name']} - {a['md5Checksum']}")
    except Exception as e:
        logging.exception(e)