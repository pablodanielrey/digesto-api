import logging
import datetime
from dateutil.parser import parse
import base64
import io

from flask import Blueprint, request, jsonify, send_file

from digesto.model import obtener_session
from digesto.model.Utils import save_file
from digesto.model.DigestoModelGoogle import DigestoModelGoogle
from digesto.model.DigestoModelLocal import DigestoModelLocal

bp = Blueprint('digesto', __name__, url_prefix='/digesto/api/v1.0')

@bp.route('/norma', methods=['POST'])
def subir_norma():
    data = request.json
    
    visible = data['visible']
    norma = {
        'numero': int(data['numero']),
        'extracto': data['extracto'],
        'fecha': parse(data['fecha']),
        'tipo': data['tipo'],
        'emisor': data['emisor'],
        'visible': True if visible == 'true' else False
    }
    archivo = data['archivo']

    with obtener_session() as session:
        nombre = archivo['name']
        mime = archivo['type']
        b64 = archivo['contenido']
        archivo_id = DigestoModelLocal.crear_archivo_b64(session, nombre, b64, mime)
        norma_id = DigestoModelLocal.crear_norma(session, norma, archivo_id)
        session.commit()

    """ subo el archivo a google para full text search """
    anorma = save_file(archivo)
    DigestoModelGoogle.subir_normativa(anorma)

    return jsonify({'status':200, 'response': {'norma': norma_id, 'archivo':archivo_id}})

@bp.route('/norma/<nid>', methods=['GET'])
def obtener_norma(nid):
    with obtener_session() as session:
        n = DigestoModelLocal.obtener_norma(session, nid)
        norma = {
            'id': n.id,
            'numero':n.numero,
            'fecha': n.fecha,
            'extracto': n.extracto,
            'tipo': n.tipo.tipo,
            'emisor': n.emisor.nombre,
            'archivo_id': n.archivo_id
        }
        return jsonify(norma)

@bp.route('/norma', methods=['GET'])
def obtener_normas():
    sdesde = request.args.get('desde')
    desde = parse(sdesde) if sdesde else datetime.datetime.now()  - datetime.timedelta(days=30)

    shasta = request.args.get('hasta')
    hasta = parse(shasta) if shasta else datetime.datetime.now()

    with obtener_session() as session:
        normativas = DigestoModelLocal.obtener_normas(session, desde, hasta)
        resultado = [
            {
                'id': n.id,
                'numero':n.numero, 
                'fecha':n.fecha,
                'emisor': n.emisor.nombre,
                'tipo': n.tipo.tipo
            }
            for n in normativas ]

        return jsonify({'normas':resultado})

@bp.route('/archivo/<aid>', methods=['GET'])
def obtener_archivo(aid):
    with obtener_session() as session:
        archivo = DigestoModelLocal.obtener_archivo(session, aid)
        contenido = archivo.contenido
        bs = base64.b64decode(contenido.encode())
        return send_file(io.BytesIO(bs), attachment_filename=archivo.nombre, mimetype=archivo.tipo)
