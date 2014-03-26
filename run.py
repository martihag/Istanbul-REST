import bcrypt
from eve import Eve
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
from eve.auth import BasicAuth

class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == 'admin' and password == 'secret'

class BCryptAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if resource == 'accounts':
            return username == 'superuser' and password == 'password'
        else:
            #use Eve's own db driver; no additional connections/resources are used
            accounts = app.data.driver.db['accounts']
            account = accounts.find_one({'username': username})
            return account and \
                bcrypt.hashpw(password, account['password']) == account['password']

def post_get_callback(resource, request, payload):
    print('A GET on the', resource, 'was just performed!', payload)

def pre_insert_accounts(items):
    #Hooks the passwords and encrypts them before storage
    for item in items:
        password = item['password']
        item['password'] = bcrypt.hashpw(password, bcrypt.gensalt())

if __name__ == '__main__':
    #app = Eve(auth=MyBasicAuth)
    #app = Eve(auth=BCryptAuth)

    app = Eve()
    Bootstrap(app)

    #Hooks
    #app.on_post_GET += post_get_callback
    app.on_insert_accounts+=pre_insert_accounts

    app.register_blueprint(eve_docs, url_prefix='/docs')

    app.run(host='0.0.0.0', debug=True)
