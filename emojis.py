import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Emoji

# Set up database
engine = create_engine(
    "postgres://clerswqmlkoytn:ec3c1ccc28d402b41b98b878c105826dc88a3ae5eb1b6ce9e41f4ef465c5cf1c@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/d5vpmlkod9ag5m")
db = scoped_session(sessionmaker(bind=engine))

def insertEmojis():
  count = db.execute("SELECT COUNT(*) FROM emojis")
  emojis = ["⛺", "🌈", "🌞", "🌸", "🐣", "🐨"]
  
  if count ==  0:
    for item in emojis:
        emoji = Emoji(content=item)
        db.add(emoji)
        print(f"This emoji {item} was added into the table")
    db.commit()
    print("Complete")