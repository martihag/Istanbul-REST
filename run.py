from eve import Eve
from flask import request
from flask.ext.bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash
from eve_docs import eve_docs
from eve.auth import TokenAuth, BasicAuth, requires_auth
import os

class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == 'admin' and password == 'secret'

class BCryptAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if username == 'superuser' and password == 'password':
            return True
        else:
            #use Eve's own db driver; no additional connections/resources are used
            print(allowed_roles, resource, method)
            accounts = app.data.driver.db['accounts']
            lookup = {'username': username}
            if allowed_roles:
                #only retreive a user if his roles match 'allowed_roles'
                lookup['roles'] = {'$in': allowed_roles}
            account = accounts.find_one(lookup)
            return account and \
                check_password_hash(account['password'], password)
                #bcrypt.hashpw(password, account['password']) == account['password']

class RolesAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        print(token)
        accounts = app.data.driver.db['accounts']
        lookup = {'token' : token}
        if allowed_roles:
            #only retrieve a user if his roles match ''allowed_roles''
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)
        return account

#app = Eve(auth=MyBasicAuth)
app = Eve(auth=BCryptAuth)
#app = Eve(auth=RolesAuth)

def post_get_callback(resource, request, payload):
    print('A GET on the', resource, 'was just performed!', payload)

def hash_pwd(items):
    #Hooks the passwords and encrypts them before storage
    for item in items:
        password = item['password']
        #item['password'] = bcrypt.hashpw(password, bcrypt.gensalt())
        item['password'] = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

#adds a role from this side to pervent user from creating admin accounts
def add_role(documents):
    for document in documents:
        document['roles'] = 'app'


@app.route('/auth')
@requires_auth('auth')
def auth():
    #print(request.headers)
    return "Authenticated."


if __name__ == '__main__':

    Bootstrap(app)

    #Hooks
    #app.on_post_GET_login += post_get_callback
    app.on_insert_accounts += hash_pwd
    #app.on_insert_accounts += add_token
    app.on_insert_accounts += add_role

    app.register_blueprint(eve_docs, url_prefix='/docs')

    if 'PORT' in os.environ:
        port = int(os.environ.get('PORT'))
        # use '0.0.0.0' to ensure your REST API is reachable from all your
        # network (and not only your computer).
        host = '0.0.0.0'
        debug = False
    else:
        port = 5000
        host = '127.0.0.1'
        debug = True

    app.run(host=host, port=port, debug=debug)
