from projectFiles.databasedetails import Account, Internship, Event
from projectFiles.database import db 
from werkzeug.security import generate_password_hash
import uuid

string_uuid = str( uuid.uuid4().int )
half_len_of_string = int( len(string_uuid)/2 )
created_id = int( string_uuid[:half_len_of_string] )

student = Account(id=created_id, is_admin=False, is_student=True, first_name="Alexa", last_name="Fern", 
email="student@gmail.com", graduation="", birthday="04/11/93", age=27, gender="female", attributes="", password=generate_password_hash("password",method="SHA512"))

db.session.add(student)
db.session.commit()