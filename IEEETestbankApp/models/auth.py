from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from IEEETestbankApp.models.db import db, initDatabase

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    # Basic models
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    #password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    
    # User data models
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    major = db.Column(db.String(20))
    grad_semester = db.Column(db.String(10))
    grad_year = db.Column(db.Integer)
    
    # Confirmation model
    confirmed_at = db.Column(db.DateTime())
    
    # User tracking models
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(40))
    current_login_ip = db.Column(db.DateTime())
    login_count = db.Column(db.Integer())
    
    # Finalize roles
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

initDatabase()
