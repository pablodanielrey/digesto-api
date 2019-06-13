"""
    https://developers.google.com/drive/api/v3/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/

    upload:
    https://youtu.be/-7YH6rdR-tk


"""


from .GoogleAuthApi import GAuthApis

class DigestoModel:

    SCOPES = [
        #'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive'
    ]

    @classmethod
    def _get_google_services(cls):
        service = GAuthApis.getService(version='v3', api='drive', scopes=cls.SCOPES, username='sistemas@econo.unlp.edu.ar')
        return service

    @classmethod
    def _get_parent(cls, service):
        res = service.files().list(q="name = 'digesto' and mimeType = 'application/vnd.google-apps.folder'").execute()
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
        res = []
        for normativa in faltantes:
            meta = {
                'name': normativa['name'],
                'parents': [parent]
            }
            service.files().emptyTrash().execute()
            r = service.files().create(body=meta, media_body=normativa['filename']).execute()
            res.append(r)
        return res

    @classmethod
    def _filtrar_existentes(cls, service, parent, normativas):
        #res = service.files().list(q=f"mimeType = 'application/pdf' and '{parent}' in parents").execute()
        req = service.files().list(q=f"mimeType = 'application/pdf'")
        res = req.execute()
        filtered = []
        while res:
            uploaded = res.get('files',[])
            names = [u['name'] for u in uploaded]
            filtered.extend(filter(lambda n: n['name'] not in names, normativas))
            res = service.files().list_next(previous_request=req, previous_response=res)
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
        results = service.files().list(q=f"fullText contains '{termino}'").execute()
        files = results.get('files',[])
        return files            