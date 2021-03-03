from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(_name_)
app.config["SQLAlchemy_DATABASE_URI"] = "sqlite:////database/ca_database.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def _repr_(self):
        return "<User %r>" % self.username




