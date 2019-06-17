
from sqlalchemy.orm import defer
from .entities.Digesto import Norma, Archivo

class DigestoModelLocal():

    @classmethod
    def obtener_norma(cls, session, nid):
        return session.query(Norma).filter(Norma.id == nid).options(defer('archivo.contenido')).one_or_none()

    @classmethod
    def obtener_normas(cls, session, desde, hasta):
        return session.query(Norma).filter(Norma.fecha >= desde, Norma.fecha <= hasta).options(defer('archivo.contenido')).all()


    @classmethod
    def obtener_archivo(cls, session, aid):
        return session.query(Archivo).filter(Archivo.id == aid).options(defer('contenido')).one_or_none()