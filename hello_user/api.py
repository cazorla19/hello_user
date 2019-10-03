# pylint: disable=R0201, C0111

import os
from datetime import datetime, date
import redis
from flask import Flask, request, abort
from flask_restful import Resource, Api

APP = Flask(__name__)
API = Api(APP)

REDIS_HOST = os.getenv("REDIS_HOST")
RS = redis.StrictRedis(REDIS_HOST, decode_responses=True)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class HealthCheck(Resource):
    def redis_available(self):
        try:
            RS.client_list()
        except redis.ConnectionError:
            return False
        return True

    def get(self):
        ## By default we return 200
        status_code = 200

        ## Dependency #1: Redis
        redis_ok = self.redis_available()
        if redis_ok:
            redis_status = {"redis": "available"}
        else:
            redis_status = {"redis": "unavailable"}
            status_code = 503

        return {'status': {'app': 'available', 'dependencies': [redis_status]}}, status_code

class HelloUser(Resource):
    def is_bday_valid(self, bday):
        today_date = date.today()
        bday_origin = datetime.strptime(bday, "%Y-%m-%d").date()
        if bday_origin > today_date:
            return False
        return True

    def days_to_bday_left(self, bday):
        today_date = date.today()
        bday_date = datetime.strptime(bday, "%Y-%m-%d").date().replace(year=today_date.year)
        # Set the birthday up to the next year if it's already gone at this one
        if bday_date < today_date:
            bday_date = bday_date.replace(year=today_date.year+1)
        diff = bday_date - today_date
        return diff.days

    def get(self, user_id):
        user_bady = RS.get(user_id)
        days_left = self.days_to_bday_left(user_bady)
        if not days_left:
            return {"message": "Hello, %s! Happy birthday!" % (user_id)}
        return {"message": "Hello, %s! Your birthday is in %s day(s)" % (user_id, days_left)}

    def put(self, user_id):
        # Requirement #1: User name must contain only letters
        if not user_id.isalpha():
            abort(400, 'User name must contain only letters')

        try:
            user_bady = request.json['dateOfBirth']
        except KeyError:
            abort(400, "Request payload doesn\'t have 'dateOfBirth' field")
        except TypeError:
            abort(400, "Invalid JSON")

        # Requirement #2: Date of birth must be a date before the today date
        if not self.is_bday_valid(user_bady):
            abort(400, 'Date of birth must be a date before the today date')

        RS.set(user_id, user_bady)
        return ('', 204)

API.add_resource(HelloWorld, '/')
API.add_resource(HealthCheck, '/health')
API.add_resource(HelloUser, '/hello/<string:user_id>')

if __name__ == '__main__':
    if not REDIS_HOST:
        raise RuntimeError('Environment variable $REDIS_HOST is not set')

    APP.run(host='0.0.0.0')
