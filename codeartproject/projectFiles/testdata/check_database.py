from projectFiles.databasedetails import Account, Internship, Event
from projectFiles.database import db 

print(Account.query.all())

admin = Account.query.filter_by(email="admin@gmail.com").first()

print("Admin Id: " + admin.id )