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

login_manager = LoginManager()                                                                       #Used for managing the login, load, and logout of an admin
login_manager.login_view = '/login'
login_blueprint = Blueprint("logins","__logins__")                                                   #Blueprint route used to connect it to the database


class AdminModelViewAcc(ModelView):
    column_searchable_list = ["first_name","last_name","email","birthday", "age", "graduation"]      #Options for the admins to search in the search bar

    form_excluded_columns = ("age")                                                                  #Excludes inputting age manually when creating or editing an account

    def is_accessible(self):
        update_all_accounts()                                                                        #Updates all ages for those that have a birthday upon viewing the dashboard
        return current_user.is_authenticated and current_user.is_admin                               #Returns whether the user is authenticated and an admin 
                                                                                                            #thus allowing them to view the dashboard

    def on_model_change(self, form, Account, is_created=False):                                      #When creating/editing an account, the password will be hashed for security
        Account.password = generate_password_hash(Account.password, method='SHA512')

    def _handle_view(self, name, **kwargs):                                                          #If user is not an admin or authenticated, they are redirected to login and can't view anything
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class AdminModelViewIntern(ModelView):                               
    column_searchable_list = ["location","company"]                                                  #Options for the admins to search in the search bar

    def is_accessible(self):                                                                         
        return current_user.is_authenticated and current_user.is_admin                               #Returns whether the user is authenticated and an admin 
                                                                                                            #thus allowing them to view the dashboard

    def _handle_view(self, name, **kwargs):                                                          #If user is not an admin or authenticated, they are redirected to login and can't view anything
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class AdminModelViewEvent(ModelView):
    column_searchable_list = ["location","organizers", "event_name"]                                 #Options for the admins to search in the search bar

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin                               #Returns whether the user is authenticated and an admin 
                                                                                                            #thus allowing them to view the dashboard

    def _handle_view(self, name, **kwargs):                                                          #If user is not an admin or authenticated, they are redirected to login and can't view anything
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class AdminLogoutLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin                               #Returns whether the user is authenticated and an admin 
                                                                                                            #thus allowing them to view the dashboard and the link

    def _handle_view(self, name, **kwargs):                                                          #If user is not an admin or authenticated, they are redirected to login and can't view anything
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class LoginForm(FlaskForm):                                                                          #Form an admin will see in login for email and password login
    email = StringField('Email', validators=[InputRequired(), Length(min=4,max=64)])                 #Email must have a minimum of 4 characters in order to accept it as an email
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=64)])         #Password must have a minimum of 8 characters in order for it to be accepted

def update_all_accounts():                                                                           #Updates the ages of all accounts in the database
    all_accounts = Account.query.all()                                                               #Gets the full list of all user accounts, including admins
    for st_account in all_accounts:                                                                  #Loops through each account in the entire list
        if st_account.birthday != "":                                                                #Some admin accounts might not have a birthday input, so it won't calculate the age for them
            try:
                stripped_birthdate = datetime.strptime(st_account.birthday, "%m/%d/%y")              #Strips the birthday string into a datetime format of a zero padded date( mm/dd/yy )
                st_account.age = update_age( stripped_birthdate )                                    #Calls update age function from getage.py to calculate the age based on the stripped birthdate
            except ValueError:                                                                       #If birthday is input incorrectly, it will catch the error and flash to the admin dashboard the message
                flash("Incorrect Birthdate Format. Please put in zero padded format: mm/dd/yy")

@login_manager.user_loader
def load_user(id):                                                                                   #Loads the admin into the dashboard when logged in
    return Account.query.get(id)

@login_blueprint.route('/login', methods=['GET','POST'])
@login_blueprint.route('/login.html', methods=['GET','POST'])
@login_blueprint.route('/signin.html', methods=['GET','POST'])
def login():                                                                                         #Login function to check credentials of admins and log them in
    form = LoginForm()                                                                               #Gets the login form for the admin to view in the login page

    log_error = '<font color="red">' + "Error: Incorrect Credentials" + '</font>'                    #Login error message in html format for the login html page

    if form.validate_on_submit():                                                                    #If the form is valid and submitted, then continue checking the email and password
        user = Account.query.filter_by(email=str(form.email.data).lower()).first()                   #Looks through the emails to see if the input email is for a registered account
        if user:                                                                                     #If the email belongs to a registered user then check the password
            if check_password_hash(user.password,str(form.password.data)):                           #Get the password that was input and check if the password is registered with that email 
                login_user(user)                                                                     #If true, then login the user and redirect them to the admin dashboard
                return redirect("/admin")
            return render_template("signin.html", login_form=form, error=log_error)                  #Otherwise, if the email or password is incorrect, show the login page with error information
        return render_template("signin.html", login_form=form, error=log_error)
    return render_template("signin.html", login_form=form)                                           #Show the login page with the form fields if nothing is input yet

@login_blueprint.route('/logout')
@login_blueprint.route('/logout.html')
@login_required
def logout():                                                                                        #Function to logout the user
    logout_user()                                                                                    #Logs the admin out and redirects them to the login page
    return redirect("/login")