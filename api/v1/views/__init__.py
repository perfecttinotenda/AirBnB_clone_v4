#!/usr/bin/python3
'''This contains the blueprint for our API.'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''This blueprint is for our AirBnB clone v3 API.'''


from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places_amenities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *