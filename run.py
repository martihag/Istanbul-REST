from eve import Eve
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
from eve.auth import BasicAuth

class MyBasicAuth(BasicAuth):
  def check_auth(self, username, password, allowed_roles, resource, method):
    return username == 'admin' and password == 'secret'

if __name__ == '__main__':
    #app = Eve(auth=MyBasicAuth)
    app = Eve()
    Bootstrap(app)
    app.register_blueprint(eve_docs, url_prefix='/docs')

    app.run(host='0.0.0.0', debug=True)
