import logging
import datetime
from dateutil.parser import parse
from flask import Blueprint, request, jsonify

from digesto.model import obtener_session
from digesto.model.Utils import save_file
from digesto.model.DigestoModelGoogle import DigestoModelGoogle
from digesto.model.DigestoModelLocal import DigestoModelLocal


bp = Blueprint('digesto', __name__, url_prefix='/digesto/api/v1.0')

@bp.route('/norma', methods=['POST'])
def subir_norma():
    data = request.json
    archivo = data['archivo']
    norma = save_file(archivo)
    DigestoModelGoogle.subir_normativa(norma)
    
    return jsonify({'status':200, 'data':norma})

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
                'numero':n.numero, 
                'fecha':n.fecha,
                'archivo_id': n.archivo_id
            }
            for n in normativas ]

        return jsonify({'normas':resultado})