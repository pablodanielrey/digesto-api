import uuid
import base64
import datetime
import re

from sqlalchemy.orm import defer

from .Utils import md5sum
from .entities.Digesto import Norma, Archivo


class DigestoModelLocal():

    extension = re.compile(r".*(\.[a-zA-Z]+)")

    @classmethod
    def obtener_norma(cls, session, nid):
        return session.query(Norma).filter(Norma.id == nid).options(defer('archivo.contenido')).one_or_none()

    @classmethod
    def obtener_normas(cls, session, desde, hasta):
        return session.query(Norma).filter(Norma.fecha >= desde, Norma.fecha <= hasta).options(defer('archivo.contenido')).all()


    @classmethod
    def obtener_archivo(cls, session, aid):
        return session.query(Archivo).filter(Archivo.id == aid).options(defer('contenido')).one_or_none()

    @classmethod
    def subir_archivo(cls, session, nombre, contenido:bytes, mime):
        ext = cls.extension.match(nombre).group(1)
        b64c = base64.b64encode(contenido).decode('utf8')
        md5s = md5sum(contenido)
        aid = session.query(Archivo.id).filter(Archivo.nombre == nombre, Archivo.hash_ == md5s).one_or_none()
        if not aid:
            a = Archivo()
            a.id = str(uuid.uuid4())
            a.created = datetime.datetime.utcnow()
            a.nombre = nombre
            a.path = f"{md5s}{ext}"
            a.hash_ = md5s
            a.contenido = b64c
            a.tipo = mime
            session.add(a)
            return a.id
        else:
            return aid

