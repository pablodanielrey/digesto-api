import logging
from flask import Blueprint, request, jsonify

from digesto.model.Utils import save_file
from digesto.model.DigestoModel import DigestoModel


bp = Blueprint('digesto', __name__, url_prefix='/digesto/api/v1.0')

@bp.route('/norma', methods=['POST'])
def subir_norma():
    data = request.json
    archivo = data['archivo']
    norma = save_file(archivo)
    DigestoModel.subir_normativa(norma)
    
    return jsonify({'status':200, 'data':norma})
