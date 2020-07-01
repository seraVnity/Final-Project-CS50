import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Emoji(db.Model):
  __tablename__ = "emojis"
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)
  solved = db.Column(db.Boolean, default = False)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, nullable=False)
  steps = db.Column(db.Integer, nullable=False, default = 0)
  time = db.Column(db.Integer, nullable=False, default = 0)





