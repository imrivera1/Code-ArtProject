from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from databasedetails import db, Account, Event, Internship
import json
import uuid
from endpoints.verify_auth import verify_auth, live_tokens

app_api = None

#Endpoint links for the app to be able to establish a connection 
def create_api(app):
    app_api = Api(app)
    app_api.add_resource(EventInfo, "/eventinfo")
    app_api.add_resource(EventAllInfo, "/eventallinfo")

#Endpoint for displaying the information of the event to the app
class EventInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()                                                       #Get the parameter id, auth, and event_id of the event
            parser.add_argument('id', type=str)
            parser.add_argument('auth', type=str)
            parser.add_argument('event_id', type=str)
            args = parser.parse_args()

            if verify_auth('auth', 'id'):                                                           #Verify that it is authenticated
                event = Event.query.get( int( args["event_id"] ) )                                        #Get the event using the event id
                if event:                                                                           #If the id matches an event in the database then return the information regarding the event
                    print("Event Exists")

                    return {"event_name": event.event_name, "organizers": event.organizers, 
                    "location": event.location, "cost": event.cost, "link": event.link, 
                    "start_datetime": event.start_datetime, "end_datetime": event.end_datetime, 
                    "details": event.details, "success": True}, 200
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400                   #If the event is not verified, return the error message 

        except Exception as exe:                                                                    #If the parameters are incorrect, return error message
            print(exe)
            return {"msg": "Incorrect Event ID", "success": False}, 400

class EventAllInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()                                                       #Get the parameter id, auth, and intern_id of the internship
            parser.add_argument('id', type=str)
            parser.add_argument('auth', type=str)
            args = parser.parse_args()

            id_list = []

            if verify_auth('auth', 'id'):                                                           #Verify that it is authenticated
                event_list = Event.query.all()
                for single_event in event_list:                                                #If the id matches an internship in the database then return the information regarding the internship
                    print("Event Exists")
                    id_list.append(single_event.id)

                return jsonify(message=f"All Event Ids", category="success", data=id_list, status=200)
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400                   #If the internship is not verified, return the error message

        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Internship ID", "success": False}, 400                        #If the parameters are incorrect, return error message