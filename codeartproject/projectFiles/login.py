from flask import Flask, flash, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required,logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from databasedetails import db, Account
from flask_admin import Admin, BaseView, expose
from flask_admin.menu import MenuLink
import uuid
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField
from datetime import datetime, date
from getage import update_age

login_manager = LoginManager()
login_manager.login_view = '/login'
login_blueprint = Blueprint("logins","__logins__")


class AdminModelViewAcc(ModelView):
    column_searchable_list = ["first_name","last_name","email","birthday", "age", "graduation"]

    def is_accessible(self):
        # call update function? update_age() based on calculation? 
        # LOOP THROUGH ALL THE ACCOUNTS --> Account query? 
        update_all_accounts()
        return current_user.is_authenticated and current_user.is_admin

    def on_model_change(self, form, Account, is_created=False):
        Account.password = generate_password_hash(Account.password, method='SHA512')

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class AdminModelViewIntern(ModelView):
    column_searchable_list = ["location","company"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class AdminModelViewEvent(ModelView):
    column_searchable_list = ["location","organizers", "event_name"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class AdminLogoutLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4,max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=64)])

def update_all_accounts():
    all_accounts = Account.query.all()
    for st_account in all_accounts:
        if st_account.birthday != "":
            print(st_account.birthday)
            stripped_birthdate = datetime.strptime(st_account.birthday, "%m/%d/%Y")
            print(stripped_birthdate)
            st_account.age = update_age( stripped_birthdate )

@login_manager.user_loader
def load_user(id):
    return Account.query.get(id)

@login_blueprint.route('/login', methods=['GET','POST'])
@login_blueprint.route('/login.html', methods=['GET','POST'])
@login_blueprint.route('/signin.html', methods=['GET','POST'])
def login():
    form = LoginForm()

    log_error = '<font color="red">' + "Error: Incorrect Credentials" + '</font>'

    if form.validate_on_submit():
        user = Account.query.filter_by(email=str(form.email.data).lower()).first()
        if user:
            if check_password_hash(user.password,str(form.password.data)):
                login_user(user)
                return redirect("/admin")
            return render_template("signin.html", login_form=form, error=log_error)
        return render_template("signin.html", login_form=form, error=log_error)
    return render_template("signin.html", login_form=form)

@login_blueprint.route('/logout')
@login_blueprint.route('/logout.html')
@login_required
def logout():
    logout_user()
    return redirect("/login")