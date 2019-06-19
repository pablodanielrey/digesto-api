from .DigestoModelLocal import DigestoModelLocal
from .DigestoModelGoogle import DigestoModelGoogle

class DigestoModel:

    @classmethod
    def obtener_normas(cls, session, desde, hasta, visible=None, texto=None):
        ''' busco las normativas por los metadatos primero '''
        normativas = DigestoModelLocal.obtener_normas(session, desde, hasta, visible)

        if texto:
            ''' busco el texto en google '''
            normativas_google = DigestoModelGoogle.buscar_normativa(texto)
            if len(normativas_google) > 0:
                hashes = [n['md5Chechsum'] for n in normativas_google]
                normativas_ = [n for n in normativas if n.hash_ in hashes]
                normativas = normativas_

        return normativas

    @classmethod
    def subir_norma(cls, session, norma):
        pass