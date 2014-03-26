# -*- coding: utf-8 -*-

import requests
import json
import random

ENTRY_POINT = 'http://127.0.0.1:5000'


def post_accounts():
    accounts = [
        {
            'username': 'johdo',
            'password': '123es',
        },
        {
            'username': 'serlo',
            'password': '123es',
        },
        {
            'username': 'magre',
            'password': '123es',
        },
        {
            'username': 'julred',
            'password': '123es',
        },
        {
            'username': 'anwhi',
            'password': '123es',
        },
    ]

    r = perform_post('accounts', json.dumps(accounts))
    print("'accounts' posted", r.status_code)

    valids = []
    if r.status_code == 201:
        response = r.json()
        for account in response:
            if account['_status'] == "OK":
                valids.append(account['_id'])

    return valids

def post_users():
    users = [
        {
            'firstname': 'John',
            'lastname': 'Doe',
            'user': 'johdo',
            'description': 'Lorem ipsum'
        },
        {
            'firstname': 'Serena',
            'lastname': 'Love',
            'user': 'serlo',
            'description': 'Lorem ipsum'
        },
        {
            'firstname': 'Mark',
            'lastname': 'Green',
            'user': 'magre',
            'description': 'Lorem ipsum'
        },
        {
            'firstname': 'Julia',
            'lastname': 'Red',
            'user': 'julred',
            'description': 'Lorem ipsum'
        },
        {
            'firstname': 'Anne',
            'lastname': 'White',
            'user': 'anwhi',
            'description': 'Lorem ipsum'
        },
    ]

    r = perform_post('users', json.dumps(users))
    print("'users' posted", r.status_code)

    valids = []
    if r.status_code == 201:
        response = r.json()
        for user in response:
            if user['_status'] == "OK":
                valids.append(user['_id'])

    return valids

def post_activities():
    activities = [
        {
            'name': 'Cat with a tie',
            'rating': 4
        },
        {
            'name': 'Swimming',
            'rating': 4
        },
        {
            'name': 'Jumping',
            'rating': 4
        },
    ]

    r = perform_post('activities', json.dumps(activities))
    print("'activities' posted", r.status_code)

    valids = []
    if r.status_code == 201:
        response = r.json()
        for account in response:
            if account['_status'] == "OK":
                valids.append(account['_id'])

    return valids

def patch_activity(id, data, etag):
    r = perform_update('activities/' + id, data, etag)
    print("'activities' updated", r.status_code, r.headers)


def perform_post(resource, data):
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint(resource), data, headers=headers)

def perform_update(resource, data, etag):
    headers = {'Content-Type': 'application/json','If-Match': ''+etag}
    return requests.patch(endpoint(resource), data, headers=headers)




def delete():
    r = perform_delete('accounts')
    print("'accounts' deleted", r.status_code)
    r = perform_delete('activities')
    print("'activities' deleted", r.status_code)
    r = perform_delete('locations')
    print("'locations' deleted", r.status_code)
    r = perform_delete('comments')
    print("'comments' deleted", r.status_code)


def perform_delete(resource):
    return requests.delete(endpoint(resource))


def endpoint(resource):
    return '%s/%s/' % (ENTRY_POINT, resource)


def get(resource):
    headers = {'Content-Type': 'application/json'}
    r = requests.get('http://127.0.0.1:5000/' + resource, headers=headers)
    return json.loads(r.text)

if __name__ == '__main__':
    delete()
    post_accounts()
    ids = post_users()
    r = post_activities()
    #print(ids[0])
    activities = get("activities")
    #print(activities['_items'][0]['_id'])
    #print(activities['_items'][0]['_etag'])
    attending = {'attending': [ids[0]]}

    patch_activity(activities['_items'][0]['_id'], json.dumps(attending), activities['_items'][0]['_etag'] )
    activities = get("activities/"+activities['_items'][0]['_id'])
    print(activities)

    attending_list = activities['attending']
    attending_list.append(ids[1])
    attending = {'attending': attending_list}
    print(attending)
    patch_activity(activities['_id'], json.dumps(attending), activities['_etag'] )
