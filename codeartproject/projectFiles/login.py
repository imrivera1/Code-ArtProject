from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required,logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from databasedetails import db, Account
from flask_admin import Admin
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField

login_manager = LoginManager()
login_manager.login_view = '/login'
login_blueprint = Blueprint("logins","__logins__")


class AdminModelViewAcc(ModelView):
    column_searchable_list = ["first_name","last_name","email","birthday","graduation"]

    def is_accessible(self):
        print("Check: " + current_user.is_authenticated + " " + current_user.is_admin)
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("login"))

class AdminModelViewIntern(ModelView):
    column_searchable_list = ["location","company"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("login"))

class AdminModelViewEvent(ModelView):
    column_searchable_list = ["location","organizers", "event_name"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("login"))

@login_manager.user_loader
def load_user(id):
    return Account.query.get(id)

@login_blueprint.route('/login', methods=['GET','POST'])
@login_blueprint.route('/login.html', methods=['GET','POST'])
@login_blueprint.route('/signin.html', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Account.query.filter_by(email=str(form.email.data).lower()).first()
        if user:
            if check_password_hash(user.password,str(form.password.data)):
                login_user(user)
                return redirect("/admin")
            return "Error: Incorrect Credentials"
        return "Admin Account Does Not Exist"
    return render_template("signin.html", form=form)

@login_blueprint.route('/logout')
@login_blueprint.route('/logout.html')
@login_required
def logout():
    logout_user()
    return redirect('/signin.html')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=4,max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=64)])


