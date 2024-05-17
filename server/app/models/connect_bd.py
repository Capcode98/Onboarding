from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app.models.model import Person, CheckList, Feedback, Token
from app.models.utils_bd import connecting_bd, sqlalchemy_to_dict
from hashlib import sha256


#________________________________Pessoas___________________________________#

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