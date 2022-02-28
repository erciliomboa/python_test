import uuid

from flask import session

from src.app import mysql


class User():
    def __init__(self, first_name, last_name, username, password, email, celphone, _id = None ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.celphone = celphone
        self._id = uuid.uuid4().hex if _id is None else _id


        def get_user_username( self, username):
            cur = mysql.connection.cursor()
            user = cur.execute("SELECT *FROM users WHERE username ='" + username+ "'")
            if user > 0:
                userDetails = cur.fetchall()
                return userDetails

        # login method
        @classmethod
        def login_valid(cls, username, password):
            user = ("SELECT * FROM users WHERE username ='" + username + "' and password ='" +password +"'")
            return cls(**user)