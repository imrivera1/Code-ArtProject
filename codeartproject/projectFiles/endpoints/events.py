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


class EventModify(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('auth', type=str)
    parser.add_argument('event_name', type=str)
    parser.add_argument('organizers', type=str)
    parser.add_argument('location', type=str)
    parser.add_argument('cost', type=str)
    parser.add_argument('start_datetime', type=str)
    parser.add_argument('end_datetime', type=str)
    parser.add_argument('details', type=str)

    def put(self):
        print(request.data)

        try:
            args = self.parser.parse_args()
            if not verify_auth(args['auth'], args['id']):
                return {"msg": "Invalid id or Auth Token", "success": False}, 400
            
            created_id = uuid.uuid4()
            mod_event = Event.query.get(args["id"])

            mod_event.event_name = args["event_name"]
            mod_event.organizers = args["organizers"]
            mod_event.location = args["location"]
            mod_event.cost = args["cost"]
            mod_event.start_datetime = args["start_datetime"]
            mod_event.end_datetime = args["end_datetime"]
            mod_event.details = args["details"]

            db.session.commit()
            return {"success": True}, 201

        except Exception as exe:
            print(exe)
            return {"success": False}, 400


class EventInfo(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            parser.add_argument('auth', type=str)
            parser.add_argument('event_id', type=str)
            args = parser.parse_args()

            if verify_auth('auth', 'id'):
                event = Event.query.get( args["event_id"] )
                if event:
                    print("Event Exists")

                    if event.accepted:
                        student_account = event.student
                    else:
                        

            if not event:
                return {"msg": "Invalid Account"}, 400
            
            return {

class EventCreate(Resource):

class EventDelete(Resource):

class EventAccept(Resource):

class EventCancel(Resource):