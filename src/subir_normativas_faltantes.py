
import logging
logging.getLogger().setLevel(logging.DEBUG)

from digesto.model.DigestoModel import DigestoModel

#logging.info(DigestoModel.buscar_normativa('algo'))

#for i in DigestoModel.listar_normativas():
#    logging.info(i['name'])

import sys
import os
import json

if __name__ == '__main__':

    path = sys.argv[1]
    print(f'subiendo normas desde {path}')
    for (dirname, dirs, files) in os.walk(path):
        print(dirname)
        normativas = [
            {
                'name':f,
                'filename': '/'.join([dirname, f])
            } 
            for f in files
        ]
        try:
            res = DigestoModel.subir_normativas(normativas)
            with open('upload.json', 'w') as f:
                for r in res:
                    print(r)
                    f.write(json.dumps(r) + '\n')
        except Exception as e:
            logging.exception(e)