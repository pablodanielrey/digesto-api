"""
    https://developers.google.com/drive/api/v3/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/

    upload:
    https://youtu.be/-7YH6rdR-tk


"""

import logging
from .GoogleAuthApi import GAuthApis

class DigestoModel:

    SCOPES = [
        #'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive'
    ]

    #PARENT_DRIVE = 'digesto'
    PARENT_DRIVE = 'prueba'

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
    def subir_normativa(cls, normativa):
        service = cls._get_google_services()
        res = cls._subir_normativas(service, [normativa])
        if len(res) <= 0:
            return None
        return res[0]
        
    @classmethod
    def subir_normativas(cls, normativas):
        service = cls._get_google_services()
        res = cls._subir_normativas(service, normativas)
        return res

    @classmethod
    def _subir_normativas(cls, service, normativas=[]):
        """
            normativas = [{
                'name': string,
                'filename': string,
                'md5': string
            }]
        """
        parent = cls._get_parent(service)
        faltantes = cls._filtrar_existentes(service, parent, normativas)
        logging.debug(f'faltan {len(faltantes)} normativas por subir')
        #service.files().emptyTrash().execute()
        res = []
        for normativa in faltantes:
            meta = {
                'name': normativa['name'],
                'parents': [parent]
            }
            logging.debug(f"subiendo archivo : {meta['name']}")
            r = service.files().create(body=meta, media_body=normativa['filename']).execute()
            logging.debug(f"respuesta : {r}")
            res.append(r)
        return res

    @classmethod
    def _filtrar_existentes(cls, service, parent, normativas):
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
        filtered = list(filter(lambda n: n['name'] not in names, normativas))
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