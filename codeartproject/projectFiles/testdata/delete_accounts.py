from projectFiles.databasedetails import Account, Internship, Event
from projectFiles.database import db 

Account.query.all().delete()

db.session.commit()