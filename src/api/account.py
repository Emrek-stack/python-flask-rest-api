from flask import Flask, request
from flask_restful  import Resource, Api
# from app import api

# todos = {}

api = Api()

# @api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}