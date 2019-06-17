
from sqlalchemy.orm import defer
from .entities.Digesto import Norma, Archivo

class DigestoModelLocal():

    @classmethod
    def obtener_normas(cls, session):
        return session.query(Norma).options(defer('archivo.contenido')).limit(10)