from . import app


@app.route('/healthcheck')
def healthcheck():
    return 'I am working'
