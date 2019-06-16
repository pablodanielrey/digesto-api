
import logging
import os
import json
import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey

from digesto.model.entities import Base

class Archivo(Base):
    __tablename__ = 'archivos'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())

    nombre = Column(String())
    hash_ = Column(String())
    tipo = Column(String())
    contenido = Column(Text())


class Norma(Base):
    __tablename__ = 'normas'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())

    numero = Column(String())
    extracto = Column(String())
    emisor = Column(String())
    visible = Column(Boolean())
    tipo = Column(String())
    fecha = Column(DateTime())
    
    archivo_id = Column(String(), ForeignKey('archivos.id'))

    def __json__(self):
        return self.__dict__


class TipoRelacionNorma(Base):
    __tablename__ = 'tipo_relacion'

    id = Column(String(), primary_key=True, default=None)
    tipo = Column(String())


class RelacionNorma(Base):
    __tablename__ = 'relacion_normas'

    id = Column(String(), primary_key=True, default=None)
    norma_id = Column(String(), ForeignKey('normas.id'))
    norma_afectada_id = Column(String(), ForeignKey('normas.id'))
    tipo_id = Column(String(), ForeignKey('tipo_relacion.id'))

