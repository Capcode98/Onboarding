from flask import request, jsonify, render_template
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.models.connect_bd import register_person, login
from app import app


#__________________________Rotas_de_Painas_Estáticas_______________________#

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

#__________________________Rotas_de_Autenticação_de_Pessoa_______________________#

@app.route('/login', methods=['POST'])
def Login():

    try:
        data = request.get_json()
        print(data)
        person = login(**data)

        if person is not None:
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
        register_person(**data)
        access_token = create_access_token(identity=request.json.get("cpf"))
        return jsonify({"msg": "Cadastro realizado com sucesso","token":f"{access_token}"}), 201
    
    except Exception as e:
        print("Erro ao cadastrar pessoa:", e)
        return jsonify({"msg": "Erro ao cadastrar pessoa"}), 500
    

@app.route("/logout", methods=["POST"])
@jwt_required()
def Logout():

    return jsonify({"msg": "Logout realizado com sucesso"}), 200

#__________________________Rotas_de_Proteção_______________________#

@app.route("/protected", methods=["GET"])
@jwt_required()
def Protected():

    current_user = get_jwt_identity()
    print(current_user)
    print(request.get_data())
    return jsonify(logged_in_as=current_user), 200
