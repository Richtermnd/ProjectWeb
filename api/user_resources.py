import datetime

from flask_restful import Resource, reqparse
from flask import jsonify, Response
import json

from data import db_session, models
from .tools import not_found_factory, correct_date_format


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('surname', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('password', required=True, type=str)
parser.add_argument('birthdate', required=True, type=str)
parser.add_argument('contact_email', required=False, type=str)
parser.add_argument('about', required=False, type=str)
parser.add_argument('address', required=False, type=str)

exist_check = not_found_factory(models.User)

rules = ('-messages', 
         '-files', 
         '-posts', 
         '-chats', 
         '-likes', 
         '-friends', 
         '-hashed_password',
         '-avatar')


class UserResources(Resource):
    def get(self, user_id):
        exist_check(user_id)
        with db_session.create_session() as session:
            try:
                user = session.get(models.User, user_id)
                return Response(json.dumps(user.to_dict(rules=rules)), status=200)
            except:
                return Response(status=500)

    def delete(self, user_id):
        exist_check(user_id)
        with db_session.create_session() as session:
            try:
                user = session.get(models.User, user_id)
                session.delete(user)
                session.commit()
                return Response(json.dumps({'success': 'OK'}), status=200)
            except:
                return Response(status=500)
    
    def put(self, user_id):
        exist_check(user_id)
        args = parser.parse_args()
        if not correct_date_format(args['birthdate']):
            return jsonify({'error': 'Bad Request'}), 400
        args['birthdate'] = datetime.datetime.strptime(args['birthdate'], '%Y-%m-%d')
        with db_session.create_session() as session:
            try:
                user = session.get(models.User, user_id)
                for key, value in args.items():
                    user.__setattr__(key, value)
                session.commit()
                return Response(json.dumps({'success': 'OK'}), status=200)
            except:
                return Response(json.dumps({'error': 'Bad Request'}), status=400)


class UserListResources(Resource):
    def get(self):
        with db_session.create_session() as session:
            try:
                users = session.query(models.User).all()
                users = {'users': [item.to_dict(rules=rules) for item in users]}
                return Response(json.dumps(users), status=200)
            except:
                return Response(status=500)

    def post(self):
        args = parser.parse_args()
        if not correct_date_format(args['birthdate']):
            return Response(json.dumps({'error': 'Wrong date format'}), status=400)
        args['birthdate'] = datetime.datetime.strptime(args['birthdate'], '%Y-%m-%d')
        with db_session.create_session() as session:
            try:
                user = models.User(**args)
                session.add(user)
                session.commit()
                return Response(json.dumps({'success': 'OK', 'user_id': user.id}), status=200)
            except:
                return Response(json.dumps({'error': 'Wrong data or non available Email'}), status=400)
