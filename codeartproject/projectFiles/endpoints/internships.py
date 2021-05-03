from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from databasedetails import db, Account, Event, Internship
import json
import uuid
from endpoints.verify_auth import verify_auth, live_tokens
from sqlalchemy.sql.functions import func

app_api = None

#Endpoint links for the app to be able to establish a connection 
def create_api(app):
    app_api = Api(app)
    app_api.add_resource(InternInfo, "/interninfo")
    app_api.add_resource(InternAllInfo, "/internallinfo")

#Endpoint for displaying the information of the internship to the app
class InternInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()                                                       #Get the parameter id, auth, and intern_id of the internship
            parser.add_argument('id', type=str)
            parser.add_argument('auth', type=str)
            parser.add_argument('intern_id', type=str)
            args = parser.parse_args()

            if verify_auth('auth', 'id'):                                                           #Verify that it is authenticated
                internship = Internship.query.get( int( args["intern_id"] ) )                       #Get the internship using the internship id
                if internship:                                                                      #If the id matches an internship in the database then return the information regarding the internship
                    print("Internship Exists")

                    return {"location": internship.location, "company": internship.company, 
                    "role": internship.role, "link": internship.link, 
                    "start_datetime": internship.start_datetime, "end_datetime": internship.end_datetime, 
                    "details": internship.details, "success": True}, 200
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400                   #If the internship is not verified, return the error message

        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Internship ID", "success": False}, 400                        #If the parameters are incorrect, return error message


class InternAllInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()                                                       #Get the parameter id, auth, and intern_id of the internship
            parser.add_argument('id', type=str)
            parser.add_argument('auth', type=str)
            args = parser.parse_args()

            id_list = []

            if verify_auth('auth', 'id'):                                                           #Verify that it is authenticated
                internship_list = Internship.query.all()
                for single_intern in internship_list:                                               #If the id matches an internship in the database then return the information regarding the internship
                    print("Internship Exists")
                    id_list.append(single_intern.id)

                return jsonify(message=f"All Internship Ids", category="success", data=id_list, status=200)
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400                   #If the internship is not verified, return the error message

        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Internship ID", "success": False}, 400                        #If the parameters are incorrect, return error message