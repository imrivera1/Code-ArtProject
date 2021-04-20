from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    __tablename__='account'
    """
    id: int
    isAdmin: bool
    isStudent: bool
    first_name: str
    last_name: str
    email: str
    graduation: str
    birthday: str
    gender: str
    attributes: str
    """
    id = db.Column(db.Text, primary_key = True, unique = True, autoincrement=False, nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False)
    is_student = db.Column(db.Boolean, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, unique=True, nullable = False)
    graduation = db.Column(db.Text, nullable = False)
    birthday =  db.Column(db.Text, nullable = False)
    gender = db.Column(db.Text, nullable = False)
    attributes = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)


class Internship(db.Model):
    __tablename__ = 'internship'
    """
    id: int
    location: str
    company: str
    role: str
    link: str
    details: str
    """
    id = db.Column(db.Text, primary_key = True, unique = True, autoincrement=False, nullable = False)
    location = db.Column(db.Text, nullable = False)
    company = db.Column(db.Text, nullable = False)
    role = db.Column(db.Text, nullable = False)
    link = db.Column(db.Text, nullable = False)
    start_datetime = db.Column(db.Text, nullable = False)
    end_datetime = db.Column(db.Text, nullable = False)
    details = db.Column(db.Text, nullable = False)

class Event(db.Model):
    __tablename__ = 'event' 
    """
    id: int
    event_name: str
    organizers: str
    location: str
    cost: str
    details: str
    """

    id = db.Column(db.Text, primary_key = True, unique = True, autoincrement=False, nullable = False)
    event_name = db.Column(db.Text, nullable = False)
    organizers = db.Column(db.Text, nullable = False)
    location = db.Column(db.Text, nullable = False)
    cost = db.Column(db.Text, nullable = False)
    start_datetime = db.Column(db.Text, nullable = False)
    end_datetime = db.Column(db.Text, nullable = False)
    details = db.Column(db.Text, nullable = False)
