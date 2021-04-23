from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from databasedetails import db, Account, Event, Internship
import json
import uuid
from endpoints.verify_auth import verify_auth, live_tokens
from werkzeug.security import check_password_hash, generate_password_hash
from getage import update_age
from datetime import datetime, date
app_api = None

#Endpoint links for the app to be able to establish a connection 
def create_api(app):
    app_api = Api(app)
    app_api.add_resource(AccountInfo, "/accountinfo")
    app_api.add_resource(AccountModify, "/accountmodify")
    app_api.add_resource(Login, "/account/login")
    app_api.add_resource(AccountCreate, "/accountcreate")

#Endpoint to connect to the app for logging in 
class Login(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()                                                     #Gets the parameters of email and password the app user input
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()
            
            user = Account.query.filter_by( email=( str( args['email'] ).lower() ) ).first()      #Checks if the input information matches the email and password in the database
            if user:
                if check_password_hash(user.password, args['password']):
                    user_id = user.id                                                             #If both are true, take the user id and create a auth token to be used for verification
                    auth_token = str( uuid.uuid4() )
                    live_tokens.append( (auth_token, user_id) )                                   #Make it active and return that the user has been logged in and has an auth token 
                    return {'id':user_id, 'auth':auth_token}, 200
            return 'Incorrect Credentials', 401                                                   #If credentials are wrong or input incorrectly, it will return the error message to the app and user
        except Exception as exe:                                                                  #If the parameters are incorrect, it will return an error message to the app and user
            print(exe)
            return {"msg":"Bad Request"}, 400 

#Endpoint for the app that modifies the account
class AccountModify(Resource):
    parser = reqparse.RequestParser()                                                             #Takes the newly modified parameters for the account
    parser.add_argument('id', type=int)
    parser.add_argument('is_admin', type=bool)
    parser.add_argument('is_student', type=bool)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('graduation', type=str)
    parser.add_argument('birthday', type=str)
    parser.add_argument('gender', type=str)
    parser.add_argument('attributes', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('auth', type=str)

    #Method that updates the account with the newly modified parameters
    def put(self):
        print(request.data)

        try:
            args = self.parser.parse_args()
            if not verify_auth(args['auth'], args['id']):                                         #If the account is not authenticated then it will return an error that the id or token are invalid
                return {"msg": "Invalid id or Auth Token", "success": False}, 400

            mod_acc = Account.query.get(args["id"])                                               #Get the id of the account that will be modified

            stripped_mod_birthdate = datetime.strptime(args["birthday"], "%m/%d/%y")              #Calculate the new age of the modified birthday if applicable
            mod_age = update_age( stripped_mod_birthdate )

            #Update all the fields whether they were modified or not 
            mod_acc.is_admin = args["is_admin"]        
            mod_acc.is_student = args["is_student"]
            mod_acc.first_name = args["first_name"]
            mod_acc.last_name = args["last_name"]
            mod_acc.email = str( args["email"] ).lower()
            mod_acc.graduation = args["graduation"]
            mod_acc.birthday = args["birthday"]
            mod_acc.age = mod_age
            mod_acc.gender = args["gender"]
            mod_acc.attributes = args["attributes"]
            mod_acc.password = generate_password_hash(args["password"], method='SHA512')

            db.session.commit()                                                                    #Commit the changes made to save it 
            return {"success": True}, 201
        except Exception as exe:
            print(exe)
            return {"success": False}, 400 

#Endpoint for displaying the information of the account to the app
class AccountInfo(Resource):

    #Method for getting the information of the account and returning it to app 
    def get(self):
        try:
            parser = reqparse.RequestParser()                                                       #Get the parameter id of the account
            parser.add_argument('id', type=int)
            args = parser.parse_args()

            acc = Account.query.get( int( args["id"] ) )                                            #Check if there is an account with that id

            if not acc:                                                                             #If not, then return an error message
                return {"msg": "Invalid Account"}, 400
            
            #Return all the fields of the account with its respective information
            return {"is_admin": acc.is_admin, "is_student": acc.is_student, "first_name": acc.first_name, "last_name": acc.last_name, 
            "email": acc.email, "graduation": acc.graduation, "birthday": acc.birthday, "age": acc.age, "gender": acc.gender, "attributes": acc.attributes, 
            "success": True}, 200 
            
        except Exception as exe:                                                                     #Return an error message if the paramter id is incorrect
            print(exe)
            return {"msg": "Incorrect Request", "success": False}, 400

#Endpoint for creating accounts for the app 
class AccountCreate(Resource):
    parser = reqparse.RequestParser()                                                                #Get the parameters for the account that wants to be registered
    parser.add_argument('is_admin', type=bool)
    parser.add_argument('is_student', type=bool)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('graduation', type=str)
    parser.add_argument('birthday', type=str)
    parser.add_argument('gender', type=str)
    parser.add_argument('attributes', type=str)
    parser.add_argument('password', type=str)

    #Method that creates an account with the paramaters information and adds it to the database
    def post(self):

        try:
            string_uuid = str( uuid.uuid4().int )                                                     #Create an uuid that is converted to a string
            half_len_of_string = int( len(string_uuid)/2 )                                            #Get the length of that string
            created_id = int( string_uuid[:half_len_of_string] )                                      #Cast the uuid into an int and only take half of the uuid (int uuids are too large to put them whole)

            args = self.parser.parse_args()

            try:
                stripped_birthdate = datetime.strptime(args["birthday"], "%m/%d/%y")                      #Calculate the age of the user by stripping the birthdate and casting it as a datetime object
                acc_age = update_age( stripped_birthdate )                                                #Take the stripped birthdate and get the age 
            except:
                return {"msg":"Incorrect Birthday Format or Missing Birthday", "success":False}, 400

            #Create the account with the parameters and calculated age 
            create_acc = Account(id=created_id, is_admin=args["is_admin"], is_student=args["is_student"], 
                first_name=args["first_name"], last_name=args["last_name"], email=str(args["email"]).lower(), graduation=args["graduation"], 
                birthday=args["birthday"], age=acc_age, gender=args["gender"], attributes=args["attributes"], password=generate_password_hash(args["password"], 
                method='SHA512') )
            
            db.session.add(create_acc)                                                                #Add the account to the database and commit the change
            db.session.commit()
            return {"success": True}, 201
        except Exception as exe:                                                                      #If parameters are input incorrectly or in the wrong format, return error message
            print(exe)
            return {"success": False}, 400 