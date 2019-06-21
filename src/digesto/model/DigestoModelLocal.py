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
    def obtener_metadatos(cls, session):
        total = session.query(Norma).count()
        norma = session.query(Norma).order_by(Norma.fecha.desc()).first()
        numero = norma.numero if norma != None else 0

        datos = {
            'numero_norma':numero + 1,
            'total': total
        }
        return datos

    @classmethod
    def obtener_tipos_de_norma(cls, session):
        return session.query(TipoNorma).all()

    @classmethod
    def obtener_emisores(cls, session):
        return session.query(Emisor).all()

    @classmethod
    def actualizar_norma(cls, session, nid, visible):
        norma = session.query(Norma).filter(Norma.id == nid).one()
        norma.visible = visible
        norma.modified = datetime.datetime.utcnow()
        return norma.id

    @classmethod
    def crear_norma(cls, session, norma, archivo_id):
        nid = str(uuid.uuid4())
        n = Norma()
        n.created = datetime.datetime.utcnow()
        n.id = nid
        n.numero = norma['numero']
        #n.extracto = norma['extracto']
        n.fecha = norma['fecha']
        n.tipo_id = norma['tipo']
        n.emisor_id = norma['emisor']
        n.visible = norma['visible']
        n.archivo_id = archivo_id

        session.add(n)
        return nid

    @classmethod
    def obtener_norma(cls, session, nid):
        return session.query(Norma).filter(Norma.id == nid).options(defer('archivo.contenido')).one_or_none()

    @classmethod
    def obtener_normas(cls, session, desde, hasta, visible=None, paths=None):
        q = session.query(Norma).filter(Norma.fecha >= desde, Norma.fecha <= hasta)
        if visible:
            q = q.filter(Norma.visible == True)
        
        if not visible and visible == False:
            q = q.filter(Norma.visible == False)
            
        if paths:
            q = q.join(Archivo).filter(Archivo.path.in_(tuple(paths)))

        return q.order_by(Norma.created.desc()).options(defer('archivo.contenido')).all()


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
        md5s = md5sum(base64.b64decode(contenido))         
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

