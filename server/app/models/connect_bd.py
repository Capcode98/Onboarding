from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.model import Person, CheckList, Feedback, Token, Meeting, Training, Question, Answer
from app.models.utils_bd import connecting_bd, sqlalchemy_to_dict
from hashlib import sha256


#________________________________Pessoas___________________________________#

def get_person_by_cpf(cpf):
        
    '''Lista todas as pessoas'''
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Person).filter(Person.cpf == cpf)
    
            person = query.one()
                
            return person
        
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def login(login, password):

    '''Faz login de uma pessoa'''

    try:

        session = connecting_bd()
        
        if session is not None:
        
            query = session.query(Person).filter((Person.email == login) | (Person.cpf == login)).filter(Person.password == sha256(password.encode()).digest())
        
            person = query.one()
        
            return person
    
    except NoResultFound:
    
        print("Combinação de email/cpf e senha não encontrada")
    
    except SQLAlchemyError as e:
    
        print("Erro ao fazer login:", e)
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def register_person(**kwargs):

    '''Adiciona uma pessoa na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            person = Person(**kwargs)
    
            session.add(person)
    
            session.commit()
    
            print("Cadastro da pessoa realizado com sucesso")
    
    except SQLAlchemyError as e:

        print("Erro ao cadastrar pessoa:", e)

        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()

#VERIFICAR SE FUNCIONA
def edit_person(login1,password1,**kwargs):

    '''Edita um ou mais campos de uma pessoa'''

    try:
        
        session = connecting_bd()

        person = login(login=login1,password=password1)

        for key, value in kwargs.items():

            setattr(person, key, value)

        session.commit()

        print("Pessoa editada com sucesso")
    
    except Exception as e:
    
        print("Erro ao editar pessoa:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()

#________________________________Token___________________________________#

#FUNCIONANDO
def register_token(token, person_cpf):
    
        '''Adiciona um token na lista'''
        
        try:
        
            session = connecting_bd()
        
            if session is not None:
        
                token1 = Token(token, person_cpf,state_of="Activated")
        
                session.add(token1)
        
                session.commit()
        
                print("Cadastro do token realizado com sucesso")
        
        except SQLAlchemyError as e:
        
            print("Erro ao cadastrar o token:", e)
        
            session.rollback()
            
            raise e 
        
        finally:
        
            if session:
        
                session.close()

#FUNCIONANDO
def transform_the_last_token_in_expired(person_cpf):
        
        '''Transforma o último token em expirado'''
        
        try:
        
            session = connecting_bd()
        
            if session is not None:
        
                query = session.query(Token).filter(Token.person_cpf == person_cpf).filter(Token.state_of == "Activated")
        
                token = query.one()
                print(token)
                token.state_of = "Expireted"
        
                session.commit()
        
                print("Token expirado com sucesso")
        
        except Exception as e:
        
            print("Erro ao expirar token:", e)
        
            session.rollback()
        
        finally:
        
            if session:
        
                session.close()

#_____________________________Funções_do_CheckList________________________________#

#FUNCIONANDO
def register_item(**kwargs):

    '''Adiciona um item na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            item = CheckList(**kwargs)
    
            session.add(item)
    
            session.commit()
    
            print("Cadastro do item realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao cadastrar o item:", e)
    
        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def list_itens(id_pessoa):
    
    """Lista todos os itens da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(CheckList).filter(CheckList.person_cpf == id_pessoa)

            items = query.all()

            items_dicts=[]

            # Convertendo os objetos para dicionários
            for item in items:

                items_dicts.append(sqlalchemy_to_dict(item)) 
         
            return items_dicts
         
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def edit_item(id_item,id_pessoa, **kwargs):
    
    """Edita os campos de um item da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(CheckList).filter(CheckList.person_cpf == id_pessoa).filter(CheckList.id == id_item)
    
            item = query.one()
    
            for key, value in kwargs.items():

                setattr(item, key, value)

            session.commit()
    
            print("Item editado com sucesso")
    
    except NoResultFound as e:
    
        raise ValueError("Item não encontrado ou não pertence ao seu usuario logado.")
    
    except Exception as e:
    
        print("Erro ao editar item:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def delete_item(id_pessoa, id_item):
        
    """Exclui um item da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(CheckList).filter(CheckList.person_cpf == id_pessoa).filter(CheckList.id == id_item)
    
            item = query.one()
    
            session.delete(item)
    
            session.commit()
    
            print("Item excluído com sucesso")
    
    except NoResultFound:
    
        raise ValueError("Item não encontrado ou não pertence ao seu usuario logado.")
    
    except Exception as e:
    
        print("Erro ao excluir item:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()

#_____________________________Funções_do_FeedBack________________________________#

#FUNCIONANDO
def register_feedback(id_pessoa,**kwargs):

    '''Adiciona um feedback na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            feedback = Feedback(**kwargs,person_cpf=id_pessoa)
    
            session.add(feedback)
    
            session.commit()
    
            print("Cadastro do feedback realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao cadastrar o feedback:", e)
    
        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def list_feedbacks():
    
    """Lista todos os feedbacks da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Feedback)

            feedbacks = query.all()

            feedbacks_dicts=[]

            # Convertendo os objetos para dicionários
            for feedback in feedbacks:

                feedbacks_dicts.append(sqlalchemy_to_dict(feedback)) 
         
            return feedbacks_dicts
         
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

