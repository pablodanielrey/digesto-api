import uuid
import base64
import datetime
import re

from sqlalchemy.orm import defer

from .Utils import md5sum
from .entities.Digesto import Norma, Archivo, Emisor, TipoNorma


class DigestoModelLocal():

    extension = re.compile(r".*(\.[a-zA-Z]+)")

    @classmethod
    def crear_norma(cls, session, norma, archivo_id):
        en = norma['emisor']
        eid = session.query(Emisor.id).filter(Emisor.nombre == en).one()

        tt = norma['tipo']
        tid = session.query(TipoNorma).filter(TipoNorma.tipo == tt).one()

        nid = str(uuid.uuid4())
        n = Norma()
        n.id = nid
        n.numero = norma['numero']
        n.extracto = norma['extracto']
        n.fecha = norma['fecha']
        n.tipo_id = tid
        n.emisor_id = eid
        n.visible = norma['visible']
        n.archivo_id = archivo_id

        session.add(n)
        return nid

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
    def crear_archivo_binario(cls, session, nombre, contenido:bytes, mime):
        b64 = base64.b64encode(contenido).decode('utf8')
        md5s = md5sum(contenido)
        return cls._crear_archivo(session, nombre, b64, md5s, mime)

    @classmethod
    def crear_archivo_b64(cls, session, nombre, contenido, mime):
        b64 = contenido
        # ver si va el .encode
        md5s = md5sum(base64.b64decode(contenido).encode())         
        return cls._crear_archivo(session, nombre, b64, md5s, mime)

    @classmethod
    def _crear_archivo(cls, session, nombre, b64, md5s, mime):
        aid = session.query(Archivo.id).filter(Archivo.nombre == nombre, Archivo.hash_ == md5s).one_or_none()
        if not aid:
            ext = cls.extension.match(nombre).group(1)
            a = Archivo()
            a.id = str(uuid.uuid4())
            a.created = datetime.datetime.utcnow()
            a.nombre = nombre
            a.path = f"{md5s}{ext}"
            a.hash_ = md5s
            a.contenido = b64
            a.tipo = mime
            session.add(a)
            return a.id
        else:
            return aid     

