import os

# MongoDB setup

if os.environ.get('PORT'):
    # We're hosted on Heroku!  Use the MongoHQ sandbox as our backend.
    MONGO_HOST = 'lennon.mongohq.com'
    MONGO_PORT = 10022
    MONGO_USERNAME = 'instabulApp'
    MONGO_PASSWORD = 'instabulApp'
    MONGO_DBNAME = 'app24248294'

    # also, correctly set the API entry point
    SERVER_NAME = 'instabul.herokuapp.com'

else:
    MONGO_HOST = 'localhost'
    #MONGO_HOST = '158.38.43.92'
    MONGO_PORT = 27017
    #MONGO_USERNAME = 'user'
    #MONGO_PASSWORD = 'user'
    MONGO_DBNAME = 'istanbulApp'

    #SERVER_NAME = 'localhost:5000'


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later-
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
EMBEDDING = True
X_DOMAINS = '*'
X_HEADERS = ['authorization', 'content-type']
URL_PROTOCOL = 'http'
IF_MATCH = False

accounts = {

    'public_methods': ['POST'],
    #'resource_methods': ['POST'],
    #'allowed_roles': ['admin'],
    #'allowed_item_roles': ['admin', 'app'],
    #many-to-many with activities
    'item_title': 'account',

    #'authentication': BCryptAuth(),

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    'cache_control': '',
    'cache_expires': 0,

    #'allowed_roles': ['admin', 'app'],

    'schema': {
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'minlength': 3,
            'required': True,
        },
        'roles': {
          'type': 'list',
          'allowed': ['app', 'admin'],
          'required': False,
        }
    }
}

users = {
    #many-to-many with activities
    'item_title': 'user',
    'public_methods': ['POST'],

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'user'
    },

    'schema': {
        'user' : {
            'type': 'string',
            'required': True,
            'unique': True,
            'data_relation': {
                'resource': 'accounts',
                'field': 'username'
            }
        },
        'firstname' : {
            'type': 'string',
            'minlength': 1,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
        },
        'description': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 149,
        },
        'attending': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'activities'
                }
            }
        },
        'favorites': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'activities'
                }
            }
        }
    }
}


comments = {
    #many-to-one with activities
    #'authentication': MyBasicAuth(),

    'item_title': 'comment',

    'schema': {
        'text_area': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 900,
        },
        'activity': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'activities'
            }
        }
    }
}

routes = {

    'item_title': 'route',

    'schema': {
        'name': {
            'type': 'string',
            'maxlength': 100,
        },
        'description': {
            'type': 'string',
            'maxlength': 900,
        },
        'start': {
            'type': 'string',
            'maxlength': 500,
        },
        'end': {
            'type': 'string',
            'maxlength': 500,
        },
        'waypoints': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'maxlength': 500,
            },
        }
    }
}

locations = {

    'item_title': 'location',

    'schema': {
        'details': {
            'type': 'string',
            'maxlength': 900,
        },
        'location': {
            'type': 'string',
            'maxlength': 500,
        },
        'rating' : {
            'type': 'float',
        },
        'category': {
            'type': 'string',
            'maxlength': 30,
        },
        'name': {
            'type': 'string',
            'maxlength': 50,
        },
        'coordinates': {
            'type': 'dict',
            'schema': {
                'lat': {'type': 'float'},
                'lng': {'type': 'float'}
            },
        }
    }
}

DOMAIN = {
    'accounts': accounts,
    'users': users,
    'comments': comments,
    'locations': locations,
    'routes': routes,
}
