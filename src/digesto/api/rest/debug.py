import sys
ip = sys.argv[1]

import ptvsd
ptvsd.enable_attach("supersecreto", address = (ip, 11304))
ptvsd.wait_for_attach()

from .wsgi import app
app.run(host='0.0.0.0', port='11302', debug=False)
