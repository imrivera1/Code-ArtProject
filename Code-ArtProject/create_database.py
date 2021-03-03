from database import db, User

db.create_all()

guest = User(username="guestUser", email="guest@gmail.com")

db.session.add(guest)
db.session.commit()


