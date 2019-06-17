
from sqlalchemy.orm import defer
from .entities.Digesto import Norma, Archivo

class DigestoModelLocal():

    @classmethod
    def obtener_normas(cls, session, desde, hasta):
        return session.query(Norma).filter(Norma.fecha >= desde, Norma.fecha <= hasta).options(defer('archivo.contenido')).all()