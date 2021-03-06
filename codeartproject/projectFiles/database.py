from flask import Flask, session, render_template, send_from_directory, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from login import login_manager, login_blueprint, AdminModelViewAcc, AdminModelViewIntern, AdminModelViewEvent, AdminLogoutLink
from databasedetails import db, Account, Internship, Event
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
import endpoints.account as account
import endpoints.internships as internship
import endpoints.events as event

#init app
app = Flask(__name__, static_url_path='')

#bootstrap
Bootstrap(app)

#init api
account.create_api(app)
internship.create_api(app)
event.create_api(app)

#init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseFiles/ca_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'pulse'
app.config["SECRET_KEY"] = "@fJ99YM20bAq"    # Change when handed over due to it being posted on Github
db.app = app
db.init_app(app)

# init flask login
login_manager.init_app(app)

# blueprints
app.register_blueprint(login_blueprint)

#admin dashboard
admin = Admin(app, name = "Admin", url = "/admin", endpoint = "admin", template_mode="bootstrap4")
admin.add_view(AdminModelViewAcc(Account, db.session))
admin.add_view(AdminModelViewIntern(Internship, db.session))
admin.add_view(AdminModelViewEvent(Event, db.session))
admin.add_link(AdminLogoutLink(name="Logout", category='', url="/logout"))


#Redirects user to login no matter if they put a slash or nothing after the link 
@app.route('/', defaults={"path":''})
def static_files(path=None):
    print("path:",path)
    if(path=="/" or path==""):
        return redirect("/login")
    return send_from_directory('static',path)