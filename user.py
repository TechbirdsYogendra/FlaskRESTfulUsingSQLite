import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_user = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_user, (username,))
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2]) OR
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_user = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_user, (_id,))
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2]) OR
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="username is required to register")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="password is required to register")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']) is None:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cursor.execute(insert_query, (data["username"], data["password"]))

            connection.commit()
            connection.close()

            return {"message": "User is created successfully."}
        else:
            return {"message": "User is already exits with this username choose another username."}, 400

class Users(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM users"
        users = cursor.execute(select_query).fetchall()

        connection.commit()
        connection.close()

        return {"users": users}
