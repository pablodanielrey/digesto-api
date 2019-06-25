import datetime

from .DigestoModelLocal import DigestoModelLocal
from .DigestoModelGoogle import DigestoModelGoogle

class DigestoModel:

    @classmethod
    def obtener_normas(cls, session, desde, hasta, visible=None, texto=None):

        if texto:
            ''' busco el texto en google '''
            normativas_google = DigestoModelGoogle.buscar_normativa(texto)
            if len(normativas_google) <= 0:
                return []

            """ ya que traigo todas las de google,. en la base busco por todas las normativas """
            desde = datetime.datetime.utcnow() - datetime.timedelta(days=99999)
            normas = DigestoModelLocal.obtener_normas(session, desde, hasta, visible, normativas_google)
            return normas

        normas = DigestoModelLocal.obtener_normas(session, desde, hasta, visible)
        return normas

    @classmethod
    def subir_norma(cls, session, norma, archivo):
        nombre = archivo['nombre']
        mime = archivo['tipo']
        b64 = archivo['contenido']

        archivo = DigestoModelLocal.crear_archivo_b64(session, nombre, b64, mime)
        norma_id = DigestoModelLocal.crear_norma(session, norma, archivo.id)
        res = DigestoModelGoogle.subir_archivo(archivo)
                       
        return (norma_id, archivo.id)
