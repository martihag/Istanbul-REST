import bcrypt
from eve import Eve
from flask import request
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
from eve.auth import TokenAuth, BasicAuth, requires_auth
import random
import string

class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == 'admin' and password == 'secret'

class BCryptAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if resource == 'accounts' and username == 'superuser' and password == 'password':
            return True
        else:
            #use Eve's own db driver; no additional connections/resources are used
            print(allowed_roles, resource, method)
            accounts = app.data.driver.db['accounts']
            lookup = {'username': username}
            print("BCrypt called")
            if allowed_roles:
                lookup['roles'] = {'$in': allowed_roles}
            account = accounts.find_one(lookup)
            return account and \
                bcrypt.hashpw(password, account['password']) == account['password']

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
#app = Eve(auth=BCryptAuth)
app = Eve(auth=RolesAuth)

def post_get_callback(resource, request, payload):
    print('A GET on the', resource, 'was just performed!', payload)

def hash_pwd(items):
    #Hooks the passwords and encrypts them before storage
    for item in items:
        password = item['password']
        item['password'] = bcrypt.hashpw(password, bcrypt.gensalt())

def add_token(documents):
    for document in documents:
        document['token'] = (''.join(random.choice(string.ascii_uppercase)
                              for x in range(10)))

@app.route('/login')
@requires_auth('login')
def login():
    #print(request.headers)
    return "Hello?"


if __name__ == '__main__':

    Bootstrap(app)

    #Hooks
    app.on_post_GET_login += post_get_callback
    app.on_insert_accounts += hash_pwd
    app.on_insert_accounts += add_token

    app.register_blueprint(eve_docs, url_prefix='/docs')

    app.run(host='0.0.0.0', debug=True)
