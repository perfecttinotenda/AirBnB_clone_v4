#!/usr/bin/python3
'''This will contain the users view for our API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    '''This will get a user per given id or all of the users.'''
    if user_id:
        user = storage.get(User, user_id)
        if user:
            obj = user.to_dict()
            if 'places' in obj:
                del obj['places']
            if 'reviews' in obj:
                del obj['reviews']
            return jsonify(obj)
        raise NotFound()
    all_users = storage.all(User).values()
    users = []
    for user in all_users:
        obj = user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        users.append(obj)
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    '''This will remove a user per given id.'''
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/users', methods=['POST'])
def add_user():
    '''This wil add a new user.'''
    data = {}
    try:
        data = request.get_json()
    except Exception:
        data = None
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')
    user = User(**data)
    user.save()
    obj = user.to_dict()
    if 'places' in obj:
        del obj['places']
    if 'reviews' in obj:
        del obj['reviews']
    return jsonify(obj), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''This will update the user per given id.'''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    user = storage.get(User, user_id)
    if user:
        data = {}
        try:
            data = request.get_json()
        except Exception:
            data = None
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in xkeys:
                setattr(user, key, value)
        user.save()
        obj = user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        return jsonify(obj), 200
    raise NotFound()