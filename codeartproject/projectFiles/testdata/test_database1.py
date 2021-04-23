from projectFiles.database import db, User

db.create_all()

guest = User(username="guest", email="guest@example.com")

db.session.add(guest)
db.session.commit()