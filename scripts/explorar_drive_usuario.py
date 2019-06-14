
import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import os
import json

from digesto.model.GoogleAuthApi import GAuthApis

SCOPES = [
        #'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive'
    ]

def get_service(usuario):
    service = GAuthApis.getService(version='v3', api='drive', scopes=SCOPES, username=f'{usuario}@econo.unlp.edu.ar')
    return service    

def get_files(service):
    req = service.files().list()
    res = req.execute()
    names = []
    while res:
        files = res.get('files',[])
        names.extend([u['name'] for u in files])
        req = service.files().list_next(previous_request=req, previous_response=res)
        if not req:
            break
        res = req.execute()
    return names

if __name__ == '__main__':

    usuario = sys.argv[1]
    logging.debug(f'listando archivos de {usuario}')
    service = get_service(usuario)
    names = get_files(service)
    logging.info('los nombres de los archivos son : ')
    logging.info(names)
