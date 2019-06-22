import os
import base64
import hashlib
import re

UPLOAD = os.environ.get('UPLOAD_DIR','/tmp')
extension = re.compile(r".*(\.[a-zA-Z]+)")

def md5sum(content):
    return hashlib.md5(content).hexdigest()

def save_file(archivo):
    b64content = archivo['contenido']
    content = base64.b64decode(b64content)
    md5s = md5sum(content)
    ud = f"{UPLOAD}/{md5s}"

    with open(ud,'wb') as file:
        file.write(content)
    
    norma = {
        'name': archivo['name'],
        'md5': md5s,
        'filename': ud,
        'mime': archivo['type']
    }
    return norma


def extraer_extension(nombre):
    ext = extension.match(nombre).group(1)
    return ext

def obtener_path(archivo):
    ext = extraer_extension(archivo.nombre)
    if not ext:
        raise Exception(f"{archivo.nombre} no tiene extension")
    path = f"{archivo.hash_}{ext}" 
    return path

def obtener_path_completo_local(path):
    return  f"{UPLOAD}/{path}"