#_____________________________Funções_do_Monthly_Schedule_________________________________#

#FUNCIONANDO
def list_meetings(id_pessoa):
    
    """Lista todas as reuniões da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Meeting).filter(Meeting.person_cpf == id_pessoa)

            meetings = query.all()

            meetings_dicts=[]

            # Convertendo os objetos para dicionários
            for meeting in meetings:

                meetings_dicts.append(sqlalchemy_to_dict(meeting)) 
        
            return meetings_dicts
        
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def register_meeting(id_pessoa, **kwargs):
    
        '''Adiciona uma reunião na lista'''
        
        try:
        
            session = connecting_bd()
        
            if session is not None:
        
                meeting = Meeting(**kwargs,person_cpf=id_pessoa)
        
                session.add(meeting)
        
                session.commit()
        
                print("Cadastro da reunião realizado com sucesso")
        
        except SQLAlchemyError as e:
        
            print("Erro ao cadastrar a reunião:", e)
        
            session.rollback()
            
            raise e 
        
        finally:
        
            if session:
        
                session.close()

#FUNCIONANDO
def list_trainings(id_pessoa):
        
    """Lista todos os treinamentos da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Training).filter(Training.person_cpf == id_pessoa)

            trainings = query.all()

            trainings_dicts=[]

            # Convertendo os objetos para dicionários
            for training in trainings:

                trainings_dicts.append(sqlalchemy_to_dict(training)) 
        
            return trainings_dicts
        
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def register_training(id_pessoa, **kwargs):
        
    '''Adiciona um treinamento na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            training = Training(**kwargs,person_cpf=id_pessoa)
    
            session.add(training)
    
            session.commit()
    
            print("Cadastro do treinamento realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao cadastrar o treinamento:", e)
    
        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()

#FUNCIONANDO
def list_monthly_schedule(id_pessoa):
    return [
        {
            "title":"Treinamentos",
            "list" : list_trainings(id_pessoa)
        }
        ,
        {
            "title":"Reuniões",
            "list" : list_meetings(id_pessoa)
        }
    ]

#RESOLVER
def delete_training(id, id_pessoa):
    """Exclui um training da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Training).filter(Training.person_cpf == id_pessoa).filter(Training.id == id)
    
            item = query.one()
    
            session.delete(item)
    
            session.commit()
    
            print("Item excluído com sucesso")
    
    except NoResultFound:
    
        raise ValueError("Item não encontrado ou não pertence ao seu usuario logado.")
    
    except Exception as e:
    
        print("Erro ao excluir item:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()

def delete_meeting(id, id_pessoa):
    """Exclui um training da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Meeting).filter(Meeting.person_cpf == id_pessoa).filter(Meeting.id == id)
    
            item = query.one()
    
            session.delete(item)
    
            session.commit()
    
            print("Item excluído com sucesso")
    
    except NoResultFound:
    
        raise ValueError("Item não encontrado ou não pertence ao seu usuario logado.")
    
    except Exception as e:
    
        print("Erro ao excluir item:", e)
    
        session.rollback()
    
    finally:
    
        if session:
    
            session.close()
    

#_____________________________Funções_do_Questions_&_Answers_________________________________#

def register_question(id_pessoa, **kwargs):
        
    '''Adiciona uma pergunta na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            question = Question(**kwargs,person_cpf=id_pessoa)
    
            session.add(question)
    
            session.commit()
    
            print("Cadastro da pergunta realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao cadastrar a pergunta:", e)
    
        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()

def list_questions():
            
    """Lista todas as perguntas da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Question)

            questions = query.all()

            questions_dicts=[]

            # Convertendo os objetos para dicionários
            for question in questions:

                questions_dicts.append(sqlalchemy_to_dict(question)) 
        
            return questions_dicts
        
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

def register_answer(id_pessoa,**kwargs):
        
    '''Adiciona uma resposta na lista'''
    
    try:
    
        session = connecting_bd()
    
        if session is not None:
    
            answer = Answer(**kwargs,person_cpf=id_pessoa)
    
            session.add(answer)
    
            session.commit()
    
            print("Cadastro da resposta realizado com sucesso")
    
    except SQLAlchemyError as e:
    
        print("Erro ao cadastrar a resposta:", e)
    
        session.rollback()
        
        raise e 
    
    finally:
    
        if session:
    
            session.close()

def list_answer(id_questions):
                
    """Lista todas as respostas da lista"""
    
    session = connecting_bd()
    
    try:
    
        if session is not None:
    
            query = session.query(Answer).filter(Answer.id_question == id_questions)

            answers = query.all()

            answers_dicts=[]

            # Convertendo os objetos para dicionários
            for answer in answers:

                answers_dicts.append(sqlalchemy_to_dict(answer)) 
        
            return answers_dicts
        
    except Exception as e:
    
        print("Erro na consulta:", e)
    
    finally:
    
        if session:
    
            session.close()

def list_questions_and_answers():
    
    list = []

    for question in list_questions():
        print(question)
        list.append({'id_question' : question['id'],'question': question['question'],'create_at': question['create_at'],'name': get_person_by_cpf(question['person_cpf']).get_name(),'answers': [{"answer": i["answer"],"create_at": i["create_at"], "name": get_person_by_cpf(question['person_cpf']).get_name()} for i in list_answer(question['id'])]})

    return list

