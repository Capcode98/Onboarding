from flask import request, jsonify, render_template
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.connect_bd import cadastrar_Pessoa, login
from app import app

@app.route('/')
def Init():
    
    return render_template("home.html")


@app.route('/modelo_protected.html')
def Modelo_Protected():
    
    return render_template("modelo_protected.html")


@app.route('/modelo_token.html')
def Modelo_Token():
    
    return render_template("modelo_token.html")


@app.route('/modelo_logout.html')
def Modelo_Logout():
    
    return render_template("modelo_logout.html")


@app.route('/modelo_login.html')
def Modelo_Login():
    
    return render_template("modelo_login.html")


@app.route('/modelo_cadastro.html')
def Modelo_Cadastro():
    
    return render_template("modelo_cadastro.html")

@app.route('/documentation.html')
def Documentation():
    
    return render_template("documentation.html")

@app.route('/login', methods=['POST'])
def Login():
    try:
        data = request.get_json()

        print(data)
        
        pessoa = login(**data)
        
        if pessoa is not None:
            
            return jsonify({"msg": "Login realizado com sucesso"}), 200
        
        else:
            
            return jsonify({"msg": "Combinação de email/cpf e senha não encontrada"}), 401
    
    except Exception as e:
        
        print("Erro ao fazer login:", e)
        
        return jsonify({"msg": "Erro ao fazer login"}), 500


@app.route("/cadastro", methods=["POST"])
def Cadastro():
    try:
        data = request.get_json()
        
        cadastrar_Pessoa(**data)

        access_token = create_access_token(identity=request.json.get("nome"))
        
        return jsonify({"msg": "Cadastro realizado com sucesso","token":f"{access_token}"}), 201
    
    except Exception as e:
        
        print("Erro ao cadastrar pessoa:", e)
        
        return jsonify({"msg": "Erro ao cadastrar pessoa"}), 500

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/token", methods=["POST"])
def Create_token():
  
    username = request.json.get("username",None)
    username_in_bd = "admin"
    password = request.json.get("password",None)
    password_in_bd = "test@"

    if username == username_in_bd and password == password_in_bd:

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
def Protected():
    
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    
    print(request.get_data())
    
    return jsonify(logged_in_as=current_user), 200
