from flask import Flask, send_from_directory, request, Blueprint, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required,logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from create_database import db, Account
from flask_admin import Admin
import uuid

login_manager = LoginManager()
login_manager.login_view = '/login'
login_blueprint = Blueprint("logins","__logins__")


class AdminModelViewAcc(ModelView):
    column_searchable_list = ["first_name","last_name","email","age","grade"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("login"))

class AdminModelViewIntern(ModelView):
    column_searchable_list = ["location","company","email", "phone_number"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("login"))

class AdminModelViewEvent(ModelView):
    column_searchable_list = ["location","organizers","email"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("login"))



@login_manager.user_loader
def load_user(id):
    return Account.query.get(id)
