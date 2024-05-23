from flask import request, jsonify, render_template
from flask_socketio import send, emit
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from app.models.connect_bd import register_person, login, register_item, edit_item, delete_item, list_itens, register_feedback, list_feedbacks, register_token, transform_the_last_token_in_expired, list_meetings, list_trainings, register_meeting, register_training, list_monthly_schedule
from app import app, socketIo

#__________________________Criação_de_Token_______________________________#

def create_token(request=None,identity=None):

    if(identity):
        access_token = create_access_token(identity=identity)
        transform_the_last_token_in_expired(person_cpf=identity)
        register_token(token=access_token, person_cpf=identity)

    else:
        identity=request.json.get("cpf")
        access_token = create_access_token(identity=identity)
        register_token(token=access_token, person_cpf=identity)

    return access_token

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

#__________________________Rotas_de_Criação,_Deleção_e_Alteração_de_Pessoa_______________________#

@app.route('/login', methods=['POST'])
def Login():

    try:
        data = request.get_json()
        print(data)
        person = login(**data)

        if person is not None:
            access_token = create_token(identity=person.get_cpf())
            return jsonify({"msg": "Login realizado com sucesso","token":f"{access_token}"}), 200
        
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
        access_token = create_token(request=request)
        return jsonify({"msg": "Cadastro realizado com sucesso","token":f"{access_token}"}), 201
    
    except Exception as e:
        print("Erro ao cadastrar pessoa:", e)
        return jsonify({"msg": "Erro ao cadastrar pessoa"}), 500
    

@app.route("/logout", methods=["POST"])
@jwt_required()
def Logout():

    return jsonify({"msg": "Logout realizado com sucesso"}), 200

#__________________________Rotas_de_Criação,_Deleção_e_Alteração_de_Itens_____________________#

@app.route('/itens', methods=['GET'])
@jwt_required()
def Listar_Itens():

    dict_items = list_itens(get_jwt_identity())
    return jsonify(dict_items),200

@app.route('/itens', methods=['POST'])
@jwt_required()
def Criar_Itens():

    data = request.get_json()

    try:
        register_item(**data)
        return jsonify({"msg": f"Itens criado com sucesso"}, request.get_json()), 200
    
    except Exception as e:
        return jsonify({"msg": f"Erro ao criar item. {e}"}), 500

@app.route('/itens', methods=['PUT'])
@jwt_required()
def Atualizar_Item():

    data = request.get_json()

    try:
        edit_item(id_item=request.json.get("id"),id_pessoa=get_jwt_identity(),**data)
        return jsonify({"msg": "Item atualizado com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"msg": f"Erro ao editar item. {e}"}), 500

@app.route('/itens', methods=['DELETE'])
@jwt_required()
def Deletar_Item():

    delete_item(id_item=request.json.get("id"),id_pessoa=get_jwt_identity())
    return jsonify({"msg": "Item deletado com sucesso"}), 200

#__________________________Rotas_de_Criação,_Deleção_e_Alteração_de_FeedBacks_______________________#

@app.route('/avaliations', methods=['GET'])
@jwt_required()
def Listar_Avaliações():

    return jsonify(list_feedbacks()), 200  

@app.route('/feedback', methods=['POST'])
@jwt_required()
def Cadastrar_Feedback():

    data = request.get_json()

    try:
        register_feedback(id_pessoa=get_jwt_identity(),**data)
        return jsonify({"msg": f"Feedback cadastrado com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"msg": f"Erro ao criar Feedback. {e}"}), 500

#__________________________Rota_de_Meeting_______________________#

@app.route('/meeting', methods=['GET'])
@jwt_required()
def Listar_Reuniões():

    return jsonify(list_meetings(id_pessoa=get_jwt_identity())), 200  

@app.route('/meeting', methods=['POST'])
@jwt_required()
def Cadastrar_Reunião():

    data = request.get_json()

    try:
        register_meeting(id_pessoa=get_jwt_identity(),**data)
        return jsonify({"msg": f"Reunião cadastrada com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"msg": f"Erro ao criar Reunião. {e}"}), 500
    
#__________________________Rota_de_Training_______________________#

@app.route('/training', methods=['GET'])   
@jwt_required()
def Listar_Treinamentos():

    return jsonify(list_trainings(id_pessoa=get_jwt_identity())), 200

@app.route('/training', methods=['POST'])
@jwt_required()
def Cadastrar_Treinamento():

    data = request.get_json()

    try:
        register_training(id_pessoa=get_jwt_identity(),**data)
        return jsonify({"msg": f"Treinamento cadastrado com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"msg": f"Erro ao criar Treinamento. {e}"}), 500


#__________________________Rota_de_Monthly_Schedule_______________________#

@app.route('/monthly_schedule', methods=['GET'])    
@jwt_required()
def Listar_Agendamentos():

    return jsonify(list_monthly_schedule(id_pessoa=get_jwt_identity())), 200

#__________________________Rota_de_Chat_______________________#

@app.route('/chat')
@app.route('/chat.html')
def chat():
    return render_template('chat.html')

@socketIo.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)

#__________________________Rotas_de_Proteção_______________________#

@app.route("/protected", methods=["GET"])
@jwt_required()
def Protected():

    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
