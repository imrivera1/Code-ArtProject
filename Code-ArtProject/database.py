from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from create_database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseFiles/ca_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

db.app = app
db.init_app(app)

# init flask login

# blueprints

#admin dashboard


@app.route("/")
# @app.route("/adminDatabase")
# @login_required
def home():
    # return render_template("admin_dashboard.html", name=current_user.first_name)
    return "" 




