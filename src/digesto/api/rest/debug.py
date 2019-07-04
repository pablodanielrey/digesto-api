import ptvsd
ptvsd.enable_attach(address=('0.0.0.0', 11304))
ptvsd.wait_for_attach()

from digesto.api.rest.wsgi import app
app.run(host='0.0.0.0', port='11302', debug=False)
