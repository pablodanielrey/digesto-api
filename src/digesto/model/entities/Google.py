import logging
import os
import json
import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from digesto.model.entities import Base

class Sincronizacion(Base):
    __tablename__ = 'sincronizacion'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())

    archivo_id = Column(String(), ForeignKey('archivos.id'))
    archivo = relationship('Archivo')

    respuesta = Column(String())