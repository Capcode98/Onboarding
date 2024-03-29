from flask import request, jsonify
from app import app


@app.route('/')
def index():
    return "hello world"



from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/token", methods=["POST"])
def create_token():
  
    username = request.json.get("username",None)
    username1 = request.json.get("username",None)
    password = request.json.get("password",None)

    if username == username1 and password == "test@":

      access_token = create_access_token(identity=username)

      return jsonify(access_token=access_token)
    
    elif username == "test@gmail.com" and password == "test@":

      access_token = create_access_token(identity=username)

      return jsonify(access_token=access_token)

    else:
        return jsonify({"msg": "Bad username or password"}), 401
 

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    
    print(request.get_data())
    
    return jsonify(logged_in_as=current_user), 200
