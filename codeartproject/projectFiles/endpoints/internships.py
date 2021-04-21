from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from databasedetails import db, Account, Event, Internship
import json
import uuid
from endpoints.verify_auth import verify_auth, live_tokens

app_api = None

def create_api(app):
    app_api = Api(app)
    app_api.add_resource(InternInfo, "/interninfo")
    app_api.add_resource(InternModify, "/internmodify")
    app_api.add_resource(InternCreate, "/interncreate")
    app_api.add_resource(InternDelete, "/interndelete")
    
class InternModify(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('auth', type=str)
    parser.add_argument('location', type=str)
    parser.add_argument('company', type=str)
    parser.add_argument('role', type=str)
    parser.add_argument('link', type=str)
    parser.add_argument('start_datetime', type=str)
    parser.add_argument('end_datetime', type=str)
    parser.add_argument('details', type=str)
    parser.add_argument('intern_id', type=int)

    def put(self):

        try:
            args = self.parser.parse_args()
            if verify_auth(args['auth'], args['id']):

                internship = Internship.query.get(args["intern_id"])
                
                if internship:

                    internship.location = args["location"]
                    internship.company = args["company"]
                    internship.cost = args["cost"]
                    internship.role = args["role"]
                    internship.link = args["link"]
                    internship.start_datetime = args["start_datetime"]
                    internship.end_datetime = args["end_datetime"]
                    internship.details = args["details"]

                    db.session.commit()
                    return {"success": True}, 201
                else:
                    return {"msg":"Invalid Internship","success":False}, 400
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400

        except Exception as exe:
            print(exe)
            return {"success": False}, 400

class InternCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('auth', type=str)
    parser.add_argument('location', type=str)
    parser.add_argument('company', type=str)
    parser.add_argument('role', type=str)
    parser.add_argument('link', type=str)
    parser.add_argument('start_datetime', type=str)
    parser.add_argument('end_datetime', type=str)
    parser.add_argument('details', type=str)
    
    def post(self):
        print(request.data)

        try:
            created_id = uuid.uuid4()
            args = self.parser.parse_args()
            if verify_auth('auth', 'id'):

                string_uuid = str( uuid.uuid4() )
                half_len_of_string = ( len(string_uuid) )/2
                intern_id = int( string_uuid[:half_len_of_string] )

                acc = Account.query.get( int( args["id"] ) )
                if acc:
                    internship = Internship(id=intern_id, location=args["location"], company=args["company"], role=args["role"], 
                    link=args["link"], start_datetime=args["start_datetime"], end_datetime=args["end_datetime"], details=args["details"])

                    db.session.add(internship)
                    db.session.commit()

                    return {"success": True}, 201
                else:
                    return {"msg":"No Account","success":False}, 400
            else:
                return {"msg":"Invalid ID or Auth Token","success":False}, 400
        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Internship Parameters", "success": False}, 400

class InternInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            parser.add_argument('auth', type=str)
            parser.add_argument('intern_id', type=int)
            args = parser.parse_args()

            if verify_auth('auth', 'id'):
                internship = Internship.query.get( args["intern_id"] )
                if internship:
                    print("Internship Exists")

                    return {"location": internship.location, "company": internship.company, "role": internship.role, 
                    "link": internship.link, "start_datetime": internship.start_datetime, "end_datetime": internship.end_datetime, 
                    "details": internship.details, "success": True}, 200
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400

        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Internship ID", "success": False}, 400

class InternDelete(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('auth', type=str)
        parser.add_argument('intern_id', type=int)

        try:
            args = parser.parse_args()
            if verify_auth('auth', 'id'):
                acc = Account.query.get( int( args["id"] ) )
                if acc:
                    internship = Internship.query.get(args["intern_id"])
                    if internship:
                        db.session.delete(internship)
                        db.session.commit()
                        return {"msg":"Internship Deleted","success":True}, 200
                else:
                    return {"msg":"No Account","success":False}, 400
            else:
                return {"msg":"Internship Could Not Be Deleted","success":False}, 400
        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Internship Parameters", "success": False}, 400