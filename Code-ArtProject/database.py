from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy 
from create_database import db, Account, Internship, Event
from login import login_manager, login_blueprint, AdminModelViewAcc, AdminModelViewIntern, AdminModelViewEvent
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_bootstrap import Bootstrap
import account as account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseFiles/ca_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

db.app = app
db.init_app(app)

#bootstrap
Bootstrap(app)

#init api
account.create_api(app)

# init flask login
login_manager.init_app(app)

# blueprints
app.register_blueprint(login_blueprint)

#admin dashboard
admin = Admin(app, name = 'Admin', url = "/admin", endpoint = "admin", template_mode="bootstrap3")
admin.add_view(AdminModelViewAcc(Account, db.session))
# admin.add_view(AdminModelViewIntern(Internship, db.session))
# admin.add_view(AdminModelViewEvent(Event, db.session))
