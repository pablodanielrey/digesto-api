
import logging
import datetime
from dateutil.parser import parse
import base64
import io
from importlib_metadata import version


"""
    /////////////////////////
    inicializo warden para consultar los permisos
"""
import os
VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']

client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']

from warden.sdk.warden import Warden
warden_url = os.environ['WARDEN_API_URL']
warden = Warden(OIDC_URL, warden_url, client_id, client_secret, verify=VERIFY_SSL)
"""
    //////////////////////
"""

NORMAS_CREATE = 'urn:digesto:normas:read'
NORMAS_UPDATE = 'urn:digesto:normas:update'
NORMAS_DELETE = 'urn:digesto:normas:delete'


from flask import Blueprint, request, jsonify, send_file

from digesto.model import obtener_session

from digesto.model.DigestoModelGoogle import DigestoModelGoogle
from digesto.model.DigestoModelLocal import DigestoModelLocal
from digesto.model.DigestoModel import DigestoModel

bp = Blueprint('digesto', __name__, url_prefix='/digesto/api/v1.0')

@bp.route('/version', methods=['GET'])
def obtener_version():
    return jsonify({'status':200, 'response':version('digesto-api')})

@bp.route('/register', methods=['GET'])
def registrar_permisos():
    try:
        tk = ''
        datos = warden.register_system_perms(tk, 'digesto-api', permisos=[
            NORMAS_CREATE,
            NORMAS_DELETE,
            NORMAS_UPDATE
        ])
        if not datos:
            raise Exception('no se pudieron registrar los permisos')
        return jsonify({'status':200, 'data':datos})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})    

