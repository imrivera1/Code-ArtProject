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
    app_api.add_resource(EventInfo, "/eventinfo")
    app_api.add_resource(EventModify, "/eventmodify")
    app_api.add_resource(EventCreate, "/eventcreate")
    app_api.add_resource(EventDelete, "/eventdelete")


class EventModify(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('auth', type=str)
    parser.add_argument('event_name', type=str)
    parser.add_argument('organizers', type=str)
    parser.add_argument('location', type=str)
    parser.add_argument('cost', type=str)
    parser.add_argument('start_datetime', type=str)
    parser.add_argument('end_datetime', type=str)
    parser.add_argument('details', type=str)
    parser.add_argument('event_id', type=int)

    def put(self):
        print(request.data)

        try:
            args = self.parser.parse_args()
            if verify_auth(args['auth'], args['id']):

                event = Event.query.get(args["event_id"])

                if event:

                    event.event_name = args["event_name"]
                    event.organizers = args["organizers"]
                    event.location = args["location"]
                    event.cost = args["cost"]
                    event.start_datetime = args["start_datetime"]
                    event.end_datetime = args["end_datetime"]
                    event.details = args["details"]

                    db.session.commit()
                    return {"success": True}, 201
                else:
                    return {"msg":"Invalid Event","success":False}, 400
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400

        except Exception as exe:
            print(exe)
            return {"success": False}, 400


class EventInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            parser.add_argument('auth', type=str)
            parser.add_argument('event_id', type=int)
            args = parser.parse_args()

            if verify_auth('auth', 'id'):
                event = Event.query.get( args["event_id"] )
                if event:
                    print("Event Exists")

                    return {"event_name": event.event_name, "organizers": event.organizers, "location": event.location, "cost": event.cost,
                    "start_datetime": event.start_datetime, "end_datetime": event.end_datetime, "details": event.details, 
                    "success": True}, 200
            else:
                return {"msg": "Invalid ID or Auth Token", "success": False}, 400

        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Event ID", "success": False}, 400

class EventCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('auth', type=str)
    parser.add_argument('event_name', type=str)
    parser.add_argument('organizers', type=str)
    parser.add_argument('location', type=str)
    parser.add_argument('cost', type=str)
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
                event_id = int( string_uuid[:half_len_of_string] )

                acc = Account.query.get( str( args["id"] ) )
                if acc:
                    event = Event(id=event_id, event_name=args["event_name"], organizers=args["organizers"], location=args["location"], 
                    cost=args["cost"], start_datetime=args["start_datetime"], end_datetime=args["end_datetime"], details=args["details"])

                    db.session.add(event)
                    db.session.commit()

                    return {"success": True}, 201
                else:
                    return {"msg":"No Account","success":False}, 400
            else:
                return {"msg":"Invalid ID or Auth Token","success":False}, 400
        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Event Parameters", "success": False}, 400
            

class EventDelete(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('auth', type=str)
        parser.add_argument('event_id', type=int)

        try:
            args = parser.parse_args()
            if verify_auth('auth', 'id'):
                acc = Account.query.get( int( args["id"] ) )
                if acc:
                    event = Event.query.get(args["event_id"])
                    if event:
                        db.session.delete(event)
                        db.session.commit()
                        return {"msg":"Event Deleted","success":True}, 200
                else:
                    return {"msg":"No Account","success":False}, 400
            else:
                return {"msg":"Event Could Not Be Deleted","success":False}, 400
        except Exception as exe:
            print(exe)
            return {"msg": "Incorrect Event Parameters", "success": False}, 400