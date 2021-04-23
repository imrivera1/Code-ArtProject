import sys
sys.path.append('/Code-ArtProject/codeartproject/projectFiles')
print(sys.path)
from projectFiles.databasedetails import Account, Internship, Event
from projectFiles.database import db 
from werkzeug.security import generate_password_hash
import uuid

string_uuid = str( uuid.uuid4().int )
half_len_of_string = int( len(string_uuid)/2 )
created_admin_id = int( string_uuid[:half_len_of_string] )

admin=Account(id=created_admin_id, is_admin=True, is_student=False, first_name="Romina", last_name="Polo", email="admin@gmail.com", 
graduation="", birthday="", age="", gender="female", attributes="", password=generate_password_hash("admin@OnlyPass!", method="SHA512"))

db.session.add(admin)
db.session.commit()