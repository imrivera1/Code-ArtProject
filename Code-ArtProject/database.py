from flask import Flask
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseFiles/ca_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def __repr__(self):
        return self.username


@app.route("/")
def home():
    check_user_names = (str) ( User.query.all() )
    check_user = (str) ( User.query.filter_by(username='guest').first() )
    return "User: " + check_user_names




