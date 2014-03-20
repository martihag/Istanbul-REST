from eve import Eve
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs

if __name__ == '__main__':
    app = Eve()
    Bootstrap(app)
    app.register_blueprint(eve_docs, url_prefix='/docs')

    app.run(host='0.0.0.0', debug=True)
