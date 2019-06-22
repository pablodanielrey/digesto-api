"""
    https://developers.google.com/drive/api/v3/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/

    upload:
    https://youtu.be/-7YH6rdR-tk


"""

import os
import logging
import base64

from .GoogleAuthApi import GAuthApis
from apiclient.http import MediaInMemoryUpload, MediaFileUpload

from .Utils import obtener_path, obtener_path_completo_local

"""
codigo de ejmplo para el archivo en memoria.
media = MediaInMemoryUpload(file_blob, mime_type, resumable=True)
file = drive.files().create(body={'name': filename},media_body=media)
file.execute()
"""

class DigestoModelGoogle:

    SCOPES = [
        #'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive'
    ]

    PARENT_DRIVE = os.environ['PARENT_DRIVE']

    @classmethod
    def _get_google_services(cls):
        service = GAuthApis.getService(version='v3', api='drive', scopes=cls.SCOPES, username='sistemas@econo.unlp.edu.ar')
        return service

    @classmethod
    def _get_parent(cls, service):
        res = service.files().list(q=f"name = '{cls.PARENT_DRIVE}' and mimeType = 'application/vnd.google-apps.folder'").execute()
        parents = res.get('files',[])
        if not parents:
            return None
        return parents[0]['id']

    @classmethod
    def subir_archivo(cls, archivo):
        service = cls._get_google_services()
        res = cls._subir_archivos(service, [archivo])
        if len(res) <= 0:
            return None
        return res[0]
        
    @classmethod
    def subir_archivos(cls, archivos):
        service = cls._get_google_services()
        res = cls._subir_archivos(service, archivos)
        return res


    @classmethod
    def _subir_archivos(cls, service, archivos=[]):
        parent = cls._get_parent(service)

        faltantes = cls._filtrar_existentes(service, parent, archivos)
        logging.debug(f'faltan {len(faltantes)} archivos por subir')

        res = []
        for datos in faltantes:
            path = datos['path']
            archivo = datos['archivo']

            meta = {
                'name': path,
                'parents': [parent]
            }
            logging.debug(f"subiendo archivo : {path}")
            
            """
            este codigo es para subirlo usando el disco como intermediario

            path_ = obtener_path_completo_local(datos['path'])
            with open(path_, 'wb') as f:
                contenido = datos['archivo'].contenido
                contenido_binario = base64.b64encode(contenido).decode('utf8')
                f.write(contenido_binario)

            media = MediaFileUpload(path_,
                        mimetype=datos['archivo'].tipo,
                        resumable=True)
            """
            
            contenido = archivo.contenido
            contenido_binario = base64.b64decode(contenido.encode())
            media = MediaInMemoryUpload(contenido_binario,
                            mimetype=archivo.tipo,
                            resumable=True)
            r = service.files().create(body=meta, media_body=media).execute()
            logging.debug(f"respuesta : {r}")
            res.append(r)
        return res

    @classmethod
    def _filtrar_existentes(cls, service, parent, archivos=[]):
        req = service.files().list(q=f"mimeType = 'application/pdf' and '{parent}' in parents and trashed = false",
                                   fields='nextPageToken, files(id, name)')
        #req = service.files().list(q=f"mimeType = 'application/pdf'")
        res = req.execute()
        names = []
        while res:
            uploaded = res.get('files',[])
            names.extend([u['name'] for u in uploaded])
            req = service.files().list_next(previous_request=req, previous_response=res)
            if not req:
                break
            res = req.execute()
        filtered = list(filter(lambda a: a['path'] not in names, [{'path': obtener_path(a), 'archivo': a} for a in archivos]))
        return filtered

    @classmethod
    def listar_normativas(cls):
        service = cls._get_google_services()
        results = service.files().list().execute()
        files = results.get('files',[])
        return files                    

    @classmethod
    def buscar_normativa(cls, termino):
        service = cls._get_google_services()
        results = service.files().list(q=f"fullText contains '{termino}'", fields="files(id,name,md5Checksum)").execute()
        files = results.get('files',[])
        return files            