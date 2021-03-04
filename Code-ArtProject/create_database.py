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
    """
    id = db.Column(db.Text, primary_key = True, unique = True, nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False)
    is_student = db.Column(db.Boolean, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, unique=True,nullable = False)
    password = db.Column(db.Text, nullable = False)

    # relationships
    internships = db.relationship("Internship", backref='student', lazy=dynamic, foreign_key='Internship.student_id')
    events = db.relationship("Event", backref='student', lazy=dynamic, foreign_key='Event.student_id')


class Internship(db.Model):
    __tablename__ = 'internship'
    """
    id: int
    location: str
    company: str
    phone_number: str
    email: str
    details: str
    accepted: bool
    """
    id = db.Column(db.Text, primary_key = True, unique = True, nullable = False)
    location = db.Column(db.Text)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    start_datetime = db.Column(db.Text, nullable = False)
    end_datetime = db.Column(db.Text, nullable = False)
    accepted = db.Column(db.Boolean, nullable = False)
    canceled = db.Column(db.Boolean, nullable = False)
    details = db.Column(db.Text)

class Event(db.Model):
    __tablename__ = 'event'
    """
    id: int
    organizers: str
    location: str
    details: str
    accepted: bool
    """

    id = db.Column(db.Text, primary_key = True, unique = True, nullable = False)
    location = db.Column(db.Text)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    start_datetime = db.Column(db.Text, nullable = False)
    end_datetime = db.Column(db.Text, nullable = False)
    accepted = db.Column(db.Boolean, nullable = False)
    canceled = db.Column(db.Boolean, nullable = False)
    details = db.Column(db.Text)
