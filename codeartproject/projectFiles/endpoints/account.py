from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from databasedetails import db, Account, Event, Internship
import json
import uuid
from endpoints.verify_auth import verify_auth, live_tokens
from werkzeug.security import check_password_hash, generate_password_hash
app_api = None


def create_api(app):
    app_api = Api(app)
    app_api.add_resource(AccountInfo, "/accountinfo")
    app_api.add_resource(AccountModify, "/accountmodify")
    app_api.add_resource(Login, "/account/login")
    app_api.add_resource(AccountCreate, "/accountcreate")

class Login(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()
            
            user = Account.query.filter_by( email=( str( args['email'] ).lower() ) ).first()
            print(user.password)
            if user:
                if check_password_hash(user.password, args['password']):
                    user_id = user.id
                    auth_token = str( uuid.uuid4() )
                    live_tokens.append( (auth_token, user_id) )
                    return {'id':user_id, 'auth':auth_token}, 200
            return 'Bad email or password', 401
        except Exception as exe:
            print(exe)
            return {"msg":"Bad Request"}, 400 


class AccountModify(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('is_admin', type=bool)
    parser.add_argument('is_student', type=bool)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('graduation', type=str)
    parser.add_argument('birthday', type=int)
    parser.add_argument('gender', type=str)
    parser.add_argument('attributes', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('auth', type=str)

    def put(self):
        print(request.data)

        try:
            args = self.parser.parse_args()
            if not verify_auth(args['auth'], args['id']):
                return {"msg": "Invalid id or Auth Token", "success": False}, 400
            
            created_id = uuid.uuid4()
            mod_acc = Account.query.get(args["id"])

            mod_acc.is_admin = args["is_admin"]
            mod_acc.is_student = args["is_student"]
            mod_acc.first_name = args["first_name"]
            mod_acc.last_name = args["last_name"]
            mod_acc.email = str( args["email"] ).lower()
            mod_acc.graduation = args["graduation"]
            mod_acc.birthday = args["birthday"]
            mod_acc.gender = args["gender"]
            mod_acc.attributes = args["attributes"]
            mod_acc.password = generate_password_hash(args["password"], method='SHA512')

            db.session.commit()
            return {"success": True}, 201
        except Exception as exe:
            print(exe)
            return {"success": False}, 400 


class AccountInfo(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            acc = Account.query.get( str( args["id"] ) )

            if not acc:
                return {"msg": "Invalid Account"}, 400
            
            return {"is_admin": acc.is_admin, "is_student": acc.is_student, "first_name": acc.first_name, "last_name": acc.last_name, 
            "email": acc.email, "graduation": acc.graduation, "birthday": acc.birthday, "gender": acc.gender, "attributes": acc.attributes, 
            "success": True}, 200 
            
        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Request", "success": False}, 400


class AccountCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('is_admin', type=bool)
    parser.add_argument('is_student', type=bool)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('graduation', type=str)
    parser.add_argument('birthday', type=int)
    parser.add_argument('gender', type=str)
    parser.add_argument('attributes', type=str)
    parser.add_argument('password', type=str)

    def post(self):
        print(request.data)

        try:
            created_id = uuid.uuid4()
            args = self.parser.parse_args()
            print("Attempting to create account: ", str(args["email"]).lower() )

            create_acc = Account(id=str(created_id), is_admin=args["is_admin"], is_student=args["is_student"], 
                first_name=args["first_name"], last_name=args["last_name"], email=str(args["email"]).lower(), graduation=args["graduation"], 
                birthday=args["birthday"], gender=args["gender"], attributes=args["attributes"], password=generate_password_hash(args["password"], 
                method='SHA512') )
            
            db.session.add(create_acc)
            db.session.commit()
            return {"success": True}, 201
        except Exception as exe:
            print(exe)
            return {"success": False}, 400 