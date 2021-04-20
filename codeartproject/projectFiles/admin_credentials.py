from databasedetails import Account, Internship, Event
from database import db 
from werkzeug.security import generate_password_hash
import uuid

created_admin_id = uuid.uuid4()

admin=Account(id=int(created_admin_id ), is_admin=True, is_student=False, first_name="Romina", last_name="Polo", email="admin@gmail.com", 
graduation="", birthday="", gender="female", attributes="", password=generate_password_hash("admin@OnlyPass!", method="SHA512"))

db.session.add(admin)
db.session.commit()