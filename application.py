import os
import random

from flask import Flask, session, redirect, flash, url_for, session, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

from models import *
# from emojis import insertEmojis


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://clerswqmlkoytn:ec3c1ccc28d402b41b98b878c105826dc88a3ae5eb1b6ce9e41f4ef465c5cf1c@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/d5vpmlkod9ag5m"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


db.init_app(app)

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block.
    db.create_all()


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(
    "postgres://clerswqmlkoytn:ec3c1ccc28d402b41b98b878c105826dc88a3ae5eb1b6ce9e41f4ef465c5cf1c@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/d5vpmlkod9ag5m?charset=utf8")
db = scoped_session(sessionmaker(bind=engine))

db = SQLAlchemy(app)


def main():
    emojis = ["⛺", "🌈", "🌞", "🌸", "🐣", "🐨"]
    for item in emojis:
        emoji = Emoji(content=item)
        db.session.add(emoji)
        print(f"This emoji {item} was added into the table")
    db.session.commit()
    print("Complete")

# main()

@app.route("/")
def index():
    if not session.get('username'):
        return redirect("/username")

    emojis = Emoji.query.all()
    container = []
    print(container)
    for emoji in emojis:
        content = emoji.content
        container.append({"id": emoji.id, "content": content, "solved": emoji.solved})
        container.append({"id": emoji.id, "content": content, "solved": emoji.solved})

    random.shuffle(container)
    print(container)
    return render_template("index.html", emojis=container)

@app.route("/username", methods=["GET", "POST"])
def enter_username():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username").lower().capitalize()
        # Ensure username was submitted
        if len(username) < 1 or username == "":
            flash("Please enter a username.")
            print("enter a username")
            return redirect("/username")
        # Ensure it is not in the list
        elif User.query.filter_by(username=username).first():
            flash("This username already exists.")
            print("username exists")
            return redirect("/username")
        # add user to users table
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        # Forget any user_id
        session.clear()
        session['username'] = username
        # Remember the session if the browser is closed.
        session.permanent = True
        return redirect("/")
    # User reached route via GET
    else:
        print("GET request")
        return render_template("username.html")


