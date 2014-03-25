# MongoDB setup
MONGO_HOST = 'localhost'
#MONGO_HOST = '158.38.43.92'
MONGO_PORT = 27017
#MONGO_USERNAME = 'user'
#MONGO_PASSWORD = 'user'
MONGO_DBNAME = 'istanbulApp'

#SERVER_NAME = '127.0.0.1:5000'


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later-
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
EMBEDDING = True

accounts = {
    #many-to-many with activities
    'item_title': 'account',

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'user'
    },

    'schema': {
    #Real name, or user name?
        'user': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
        },
        'firstname' : {
            'type': 'string',
            'minlength': 1,
            'maxlength': 20,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 20,
        },
        'password': {
            'type': 'string',
            'minlength': 5,
            'required': True,
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

activities = {
    #many-to-many with accounts
    #one-to-many with comments
    #many-to-one with locations
    'item_title': 'activity',

    'schema': {
        'name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 35,
        },
        'rating': {
            'type': 'number'
        },
        'attending': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'accounts'
                }
            }
        },
        'comments': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'comments'
                }
            }
        },
        'location': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'locations'
            }
        }
    }
}

comments = {
    #many-to-one with activities

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

locations = {

    'item_title': 'location',

    'schema': {
        'coordinates': {
            'type': 'dict',
            'schema': {
                'lon': {'type': 'float'},
                'lat': {'type': 'float'}
            },
        }
    }
}

DOMAIN = {
    'accounts': accounts,
    'activities': activities,
    'comments': comments,
    'locations': locations,
}
