from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity as identity_function

from user import UserRegister, Users
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "yogendra"
api = Api(app)

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

app.config['JWT_AUTH_URL_RULE'] = "/login"  # This create the end point "/login" for authentication instead "/auth".
jwt = JWT(app, authenticate, identity_function)  # creates a end point /auth


# customize JWT auth response, include user_id and user_name in response body
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id,
        "user_name": identity.username
    })

# Error handler
@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Users, "/users")

if __name__ == "__main__":
    # This below line will execute only if we run this file not in the case of import.
    app.run(port=500, debug=True)
