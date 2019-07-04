import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().propagate = True


from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.debug = False
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

from . import digesto
app.register_blueprint(digesto.bp)

app.route('/version', methods=['GET'])
def obtener_version():
    from importlib_metadata import version
    return jsonify({'status':200, 'response':version('digesto-api')})