@bp.route('/tipo', methods=['GET'])
def obtener_tipos_de_normativas():
    try:
        with obtener_session() as session:
            tipos = DigestoModelLocal.obtener_tipos_de_norma(session)
            resultado = [
                {
                    'id': e.id,
                    'tipo': e.tipo
                }
                for e in tipos
            ]
            return jsonify({'status':200,'tipos':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/emisor', methods=['GET'])
def obtener_emisores():
    try:
        with obtener_session() as session:
            emisores = DigestoModelLocal.obtener_emisores(session)
            resultado = [
                {
                    'id': e.id,
                    'nombre': e.nombre
                }
                for e in emisores
            ]
            return jsonify({'status':200,'emisores':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})

"""
    solo para chequear de forma intermedia los usuarios que permiten acceso a modificar
"""
def _chequear_usuarios_digesto(uid):
    """
        por ahora chequeo los uids de los usuarios.
        bb559acd-2908-4c17-a309-4b517da3d0ce - betiana galle
        03ed8dc9-f43f-4f78-b013-40e2f4fa90f5 - fabiana puebla
        77979435-b43f-4c8b-91a9-5a84ecb46261 - graciela ganduglia
        853cd3dd-739c-4423-a88e-4fe722209fc7 - julio ciappa
        55cbbfe4-d8ec-40ce-9bd3-8e9d285a2781 - araceli mangano
        ef596bd6-eec8-4215-a344-b9b3fb5b8044 - martin ferrari
        4f097a2e-fa62-487f-bfe7-142ccf6f9a01 - nicolas colombo
        e4a72493-e13f-4c86-8620-8723701013f8 - martin pietro battista
        3209c066-c2a6-4e57-be3d-4dac0483dc90 - gabriela bauer
        89d88b81-fbc0-48fa-badb-d32854d3d93a - pablo rey
    """
    uids = [
        'bb559acd-2908-4c17-a309-4b517da3d0ce',
        '03ed8dc9-f43f-4f78-b013-40e2f4fa90f5',
        '77979435-b43f-4c8b-91a9-5a84ecb46261',
        '853cd3dd-739c-4423-a88e-4fe722209fc7',
        '55cbbfe4-d8ec-40ce-9bd3-8e9d285a2781',
        'ef596bd6-eec8-4215-a344-b9b3fb5b8044',
        '4f097a2e-fa62-487f-bfe7-142ccf6f9a01',
        'e4a72493-e13f-4c86-8620-8723701013f8',
        '3209c066-c2a6-4e57-be3d-4dac0483dc90',
        '89d88b81-fbc0-48fa-badb-d32854d3d93a'
    ]
    return uid in uids


@bp.route('/google/sinc', methods=['GET'])
def actualizar_archivos_faltantes_de_google():
    try:
        with obtener_session() as session:
            archivos = DigestoModelLocal.obtener_archivos(session)
            generados = DigestoModelGoogle.actualizar_sincronizados_desde_google(session, archivos)
            session.commit()
            return jsonify({'status':200, 'response': generados})

    except Exception as e:
        logging.exception(e)
        return jsonify({'status':500, 'response': str(e)})    

@bp.route('/google/upload', methods=['GET'])
def subir_normas_faltantes_a_google():
    try:
        with obtener_session() as session:
            response = DigestoModelGoogle.subir_archivos_no_sincronizados(session)
            session.commit()
            return jsonify({'status':200, 'response':response})

    except Exception as e:
        logging.exception(e)
        return jsonify({'status':500, 'response': str(e)})

@bp.route('/norma', methods=['POST'])
def subir_norma():
    (token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    uid = tkdata['sub']
    if not _chequear_usuarios_digesto(uid):
        return ('No tiene permisos para realizar esta acción', 403)
    
    try:
        data = request.json
        
        norma = {
            'numero': int(data['numero']),
            #'extracto': data['extracto'],
            'fecha': parse(data['fecha']),
            'tipo': data['tipo'],
            'emisor': data['emisor'],
            'visible': data['visible']
        }

        parchivo = data['archivo']
        if not parchivo['type'] or parchivo['type'] != 'application/pdf':
            raise Exception('no se permite archivos sin tipo o que no sean pdf')

        archivo = {
            'contenido': parchivo['contenido'],
            'nombre': parchivo['name'],
            'tipo': parchivo['type']
        }

        with obtener_session() as session:
            (norma_id, archivo_id) = DigestoModel.subir_norma(session, norma, archivo, creador=uid)
            session.commit()

        return jsonify({'status':200, 'response': {'norma': norma_id, 'archivo':archivo_id}})

    except Exception as e:
        logging.exception(e)
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/norma/<nid>', methods=['PUT'])
def actualizar_norma(nid):
    (token,tkdata) = warden._require_valid_token()
    """
        TODO: usar este codigo cuando se implemente la nueva versión de warden
    if not warden.has_permissions(token, permisos=[NORMAS_UPDATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    uid = tkdata['sub']
    if not _chequear_usuarios_digesto(uid):
        return ('No tiene permisos para realizar esta acción', 403)

    try:
        data = request.json
        visible = data['visible']
        with obtener_session() as session:
            nid = DigestoModelLocal.actualizar_norma(session, nid, visible)
            session.commit()

        return jsonify({'status':200, 'response': nid})


    except Exception as e:
        logging.exception(e)
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/norma/<nid>', methods=['GET'])
def obtener_norma(nid):
    with obtener_session() as session:
        n = DigestoModelLocal.obtener_norma(session, nid)

        if not n.visible:
            """ chequeo para ver si tiene permiso para ver las no visibles """
            (token,tkdata) = warden._require_valid_token()
            if token and tkdata:
                uid = tkdata['sub']
                if not _chequear_usuarios_digesto(uid):
                    return ('No tiene permisos para realizar esta acción', 403)
            else:
                return ('No tiene permisos para realizar esta acción', 403)

        norma = {
            'id': n.id,
            'numero':n.numero,
            'creada': n.created.isoformat() if n.created else None,
            'modificada': n.modified.isoformat() if n.modified else None,
            'fecha': _convertir_a_aware_utc(n.fecha) if n.fecha else None,
            'extracto': n.extracto,
            'tipo': n.tipo.tipo,
            'emisor': n.emisor.nombre,
            'archivo_id': n.archivo_id,
            'creador_id': n.creador_id,
            'visible': n.visible
        }
        return jsonify({'status':200, 'norma':norma})


def _convertir_a_aware_utc(date):
    """
        TODO: horrible hack!!! ahora se asume que es timezone -3
    """
    hora = datetime.time(3)
    return datetime.datetime.combine(date, hora)


@bp.route('/norma', methods=['GET'])
def obtener_normas():
    sdesde = request.args.get('desde')
    desde = parse(sdesde) if sdesde else datetime.datetime.now()  - datetime.timedelta(days=30)

    shasta = request.args.get('hasta')
    hasta = parse(shasta) if shasta else datetime.datetime.now()

    ''' visible == None --> retorna todas las normas independeintemente si son visibles o no '''
    visible = None
    estado = request.args.get('estado', None)
    if estado:
        ''' pendientes '''
        if 'P' in estado:
            visible = False

        ''' aprobadas '''
        if 'A' in estado:
            visible = True

    texto = request.args.get('texto', None)

    """ chequeo para ver si tiene permiso para ver las no visibles """
    (token,tkdata) = warden._require_valid_token()
    if token and tkdata:
        uid = tkdata['sub']
        if not _chequear_usuarios_digesto(uid):
            visible = True
    else:
        visible = True

    with obtener_session() as session:
        normativas = DigestoModel.obtener_normas(session, desde, hasta, visible, texto)
        resultado = [
            {
                'id': n.id,
                'numero':n.numero, 
                'fecha':_convertir_a_aware_utc(n.fecha) if n.fecha else None,
                'creada':n.created.isoformat() if n.created else None,
                'modificada':n.modified.isoformat() if n.modified else None,
                'emisor': n.emisor.nombre,
                'tipo': n.tipo.tipo,
                'archivo_id': n.archivo_id,
                'creador_id': n.creador_id,
                'visible': n.visible
            }
            for n in normativas ]

        return jsonify({'status':200,'normas':resultado})

@bp.route('/metadatos', methods=['GET'])
def obtener_metadatos():
    with obtener_session() as session:
        m = DigestoModelLocal.obtener_metadatos(session)
        r = {
            'numero_norma': m['numero_norma'],
            'cantidad': m['total']
        }
        return jsonify({'status':200, 'data':r})

@bp.route('/archivo/<aid>', methods=['GET'])
def obtener_archivo(aid):
    with obtener_session() as session:
        archivo = DigestoModelLocal.obtener_archivo(session, aid)
        contenido = archivo.contenido
        bs = base64.b64decode(contenido.encode())
        return send_file(io.BytesIO(bs), attachment_filename=archivo.nombre, mimetype=archivo.tipo)
