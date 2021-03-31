from databasedetails import Account, Internship, Event
from database import db 
from werkzeug.security import generate_password_hash
import uuid

student = Account(id=str( uuid.uuid4() ), is_admin=False, is_student=True, first_name="Alexa", last_name="Fern", 
email="email1@gmail.com", grade="6th", age="11", gender="female", attributes="", password=generate_password_hash("password",method="SHA512"))

db.session.add(student)
db.session.commit()