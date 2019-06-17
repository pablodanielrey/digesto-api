
import logging
import os
import json
import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from digesto.model.entities import Base

class Archivo(Base):
    __tablename__ = 'archivos'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())

    nombre = Column(String())
    path = Column(String())
    hash_ = Column(String())
    tipo = Column(String())
    contenido = Column(Text())


class TipoNorma(Base):
    __tablename__ = 'tipo_norma'

    id = Column(String(), primary_key=True, default=None)
    tipo = Column(String())


class Norma(Base):
    __tablename__ = 'normas'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())

    numero = Column(Integer())
    fecha = Column(Date())
    extracto = Column(String())

    visible = Column(Boolean(), default=False)

    tipo_id = Column(String(), ForeignKey('tipo_norma.id'))
    tipo = relationship('TipoNorma')

    emisor_id = Column(String(), ForeignKey('emisores.id'))
    emisor = relationship('Emisor')

    archivo_id = Column(String(), ForeignKey('archivos.id'))
    archivo = relationship('Archivo')

    def __json__(self):
        return self.__dict__


class Emisor(Base):
    __tablename__ = 'emisores'

    id = Column(String(), primary_key=True, default=None)
    nombre = Column(String())


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

