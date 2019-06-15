import os
import base64
import hashlib

UPLOAD = os.environ.get('UPLOAD_DIR','/tmp')

def md5sum(content):
    return hashlib.md5(content).hexdigest()

def save_file(archivo):
    b64content = archivo['contenido']
    content = base64.b64decode(b64content)
    md5s = md5sum(content)
    #name = f"{md5s}.pdf"
    name = archivo['name']
    ud = f"{UPLOAD}/{name}"

    with open(ud,'wb') as file:
        file.write(content)
    
    norma = {
        'name': archivo['name'],
        'md5': md5s,
        'filename': ud
    }
    return norma
