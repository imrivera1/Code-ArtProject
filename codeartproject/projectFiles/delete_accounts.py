from databasedetails import Account, Internship, Event
from database import db 

Account.query.all().delete()

db.session.commit()